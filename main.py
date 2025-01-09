import os
import logging
from datetime import datetime
import constants.configs as configs
from modules.excel.services.excel_service import ExcelService
from modules.ai.services.custom_ai_service import CustomAiService
from modules.ai.services.azure_ai_service import AzureAiService
from modules.ai.agents.excel_categorizer_agent.excel_categorizer_agent import ExcelCategorizerAgent
from modules.ai.agents.excel_header_finder_agent.excel_header_finder_agent import ExcelHeaderFinderAgent
from modules.ai.agents.excel_pre_header_modifier_agent.excel_pre_header_modifier_agent import ExcelPreHeaderModifierAgent
from modules.ai.agents.excel_content_modifier_agent.excel_content_modifier_agent import ExcelContentModifierAgent
from modules.ai.agents.excel_generic_content_modifier_agent.excel_generic_content_modifier_agent import ExcelGenericContentModifierAgent
from modules.ai.function_calls_agent.excel_sum_columns_agent.excel_sum_columns_agent import ExcelSumColumnsAgent
from modules.ai.file_search_agent.file_search_agent.file_search_agent import FileSearchAgent
from modules.ai.code_interpreter_agent.code_interpreter_agent.code_interpreter_agent import CodeInterpreterAgent
from modules.ai.fine_tuning_agents.excel_generic_agent.excel_generic_fine_tuning_agent import ExcelGenericFinetuningAgent
from modules.ai.enums.file_category import FileCategory
from modules.ai.enums.ai_type import AiType
from modules.analytics.services.ai_analytics import AiAnalytics


