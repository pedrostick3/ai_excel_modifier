import logging
import os
import json
import shutil
import modules.ai.agents.excel_categorizer_agent.excel_categorizer_agent_prompts as prompts
from modules.ai.services.ai_service import AiService
from modules.excel.services.excel_service import ExcelService
from modules.ai.agents.excel_categorizer_agent.enums.file_category import FileCategory
import constants.configs as configs


class ExcelCategorizerAgent:
    """
    Class to interact with the AI for categorizing an Excel file.
    """

    def __init__(self, ai_service: AiService, model: str):
        """
        Initialize the AI Agent.
        """
        self.ai_service = ai_service
        self.model = model

    def ask_ai(
        self,
        file_name: str,
        excel_data: str,
        ai_analytics_file_name: str = None,
        log_messages: bool = True,
    ) -> str:
        """
        Ask the AI for a response based on the given excel_data.

        Args:
            file_name (str): The file name to be used.
            excel_data (str): The Excel data to be used.
            ai_analytics_file_name (str): The AI analytics file name to be used.
            log_messages (bool): Flag to indicate if the request messages should be logged.

        Returns:
            str: The AI's response.
        """
        try:
            user_prompt = f"""
Filename = '{file_name}'
```csv
{excel_data}
```
"""
            ai_response = self.ai_service.ask_ai(
                model=self.model,
                system_prompt=prompts.SYSTEM_PROMPT,
                example_prompts=prompts.EXAMPLE_PROMPTS,
                first_user_prompt=user_prompt,
                use_assistant_instead_of_system=False,  # True caso o modelo seja "o1-preview" ou "o1-mini"
                ai_analytics_file_name=ai_analytics_file_name if ai_analytics_file_name else file_name,
                ai_analytics_agent_name="ExcelCategorizerAgent",
                log_request_messages=log_messages,
                log_response_message=log_messages,
            )

            return ai_response
        except Exception as e:
            logging.error(f"Erro ao comunicar com o AI ExcelHeaderFinderAgent: {e}")
            raise

    def do_your_work_with(
        self,
        excel_file_path: str,
        invalid_output_path: str = configs.OUTPUT_FOLDER,
        ai_analytics_file_name: str = None,
    ) -> FileCategory:
        """
        Do the agent's work with the given parameters.

        Args:
            excel_file_path (str): The Excel file path.
            invalid_output_path (str): The invalid output path.
            ai_analytics_file_name (str): The AI analytics file name.

        Returns:
            str: The file's category.
        """
        excel_data_first_5_rows = ExcelService.get_excel_csv_to_csv_str(excel_file_path, only_get_first_rows=5)
        file_name = os.path.basename(excel_file_path)
        excel_categortizer_agent_response = self.ask_ai(
            file_name=file_name,
            excel_data=excel_data_first_5_rows,
            ai_analytics_file_name=ai_analytics_file_name,
        )

        try:
            excel_categortizer_agent_response_dict = json.loads(excel_categortizer_agent_response)
        except json.JSONDecodeError or ValueError as e:
            logging.error(f"Warning - AI ExcelCategorizerAgent: Erro ao converter a resposta do AI para JSON: {e}\nexcel_categortizer_agent_response = {excel_categortizer_agent_response}")
            raise

        try:
            category_by_ai = excel_categortizer_agent_response_dict['category']
        except KeyError as e:
            logging.error(f"Warning - AI ExcelCategorizerAgent: Erro ao obter a chave 'category' do JSON: {e}\nexcel_categortizer_agent_response_dict = {excel_categortizer_agent_response_dict}")
            raise

        category = FileCategory.get_category_by_name(category_by_ai)
        logging.info(f"AI ExcelCategorizerAgent: returned '{category_by_ai}' so the file '{file_name}' is the '{category}' category.")
        
        if category == FileCategory.INVALIDO:
            logging.info(f"AI ExcelCategorizerAgent: O ficheiro '{file_name}' foi categorizado como 'INVALIDO'.")
            invalid_output_path = f"{invalid_output_path}/{category.value} - {file_name}"
            try:
                shutil.copy2(excel_file_path, invalid_output_path)
            except shutil.Error as e:
                logging.error(f"AI ExcelCategorizerAgent: Erro ao guardar o ficheiro '{invalid_output_path}'.")
                raise
            
        return category