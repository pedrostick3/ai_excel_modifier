import os
import logging
from datetime import datetime
import constants.configs as configs
from modules.excel.services.excel_service import ExcelService
from modules.ai.services.custom_ai_service import CustomAiService
from modules.ai.services.azure_ai_service import AzureAiService
from modules.ai.services.openai_ai_service import OpenAiAiService
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
FINETUNING_BASE_MODEL = configs.OPENAI_FINE_TUNING_BASE_MODEL
FINETUNING_MODEL = configs.OPENAI_FINE_TUNING_MODEL_28_01_2025
AI_TYPE = AiType.FINE_TUNING

def main():
    # PoC3 Files to process
    input_files = [
        ###### Main Files:
        "Execution_data Template.xlsx",
        "ParameterizationFile_testes_13112024.xlsx",
        "Test_Execution_data Template.xlsx",
        ###### Test Files (Test_Execution category):
        #"Test_Execution_data Template_half.xlsx",
        #"Test_Execution_data Template_quarter.xlsx",
        #"Test_Execution_data Template_50rows.xlsx",
        #"TE_unnamed.xlsx",
        #"TE lower content.xlsx",
        #"test_execution_data template lower.xlsx",
        #"Test_Execution_data Template some_empty_cells.xlsx",
        #"Test_Execution_data Template empty columns and rows.xlsx",
        ###### Test Files (Execution category):
        #"E_unnamed.xlsx",
        #"E lower content.xlsx",
        #"execution_data template lower.xlsx",
        #"Execution_data Template some_empty_cells.xlsx",
        #"Execution_data Template empty columns and rows.xlsx",
        ###### Test Files (Invalid category):
        #"E_unnamed_inv.xlsx",
        #"file-3.xlsx",
        #"TE_unnamed_inv.xlsx",
        #"file-73.xlsx",
        #"id-24543.xlsx",
        #"Ai_Fine-tuning_Estimates_Investigation_Azure_vs_OpenAI.xlsx",
    ]

    # Configurar logs
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler("process.log", encoding='utf-8'), logging.StreamHandler()],
        )
    logging.info("A iniciar AI APP")

    if AI_TYPE == AiType.COMPLETION or AI_TYPE == AiType.COMPLETION_FUNCTION_CALLING:
        # Configurar AI Service
        ai_service = CustomAiService(CUSTOM_AI_SERVICE_KEY, CUSTOM_AI_SERVICE_BASE_URL)

    if AI_TYPE == AiType.FINE_TUNING:
        # Configurar Fine-Tuning AI Service
        fine_tuning_agent = ExcelGenericFinetuningAgent(
            ai_service=OpenAiAiService(),
            base_model=FINETUNING_BASE_MODEL,
            fine_tuning_model=FINETUNING_MODEL,
            #delete_fine_tuning_model=True,
            #delete_fine_tuning_model_safety_trigger=True,
            #create_fine_tuning_model=True,
            #force_rewrite_training_file=True,
        )

    if AI_TYPE == AiType.ASSISTANT_FILE_SEARCH or AI_TYPE == AiType.ASSISTANT_CODE_INTERPRETER:
        # Configurar Assistants AI Service
        ai_service = AzureAiService()
    
    os.makedirs(configs.OUTPUT_FOLDER, exist_ok=True) # Criar pasta de output se não existir

    # Processar cada ficheiro
    for file_name in input_files:
        file_path = os.path.join(configs.INPUT_FOLDER, file_name)
        logging.info(f"#### Start processing file: {file_path} ####")

        if AI_TYPE == AiType.ASSISTANT_CODE_INTERPRETER:
            # TODO: Not tested yet
            logging.info("#ASSISTANT_CODE_INTERPRETER - START - CodeInterpreterAgent")
            code_interpreter_agent_response = CodeInterpreterAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_with(
                column_to_sum="RunTimeSeconds",
                input_excel_file_path=file_path,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            logging.info(f"The 'RunTimeSeconds' column sum is: {code_interpreter_agent_response}")
            logging.info("#ASSISTANT_CODE_INTERPRETER - END - CodeInterpreterAgent")
            continue

        if AI_TYPE == AiType.ASSISTANT_FILE_SEARCH:
            # TODO: Not tested yet
            logging.info("#ASSISTANT_FILE_SEARCH - START - FileSearchAgent")
            file_search_agent_response = FileSearchAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_with(
                column_to_sum="RunTimeSeconds",
                input_excel_file_path=file_path,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            logging.info(f"The 'RunTimeSeconds' column sum is: {file_search_agent_response}")
            logging.info("#ASSISTANT_FILE_SEARCH - END - FileSearchAgent")
            continue

        if AI_TYPE == AiType.COMPLETION_FUNCTION_CALLING:
            excel_header_finder_agent_response_row_content = ExcelHeaderFinderAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).get_row_content(
                excel_file_path=file_path,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            excel_header_row_index = ExcelService.get_excel_csv_row_number(file_path, excel_header_finder_agent_response_row_content) - 1

            logging.info("#COMPLETION_FUNCTION_CALLING - START - ExcelSumColumnsAgent")
            function_call_agent_response = ExcelSumColumnsAgent(ai_service, CUSTOM_AI_SERVICE_MODEL).do_your_work_with(
                column_to_sum="RunTimeSeconds",
                input_excel_file_path=file_path,
                excel_header_row_index=excel_header_row_index,
                ai_analytics_file_name=os.path.basename(file_path),
            )
            logging.info(f"The 'RunTimeSeconds' column sum is: {function_call_agent_response}")
            logging.info("#COMPLETION_FUNCTION_CALLING - END - ExcelSumColumnsAgent")
            continue

        if AI_TYPE == AiType.FINE_TUNING:
            if AiType.FINE_TUNING.value["USE_CATEGORIZER_AND_HEADER_FINDER_IN_1_REQUEST"]:
                # 1. 2. Categorizar Excel & perceber onde começa a tabela retornando a linha do cabeçalho
                logging.info("#1. 2. START - ExcelGenericFinetuningAgent")
                file_category_and_header = fine_tuning_agent.get_file_category_and_header(
                    excel_file_path=file_path,
                    ai_analytics_file_name=os.path.basename(file_path),
                )

                # Get category from the agent response
                try:
                    category_by_ai = file_category_and_header['category']
                except KeyError as e:
                    logging.error(f"Warning - main() - AI_TYPE == AiType.FINE_TUNING: Erro ao obter \"file_category_and_header['category']\": {e}\nfile_category_and_header = {file_category_and_header}")
                    raise
                file_category = FileCategory.get_category_by_name(category_by_ai)
                logging.info(f"main() - AI_TYPE == AiType.FINE_TUNING: The file '{file_name}' is '{file_category}' category.")
                if file_category == FileCategory.INVALIDO:
                    continue

                # Get header from the agent response
                try:
                    excel_header = file_category_and_header['header']['row_content']
                except KeyError as e:
                    logging.error(f"Warning - main() - AI_TYPE == AiType.FINE_TUNING: Erro ao obter \"file_category_and_header['header']['row_content']\": {e}\nfile_category_and_header = {file_category_and_header}")
                    raise

                logging.info("#1. 2. END - ExcelGenericFinetuningAgent")
            else:
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

                # 2. Perceber onde começa a tabela retornando a linha do cabeçalho
                logging.info("#2. START - ExcelGenericFinetuningAgent")
                excel_header = fine_tuning_agent.get_excel_header(
                    excel_file_path=file_path,
                    ai_analytics_file_name=os.path.basename(file_path),
                )
                logging.info("#2. END - ExcelGenericFinetuningAgent")

            new_file_name = f'{file_category.value} - {datetime.now().strftime("%d_%m_%Y")} - {file_name}'
            output_file_path = f"{configs.OUTPUT_FOLDER}/{new_file_name}"

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

            # 4. Modificar Excel depois do cabeçalho
            if AiType.FINE_TUNING.value["USE_FUNCTION_CALLING_TO_MODIFY_CONTENT"]:
                logging.info("#4. START - ExcelGenericFinetuningAgent - modify_content_returning_function_calling()")
                
                fine_tuning_agent.modify_content_returning_function_calling(
                    category=file_category,
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
                    excel_header_row_index=header_row_number - 1, # -1 para obter o index
                    ai_analytics_file_name=os.path.basename(file_path),
                )
                
                logging.info("#4. END - ExcelGenericFinetuningAgent - modify_content_returning_function_calling()")
            else:
                logging.info("#4. START - ExcelGenericFinetuningAgent - modify_content_returning_code()")
                fine_tuning_agent.modify_content_returning_code(
                    category=file_category,
                    input_excel_file_path=output_file_path,
                    output_excel_file_path=output_file_path,
                    excel_header_row_index=header_row_number - 1, # -1 para obter o index
                    ai_analytics_file_name=os.path.basename(file_path),
                )
                logging.info("#4. END - ExcelGenericFinetuningAgent - modify_content_returning_code()")
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
