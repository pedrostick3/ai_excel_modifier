import logging
import json
import os
import modules.ai.agents.excel_header_finder_agent.excel_header_finder_agent_prompts as prompts
from modules.ai.services.ai_service import AiService
from modules.excel.services.excel_service import ExcelService


class ExcelHeaderFinderAgent:
    """
    Class to interact with the AI for finding the header of an Excel file.
    """

    def __init__(self, ai_service: AiService, model: str):
        """
        Initialize the AI Agent.
        """
        self.ai_service = ai_service
        self.model = model

    def ask_ai(
        self,
        excel_data: str,
        system_prompt: str,
        example_prompts: list[dict] | None = None,
        response_format: dict = None,
        ai_analytics_file_name: str = None,
        log_messages: bool = True,
    ) -> str:
        """
        Ask the AI for a response based on the given excel_data.

        Args:
            excel_data (str): The Excel data to be used.
            system_prompt (str): The system prompt to be used.
            example_prompts (list[dict]): The example prompts to be used.
            response_format (dict): The response format to be used.
            ai_analytics_file_name (str): The AI analytics file name to be used.
            log_messages (bool): Flag to indicate if the request messages should be logged.

        Returns:
            str: The AI's response.
        """
        try:
            user_prompt = f"""{excel_data}"""
            ai_response = self.ai_service.ask_ai(
                model=self.model,
                system_prompt=system_prompt,
                example_prompts=example_prompts,
                first_user_prompt=user_prompt,
                use_assistant_instead_of_system=False,  # True caso o modelo seja "o1-preview" ou "o1-mini"
                response_format=response_format,
                ai_analytics_file_name=ai_analytics_file_name,
                ai_analytics_agent_name="ExcelHeaderFinderAgent",
                log_request_messages=log_messages,
                log_response_message=log_messages,
            )

            return ai_response
        except Exception as e:
            logging.error(f"Erro ao comunicar com o AI ExcelHeaderFinderAgent: {e}")
            raise
    
    def do_your_work_returning_json(self, excel_file_path: str, ai_analytics_file_name: str = None) -> dict:
        """
        Do the agent's work with the given parameters.

        Args:
            file_path (str): The file path to be used.
            ai_analytics_file_name (str): The AI analytics file name to be used.

        Returns:
            dict: The header row.
        """
        file_name = os.path.basename(excel_file_path)
        excel_data_first_5_rows = ExcelService.get_excel_csv_to_csv_str(excel_file_path, only_get_first_rows=5)
        excel_header_finder_agent_response = self.ask_ai(
            excel_data_first_5_rows,
            system_prompt=prompts.SYSTEM_PROMPT_JSON,
            example_prompts=prompts.EXAMPLE_PROMPTS_JSON,
            response_format=self.ai_service.JSON_RESPONSE_FORMAT,
            ai_analytics_file_name=ai_analytics_file_name if ai_analytics_file_name else file_name,
        )

        try:
            excel_header_finder_agent_response_dict = json.loads(excel_header_finder_agent_response)
        except ValueError:
            logging.error(f"Warning - AI ExcelHeaderFinderAgent - Cabeçalho não encontrado nas primeiras 10 linhas do ficheiro {excel_file_path}. ai_agent_response: {excel_header_finder_agent_response}")
            excel_header_finder_agent_response_dict = {}
        
        return excel_header_finder_agent_response_dict

    def get_row_number(self, excel_file_path: str, ai_analytics_file_name: str = None) -> int:
        """
        Get the row number of the header through AI JSON call.

        Args:
            file_path (str): The file path to be used.
            ai_analytics_file_name (str): The AI analytics file name to be used.

        Returns:
            int: The number of the header row.
        """
        excel_header_finder_agent_response = self.do_your_work_returning_json(excel_file_path, ai_analytics_file_name)['row_number']
        try:
            excel_header_finder_agent_response_number = int(excel_header_finder_agent_response)
        except ValueError:
            excel_header_finder_agent_response_number = -1

        if excel_header_finder_agent_response_number < 0:
            logging.error(f"Warning - AI ExcelHeaderFinderAgent - Cabeçalho não encontrado nas primeiras 10 linhas do ficheiro {excel_file_path}. ai_agent_response: {excel_header_finder_agent_response}")

        return excel_header_finder_agent_response_number
    
    def get_row_content(self, excel_file_path: str, ai_analytics_file_name: str = None) -> str:
        """
        Get the content of the header through AI JSON call.

        Args:
            file_path (str): The file path to be used.
            ai_analytics_file_name (str): The AI analytics file name to be used.

        Returns:
            str: The header row.
        """
        excel_header_finder_agent_response = self.do_your_work_returning_json(excel_file_path, ai_analytics_file_name)['row_content']
        return excel_header_finder_agent_response if excel_header_finder_agent_response else ""