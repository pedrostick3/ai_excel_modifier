import os
import logging
import modules.ai.agents.excel_generic_content_modifier_agent.excel_generic_content_modifier_agent_code_prompts as code_prompts
from modules.ai.services.ai_service import AiService


class ExcelGenericContentModifierAgent:
    """
    Class to interact with the AI for modifying the content of an Excel file.
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
        system_prompt: str = code_prompts.SYSTEM_CODE_PROMPT,
        example_prompts: list[dict] | None = None,
        ai_analytics_file_name: str = None,
        log_messages: bool = True,
    ) -> str:
        """
        Ask the AI for a response based on the given excel_data.

        Args:
            excel_data (str): The Excel data to be used.
            system_prompt (str): The system prompt to be used.
            example_prompts (list[dict]): The example prompts to be used.
            ai_analytics_file_name (str): The AI analytics file name to be used.
            log_messages (bool): Flag to indicate if the request messages should be logged.

        Returns:
            str: The AI's response.
        """
        try:
            ai_response = self.ai_service.ask_ai(
                model=self.model,
                system_prompt=system_prompt,
                example_prompts=example_prompts,
                first_user_prompt=user_role_request_prompt,
                use_assistant_instead_of_system=False,  # True caso o modelo seja "o1-preview" ou "o1-mini"
                response_format=None,
                ai_analytics_file_name=ai_analytics_file_name,
                ai_analytics_agent_name="ExcelGenericContentModifierAgent",
                log_request_messages=log_messages,
                log_response_message=log_messages,
            )

            return ai_response
        except Exception as e:
            logging.error(f"Erro ao comunicar com o AI ExcelGenericContentModifierAgent: {e}")
            raise
    
    def do_your_work_by_category_returning_code(
        self,
        user_prompt: str,
        input_excel_file_path: str,
        output_excel_file_path: str,
        excel_header_row_index: int = 0,
        ai_analytics_file_name: str = None,
    ) -> None:
        """
        Processes an Excel file by sending a user prompt to the AI for modification and executing the returned python code.

        Args:
            user_prompt (str): The user prompt to be used.
            excel_input_file_path (str): The path to the Excel file to be processed.
            excel_output_file_path (str): The path to the Excel file to be saved.
            excel_header_row_index (int): The row index of the header in the Excel file.
            ai_analytics_file_name (str, optional): The AI analytics file name to be used. Defaults to None.

        Returns:
            None
        """
        try:
            python_code = self.ask_ai(
                user_role_request_prompt=f"""{user_prompt}
Vars:
input_excel_file_path = '{input_excel_file_path}'
output_excel_file_path = '{output_excel_file_path}'
excel_header_row_index = {excel_header_row_index}""",
                ai_analytics_file_name=ai_analytics_file_name,
            )
        except Exception as e:
            logging.error(f"AI ExcelGenericContentModifierAgent: Error communicating with AI: {e}")
            raise

        try:
            exec(python_code, globals())
        except Exception as e:
            logging.error(f"AI ExcelGenericContentModifierAgent: Error running the AI python code: {e}")
            raise