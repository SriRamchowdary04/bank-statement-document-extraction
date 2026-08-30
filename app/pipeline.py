from pathlib import Path
import json

from pydantic import ValidationError

from app.config import OUTPUT_DIR, LLM_PROVIDERS
from app.detector import inspect_pdf
from app.extractors.native_text import extract_native_text
from app.validators import (
    looks_like_bank_statement,
    split_merged_statements,
)
from app.schemas import ExtractionResult
from app.quality import validate_result_quality


def get_adapters():

    adapters = []

    if "mock" in LLM_PROVIDERS:
        from app.llm.mock_adapter import MockAdapter
        adapters.append(MockAdapter())

    if "openai" in LLM_PROVIDERS:
        from app.config import OPENAI_API_KEY

        if OPENAI_API_KEY:
            from app.llm.openai_adapter import OpenAIAdapter
            adapters.append(OpenAIAdapter())
        else:
            print("Skipping OpenAI: API key not configured.")

    if "anthropic" in LLM_PROVIDERS:
        from app.config import ANTHROPIC_API_KEY

        if ANTHROPIC_API_KEY:
            from app.llm.anthropic_adapter import AnthropicAdapter
            adapters.append(AnthropicAdapter())
        else:
            print("Skipping Anthropic: API key not configured.")

    if "gemini" in LLM_PROVIDERS:
        from app.config import GEMINI_API_KEY

        if GEMINI_API_KEY:
            from app.llm.gemini_adapter import GeminiAdapter
            adapters.append(GeminiAdapter())
        else:
            print("Skipping Gemini: API key not configured.")

    if "ollama" in LLM_PROVIDERS:
        from app.llm.ollama_adapter import OllamaAdapter
        adapters.append(OllamaAdapter())

    if "ollama_llama" in LLM_PROVIDERS:
        from app.llm.ollama_adapter import OllamaAdapter
        adapters.append(
            OllamaAdapter("llama3.2:3b")
        )

    if "ollama_qwen" in LLM_PROVIDERS:
        from app.llm.ollama_adapter import OllamaAdapter
        adapters.append(
            OllamaAdapter("qwen2.5:3b")
        )

    return adapters


