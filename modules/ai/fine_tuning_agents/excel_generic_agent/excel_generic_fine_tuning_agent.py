import logging
import os
import json
import shutil
import time
from modules.ai.fine_tuning_agents.utils.training_file_generator.fine_tuning_training_file_generator import FinetuningTrainingFileGenerator
from modules.ai.services.ai_service import AiService
from modules.ai.services.openai_ai_service import OpenAiAiService
from modules.excel.services.excel_service import ExcelService
from modules.ai.enums.file_category import FileCategory
from modules.ai.enums.ai_fine_tuning_job_status import AiFineTuningJobStatus
from modules.ai.enums.ai_file_status import AiFileStatus
import modules.excel.constants.excel_constants as excel_constants
import constants.configs as configs
import modules.ai.fine_tuning_agents.excel_generic_agent.excel_generic_fine_tuning_agent_prompts as prompts
from modules.ai.function_calls_agent.enums.functions_to_call import FunctionsToCall



class ExcelGenericFinetuningAgent:
    """
    Class to interact with the AI Fine-Tuning Agent.
    """
    fine_tuning_model = None

    def __init__(self,
        ai_service: OpenAiAiService,
        base_model: str,
        fine_tuning_model: str = None,
        delete_fine_tuning_model: bool = False,
        delete_fine_tuning_model_safety_trigger: bool = False,
        create_fine_tuning_model: bool = False,
        only_create_fine_tuning_model_if_not_exists: bool = True,
        force_rewrite_training_file: bool = False,
    ):
        """
        Initialize the AI Agent.

        To create a fine-tuning model, the parameter 'create_fine_tuning_model' must be True and it's not necessary to pass the 'fine_tuning_model' parameter.

        To delete a fine-tuning model, the parameters 'delete_fine_tuning_model' and 'delete_fine_tuning_model_safety_trigger' must be True and it's necessary to pass the 'fine_tuning_model' parameter.
        """
        self.ai_service = ai_service
        self.base_model = base_model
        self.fine_tuning_model = fine_tuning_model
        if delete_fine_tuning_model and delete_fine_tuning_model_safety_trigger:
            self.delete_fine_tuning_model(fine_tuning_model_to_delete=fine_tuning_model)
        if create_fine_tuning_model:
            self.create_fine_tuning_model(
                only_create_fine_tuning_model_if_not_exists=only_create_fine_tuning_model_if_not_exists,
                force_rewrite_training_file=force_rewrite_training_file,
            )
    
    def delete_fine_tuning_model(
        self, 
        fine_tuning_model_to_delete: str,
        exit_to_delete_the_training_file_of_fine_tuning_model_in_the_web_interface: bool = True,
        delete_all_step_models: bool = True,
    ) -> bool:
        """
        Delete the fine-tuning model.
        You must have the Owner role in your organization to delete a model.
        Notes:
        - After deleting a model, you can't use it and recover it anymore.
        - After deleting a model, the historical job data records will still show the model name, but the model won't be available for use. [Source](https://community.openai.com/t/how-to-delete-a-fine-tune-model-via-api/13831/12)
        - When training a model, the job creates checkpoint-step models that are irelevant. That checkpoint-step models have "ckpt-step-" in its name. All those checkpoint-step models will be delete since 'delete_all_step_models' parameter is True by default.
        """
        if delete_all_step_models:
            models = self.ai_service.get_ai_client().models.list()
            logging.info(f"ExcelGenericFinetuningAgent - delete_fine_tuning_model(): Found {len(models.data)} models: {models.data}")
            step_models_ids = [model.id for model in models.data if "ckpt-step-" in model.id]
            for step_model_id in step_models_ids:
                deleted_model = self.ai_service.get_ai_client().models.delete(step_model_id)
                if deleted_model.deleted:
                    logging.info(f"ExcelGenericFinetuningAgent - delete_fine_tuning_model(): Step model deleted. (step_model_id = {step_model_id})")
                else:
                    logging.error(f"ExcelGenericFinetuningAgent - delete_fine_tuning_model(): Step model not deleted. (step_model_id = {step_model_id})")

        if fine_tuning_model_to_delete:
            models = self.ai_service.get_ai_client().models.list()
            logging.info(f"ExcelGenericFinetuningAgent - delete_fine_tuning_model(): Found {len(models.data)} models: {models.data}")
            model_exists = any(fine_tuning_model_to_delete == model.id for model in models.data)
            if not model_exists:
                logging.info(f"ExcelGenericFinetuningAgent - delete_fine_tuning_model(): Fine-tuning model not found. (fine_tuning_model_to_delete = {fine_tuning_model_to_delete})")
                return False
            
            deleted_model = self.ai_service.get_ai_client().models.delete(fine_tuning_model_to_delete)
            if deleted_model.deleted:
                logging.info(f"ExcelGenericFinetuningAgent - delete_fine_tuning_model(): Fine-tuning model deleted. (fine_tuning_model_to_delete = {fine_tuning_model_to_delete})")
                if exit_to_delete_the_training_file_of_fine_tuning_model_in_the_web_interface:
                    logging.info("ExcelGenericFinetuningAgent - delete_fine_tuning_model(): You should manually delete the training file of the fine-tuning model in the respective AI Provider Web Interface.\nExiting...")
                    exit()
                return True
        
        logging.info(f"ExcelGenericFinetuningAgent - delete_fine_tuning_model(): No fine-tuning model to delete. (fine_tuning_model_to_delete = {fine_tuning_model_to_delete})")
        return False

    def create_fine_tuning_model(
        self,
        generate_training_file: bool = True,
        force_rewrite_training_file: bool = False,
        only_create_fine_tuning_model_if_not_exists: bool = True,
        exit_to_deploy_fine_tuning_model_in_azure_ai_foundry_web_interface: bool = True,
    ) -> None:
        """
        Create the fine-tuning model.
        To deploy the created fine-tuning model, use the Azure AI Foundry Web Interface by following this [tutorial](https://dev.to/icebeam7/fine-tuning-a-model-with-azure-open-ai-studio-39p7).
        You can try to deploy with code like [this](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning?tabs=azure-openai%2Cturbo%2Cpython-new&pivots=programming-language-python#deploy-a-fine-tuned-model).
        If your're gona try to deploy with code, check this [stackoverflow answer](https://stackoverflow.com/a/77492894/16451258) too.
        """
        if only_create_fine_tuning_model_if_not_exists:
            jobs = self.ai_service.get_ai_client().fine_tuning.jobs.list()
            logging.info(f"ExcelGenericFinetuningAgent - create_fine_tuning_model(): Found {len(jobs.data)} fine-tuning jobs: {jobs.data}")
            model_job_exists_and_is_succeed = any(self.fine_tuning_model == job.fine_tuned_model and AiFineTuningJobStatus.is_succeed(job.status) for job in jobs.data)
            models = self.ai_service.get_ai_client().models.list()
            logging.info(f"ExcelGenericFinetuningAgent - create_fine_tuning_model(): Found {len(models.data)} models: {models.data}")
            model_exists = any(self.fine_tuning_model == model.id for model in models.data)
            if model_job_exists_and_is_succeed and model_exists:
                self.fine_tuning_model = next(model.id for model in models.data if self.fine_tuning_model == model.id)
                logging.info(f"ExcelGenericFinetuningAgent - create_fine_tuning_model(): Fine-tuning model already exists: {self.fine_tuning_model}")
                return self.fine_tuning_model

        if generate_training_file:
            FinetuningTrainingFileGenerator.generate_training_file(force_rewrite=force_rewrite_training_file)
        
        uploaded_files = self.ai_service.get_ai_client().files.list().data
        training_file_already_uploaded = any(file.filename == os.path.basename(FinetuningTrainingFileGenerator.training_file) for file in uploaded_files)
        logging.info(f"ExcelGenericFinetuningAgent - create_fine_tuning_model(): Training file already uploaded: {training_file_already_uploaded}")

        if training_file_already_uploaded:
            uploaded_file = next(file for file in uploaded_files if file.filename == os.path.basename(FinetuningTrainingFileGenerator.training_file))
        else:
            uploaded_file = self.ai_service.get_ai_client().files.create(
                file=open(FinetuningTrainingFileGenerator.training_file, "rb"), # Individual files can be up to 512 MB in size.
                purpose="fine-tune", # Can't be "fine-tuning"
            )
            uploaded_file = self.ai_service.get_ai_client().files.retrieve(uploaded_file.id)
            if not AiFileStatus.has_finished(uploaded_file.status):
                logging.info(f"Uploaded file {uploaded_file.id} not finished. Status: {uploaded_file.status}. Waiting...")
                while not AiFileStatus.has_finished(uploaded_file.status): # É quase instantâneo
                    time.sleep(1) # 1 second
                    uploaded_file = self.ai_service.get_ai_client().files.retrieve(uploaded_file.id)
        logging.info(f"ExcelGenericFinetuningAgent - create_fine_tuning_model(): Uploaded file: {uploaded_file.model_dump_json(indent=2)}")

        training_job = self.ai_service.get_ai_client().fine_tuning.jobs.create(
            training_file=uploaded_file.id, # The maximum file upload size is 1 GB. Training file must have at least 10 examples.
            model=self.base_model,
            hyperparameters={
                "n_epochs": 10, # The default number of epochs is 5. Epochs are the number of iterations the model will go through the training_file to learn the data.
            },
        )
        training_start_time = time.time()
        logging.info(f"ExcelGenericFinetuningAgent - create_fine_tuning_model(): Training job: {training_job.model_dump_json(indent=2)}")
        training_job = self.ai_service.get_ai_client().fine_tuning.jobs.retrieve(training_job.id)
        if not AiFineTuningJobStatus.has_finished(training_job.status):
            logging.info(f"Training job {training_job.id} not finished. Status: {training_job.status}. Waiting...")
            while not AiFineTuningJobStatus.has_finished(training_job.status):
                # Azure - It took 20m36s and billed 55k tokens to train with the "gpt-4o-mini" model and 11 examples.
                # Azure - It took 21m57s and billed 55k tokens to train with the "gpt-4o-mini" model and 18 examples.
                # OpenAI - It took 9m2s and billed 56825 tokens to train with the "gpt-4o-mini-2024-07-18" model and 18 examples.
                time.sleep(5) # 5 seconds
                training_job = self.ai_service.get_ai_client().fine_tuning.jobs.retrieve(training_job.id)
        training_time = time.time() - training_start_time
        logging.info(f"ExcelGenericFinetuningAgent - create_fine_tuning_model(): Training job {training_job.id} finished with status: {training_job.status} in {training_time} seconds.")

        logging.info(f"ExcelGenericFinetuningAgent - create_fine_tuning_model(): Checking other fine-tuning jobs in the subscription.")
        jobs = self.ai_service.get_ai_client().fine_tuning.jobs.list()
        logging.info(f"ExcelGenericFinetuningAgent - create_fine_tuning_model(): Found {len(jobs.data)} fine-tuning jobs: {jobs.data}")

        if len(jobs.data) == 0 or not AiFineTuningJobStatus.is_succeed(training_job.status):
            logging.error("ExcelGenericFinetuningAgent - create_fine_tuning_model(): No valid fine-tuning jobs found.")
            return None

        logging.info(f"ExcelGenericFinetuningAgent - create_fine_tuning_model(): Fine-tuning model: {jobs.data[0].fine_tuned_model}")
        self.fine_tuning_model = jobs.data[0].fine_tuned_model

        if exit_to_deploy_fine_tuning_model_in_azure_ai_foundry_web_interface:
            logging.info("ExcelGenericFinetuningAgent - create_fine_tuning_model(): If you're using Azure, you must deploy the fine-tuning model in the Azure AI Foundry Web Interface.\nExiting...")
            exit()
        return jobs.data[0].fine_tuned_model

    def ask_ai(
        self,
        user_prompt: str,
        system_prompt: str,
        tools: list[dict] = None,
        tool_choice: str = None,
        ai_analytics_file_name: str = None,
        log_messages: bool = True,
    ) -> str:
        """
        Ask the AI for a response based on the given excel_data.

        Args:
            user_prompt (str): The user prompt to be used.
            tools (list[dict]): The tools to be used.
            tool_choice (str): Force the function calling by setting the tool choice to "required". [Source](https://community.openai.com/t/new-api-feature-forcing-function-calling-via-tool-choice-required/731488) 
            ai_analytics_file_name (str): The AI analytics file name to be used.
            log_messages (bool): Flag to indicate if the request messages should be logged.

        Returns:
            str: The AI's response.
        """
        try:
            ai_response = self.ai_service.ask_ai(
                model=self.fine_tuning_model,
                base_model=self.base_model,
                first_user_prompt=user_prompt,
                system_prompt=system_prompt,
                tools=tools,
                tool_choice=tool_choice,
                use_assistant_instead_of_system=False,  # True caso o modelo seja "o1-preview" ou "o1-mini"
                response_format=None,
                ai_analytics_file_name=ai_analytics_file_name,
                ai_analytics_agent_name="ExcelGenericFinetuningAgent",
                log_request_messages=log_messages,
                log_response_message=log_messages,
            )

            return ai_response
        except Exception as e:
            logging.error(f"Erro ao comunicar com o AI ExcelGenericFinetuningAgent: {e}")
            raise
    
    def _handle_category_from_ai_category_agent_response_string(
        self,
        ai_agent_response: str,
        file_name: str,
        excel_file_path: str,
        invalid_output_path: str,
        function_id_to_log: str,
    ) -> FileCategory:
        """
        Handle the category from the AI category agent response string.

        Args:
            ai_agent_response (str): The AI category agent response.
            file_name (str): The file name.
            excel_file_path (str): The Excel file path.
            invalid_output_path (str): The invalid output path.
            function_id_to_log (str): The function ID to log.

        Returns:
            FileCategory: The FileCategory.
        """
        try:
            ai_agent_response_dict = json.loads(ai_agent_response)
        except json.JSONDecodeError or ValueError as e:
            logging.error(f"Warning - {function_id_to_log}: Erro ao converter a resposta do AI para JSON: {e}\nai_agent_response = {ai_agent_response}")
            raise

        try:
            category_by_ai = ai_agent_response_dict['category']
        except KeyError as e:
            logging.error(f"Warning - {function_id_to_log}: Erro ao obter a chave 'category' do JSON: {e}\nai_agent_response = {ai_agent_response_dict}")
            raise

        category = FileCategory.get_category_by_name(category_by_ai)
        logging.info(f"{function_id_to_log}: returned '{category_by_ai}' so the file '{file_name}' is the '{category}' category.")
        
        if category == FileCategory.INVALIDO:
            logging.info(f"{function_id_to_log}: O ficheiro '{file_name}' foi categorizado como 'INVALIDO'.")
            invalid_output_path = f"{invalid_output_path}/{category.value} - {file_name}"
            try:
                shutil.copy2(excel_file_path, invalid_output_path)
            except shutil.Error as e:
                logging.error(f"{function_id_to_log}: Erro ao guardar o ficheiro '{invalid_output_path}'.")
                raise
        
        return category

    def get_file_category_and_header(
        self,
        excel_file_path: str,
        invalid_output_path: str = configs.OUTPUT_FOLDER,
        ai_analytics_file_name: str = None,
    ) -> dict:
        """
        Get the file's category and header.

        Args:
            excel_file_path (str): The Excel file path.
            invalid_output_path (str): The invalid output path.
            ai_analytics_file_name (str): The AI analytics file name.

        Returns:
            dict: The file's category and header.
        """
        excel_data_first_5_rows = ExcelService.get_excel_csv_to_csv_str(excel_file_path, only_get_first_rows=5)
        file_name = os.path.basename(excel_file_path)
        excel_categorizer_and_header_finder_agent_response = self.ask_ai(
            system_prompt=prompts.CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
            user_prompt=f"""Categorize and find the header of the following file:
Filename = '{file_name}'
```csv
{excel_data_first_5_rows}
```""",
            ai_analytics_file_name=ai_analytics_file_name,
        )

        self._handle_category_from_ai_category_agent_response_string(
            ai_agent_response=excel_categorizer_and_header_finder_agent_response,
            file_name=file_name,
            excel_file_path=excel_file_path,
            invalid_output_path=invalid_output_path,
            function_id_to_log="AI ExcelGenericFinetuningAgent - get_file_category_and_header()",
        )

        try:
            excel_categorizer_and_header_finder_agent_response_dict = json.loads(excel_categorizer_and_header_finder_agent_response)
        except json.JSONDecodeError or ValueError as e:
            logging.error(f"Warning - AI ExcelGenericFinetuningAgent - get_file_category_and_header(): Erro ao converter a resposta do AI para JSON: {e}\nexcel_categorizer_and_header_finder_agent_response = {excel_categorizer_and_header_finder_agent_response}")
            raise
            
        return excel_categorizer_and_header_finder_agent_response_dict if excel_categorizer_and_header_finder_agent_response_dict else {}

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
        excel_categorizer_agent_response = self.ask_ai(
            system_prompt=prompts.CATEGORIZER_SYSTEM_PROMPT,
            user_prompt=f"""Categorize the following file:
Filename = '{file_name}'
```csv
{excel_data_first_5_rows}
```""",
            ai_analytics_file_name=ai_analytics_file_name,
        )

        return self._handle_category_from_ai_category_agent_response_string(
            ai_agent_response=excel_categorizer_agent_response,
            file_name=file_name,
            excel_file_path=excel_file_path,
            invalid_output_path=invalid_output_path,
            function_id_to_log="AI ExcelGenericFinetuningAgent - get_file_category()",
        )
    
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
            system_prompt=prompts.HEADER_FINDER_SYSTEM_PROMPT,
            user_prompt=f"Find the header of the following file:\n{excel_data_first_5_rows}",
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
            system_prompt=prompts.PRE_HEADER_MODIFIER_SYSTEM_PROMPT,
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

    def modify_content_returning_code(
        self,
        category: FileCategory,
        input_excel_file_path: str,
        output_excel_file_path: str,
        excel_header_row_index: int,
        ai_analytics_file_name: str = None,
    ) -> None:
        """
        Make AI return the code to modify the content of the Excel file.

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
                system_prompt=prompts.CONTENT_MODIFIER_SYSTEM_PROMPT,
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
    
    def modify_content_returning_function_calling(
        self,
        category: FileCategory,
        input_excel_file_path: str,
        output_excel_file_path: str,
        excel_header_row_index: int,
        ai_analytics_file_name: str = None,
    ) -> None:
        """
        Make AI return the function to call that modifies the content of the Excel file.

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
            ai_response = self.ask_ai(
                system_prompt=prompts.CONTENT_MODIFIER_SYSTEM_PROMPT,
                user_prompt=f"""Return the function to call that modifies the content of the following file that belongs to the '{category.value}' category:
input_excel_file_path = '{input_excel_file_path}'
output_excel_file_path = '{output_excel_file_path}'
excel_header_row_index = {excel_header_row_index}""",
                ai_analytics_file_name=ai_analytics_file_name,
                tool_choice="required",
                tools=[
                    *FunctionsToCall.MODIFY_EXCEL_CONTENT_FOR_EXECUTION_CATEGORY.value["tools"],
                    *FunctionsToCall.MODIFY_EXCEL_CONTENT_FOR_TEST_EXECUTION_CATEGORY.value["tools"],
                ],
            )
        except Exception as e:
            logging.error(f"AI ExcelGenericFinetuningAgent: Error communicating with AI: {e}")
            raise

        try:
            response_json = json.loads(ai_response)
        except json.JSONDecodeError:
            logging.error(f"AI ExcelGenericFinetuningAgent: Error parsing AI response JSON: {ai_response}")
            raise
        
        if "function" not in response_json:
            logging.error(f"AI ExcelGenericFinetuningAgent: The AI response JSON does not contain the 'function' key. ai_response = {ai_response}")
            raise

        try:
            FunctionsToCall.get_enum_by_function_name(response_json["function"]["name"]).run_function_from_ai_response(
                str_dict_func_args=response_json["function"]["arguments"],
            )
        except json.JSONDecodeError:
            logging.error(f"AI ExcelGenericFinetuningAgent: Error executing function. response_json: {response_json}")
            raise