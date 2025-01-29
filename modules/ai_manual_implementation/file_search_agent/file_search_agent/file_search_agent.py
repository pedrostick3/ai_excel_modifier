import logging
import json
from modules.ai_manual_implementation.services.ai_service import AiService
from modules.ai_manual_implementation.services.custom_ai_service import CustomAiService
from modules.excel.services.excel_service import ExcelService


class FileSearchAgent:
    """
    AI Agent for searching files.
    [https://platform.openai.com/docs/assistants/tools/file-search]
    """

    def __init__(self, ai_service: CustomAiService, model: str):
        """
        Initialize the AI Agent.
        """
        self.ai_service = ai_service
        self.model = model

    def ask_ai(
        self,
        file_to_upload: str,
        user_role_request_prompt: str,
        ai_analytics_file_name: str = None,
        log_messages: bool = True,
    ) -> str:
        """
        Ask the AI for a response based on the given excel_data.

        Args:
            excel_data (str): The Excel data to be used.
            ai_analytics_file_name (str): The AI analytics file name to be used.
            log_messages (bool): Flag to indicate if the request messages should be logged.

        Returns:
            str: The AI's response.
        """
        try:
            assistant = self.ai_service.get_ai_client().beta.assistants.create(
                name="Excel Analyst Assistant",
                instructions="You are an expert excel analyst. Use your knowledge base to answer questions about excel statements.",
                model=self.model,
                tools=[{"type": "file_search"}],
            )

            # Upload the user provided file to OpenAI
            message_file = self.ai_service.get_ai_client().files.create(
                file=open(file_to_upload, "rb"), # Individual files can be up to 512 MB
                purpose="assistants",
            )

            # Create a thread and attach the file to the message
            thread = self.ai_service.get_ai_client().beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_role_request_prompt,
                        "attachments": [
                            {
                                "file_id": message_file.id,
                                "tools": [{"type": "file_search"}],
                            },
                        ],
                    },
                ],
            )

            # The thread now has a vector store with that file in its tool resources.
            print(thread.tool_resources.file_search)

            run = self.ai_service.get_ai_client().beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )

            messages = list(self.ai_service.get_ai_client().beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

            message_content = messages[0].content[0].text
            annotations = message_content.annotations
            citations = []
            for index, annotation in enumerate(annotations):
                message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
                if file_citation := getattr(annotation, "file_citation", None):
                    cited_file = self.ai_service.get_ai_client().files.retrieve(file_citation.file_id)
                    citations.append(f"[{index}] {cited_file.filename}")

            print(message_content.value)
            print("\n".join(citations))

            # Delete the assistant, thread, and file
            # self.ai_service.get_ai_client().beta.assistants.delete(assistant.id)
            # self.ai_service.get_ai_client().beta.threads.delete(thread.id)
            # self.ai_service.get_ai_client().files.delete(message_file.id)
            """
            ai_response = self.ai_service.ask_ai(
                model=self.model,
                first_user_prompt=user_role_request_prompt,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "sum_column",
                            "description": "Sum the given column values.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "column_values": {
                                        "type": "array",
                                        "items": {"type": "number"},
                                        "description": "The column values to be summed.",
                                    },
                                },
                                "required": ["column_values"],
                            },
                        }
                    }
                ],
                use_assistant_instead_of_system=False,  # True caso o modelo seja "o1-preview" ou "o1-mini"
                response_format=None,
                ai_analytics_file_name=ai_analytics_file_name,
                ai_analytics_agent_name="FileSearchAgent",
                log_request_messages=log_messages,
                log_response_message=log_messages,
            )

            return ai_response
            """
        except Exception as e:
            logging.error(f"Erro ao comunicar com o AI FileSearchAgent: {e}")
            raise
    
    def do_your_work_with(
        self,
        column_to_sum: str,
        input_excel_file_path: str,
        excel_header_row_index: int = 0,
        ai_analytics_file_name: str = None,
    ) -> float:
        """
        Processes an Excel file by sending a user prompt to the AI for modification and executing the returned python code.

        Args:
            column_to_sum (str): The column to be summed.
            excel_input_file_path (str): The path to the Excel file to be processed.
            excel_header_row_index (int): The row index of the header in the Excel file.
            ai_analytics_file_name (str, optional): The AI analytics file name to be used. Defaults to None.

        Returns:
            float: The sum of the column values.
        """
        try:
            reponse = self.ask_ai(
                user_role_request_prompt=f"Quais os valores da coluna {column_to_sum}?",
                file_to_upload=input_excel_file_path,
                ai_analytics_file_name=ai_analytics_file_name,
            )
            print(f"###$### AI response: {reponse}")
            return -1
        except Exception as e:
            logging.error(f"AI FileSearchAgent: Error communicating with AI: {e}")
            raise

        try:
            response_json = json.loads(reponse)
        except json.JSONDecodeError:
            logging.error(f"AI FileSearchAgent: Error parsing AI response JSON: {reponse}")
            raise
        
        if "function" not in response_json or response_json["function"]["name"] != "sum_column":
            raise
        
        try:
            function_args = json.loads(response_json["function"]["arguments"])
        except json.JSONDecodeError:
            logging.error(f"AI FileSearchAgent: Error parsing AI response JSON arguments: {response_json['function']['arguments']}")
            raise
        
        return self.sum_column(column_values=function_args["column_values"])

    def sum_column(self, column_values: list) -> float:
        """
        Sum the given column values.

        Args:
            column_values (list): The column values to be summed.

        Returns:
            float: The sum of the column values.
        """
        return sum(column_values)