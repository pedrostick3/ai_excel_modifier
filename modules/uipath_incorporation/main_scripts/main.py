import os
import logging
from datetime import datetime
from modules.ai_manual_implementation.services.openai_ai_service import OpenAiAiService
from modules.ai_manual_implementation.core.fine_tuning_agents.excel_fine_tuning_agent import ExcelFinetuningAgent
from modules.ai_manual_implementation.core.enums.file_category import FileCategory
from modules.excel.services.excel_service import ExcelService
from modules.analytics.services.ai_analytics import AiAnalytics

OPENAI_FINE_TUNING_BASE_MODEL = "gpt-4o-mini-2024-07-18" # https://platform.openai.com/docs/models OR https://openai.com/api/pricing
OPENAI_FINE_TUNING_MODEL = "ft:gpt-4o-mini-2024-07-18:inspireit::AqjmD7gd" # Can be found in https://platform.openai.com/finetune/. It's the name of the model or you can check too in the 'Output model' propriety.

def runExcelAiAgentWith(
    openai_api_key: str,
    input_excel_file_path: str,
    output_folder_path: str = "./assets/docs_output",
    is_to_log: bool = True,
) -> bool:
    # Configurar logs
    if is_to_log and not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler("process.log", encoding='utf-8'), logging.StreamHandler()],
        )
    logging.info("Starting...")

    # Configurar Fine-Tuning AI Service
    fine_tuning_agent = ExcelFinetuningAgent(
        ai_service=OpenAiAiService(api_key=openai_api_key),
        base_model=OPENAI_FINE_TUNING_BASE_MODEL,
        fine_tuning_model=OPENAI_FINE_TUNING_MODEL,
    )
    
    os.makedirs(output_folder_path, exist_ok=True) # Criar pasta de output se não existir

    # Processar ficheiro
    input_excel_file_name = os.path.basename(input_excel_file_path)
    logging.info(f"#### Start processing file: {input_excel_file_path} ####")

    # 1. 2. Categorizar Excel & perceber onde começa a tabela retornando a linha do cabeçalho
    logging.info("#1. 2. START - ExcelGenericFinetuningAgent")
    file_category_and_header = fine_tuning_agent.get_file_category_and_header(
        excel_file_path=input_excel_file_path,
        invalid_output_path=output_folder_path,
        ai_analytics_file_name=input_excel_file_name,
    )

    # Get category from the agent response
    try:
        category_by_ai = file_category_and_header['category']
    except KeyError as e:
        logging.error(f"Warning - Erro ao obter \"file_category_and_header['category']\": {e}\nfile_category_and_header = {file_category_and_header}")
        raise
    file_category = FileCategory.get_category_by_name(category_by_ai)
    logging.info(f"The file '{input_excel_file_name}' is '{file_category}' category.")
    if file_category == FileCategory.INVALIDO:
        logging.info(AiAnalytics.__str__())
        AiAnalytics.export_str_ai_analytics_data_to_excel()
        return False

    # Get header from the agent response
    try:
        excel_header = file_category_and_header['header']['row_content']
    except KeyError as e:
        logging.error(f"Warning - Erro ao obter \"file_category_and_header['header']['row_content']\": {e}\nfile_category_and_header = {file_category_and_header}")
        raise
    logging.info("#1. 2. END - ExcelGenericFinetuningAgent")

    new_file_name = f'{file_category.value} - {datetime.now().strftime("%d_%m_%Y")} - {input_excel_file_name}'
    output_file_path = f"{output_folder_path}/{new_file_name}"

    # 3. Modificar Excel antes do cabeçalho
    logging.info("#3. START - ExcelGenericFinetuningAgent")
    fine_tuning_agent.modify_pre_header(
        category=file_category,
        input_excel_file_path=input_excel_file_path,
        header_row_number=ExcelService.get_excel_csv_row_number(input_excel_file_path, excel_header),
        output_excel_file_path=output_file_path,
        ai_analytics_file_name=input_excel_file_name,
    )
    logging.info("#3. END - ExcelGenericFinetuningAgent")

    header_row_number = ExcelService.get_excel_csv_row_number(output_file_path, excel_header)

    # 4. Modificar Excel depois do cabeçalho
    logging.info("#4. START - ExcelGenericFinetuningAgent - modify_content_returning_function_calling()")
    fine_tuning_agent.modify_content_returning_function_calling(
        category=file_category,
        input_excel_file_path=output_file_path,
        output_excel_file_path=output_file_path,
        excel_header_row_index=header_row_number - 1, # -1 para obter o index
        ai_analytics_file_name=input_excel_file_name,
    )
    logging.info("#4. END - ExcelGenericFinetuningAgent - modify_content_returning_function_calling()")
        
    logging.info(AiAnalytics.__str__())
    AiAnalytics.export_str_ai_analytics_data_to_excel()

    return True

def testRun(
    openai_api_key: str,
    execution_data_file_path: str = "./assets/docs_input/Execution_data Template.xlsx",
    test_execution_data_file_path: str = "./assets/docs_input/Test_Execution_data Template.xlsx",
    parameterization_file_path: str = "./assets/docs_input/ParameterizationFile_testes_13112024.xlsx",
    output_folder_path: str = "./assets/docs_output",
) -> list[bool]:
    execution_data_file_result = runExcelAiAgentWith(
        openai_api_key=openai_api_key,
        input_excel_file_path=execution_data_file_path,
        output_folder_path=output_folder_path,
    )
    test_execution_data_file_result = runExcelAiAgentWith(
        openai_api_key=openai_api_key,
        input_excel_file_path=test_execution_data_file_path,
        output_folder_path=output_folder_path,
    )
    parameterization_file_result = runExcelAiAgentWith(
        openai_api_key=openai_api_key,
        input_excel_file_path=parameterization_file_path,
        output_folder_path=output_folder_path,
    )
    return [execution_data_file_result, test_execution_data_file_result, parameterization_file_result]

if __name__ == "__main__":
    results = testRun("YOUR_OPENAI_API_KEY")
    print(f"Results: {results}")