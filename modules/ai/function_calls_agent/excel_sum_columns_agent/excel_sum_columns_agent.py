import logging
import json
from modules.ai.services.ai_service import AiService
from modules.excel.services.excel_service import ExcelService


class ExcelSumColumnsAgent:
    """
    AI Agent for summing columns in an Excel file.
    """

    def __init__(self, ai_service: AiService, model: str):
        """
        Initialize the AI Agent.
        """
        self.ai_service = ai_service
        self.model = model

    def ask_ai(
        self,
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
                ai_analytics_agent_name="ExcelSumColumnsAgent",
                log_request_messages=log_messages,
                log_response_message=log_messages,
            )

            return ai_response
        except Exception as e:
            logging.error(f"Erro ao comunicar com o AI ExcelSumColumnsAgent: {e}")
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
        column_values = ExcelService.get_excel_csv_column_values(
            column=column_to_sum,
            excel_input_file_path=input_excel_file_path,
            header_row_index=excel_header_row_index,
        )
        try:
            reponse = self.ask_ai(
                user_role_request_prompt=f"Need to sum the column {column_to_sum} that has the following values: {column_values}",
                ai_analytics_file_name=ai_analytics_file_name,
            )
        except Exception as e:
            logging.error(f"AI ExcelSumColumnsAgent: Error communicating with AI: {e}")
            raise

        try:
            response_json = json.loads(reponse)
        except json.JSONDecodeError:
            logging.error(f"AI ExcelSumColumnsAgent: Error parsing AI response JSON: {reponse}")
            raise
        
        if "function" not in response_json or response_json["function"]["name"] != "sum_column":
            raise
        
        try:
            function_args = json.loads(response_json["function"]["arguments"])
        except json.JSONDecodeError:
            logging.error(f"AI ExcelSumColumnsAgent: Error parsing AI response JSON arguments: {response_json['function']['arguments']}")
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