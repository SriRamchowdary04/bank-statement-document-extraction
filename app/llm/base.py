from abc import ABC, abstractmethod

class LLMAdapter(ABC):
    name: str

    @abstractmethod
    def extract(self, document_text: str) -> dict:
        raise NotImplementedError
