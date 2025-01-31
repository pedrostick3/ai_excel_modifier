import os
import logging
from datetime import datetime
import constants.configs as configs
from modules.excel.services.excel_service import ExcelService
from modules.ai_langchain_implementation.poc3_agent.poc3_langchain_agent import PoC3LangChainAgent
from modules.ai_langchain_implementation.services.langchain_ai_service import LangChainAiService
from modules.ai_manual_implementation.enums.file_category import FileCategory

class AiLangChainImplementation:
    """
    This class is a LangChain implementation of the AI process for PoC3.
    """
    
    @staticmethod
    def run(
        input_files: list[str],
        finetuning_model: str,
        only_test_simple_examples: bool = False,
    ):
        """
        Run the AI process for PoC3.

        Args:
            input_files (list[str]): List of input files to process.
            finetuning_model (str): Fine-tuning model.
        """
        # Config logs
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                handlers=[logging.FileHandler("process.log", encoding='utf-8'), logging.StreamHandler()],
            )
        logging.info("A iniciar AI APP")

        # Initialize the LangChain AI Service and the PoC3 LangChain Agent
        langchain_ai_service = LangChainAiService(
            openai_api_key=configs.OPENAI_API_KEY,
            ai_model=finetuning_model,
        )
        ai_agent = PoC3LangChainAgent(ai_service=langchain_ai_service)

        # Create the output folder if it does not exist
        os.makedirs(configs.OUTPUT_FOLDER, exist_ok=True)

        if only_test_simple_examples:
            # Test the LangChain AI service
            response = langchain_ai_service.test_invocation()
            print(f"langchain_ai_service.test_invocation().response = {response}")
            response = langchain_ai_service.test_chaining()
            print(f"langchain_ai_service.test_chaining().response = {response}")
            response = langchain_ai_service.test_tool_function_calling()
            print(f"langchain_ai_service.test_tool_function_calling().response = {response}")
            return

        # Process the input files
        for file_name in input_files:
            file_path = os.path.join(configs.INPUT_FOLDER, file_name)
            logging.info(f"#### Start processing file: {file_path} ####")
        
            logging.info("#1. START - ExcelCategorizerAndHeaderFinderAgent")
            file_category_and_header = ai_agent.get_file_category_and_header(
                excel_file_path=file_path,
                ai_analytics_file_name=os.path.basename(file_path),
            )

            # Get category from the agent response
            try:
                category_by_ai = file_category_and_header['category']
            except KeyError as e:
                logging.error(f"Erro ao obter \"file_category_and_header['category']\": {e}\nfile_category_and_header = {file_category_and_header}")
                raise
            file_category = FileCategory.get_category_by_name(category_by_ai)
            logging.info(f"The file '{file_name}' is '{file_category}' category.")
            if file_category == FileCategory.INVALIDO:
                continue

            # Get header from the agent response
            try:
                excel_header = file_category_and_header['header']['row_content']
            except KeyError as e:
                logging.error(f"Erro ao obter \"file_category_and_header['header']['row_content']\": {e}\nfile_category_and_header = {file_category_and_header}")
                raise

            logging.info("#1. END - ExcelCategorizerAndHeaderFinderAgent")
            new_file_name = f'{file_category.value} - {datetime.now().strftime("%d_%m_%Y")} - {file_name}'
            output_file_path = f"{configs.OUTPUT_FOLDER}/{new_file_name}"

            # 3. Modificar Excel antes do cabeçalho
            logging.info("#3. START - ExcelGenericFinetuningAgent")
            ai_agent.modify_pre_header(
                category=file_category,
                input_excel_file_path=file_path,
                header_row_number=ExcelService.get_excel_csv_row_number(file_path, excel_header),
                output_excel_file_path=output_file_path,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            logging.info("#3. END - ExcelGenericFinetuningAgent")

            header_row_number = ExcelService.get_excel_csv_row_number(output_file_path, excel_header)

            # 4. Modificar Excel depois do cabeçalho
            logging.info("#4. START - ExcelGenericFinetuningAgent - modify_content_returning_function_calling()")
            ai_agent.modify_content_returning_function_calling(
                category=file_category,
                input_excel_file_path=output_file_path,
                output_excel_file_path=output_file_path,
                excel_header_row_index=header_row_number - 1, # -1 para obter o index
                ai_analytics_file_name=os.path.basename(file_path),
            )
            logging.info("#4. END - ExcelGenericFinetuningAgent - modify_content_returning_function_calling()")
