from enum import Enum


class AiImplementation(Enum):
    """
    Enum for the different AI implementations.
    """

    UNKNOWN = {"description": "Unknown"}
    MANUAL = {"description": "Manual Implementation"}
    LANGCHAIN = {"description": "LangChain Implementation"}

    @staticmethod
    def get_implementation_by_description(implementation_description: str) -> "AiImplementation":
        """
        Get the AI Implementation by its description.

        Args:
            implementation_description (str): The AI Implementation description.

        Returns:
            AiImplementation: The AI Implementation.
        """
        for implementation in AiImplementation:
            if implementation.value["description"] == implementation_description:
                return implementation

        return AiImplementation.UNKNOWN
