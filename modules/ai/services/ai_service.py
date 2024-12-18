from modules.ai.utils.token_utils import TokenUtils
import json
import logging


class AiService(object):
    """
    Abstract class to interact with an AI for generating responses based on prompts.
    """
    JSON_RESPONSE_FORMAT = {"type": "json_object"}
    
    followup_conversation_messages = []

    def ask_ai(
        self,
        model: str,
        system_prompt: str,
        first_user_prompt: str,
        example_prompts: list[dict] | None = None,
        continuous_user_conversation_prompt: str = None,
        use_assistant_instead_of_system: bool = False,
        response_format: None | dict = JSON_RESPONSE_FORMAT,
        temperature: float = 1,
        top_p: float = 1,
        ai_analytics_file_name: str = None,
        ai_analytics_agent_name: str = None,
        log_request_messages: bool = True,
        log_response_message: bool = True,
    ) -> str:
        """
        Ask the AI for a response based on the given prompt.

        Args:
            model (str): The model to be used.
            system_prompt (str): The system prompt to be used.
            first_user_prompt (str): The first user prompt to be used.
            example_prompts (list[dict] | None): The example prompts to be used.
            continuous_user_conversation_prompt (str): The continuous user conversation message to be used.
            use_assistant_instead_of_system (bool): Flag to indicate if the assistant should be used instead of the system.
            response_format (None | dict): The response format to be used.
            temperature (float): The temperature to be used that determines the randomness of the response [deterministic = 0 < temp < 2 = creative].
            top_p (float): The nucleus sampling parameter to be used. It is the probability mass below which, the model will not consider the next token [0 < top_p <= 1].
            ai_analytics_file_name (str): The AI analytics file name to be used.
            ai_analytics_agent_name (str): The AI analytics agent name to be used.
            log_request_messages (bool): Flag to indicate if the request messages should be logged.
            log_response_message (bool): Flag to indicate if the response message should be logged.

        Returns:
            str: The AI's response.
        """
        raise NotImplementedError("Please Implement this method")
    
    def handle_conversation_messages_length(self, model: str, messages: list[dict], not_to_replace_first_messages: int = 0) -> list[dict]:
        """
        Handles the conversation messages length to ensure it is within the maximum token limit for the specified model.

        Args:
            model (str): The model name to validate against.
            messages (list[dict]): The conversation messages to be validated.

        Returns:
            list[dict]: The conversation messages with the correct length.
        """
        while not TokenUtils.is_context_window_valid(model, json.dumps(messages), log_id="messages") and len(messages) > 1:
            messages.pop(not_to_replace_first_messages)
        logging.info(f"Exists {len(messages)} messages in the conversation, with the following roles: {', '.join([message['role'] for message in messages])}.")
        return messages