CUSTOM_AI_SERVICE_BASE_URL = configs.GITHUB_BASE_URL
CUSTOM_AI_SERVICE_KEY = configs.GITHUB_KEY
CUSTOM_AI_SERVICE_MODEL = configs.GITHUB_MODEL
AZURE_FINETUNING_MODEL = configs.AZURE_FINETUNING_MODEL
AI_TYPE = AiType.ASSISTANT_CODE_INTERPRETER

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

    if AI_TYPE == AiType.COMPLETION or AI_TYPE == AiType.COMPLETION_FUNCTION_CALLING:
        # Configurar Custom AI Service
        ai_service = CustomAiService(CUSTOM_AI_SERVICE_KEY, CUSTOM_AI_SERVICE_BASE_URL)

    if AI_TYPE == AiType.FINE_TUNING:
        # Configurar Azure AI Service para Fine Tuning
        fine_tuning_agent = ExcelGenericFinetuningAgent(AzureAiService(), AZURE_FINETUNING_MODEL)
        fine_tuning_agent.create_fine_tuning_model()

    if AI_TYPE == AiType.ASSISTANT_FILE_SEARCH or AI_TYPE == AiType.ASSISTANT_CODE_INTERPRETER:
        # Configurar Azure AI Service para Assistants
        ai_service = AzureAiService()
    
    os.makedirs(configs.OUTPUT_FOLDER, exist_ok=True) # Criar pasta de output se não existir

    # Processar cada ficheiro
    for file_name in input_files:
        file_path = os.path.join(configs.INPUT_FOLDER, file_name)
        logging.info(f"#### Start processing file: {file_path} ####")

        if AI_TYPE == AiType.ASSISTANT_CODE_INTERPRETER:
            # TODO: Not tested yet
            ##### Teste Code Interpreter - START #####
            # Somar colunas indicadas pelo user
            logging.info("#ASSISTANT_CODE_INTERPRETER - START - CodeInterpreterAgent")
            code_interpreter_agent_response = CodeInterpreterAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_with(
                column_to_sum="RunTimeSeconds",
                input_excel_file_path=file_path,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            logging.info(f"A soma da coluna 'RunTimeSeconds' é: {code_interpreter_agent_response}")
            logging.info("#ASSISTANT_CODE_INTERPRETER - END - CodeInterpreterAgent")
            ##### Teste Code Interpreter - END #####
            continue

        if AI_TYPE == AiType.ASSISTANT_FILE_SEARCH:
            # TODO: Not tested yet
            ##### Teste File Search - START #####
            # Somar colunas indicadas pelo user
            logging.info("#ASSISTANT_FILE_SEARCH - START - FileSearchAgent")
            file_search_agent_response = FileSearchAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_with(
                column_to_sum="RunTimeSeconds",
                input_excel_file_path=file_path,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            logging.info(f"A soma da coluna 'RunTimeSeconds' é: {file_search_agent_response}")
            logging.info("#ASSISTANT_FILE_SEARCH - END - FileSearchAgent")
            ##### Teste File Search - END #####
            continue

        if AI_TYPE == AiType.COMPLETION_FUNCTION_CALLING:
            logging.info("#COMPLETION_FUNCTION_CALLING - START - ExcelHeaderFinderAgent (getting excel_header_row_index)")
            excel_header_finder_agent_response_row_content = ExcelHeaderFinderAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).get_row_content(
                excel_file_path=file_path,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            excel_header_row_index = ExcelService.get_excel_csv_row_number(file_path, excel_header_finder_agent_response_row_content) - 1
            logging.info("#COMPLETION_FUNCTION_CALLING - END - ExcelHeaderFinderAgent (getting excel_header_row_index)")

            ##### Teste Function Calls - START #####
            # Somar colunas indicadas pelo user
            logging.info("#COMPLETION_FUNCTION_CALLING - START - ExcelSumColumnsAgent")
            function_call_agent_response = ExcelSumColumnsAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_with(
                column_to_sum="RunTimeSeconds",
                input_excel_file_path=file_path,
                excel_header_row_index=excel_header_row_index,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            logging.info(f"A soma da coluna 'RunTimeSeconds' é: {function_call_agent_response}")
            logging.info("#COMPLETION_FUNCTION_CALLING - END - ExcelSumColumnsAgent")
            ##### Teste Function Calls - END #####
            continue

        if AI_TYPE == AiType.FINE_TUNING:
            ##### Teste Fine Tuning - START #####
            # 1. Categorizar Excel
            logging.info("#1. START - ExcelGenericFinetuningAgent")
            file_category = fine_tuning_agent.get_file_category(
                excel_file_path=file_path,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            print(f"Fine Tuning file_category: {file_category}")
            if file_category == FileCategory.INVALIDO:
                logging.info(f"AI ExcelCategorizerAgent: The file '{file_path}' is '{file_category}'.")
                continue
            logging.info("#1. END - ExcelGenericFinetuningAgent")
            exit() # TODO: EXIT() HERE!

            new_file_name = f'{file_category.value} - {datetime.now().strftime("%d_%m_%Y")} - {file_name}'
            output_file_path = f"{configs.OUTPUT_FOLDER}/{new_file_name}"

            # 2. Perceber onde começa a tabela retornando a linha do cabeçalho
            logging.info("#2. START - ExcelGenericFinetuningAgent")
            excel_header = fine_tuning_agent.get_excel_header(
                excel_file_path=file_path,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            logging.info("#2. END - ExcelGenericFinetuningAgent")

            # 3. Modificar Excel antes do cabeçalho
            logging.info("#3. START - ExcelGenericFinetuningAgent")
            fine_tuning_agent.modify_pre_header(
                category=file_category,
                input_excel_file_path=file_path,
                header_row_number=ExcelService.get_excel_csv_row_number(file_path, excel_header),
                output_excel_file_path=output_file_path,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            logging.info("#3. END - ExcelGenericFinetuningAgent")

            header_row_number = ExcelService.get_excel_csv_row_number(output_file_path, excel_header)
            
            # 4. Modificar Excel a partir do cabeçalho
            logging.info("#4. START - ExcelGenericFinetuningAgent")
            
            # TODO: Parte 4 é a mais importante. Testar:
            # TODO (continuação): - 1º retorna código a correr de acordo com o tipo/categoria do file;
            # TODO (continuação): - 2º enviar o conteudo do ficheiro inteiro e transforma o conteudo para o que estamos à espera;
            # TODO (continuação): - 3º utilizando as FunctionCalls, retorna a função a correr de acordo com o tipo/categoria do file; (será a mais infalivel)
            # TODO: Testes Extras:
            # TODO (continuação): - Fazer apenas 1 pedido com todos os steps numa única prompt
            # TODO (continuação): - Fazer testes com vários tamanhos de ficheiros (e meio desorganizados)

            # TODO [PD]: Testes a realizar com a conta da Azure (com subscrição pay-as-you-go):
            # TODO [PD]: - Fine-Tuning (AI_TYPE == AiType.FINE_TUNING);
            # TODO [PD]: - File Search (AI_TYPE == AiType.ASSISTANT_FILE_SEARCH);
            # TODO [PD]: - Code Interpreter (AI_TYPE == AiType.ASSISTANT_CODE_INTERPRETER);

            fine_tuning_agent.modify_content(
                category=excel_categorizer_agent_response,
                input_excel_file_path=output_file_path,
                output_excel_file_path=output_file_path,
                excel_header_row_index=header_row_number - 1, # -1 para obter o index
                ai_analytics_file_name=os.path.basename(file_path),
            )
            logging.info("#4. END - ExcelGenericFinetuningAgent")
            ##### Teste Fine Tuning - END #####
            continue

        if AI_TYPE == AiType.COMPLETION:
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
            if AiType.COMPLETION.value["RETURN_CODE_TO_EDIT_INSTEAD_OF_RETURN_EDITED_CONTENT"] and AiType.COMPLETION.value["USE_GENERIC_CONTENT_MODIFIER_AGENT_WHEN_RETURNING_CODE"]:
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
                        user_prompt="Change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Make sure that every cell of 'TaskWorkload' column have 5 decimal places after the ','.",
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
                        user_prompt="Change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Make sure that every cell of 'TaskWorkload' column have 5 decimal places after the ','.",
                        input_excel_file_path=output_file_path,
                        output_excel_file_path=output_file_path,
                        ai_analytics_file_name=os.path.basename(file_path),
                    )
                else:
                    raise ValueError(f"AI ExcelGenericContentModifierAgent: Invalid category: {excel_categorizer_agent_response}")
                
                ExcelService.add_excel_csv_pre_header(excel_pre_header, output_file_path)
            elif AiType.COMPLETION.value["RETURN_CODE_TO_EDIT_INSTEAD_OF_RETURN_EDITED_CONTENT"]:
                excel_pre_header = ExcelService.get_excel_csv_pre_header(output_file_path, header_row_number)

                ExcelContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category_returning_code(
                    category=excel_categorizer_agent_response,
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
                    excel_header_row_index=header_row_number - 1, # -1 para obter o index
                    ai_analytics_file_name=os.path.basename(file_path),
                )

                # AI don't have a consistent behavior for this task. This task was seperated from the ExcelContentModifierAgent prompt and it's being handled as a specific case by the ExcelGenericContentModifierAgent.
                ExcelGenericContentModifierAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_by_category_returning_code(
                    user_prompt="Change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Make sure that every cell of 'TaskWorkload' column have 5 decimal places after the ','.",
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
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

            if excel_categorizer_agent_response == FileCategory.TESTE_EXECUCAO and not AiType.COMPLETION.value["RETURN_CODE_TO_EDIT_INSTEAD_OF_RETURN_EDITED_CONTENT"]:
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
