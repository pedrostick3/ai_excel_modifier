import os
import logging
import modules.ai.agents.excel_pre_header_modifier_agent.excel_pre_header_modifier_agent_prompts as prompts
from modules.ai.services.ai_service import AiService
from modules.excel.services.excel_service import ExcelService
from modules.ai.agents.excel_categorizer_agent.enums.file_category import FileCategory


class ExcelPreHeaderModifierAgent:
    """
    Class to interact with the AI for modifying the pre-header of an Excel file.
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
            user_prompt = f"""
```csv
{excel_data}
```
            """
            ai_response = self.ai_service.ask_ai(
                model=self.model,
                system_prompt=system_prompt,
                example_prompts=example_prompts,
                first_user_prompt=user_prompt,
                use_assistant_instead_of_system=False,  # True caso o modelo seja "o1-preview" ou "o1-mini"
                response_format=None,
                ai_analytics_file_name=ai_analytics_file_name,
                ai_analytics_agent_name="ExcelPreHeaderModifierAgent",
                log_request_messages=log_messages,
                log_response_message=log_messages,
            )

            return ai_response
        except Exception as e:
            logging.error(f"Erro ao comunicar com o AI ExcelPreHeaderModifierAgent: {e}")
            raise
    
    def do_your_work_by_category(
        self,
        category: FileCategory,
        input_excel_file_path: str,
        header_row_number: int,
        output_excel_file_path: str,
    ) -> bool:
        """
        Do the agent's work with the given parameters.

        Args:
            category (FileCategory): The category of the file.
            input_excel_file_path (str): The path to the input Excel file.
            header_row_number (int): The number of the header row.
            output_excel_file_path (str): The path to the output Excel file.

        Returns:
            bool: The success of the operation.
        """
        if category == FileCategory.EXECUCAO:
            system_prompt = prompts.SYSTEM_PROMPT_CATEGORY_EXECUTION
            example_prompts = prompts.EXAMPLE_PROMPTS_CATEGORY_EXECUTION
        elif category == FileCategory.TESTE_EXECUCAO:
            system_prompt = prompts.SYSTEM_PROMPT_CATEGORY_TEST_EXECUTION
            example_prompts = prompts.EXAMPLE_PROMPTS_CATEGORY_TEST_EXECUTION
        else:
            system_prompt = prompts.SYSTEM_PROMPT_TEST_ALL
            example_prompts = prompts.EXAMPLE_PROMPTS_TEST_ALL

        file_name = os.path.basename(input_excel_file_path)
        excel_data_first_rows_until_header = ExcelService.get_excel_csv_to_csv_str(input_excel_file_path, only_get_first_rows=header_row_number)
        logging.info(f"AI ExcelPreHeaderModifierAgent - {category} - excel_data_first_rows_until_header = {excel_data_first_rows_until_header}")
        excel_pre_header_modifier_agent_response = self.ask_ai(
            excel_data=excel_data_first_rows_until_header,
            system_prompt=system_prompt,
            example_prompts=example_prompts,
            ai_analytics_file_name=file_name,
        )

        try:
            success = ExcelService.replace_excel_csv_data_in_file(
                excel_input_file_path=input_excel_file_path,
                excel_output_file_path=output_excel_file_path,
                excel_data=excel_pre_header_modifier_agent_response,
                initial_index_for_replacement=0,
                final_index_for_replacement=header_row_number,
            )

            if not success:
                logging.error(f"Warning - AI ExcelPreHeaderModifierAgent - Não foi possível guardar o ficheiro '{output_excel_file_path}'.")

            return success
        except Exception as e:
            logging.error(f"Erro ao processar o retorno do AI ExcelPreHeaderModifierAgent: {e}")
            raise