def write_output(document_name, model_name, result):

    output_path = (
        Path(OUTPUT_DIR)
        / f"{document_name}__{model_name}.json"
    )

    output_path.write_text(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("Output:", output_path)


def process_document(path):

    Path(OUTPUT_DIR).mkdir(
        parents=True,
        exist_ok=True
    )

    document_name = Path(path).stem

    print("\n")
    print("=" * 70)
    print("PROCESSING:", Path(path).name)
    print("=" * 70)

    # --------------------------------------------------
    # 1. Detect PDF
    # --------------------------------------------------

    info = inspect_pdf(path)

    print(
        "Detected format:",
        info["detected_format"]
    )

    print(
        "Status:",
        info["status"]
    )

    # --------------------------------------------------
    # 2. Password protected
    # --------------------------------------------------

    if info["status"] == "password_protected":

        for adapter in get_adapters():

            result = {
                "detected_format":
                    info["detected_format"],

                "model":
                    adapter.name,

                "document_status":
                    "could_not_process",

                "reason":
                    "Password-protected PDF. "
                    "Request the password.",

                "transactions": []
            }

            write_output(
                document_name,
                adapter.name,
                result
            )

        return

    # --------------------------------------------------
    # 3. Extract text
    # --------------------------------------------------

    if info["detected_format"] == "native_text":

        print(
            "Route: Native text extraction"
        )

        text = extract_native_text(path)

    else:

        print("Route: OCR")

        try:

            from app.extractors.ocr import (
                extract_ocr_text
            )

            ocr_result = extract_ocr_text(path)

            text = ocr_result["text"]

            ocr_confidence = ocr_result[
                "ocr_confidence"
            ]

            ocr_needs_review = ocr_result[
                "needs_review"
            ]

            print(
                "OCR confidence:",
                ocr_confidence
            )

            if ocr_needs_review:

                print(
                    "OCR confidence is low. "
                    "Document requires review."
                )

                # -----------------------------------------
                # Stop processing low-confidence OCR
                # -----------------------------------------

                for adapter in get_adapters():

                    result = {
                        "detected_format":
                            "image_based",

                        "model":
                            adapter.name,

                        "document_status":
                            "could_not_process",

                        "reason":
                            (
                                "OCR confidence too low: "
                                f"{ocr_confidence:.2f}. "
                                "Manual review required."
                            ),

                        "transactions": []
                    }

                    write_output(
                        document_name,
                        adapter.name,
                        result
                    )

                return

        except Exception as exc:

            for adapter in get_adapters():

                result = {
                    "detected_format":
                        "image_based",

                    "model":
                        adapter.name,

                    "document_status":
                        "could_not_process",

                    "reason":
                        f"OCR failed: "
                        f"{type(exc).__name__}: {exc}",

                    "transactions": []
                }

                write_output(
                    document_name,
                    adapter.name,
                    result
                )

            return

    # --------------------------------------------------
    # 4. Split merged statements
    # --------------------------------------------------

    statements = split_merged_statements(text)

    print(
        "Statements detected:",
        len(statements)
    )

    # --------------------------------------------------
    # 5. Process each statement
    # --------------------------------------------------

    for statement_number, statement in enumerate(
        statements,
        start=1
    ):

        statement_name = (
            f"{document_name}"
            f"_statement_{statement_number}"
        )

        # ------------------------------------------------
        # 6. Validate bank statement
        # ------------------------------------------------

        if not looks_like_bank_statement(statement):

            print(
                "Not a bank statement."
            )

            for adapter in get_adapters():

                result = {
                    "detected_format":
                        info["detected_format"],

                    "model":
                        adapter.name,

                    "document_status":
                        "could_not_process",

                    "reason":
                        "Document content does not "
                        "appear to be a bank statement.",

                    "transactions": []
                }

                write_output(
                    statement_name,
                    adapter.name,
                    result
                )

            continue

        # ------------------------------------------------
        # 7. Run each LLM
        # ------------------------------------------------

        for adapter in get_adapters():

            print(
                "Running model:",
                adapter.name
            )

            try:

                raw_result = adapter.extract(
                    statement
                )

                result = {
                    "detected_format":
                        info["detected_format"],

                    "model":
                        adapter.name,

                    "document_status":
                        raw_result.get(
                            "document_status",
                            "extracted"
                        ),

                    "reason":
                        raw_result.get(
                            "reason"
                        ),

                    "transactions":
                        raw_result.get(
                            "transactions",
                            []
                        )
                }

                # ----------------------------------------
                # 8. Pydantic validation
                # ----------------------------------------

                validated = (
                    ExtractionResult
                    .model_validate(result)
                )

                final_result = (
                    validated.model_dump()
                )

                # ----------------------------------------
                # 9. Quality validation
                # ----------------------------------------

                quality_errors = (
                    validate_result_quality(
                        final_result
                    )
                )

                if quality_errors:

                    final_result[
                        "document_status"
                    ] = "could_not_process"

                    final_result[
                        "reason"
                    ] = (
                        "Quality validation failed: "
                        + "; ".join(
                            quality_errors
                        )
                    )

                    print(
                        "Quality check failed."
                    )

                else:

                    print(
                        "Quality check passed."
                    )

            except (
                ValidationError,
                ValueError,
                json.JSONDecodeError
            ) as exc:

                final_result = {
                    "detected_format":
                        info["detected_format"],

                    "model":
                        adapter.name,

                    "document_status":
                        "could_not_process",

                    "reason":
                        "Invalid structured output: "
                        + str(exc),

                    "transactions": []
                }

            except Exception as exc:

                final_result = {
                    "detected_format":
                        info["detected_format"],

                    "model":
                        adapter.name,

                    "document_status":
                        "could_not_process",

                    "reason":
                        f"Model call failed: "
                        f"{type(exc).__name__}: {exc}",

                    "transactions": []
                }

            # --------------------------------------------
            # 10. Save final JSON
            # --------------------------------------------

            write_output(
                statement_name,
                adapter.name,
                final_result
            )


def run(input_dir):

    input_path = Path(input_dir)

    pdfs = sorted(
        input_path.glob("*.pdf")
    )

    if not pdfs:

        print(
            f"No PDFs found in {input_dir}"
        )

        return

    print(
        f"Found {len(pdfs)} PDF(s)."
    )

    for pdf in pdfs:

        process_document(
            str(pdf)
        )
