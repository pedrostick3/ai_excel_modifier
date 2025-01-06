import logging
import os
import json
import shutil
import time
from modules.ai.fine_tuning_agents.utils.training_file_generator.fine_tuning_training_file_generator import FinetuningTrainingFileGenerator
from modules.ai.services.azure_ai_service import AzureAiService
from modules.excel.services.excel_service import ExcelService
from modules.ai.enums.file_category import FileCategory
import modules.excel.constants.excel_constants as excel_constants
import constants.configs as configs


class ExcelGenericFinetuningAgent:
    """
    Class to interact with the AI Fine-Tuning Agent.
    """
    fine_tuning_model = None

    def __init__(self,
        ai_service: AzureAiService,
        model: str,
        fine_tuning_model: str = None,
    ):
        """
        Initialize the AI Agent.
        """
        self.ai_service = ai_service
        self.base_model = model
        self.fine_tuning_model = fine_tuning_model
    
    def create_fine_tuning_model(
        self,
        generate_training_file: bool = False,
        only_create_fine_tuning_model_if_not_exists: bool = True,
    ) -> None:
        """
        Create the fine-tuning model.
        """
        if only_create_fine_tuning_model_if_not_exists:
            jobs = self.ai_service.get_ai_client().fine_tuning.jobs.list()
            if len(jobs.data) > 0:
                self.fine_tuning_model = jobs.data[0].fine_tuned_model
                return self.fine_tuning_model
        
        if generate_training_file:
            FinetuningTrainingFileGenerator.generate_training_file()
        
        uploaded_file = self.ai_service.get_ai_client().files.create(
            file=open(FinetuningTrainingFileGenerator.training_file, "rb"), # Individual files can be up to 512 MB in size.
            purpose="fine-tune",
        )

        training_job = self.ai_service.get_ai_client().fine_tuning.jobs.create(
            training_file=uploaded_file.id, # The maximum file upload size is 1 GB.
            model=self.model,
        )
        print(f"create_fine_tuning_model - job: {training_job.model_dump_json(indent=2)}")

        status = self.ai_service.get_ai_client().fine_tuning.jobs.retrieve(training_job.id).status
        if status not in ["succeeded", "failed"]:
            print(f"Job not in terminal status: {status}. Waiting.")
            while status not in ["succeeded", "failed"]: # TODO: Quanto tempo vai demorar? pode-se reescrever o treino através de algum id?
                time.sleep(2)
                status = self.ai_service.get_ai_client().fine_tuning.jobs.retrieve(training_job.id).status
                print(f"Status: {status}")
        else:
            print(f"Finetune job {training_job.id} finished with status: {status}")

        print("Checking other finetune jobs in the subscription.")
        jobs = self.ai_service.get_ai_client().fine_tuning.jobs.list()
        print(f"Found {len(jobs.data)} finetune jobs: {jobs.data}")

        if len(jobs.data) == 0:
            print("No finetune jobs found. Exiting.")
            return None

        print(f"create_fine_tuning_model - fine_tuning_model: {jobs.data[0].fine_tuned_model}")
        self.fine_tuning_model = jobs.data[0].fine_tuned_model # TODO: verificar se [0] é o mais recente
        return jobs.data[0].fine_tuned_model

    def ask_ai(
        self,
        user_prompt: str,
        ai_analytics_file_name: str = None,
        log_messages: bool = True,
    ) -> str:
        """
        Ask the AI for a response based on the given excel_data.

        Args:
            user_prompt (str): The user prompt to be used.
            ai_analytics_file_name (str): The AI analytics file name to be used.
            log_messages (bool): Flag to indicate if the request messages should be logged.

        Returns:
            str: The AI's response.
        """
        try:
            ai_response = self.ai_service.ask_ai(
                model=self.fine_tuning_model,
                first_user_prompt=user_prompt,
                use_assistant_instead_of_system=False,  # True caso o modelo seja "o1-preview" ou "o1-mini"
                ai_analytics_file_name=ai_analytics_file_name,
                ai_analytics_agent_name="ExcelGenericFinetuningAgent",
                log_request_messages=log_messages,
                log_response_message=log_messages,
            )

            return ai_response
        except Exception as e:
            logging.error(f"Erro ao comunicar com o AI ExcelGenericFinetuningAgent: {e}")
            raise

    def get_file_category(
        self,
        excel_file_path: str,
        invalid_output_path: str = configs.OUTPUT_FOLDER,
        ai_analytics_file_name: str = None,
    ) -> FileCategory:
        """
        Get the file's category.

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
            user_prompt=f"""Categorize the following file:
