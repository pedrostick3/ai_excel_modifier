import logging
import os
import ast
import json
import shutil
from modules.ai_langchain_implementation.services.langchain_ai_service import LangChainAiService
from modules.excel.services.excel_service import ExcelService
from modules.ai_manual_implementation.enums.file_category import FileCategory
import modules.excel.constants.excel_constants as excel_constants
import constants.configs as configs
from modules.ai_manual_implementation.fine_tuning_agents.excel_generic_agent.prompts import excel_categorizer_and_header_finder_agent_prompts
from modules.ai_manual_implementation.fine_tuning_agents.excel_generic_agent.prompts import excel_pre_header_modifier_agent_prompts
from modules.ai_manual_implementation.fine_tuning_agents.excel_generic_agent.prompts import excel_content_modifier_with_function_calling_agent_prompts
from modules.ai_langchain_implementation.function_calling.poc3_functions_to_call import PoC3FunctionsToCall



class PoC3LangChainAgent:
    """
    This class is a Langchain implementation of the AI process for PoC3.
    """
    fine_tuning_model = None

    def __init__(self, ai_service: LangChainAiService):
        """
        Initialize the AI Agent.
        """
        self.ai_service = ai_service
    
    def ask_ai(
        self,
        prompt: list,
        input_vars: dict = None,
        functions_signature_list_for_tools: list = None,
        tool_choice: str = None,
        ai_analytics_file_name: str = None,
        ai_analytics_agent_name: str = None,
        log_messages: bool = True,
    ) -> str:
        """
        Ask the AI for a response based on the given excel_data.

        Args:
            prompt (list): The prompt to be used.
            input_vars (dict): The input variables to be used.
            functions_signature_list_for_tools (list): The functions signature list for tools.
            tool_choice (str): Force the function calling by setting the tool choice to "required". [Source](https://community.openai.com/t/new-api-feature-forcing-function-calling-via-tool-choice-required/731488) 
            ai_analytics_file_name (str): The AI analytics file name to be used.
            ai_analytics_agent_name (str): The AI analytics agent name to be used.
            log_messages (bool): Flag to indicate if the request messages should be logged.

        Returns:
            str: The AI's response.
        """
        try:
            ai_response = self.ai_service.ask_ai(
                prompt=prompt,
                input_vars=input_vars,
                functions_signature_list_for_tools=functions_signature_list_for_tools,
                tool_choice=tool_choice,
                ai_analytics_file_name=ai_analytics_file_name,
                ai_analytics_agent_name=ai_analytics_agent_name,
                log_response_message=log_messages,
            )

            return ai_response
        except Exception as e:
            logging.error(f"Erro ao comunicar com o AI PoC3Agent: {e}")
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
            prompt=[
                (
                    "system",
                    excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
                ),
                (
                    "human",
                    f"""Categorize and find the header of the following file:
Filename = '{file_name}'
```csv
{excel_data_first_5_rows}
```""",
                ),
            ],
            ai_analytics_file_name=ai_analytics_file_name,
            ai_analytics_agent_name="PoC3LangChainAgent (ExcelCategorizerAndHeaderFinderAgent)",
        )

        self._handle_category_from_ai_category_agent_response_string(
            ai_agent_response=excel_categorizer_and_header_finder_agent_response,
            file_name=file_name,
            excel_file_path=excel_file_path,
            invalid_output_path=invalid_output_path,
            function_id_to_log="AI PoC3LangChainAgent - get_file_category_and_header()",
        )

        try:
            excel_categorizer_and_header_finder_agent_response_dict = json.loads(excel_categorizer_and_header_finder_agent_response)
        except json.JSONDecodeError or ValueError as e:
            logging.error(f"Warning - AI PoC3LangChainAgent - get_file_category_and_header(): Erro ao converter a resposta do AI para JSON: {e}\nexcel_categorizer_and_header_finder_agent_response = {excel_categorizer_and_header_finder_agent_response}")
            raise
            
        return excel_categorizer_and_header_finder_agent_response_dict if excel_categorizer_and_header_finder_agent_response_dict else {}
    
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
        logging.info(f"AI PoC3LangChainAgent - {category} - excel_data_first_rows_until_header = {excel_data_first_rows_until_header}")
        excel_pre_header_modifier_agent_response = self.ask_ai(
            prompt=[
                (
                    "system",
                    excel_pre_header_modifier_agent_prompts.PRE_HEADER_MODIFIER_SYSTEM_PROMPT,
                ),
                (
                    "human",
                    f"Modify the pre-header of the following file that belongs to the '{category.value}' category:\n{excel_data_first_rows_until_header}",
                ),
            ],
            ai_analytics_file_name=ai_analytics_file_name,
            ai_analytics_agent_name="PoC3LangChainAgent (ExcelPreHeaderModifierAgent)",
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
                logging.error(f"Warning - AI PoC3LangChainAgent - Não foi possível guardar o ficheiro '{output_excel_file_path}'.")

            return success
        except Exception as e:
            logging.error(f"Erro ao processar o retorno do AI PoC3LangChainAgent: {e}")
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
            logging.error(f"AI PoC3LangChainAgent: Error reading Excel file: {e}")
            raise

        excel_lines = excel_data.split(excel_constants.EXCEL_LINE_BREAK)
        excel_lines_count = len(excel_lines) - 1
        logging.info(f"AI PoC3LangChainAgent - {category} - The file '{input_excel_file_path}' has {excel_lines_count} lines.")

        try:
            ai_response = self.ask_ai(
                prompt=[
                    (
                        "system",
                        excel_content_modifier_with_function_calling_agent_prompts.CONTENT_MODIFIER_SYSTEM_PROMPT,
                    ),
                    (
                        "human",
                        f"""Return the function to call that modifies the content of the following file that belongs to the '{category.value}' category:
input_excel_file_path = '{input_excel_file_path}'
output_excel_file_path = '{output_excel_file_path}'
excel_header_row_index = {excel_header_row_index}""",
                    ),
                ],
                tool_choice="required",
                functions_signature_list_for_tools=[
                    PoC3FunctionsToCall.modify_excel_content_for_execution_category,
                    PoC3FunctionsToCall.modify_excel_content_for_test_execution_category,
                ],
                ai_analytics_file_name=ai_analytics_file_name,
                ai_analytics_agent_name="PoC3LangChainAgent (ExcelContentModifierWithFunctionCallingAgent)",
            )
        except Exception as e:
            logging.error(f"AI PoC3LangChainAgent: Error communicating with AI: {e}")
            raise

        try:
            response_json = json.load(ai_response) if self.ai_service._is_valid_json(ai_response) else ast.literal_eval(ai_response)
        except json.JSONDecodeError:
            logging.error(f"AI PoC3LangChainAgent: Error parsing AI response JSON: {ai_response}")
            raise
        
        if "name" not in response_json:
            logging.error(f"AI PoC3LangChainAgent: The AI response JSON does not contain the 'name' key. ai_response = {ai_response}")
            raise

        try:
            if response_json["name"] == "modify_excel_content_for_execution_category":
                tool_function_response = PoC3FunctionsToCall.modify_excel_content_for_execution_category.invoke(response_json["args"])
            elif response_json["name"] == "modify_excel_content_for_test_execution_category":
                tool_function_response = PoC3FunctionsToCall.modify_excel_content_for_test_execution_category.invoke(response_json["args"])
            logging.info(f"LangChainAiService.test_tool_calling() - Tool function response: {tool_function_response}")
            return tool_function_response
        except json.JSONDecodeError:
            logging.error(f"AI PoC3LangChainAgent: Error executing function. response_json: {response_json}")
            raise