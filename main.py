import os
import logging
from datetime import datetime
import constants.configs as configs
from modules.excel.services.excel_service import ExcelService
from modules.ai.services.custom_ai_service import CustomAiService
from modules.ai.agents.excel_categorizer_agent.excel_categorizer_agent import ExcelCategorizerAgent
from modules.ai.agents.excel_header_finder_agent.excel_header_finder_agent import ExcelHeaderFinderAgent
from modules.ai.agents.excel_pre_header_modifier_agent.excel_pre_header_modifier_agent import ExcelPreHeaderModifierAgent
from modules.ai.agents.excel_content_modifier_agent.excel_content_modifier_agent import ExcelContentModifierAgent
from modules.ai.agents.excel_categorizer_agent.enums.file_category import FileCategory
from modules.analytics.services.ai_analytics import AiAnalytics


CUSTOM_AI_SERVICE_BASE_URL = configs.GITHUB_BASE_URL
CUSTOM_AI_SERVICE_KEY = configs.GITHUB_KEY
CUSTOM_AI_SERVICE_MODEL = configs.GITHUB_MODEL

def main():
    # Ficheiros para o PoC3
    input_files = [
        #"Execution_data Template.xlsx", # OK (testado com o gpt-4o) - CompletionUsage(completion_tokens=35335, prompt_tokens=58397, total_tokens=93732) - Demorou 16m14s para excel de 495 linhas por 9 colunas (25 partes | 20 linhas por cada parte em que a última parte tinha 15 linhas)
        #"ParameterizationFile_testes_13112024.xlsx", # OK - CompletionUsage(completion_tokens=7, prompt_tokens=992, total_tokens=999) - Demorou menos de 1s tendo usado apenas o ExcelCategorizerAgent.
        "Test_Execution_data Template.xlsx", # OK (testado com o gpt-4o) - CompletionUsage(completion_tokens=36509, prompt_tokens=57348, total_tokens=93857) - Demorou 15m56s para excel de 497 linhas por 9 colunas (25 partes | 20 linhas por cada parte em que a última parte tinha 17 linhas)
        #"Test_Execution_data Template_half.xlsx",
        #"Test_Execution_data Template_quarter.xlsx",
        #"Test_Execution_data Template_50rows.xlsx",
    ]

    # Configurar logs
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("process.log"), logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)
    logger.info("A iniciar AI APP")

    # Configurar Custom AI Service
    ai_service = CustomAiService(CUSTOM_AI_SERVICE_KEY, CUSTOM_AI_SERVICE_BASE_URL)
    
    os.makedirs(configs.OUTPUT_FOLDER, exist_ok=True) # Criar pasta de output se não existir

    # Processar cada ficheiro
    for file_name in input_files:
        file_path = os.path.join(configs.INPUT_FOLDER, file_name)
        print(f"Processando ficheiro: {file_path}")

        # 1. Categorizar Excel
        print("#1. START .1#")
        excel_categorizer_agent_response = ExcelCategorizerAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_with(file_path)
        if excel_categorizer_agent_response == FileCategory.INVALIDO:
            logging.info(f"AI ExcelCategorizerAgent: The file '{file_path}' is '{excel_categorizer_agent_response}'.")
            continue
        print("#1. END .1#")

        new_file_name = f'{excel_categorizer_agent_response.value} - {datetime.now().strftime("%d_%m_%Y")} - {file_name}'
        output_file_path = f"{configs.OUTPUT_FOLDER}/{new_file_name}"
        
        # 2. Perceber onde começa a tabela retornando a linha do cabeçalho
        print("#2. START .2#")
        excel_header_finder_agent_response_row_content = ExcelHeaderFinderAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).get_row_content(file_path)
        #excel_header_finder_agent_response_row_content = "ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds"
        print("#2. END .2#")
        
        # 3. Modificar Excel antes do cabeçalho
        print("#3. START .3#")
        ExcelPreHeaderModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category(
            category=excel_categorizer_agent_response,
            input_excel_file_path=file_path,
            header_row_number=ExcelService.get_excel_csv_row_number(file_path, excel_header_finder_agent_response_row_content),
            output_excel_file_path=output_file_path,
        )
        print("#3. END .3#")
        
        # 4. Modificar Excel a partir do cabeçalho
        print("#4. START .4#")
        ExcelContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category(
            category=excel_categorizer_agent_response,
            input_excel_file_path=output_file_path,
            output_excel_file_path=output_file_path,
            excel_header=excel_header_finder_agent_response_row_content,
            max_excel_lines_per_ai_request=configs.MAX_EXCEL_LINES_PER_AI_REQUEST
        )
        print("#4. END .4#")
    logging.info(AiAnalytics.__str__())

if __name__ == "__main__":
    main()