Filename = '{file_name}'
```csv
{excel_data_first_5_rows}
```""",
            file_name=file_name,
            excel_data=excel_data_first_5_rows,
            ai_analytics_file_name=ai_analytics_file_name,
        )

        try:
            excel_categortizer_agent_response_dict = json.loads(excel_categortizer_agent_response)
        except json.JSONDecodeError or ValueError as e:
            logging.error(f"Warning - AI ExcelGenericFinetuningAgent: Erro ao converter a resposta do AI para JSON: {e}\nexcel_categortizer_agent_response = {excel_categortizer_agent_response}")
            raise

        try:
            category_by_ai = excel_categortizer_agent_response_dict['category']
        except KeyError as e:
            logging.error(f"Warning - AI ExcelGenericFinetuningAgent: Erro ao obter a chave 'category' do JSON: {e}\nexcel_categortizer_agent_response_dict = {excel_categortizer_agent_response_dict}")
            raise

        category = FileCategory.get_category_by_name(category_by_ai)
        logging.info(f"AI ExcelGenericFinetuningAgent: returned '{category_by_ai}' so the file '{file_name}' is the '{category}' category.")
        
        if category == FileCategory.INVALIDO:
            logging.info(f"AI ExcelGenericFinetuningAgent: O ficheiro '{file_name}' foi categorizado como 'INVALIDO'.")
            invalid_output_path = f"{invalid_output_path}/{category.value} - {file_name}"
            try:
                shutil.copy2(excel_file_path, invalid_output_path)
            except shutil.Error as e:
                logging.error(f"AI ExcelGenericFinetuningAgent: Erro ao guardar o ficheiro '{invalid_output_path}'.")
                raise
            
        return category
    
    def get_excel_header(self, excel_file_path: str, ai_analytics_file_name: str = None) -> str:
        """
        Get the header of the Excel file.

        Args:
            file_path (str): The file path to be used.
            ai_analytics_file_name (str): The AI analytics file name to be used.

        Returns:
            dict: The header row.
        """
        file_name = os.path.basename(excel_file_path)
        excel_data_first_5_rows = ExcelService.get_excel_csv_to_csv_str(excel_file_path, only_get_first_rows=5)
        excel_header_finder_agent_response = self.ask_ai(
            user_prompt=f"Find the header of the following file:\n{excel_data_first_5_rows}",
            response_format=self.ai_service.JSON_RESPONSE_FORMAT, # {"type": "json_object"}
            ai_analytics_file_name=ai_analytics_file_name if ai_analytics_file_name else file_name,
        )

        try:
            excel_header_finder_agent_response_dict = json.loads(excel_header_finder_agent_response)
        except ValueError:
            logging.error(f"Warning - AI ExcelGenericFinetuningAgent - Cabeçalho não encontrado nas primeiras 10 linhas do ficheiro {excel_file_path}. ai_agent_response: {excel_header_finder_agent_response}")
            excel_header_finder_agent_response_dict = {}
        
        return excel_header_finder_agent_response_dict['row_content']
    
    def modify_pre_header(
        self,
        category: FileCategory,
        input_excel_file_path: str,
        header_row_number: int,
        output_excel_file_path: str,
        ai_analytics_file_name: str = None,
    ) -> bool:
        """
        Modify the pre-header of the Excel file.

        Args:
            category (FileCategory): The category of the file.
            input_excel_file_path (str): The path to the input Excel file.
            header_row_number (int): The number of the header row.
            output_excel_file_path (str): The path to the output Excel file.
            ai_analytics_file_name (str): The AI analytics file name to be used.

        Returns:
            bool: The success of the operation.
        """
        excel_data_first_rows_until_header = ExcelService.get_excel_csv_to_csv_str(input_excel_file_path, only_get_first_rows=header_row_number)
        logging.info(f"AI ExcelGenericFinetuningAgent - {category} - excel_data_first_rows_until_header = {excel_data_first_rows_until_header}")
        excel_pre_header_modifier_agent_response = self.ask_ai(
            user_prompt=f"Modify the pre-header of the following file that belongs to the '{category.value}' category:\n{excel_data_first_rows_until_header}",
            ai_analytics_file_name=ai_analytics_file_name,
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
                logging.error(f"Warning - AI ExcelGenericFinetuningAgent - Não foi possível guardar o ficheiro '{output_excel_file_path}'.")

            return success
        except Exception as e:
            logging.error(f"Erro ao processar o retorno do AI ExcelGenericFinetuningAgent: {e}")
            raise

    def modify_content(
        self,
        category: FileCategory,
        input_excel_file_path: str,
        output_excel_file_path: str,
        excel_header_row_index: int,
        ai_analytics_file_name: str = None,
    ) -> None:
        """
        Processes an Excel file by splitting it into parts if it exceeds a specified number of lines,
        sends each part to an AI service for modification, and saves the modified content back to the file.

        Args:
            category (FileCategory): The category of the file.
            excel_input_file_path (str): The path to the Excel file to be processed.
            excel_output_file_path (str): The path to the Excel file to be saved.
            excel_header_row_index (int): The row index of the header in the Excel file.
            ai_analytics_file_name (str, optional): The AI analytics file name to be used. Defaults to None.

        Returns:
            None
        """
        try:
            excel_data = ExcelService.get_excel_csv_to_csv_str(input_excel_file_path)
        except Exception as e:
            logging.error(f"AI ExcelGenericFinetuningAgent: Error reading Excel file: {e}")
            raise

        excel_lines = excel_data.split(excel_constants.EXCEL_LINE_BREAK)
        excel_lines_count = len(excel_lines) - 1
        logging.info(f"AI ExcelGenericFinetuningAgent - {category} - The file '{input_excel_file_path}' has {excel_lines_count} lines.")
        
        try:
            python_code = self.ask_ai(
                user_prompt=f"""Return the python code to modify the content of the following file that belongs to the '{category.value}' category:
input_excel_file_path = '{input_excel_file_path}'
output_excel_file_path = '{output_excel_file_path}'
excel_header_row_index = {excel_header_row_index}""",
                ai_analytics_file_name=ai_analytics_file_name,
            )
        except Exception as e:
            logging.error(f"AI ExcelGenericFinetuningAgent: Error communicating with AI: {e}")
            raise

        try:
            exec(python_code, globals())
        except Exception as e:
            logging.error(f"AI ExcelGenericFinetuningAgent: Error running the AI python code: {e}")
            raise