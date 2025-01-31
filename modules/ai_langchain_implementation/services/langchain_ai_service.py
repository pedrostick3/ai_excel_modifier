from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
import modules.ai_langchain_implementation.function_calling.simple_math_functions as simple_math_functions
from modules.analytics.services.ai_analytics import AiAnalytics
import logging
import time
import json
import ast


class LangChainAiService():
    """
    This class implements the LangChain AI Service with OpenAI.
    """

    def __init__(self,
        openai_api_key: str,
        ai_model: str,
    ):
        """
        Initialize the OpenAI API.
        """
        self.model = ai_model
        self.client = ChatOpenAI(
            model=ai_model,
            api_key=openai_api_key,
        )

    def get_ai_client(self) -> ChatOpenAI:
        """
        Get the client to be used for the AI/ML API.

        Returns:
            object: The client to be used.
        """
        return self.client

    def ask_ai(
        self,
        prompt: list,
        input_vars: dict = None,
        functions_signature_list_for_tools: list = None,
        tool_choice: str = None,
        ai_analytics_file_name: str = None,
        ai_analytics_agent_name: str = None,
        log_response_message: bool = True,
    ) -> str:
        """
        Ask the AI for a response based on the given prompt.

        Args:
            prompt (list): The prompt to be used.
            input_vars (dict): The input variables to be used.
            functions_signature_list_for_tools (list): The functions signature list for tools.
            tool_choice (str): Force the function calling by setting the tool choice to "required". [Source](https://community.openai.com/t/new-api-feature-forcing-function-calling-via-tool-choice-required/731488)
            ai_analytics_file_name (str): The AI analytics file name.
            ai_analytics_agent_name (str): The AI analytics agent name.
            log_response_message (bool): Flag to indicate if the response message should be logged

        Returns:
            str: The AI's response.
        """
        try:
            if functions_signature_list_for_tools:
                print(f"functions_signature_list_for_tools = {functions_signature_list_for_tools}")
                print(f"tool_choice = {tool_choice}")
                llm_with_tools = self.get_ai_client().bind_tools(functions_signature_list_for_tools, tool_choice=tool_choice)
            elif input_vars:
                llm_chain = ChatPromptTemplate.from_messages(prompt) | self.get_ai_client()
            else:
                llm = self.get_ai_client()

            logging.info(f"LangChainAiService.ask_ai() - Wait for AI response...")
            start_time = time.time()
            if functions_signature_list_for_tools:
                most_recent_message = prompt[-1][-1] # Get the most recent message and the last element of the tuple wich is the message
                response = llm_with_tools.invoke(most_recent_message)
            elif input_vars:
                response = llm_chain.invoke(input=input_vars)
            else:
                response = llm.invoke(prompt)
            execution_time = time.time() - start_time

            logging.info(f"LangChainAiService.ask_ai() - AI response received after {execution_time} seconds")
            AiAnalytics.add_file_agent_request(
                file_name=ai_analytics_file_name,
                agent_name=ai_analytics_agent_name,
                ai_model=self.model,
                prompt_tokens=response.response_metadata["token_usage"]["prompt_tokens"],
                completion_tokens=response.response_metadata["token_usage"]["completion_tokens"],
                total_tokens=response.response_metadata["token_usage"]["total_tokens"],
                execution_time_in_seconds=execution_time,
            )
            
            messageContent = response.content
            messageFunctionCalls = response.model_dump()["tool_calls"][0] if response.model_dump()["tool_calls"] else None

            if log_response_message:
                logging.info(f"LangChainAiService.ask_ai() - response message: {response.model_dump_json(indent=2)}")
                logging.info(f"LangChainAiService.ask_ai() - response messages usage: {response.response_metadata["token_usage"]}")
                logging.info(f"LangChainAiService.ask_ai() - response message content: {messageContent}")
                if functions_signature_list_for_tools and messageFunctionCalls:
                    logging.info(f"LangChainAiService.ask_ai() - response message tool function calls: {messageFunctionCalls}")

            return str(messageFunctionCalls) if functions_signature_list_for_tools and messageFunctionCalls else messageContent
        except Exception as e:
            logging.error(f"LangChainAiService.ask_ai() - Error communicating with the AI: {e}")
            raise

    def test_invocation(self) -> str:
        """
        Test the invocation of the AI.
        Reference: [LangChain Docs - Invocation](https://python.langchain.com/docs/integrations/chat/openai/#invocation)
        """
        response = self.ask_ai(
            prompt=[
                (
                    "system",
                    "You are a helpful assistant that translates English to Portugal Portuguese. Translate the user sentence.",
                ),
                ("human", "I love programming."),
            ],
        )
        logging.info(f"LangChainAiService.test_invocation() - Response: {response}")
        return response

    def test_chaining(self) -> str:
        """
        Test the chaining of the AI.
        Reference: [LangChain Docs - Chaining](https://python.langchain.com/docs/integrations/chat/openai/#chaining)
        """
        response = self.ask_ai(
            prompt=[
                (
                    "system",
                    "You are a helpful assistant that translates {input_language} to {output_language}.",
                ),
                (
                    "human",
                    "{input}",
                ),
            ],
            input_vars={
                "input_language": "English",
                "output_language": "Portugal Portuguese",
                "input": "I love programming.",
            },
        )
        logging.info(f"LangChainAiService.test_chaining() - Response: {response}")
        return response
    
    def test_tool_function_calling(self) -> str:
        """
        Test the tool function calling of the AI.
        References:
        - [LangChain Docs - Tool Calling](https://python.langchain.com/docs/integrations/chat/openai/#tool-calling)
        - [LangChain Docs - Tool Function Calling](https://python.langchain.com/docs/how_to/function_calling/#passing-tools-to-llms)
        """
        response = self.ask_ai(
            prompt=[
                (
                    "human",
                    "whats 5 times forty two",
                ),
            ],
            functions_signature_list_for_tools=[simple_math_functions.multiply],
            tool_choice="required",
        )
        logging.info(f"LangChainAiService.test_tool_calling() - Response: {response}")
    
        try:
            response_json = json.load(response) if self._is_valid_json(response) else ast.literal_eval(response)
        except json.JSONDecodeError:
            logging.error(f"LangChainAiService.test_tool_calling() - Error parsing AI response JSON: {response}")
            raise
        
        if "name" not in response_json:
            logging.error(f"LangChainAiService.test_tool_calling() - The AI response JSON does not contain the 'name' key. response = {response}")
            raise

        try:
            if response_json["name"] == "multiply":
                tool_function_response = simple_math_functions.multiply.invoke(response_json["args"])
                logging.info(f"LangChainAiService.test_tool_calling() - Tool function response: {tool_function_response}")
                return tool_function_response
        except json.JSONDecodeError:
            logging.error(f"LangChainAiService.test_tool_calling() - Error executing function. response_json: {response_json}")
            raise

    def _is_valid_json(self, json_str: str) -> bool:
        """
        Check if a string is a valid JSON.

        Args:
            json_str (str): The JSON string.

        Returns:
            bool: True if the string is a valid JSON, False otherwise.

        Examples:
            _is_valid_json('{"key": "value"}') -> True
            _is_valid_json("{'key': 'value'}") -> False
        """
        try:
            json.loads(json_str)
            return True
        except json.JSONDecodeError:
            return False