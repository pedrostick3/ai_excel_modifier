import constants.configs as configs
from modules.analytics.services.ai_analytics import AiAnalytics
from openai import AzureOpenAI
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import logging
import time


class AzureAiService:
    """
    Service class to interact with Azure AI for generating responses based on prompts.
    """

    def __init__(self):
        """
        Initialize the Azure AI API.
        """
        self.project = AIProjectClient.from_connection_string(
            conn_str=configs.AZURE_PROJECT_CONNECTION_STRING,
            credential=DefaultAzureCredential(),
        )
        self.chat = self.project.inference.get_chat_completions_client()
        self.client = self.project.inference.get_azure_openai_client()

    def get_ai_client(self) -> AzureOpenAI:
        """
        Get the client to be used for the AI/ML API.

        Returns:
            object: The client to be used.
        """
        return self.client

    def ask_ai(
        self,
        model: str,
        first_user_prompt: str,
        system_prompt: str | None = None,
        example_prompts: list[dict[str, str]] | None = None,
        continuous_user_conversation_prompt: str = None,
        use_assistant_instead_of_system: bool = False,
        response_format: None | dict = {"type": "json_object"},
        temperature: float = 1,
        top_p: float = 1,
        tools: list[dict] = None,
        ai_analytics_file_name: str = None,
        ai_analytics_agent_name: str = None,
        log_request_messages: bool = True,
        log_response_message: bool = True,
    ) -> str:
        """
        Ask the AI for a response based on the given prompt.

        Args:
            model (str): The model to be used.
            first_user_prompt (str): The first user prompt to be used.
            system_prompt (str | None): The system prompt to be used.
            example_prompts (list[dict[str, str]] | None): The example prompts to be used.
            continuous_user_conversation_prompt (str): The continuous user conversation message to be used.
            use_assistant_instead_of_system (bool): Flag to indicate if the assistant should be used instead of the system.
            response_format (None | dict): The response format to be used.
            temperature (float): The temperature to be used that determines the randomness of the response [deterministic = 0 < temp < 2 = creative].
            top_p (float): The nucleus sampling parameter to be used. It is the probability mass below which, the model will not consider the next token [0 < top_p <= 1].
            tools (list[dict]): The tools to be used.
            ai_analytics_file_name (str): The AI analytics file name to be used.
            ai_analytics_agent_name (str): The AI analytics agent name to be used.
            log_request_messages (bool): Flag to indicate if the request messages should be logged.
            log_response_message (bool): Flag to indicate if the response message should be logged.

        Returns:
            str: The AI's response.
        """
        try:
            if continuous_user_conversation_prompt:
                self.followup_conversation_messages.append({"role": "user", "content": continuous_user_conversation_prompt})
            else:
                ai_role = "assistant" if use_assistant_instead_of_system else "system"

                messages = []
                if system_prompt:
                    messages.append({"role": ai_role, "content": system_prompt})
                if example_prompts and len(example_prompts) % 2 == 0:
                    messages.extend(example_prompts)
                messages.append({"role": "user", "content": first_user_prompt})

                self.followup_conversation_messages = messages
            
            
            self.followup_conversation_messages = self.handle_conversation_messages_length(
                model,
                self.followup_conversation_messages,
                not_to_replace_first_messages=1 + len(example_prompts) if example_prompts and len(example_prompts) % 2 == 0 else 1, # system_prompt + example_prompts
            )

            if log_request_messages:
                logging.info(f"request messages: {self.followup_conversation_messages}")

            logging.info(f"Wait for AI response...")
            start_time = time.time()
            response = self.get_ai_client().completions.create(
                model=model,
                messages=self.followup_conversation_messages,
                response_format=response_format,
                temperature=temperature,
                top_p=top_p,
                tools=tools, # [https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling#single-toolfunction-calling-example]
            )
            execution_time = time.time() - start_time
            logging.info(f"AI response received after {execution_time} seconds")
            AiAnalytics.add_file_agent_request(
                file_name=ai_analytics_file_name,
                agent_name=ai_analytics_agent_name,
                ai_model=model,
                prompt_tokens=response["usage"]["prompt_tokens"],
                completion_tokens=response["usage"]["completion_tokens"],
                total_tokens=response["usage"]["total_tokens"],
                execution_time_in_seconds=execution_time,
            )

            messageContent = response["choices"][0]["message"]["content"]
            messageFunctionCalls = response["choices"][0]["message"]["tool_calls"]

            if log_response_message:
                logging.info(f"response messages usage: {response['usage']}")
                logging.info(f"response message content: {messageContent}")
                if tools:
                    logging.info(f"response message tool function calls: {messageFunctionCalls}")

            self.followup_conversation_messages.append({"role": response["choices"][0]["message"]["role"], "content": messageContent})

            return str(messageFunctionCalls) if tools and messageFunctionCalls else messageContent
        except Exception as e:
            logging.error(f"Erro ao comunicar com a AI: {e}")
            raise
