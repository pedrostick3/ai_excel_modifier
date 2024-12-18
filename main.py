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
from modules.ai.agents.excel_generic_content_modifier_agent.excel_generic_content_modifier_agent import ExcelGenericContentModifierAgent
from modules.ai.agents.excel_categorizer_agent.enums.file_category import FileCategory
from modules.analytics.services.ai_analytics import AiAnalytics


CUSTOM_AI_SERVICE_BASE_URL = configs.GITHUB_BASE_URL
CUSTOM_AI_SERVICE_KEY = configs.GITHUB_KEY
CUSTOM_AI_SERVICE_MODEL = configs.GITHUB_MODEL
MAKE_AI_RETURN_CODE = True
USE_GENERIC_CONTENT_MODIFIER_AGENT = False

def main():
    # Ficheiros para o PoC3
    input_files = [
        "Execution_data Template.xlsx",
        "ParameterizationFile_testes_13112024.xlsx",
        "Test_Execution_data Template.xlsx",
        #"Test_Execution_data Template_half.xlsx",
        #"Test_Execution_data Template_quarter.xlsx",
        #"Test_Execution_data Template_50rows.xlsx",
    ]

    # Configurar logs
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("process.log", encoding='utf-8'), logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)
    logger.info("A iniciar AI APP")

    # Configurar Custom AI Service
    ai_service = CustomAiService(CUSTOM_AI_SERVICE_KEY, CUSTOM_AI_SERVICE_BASE_URL)
    
    os.makedirs(configs.OUTPUT_FOLDER, exist_ok=True) # Criar pasta de output se não existir

    # Processar cada ficheiro
    for file_name in input_files:
        file_path = os.path.join(configs.INPUT_FOLDER, file_name)
        logging.info(f"#### Start processing file: {file_path} ####")

        # 1. Categorizar Excel
        logging.info("#1. START - ExcelCategorizerAgent")
        excel_categorizer_agent_response = ExcelCategorizerAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_with(
            excel_file_path=file_path,
            ai_analytics_file_name=os.path.basename(file_path),
        )
        if excel_categorizer_agent_response == FileCategory.INVALIDO:
            logging.info(f"AI ExcelCategorizerAgent: The file '{file_path}' is '{excel_categorizer_agent_response}'.")
            continue
        logging.info("#1. END - ExcelCategorizerAgent")

        new_file_name = f'{excel_categorizer_agent_response.value} - {datetime.now().strftime("%d_%m_%Y")} - {file_name}'
        output_file_path = f"{configs.OUTPUT_FOLDER}/{new_file_name}"
        
        # 2. Perceber onde começa a tabela retornando a linha do cabeçalho
        logging.info("#2. START - ExcelHeaderFinderAgent")
        excel_header_finder_agent_response_row_content = ExcelHeaderFinderAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).get_row_content(
            excel_file_path=file_path,
            ai_analytics_file_name=os.path.basename(file_path),
        )
        logging.info("#2. END - ExcelHeaderFinderAgent")
        
        # 3. Modificar Excel antes do cabeçalho
        logging.info("#3. START - ExcelPreHeaderModifierAgent")
        ExcelPreHeaderModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category(
            category=excel_categorizer_agent_response,
            input_excel_file_path=file_path,
            header_row_number=ExcelService.get_excel_csv_row_number(file_path, excel_header_finder_agent_response_row_content),
            output_excel_file_path=output_file_path,
            ai_analytics_file_name=os.path.basename(file_path),
        )
        logging.info("#3. END - ExcelPreHeaderModifierAgent")

        header_row_number = ExcelService.get_excel_csv_row_number(output_file_path, excel_header_finder_agent_response_row_content)
        
        # 4. Modificar Excel a partir do cabeçalho
        logging.info("#4. START - ExcelContentModifierAgent")
        if MAKE_AI_RETURN_CODE and USE_GENERIC_CONTENT_MODIFIER_AGENT:
            excel_pre_header = ExcelService.get_excel_csv_pre_header(output_file_path, header_row_number)

            if excel_categorizer_agent_response == FileCategory.EXECUCAO:
                ExcelGenericContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category_returning_code(
                    user_prompt="Move the 'IsSuccessful' column to column A, shifting the remaining columns to the right.",
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
                    excel_header_row_index=header_row_number - 1,
                    ai_analytics_file_name=os.path.basename(file_path),
                )
                ExcelGenericContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category_returning_code(
                    user_prompt="Remove the 'AverageRunTimeSeconds' column.",
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
                    ai_analytics_file_name=os.path.basename(file_path),
                )
                ExcelGenericContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category_returning_code(
                    user_prompt="Add a new column 'RunTimeMinutes' at the last position of the table and set each value to 'RunTimeSeconds/60'. Careful with the division and try to convert the values to numeric before dividing.",
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
                    ai_analytics_file_name=os.path.basename(file_path),
                )
                ExcelGenericContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category_returning_code(
                    user_prompt="Change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000).",
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
                    ai_analytics_file_name=os.path.basename(file_path),
                )
                ExcelGenericContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category_returning_code(
                    user_prompt="Change the format of the columns 'ExecutionStartDate', 'ExecutionEndDate', 'CaseStartDate', and 'CaseEndDate' 'dd-MM-yyyy HH:mm:ss.mmm'. Avoid potential parsing issues.",
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
                    ai_analytics_file_name=os.path.basename(file_path),
                )
            elif excel_categorizer_agent_response == FileCategory.TESTE_EXECUCAO:
                ExcelGenericContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category_returning_code(
                    user_prompt="Reorder the columns to: 'ExecutionId', 'ExecutionStartDate', 'ExecutionEndDate', 'TaskWorkload', 'CaseStartDate', 'CaseEndDate', 'IsSuccessful', 'RunTimeSeconds', 'AverageRunTimeSeconds'.",
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
                    excel_header_row_index=header_row_number - 1,
                    ai_analytics_file_name=os.path.basename(file_path),
                )
                ExcelGenericContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category_returning_code(
                    user_prompt="""Add the sum of 'RunTimeSeconds' and 'TaskWorkload' columns at the end of the table.
Important:
1. Use a separate DataFrame or copy to convert the values to numeric only for the purpose of summing.
2. Do not modify or overwrite the original values in the main DataFrame.""",
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
                    ai_analytics_file_name=os.path.basename(file_path),
                )
                ExcelGenericContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category_returning_code(
                    user_prompt="Change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Every cell of 'TaskWorkload' column must have 5 decimal places after the ','.",
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
                    ai_analytics_file_name=os.path.basename(file_path),
                )
            else:
                raise ValueError(f"AI ExcelGenericContentModifierAgent: Invalid category: {excel_categorizer_agent_response}")
            
            ExcelService.add_excel_csv_pre_header(excel_pre_header, output_file_path)
        elif MAKE_AI_RETURN_CODE:
            excel_pre_header = ExcelService.get_excel_csv_pre_header(output_file_path, header_row_number)

            ExcelContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category_returning_code(
                category=excel_categorizer_agent_response,
                input_excel_file_path=output_file_path,
                output_excel_file_path=output_file_path,
                excel_header_row_index=header_row_number - 1, # -1 para obter o index
                ai_analytics_file_name=os.path.basename(file_path),
            )

            ExcelService.add_excel_csv_pre_header(excel_pre_header, output_file_path)
        else:
            ExcelContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category(
                category=excel_categorizer_agent_response,
                input_excel_file_path=output_file_path,
                output_excel_file_path=output_file_path,
                excel_header=excel_header_finder_agent_response_row_content,
                max_excel_lines_per_ai_request=configs.MAX_EXCEL_LINES_PER_AI_REQUEST,
                ai_analytics_file_name=os.path.basename(file_path),
            )
        logging.info("#4. END - ExcelContentModifierAgent")

        if excel_categorizer_agent_response == FileCategory.TESTE_EXECUCAO and not MAKE_AI_RETURN_CODE:
            # 5. Somar colunas 'RunTimeSeconds' e 'TaskWorkload' programáticamente
            logging.info("#5. START - Sum columns 'RunTimeSeconds' and 'TaskWorkload' programmatically")
            ExcelService.sumColumnsAndAddTotalColumnAtBottom(
                excel_input_file_path=output_file_path,
                header_row_number=4,
                excel_output_file_path=output_file_path,
                columns=['RunTimeSeconds', 'TaskWorkload'],
            )
            logging.info("#5. END - Sum columns 'RunTimeSeconds' and 'TaskWorkload' programmatically")

    logging.info(AiAnalytics.__str__())
    AiAnalytics.export_str_ai_analytics_data_to_excel()

if __name__ == "__main__":
    main()
