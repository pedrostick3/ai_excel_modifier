import os
import logging
import modules.ai.agents.excel_content_modifier_agent.excel_content_modifier_agent_prompts as prompts
from modules.ai.services.ai_service import AiService
from modules.excel.services.excel_service import ExcelService
import modules.excel.constants.excel_constants as excel_constants
from modules.ai.agents.excel_categorizer_agent.enums.file_category import FileCategory


class ExcelContentModifierAgent:
    """
    Class to interact with the AI for modifying the content of an Excel file.
    """

    def __init__(self, ai_service: AiService, model: str):
        """
        Initialize the AI Agent.
        """
        self.ai_service = ai_service
        self.model = model

    def ask_ai(
        self,
        excel_data: str,
        system_prompt: str,
        example_prompts: list[dict] | None = None,
        ai_analytics_file_name: str = None,
        log_messages: bool = True,
    ) -> str:
        """
        Ask the AI for a response based on the given excel_data.

        Args:
            excel_data (str): The Excel data to be used.
            system_prompt (str): The system prompt to be used.
            example_prompts (list[dict]): The example prompts to be used.
            ai_analytics_file_name (str): The AI analytics file name to be used.
            log_messages (bool): Flag to indicate if the request messages should be logged.

        Returns:
            str: The AI's response.
        """
        try:
            user_prompt = f"""
```csv
{excel_data}
```
            """

            ai_response = self.ai_service.ask_ai(
                model=self.model,
                system_prompt=system_prompt,
                example_prompts=example_prompts,
                first_user_prompt=user_prompt,
                use_assistant_instead_of_system=False,  # True caso o modelo seja "o1-preview" ou "o1-mini"
                response_format=None,
                ai_analytics_file_name=ai_analytics_file_name,
                ai_analytics_agent_name="ExcelContentModifierAgent",
                log_request_messages=log_messages,
                log_response_message=log_messages,
            )

            return ai_response
        except Exception as e:
            logging.error(f"Erro ao comunicar com o AI ExcelPreHeaderModifierAgent: {e}")
            raise
    
    def do_your_work_by_category(
        self,
        category: FileCategory,
        input_excel_file_path: str,
        output_excel_file_path: str,
        excel_header: str,
        max_excel_lines_per_ai_request: int = 20
    ) -> None:
        """
        Processes an Excel file by splitting it into parts if it exceeds a specified number of lines,
        sends each part to an AI service for modification, and saves the modified content back to the file.

        Args:
            category (FileCategory): The category of the file.
            excel_input_file_path (str): The path to the Excel file to be processed.
            excel_output_file_path (str): The path to the Excel file to be saved.
            excel_header (str): The header of the Excel file to be included in each part sent to the AI.
            max_excel_lines_per_ai_request (int, optional): The maximum number of lines to include in each part sent to the AI. Defaults to 20.

        Returns:
            None
        """
        if category == FileCategory.EXECUCAO:
            system_prompt = prompts.SYSTEM_PROMPT_CATEGORY_EXECUTION
            example_prompts = prompts.EXAMPLE_PROMPTS_CATEGORY_EXECUTION
        elif category == FileCategory.TESTE_EXECUCAO:
            system_prompt = prompts.SYSTEM_PROMPT_CATEGORY_TEST_EXECUTION
            example_prompts = prompts.EXAMPLE_PROMPTS_CATEGORY_TEST_EXECUTION
        else:
            system_prompt = prompts.SYSTEM_PROMPT_TEST_ALL
            example_prompts = prompts.EXAMPLE_PROMPTS_TEST_ALL

        try:
            excel_data = ExcelService.get_excel_csv_to_csv_str(input_excel_file_path)
        except Exception as e:
            logging.error(f"AI ExcelContentModifierAgent: Error reading Excel file: {e}")
            raise

        file_name = os.path.basename(input_excel_file_path)
        excel_lines = excel_data.split(excel_constants.EXCEL_LINE_BREAK)
        excel_lines_count = len(excel_lines) - 1
        logging.info(f"AI ExcelContentModifierAgent - {category} - The file '{input_excel_file_path}' has {excel_lines_count} lines.")

        excel_content_modifier_agent_response = []

        if excel_lines_count > max_excel_lines_per_ai_request:
            parts = (excel_lines_count + max_excel_lines_per_ai_request - 1) // max_excel_lines_per_ai_request  # Ceiling division
            logging.info(f"AI ExcelContentModifierAgent: The file '{input_excel_file_path}' will be sent in {parts} parts to the AI.")

            # TODO: Não enviar o pre-header na primeira parte (refazer system e example prompts)

            for i in range(parts):
                start = i * max_excel_lines_per_ai_request
                end = min((i + 1) * max_excel_lines_per_ai_request, excel_lines_count)
                excel_to_send = excel_constants.EXCEL_LINE_BREAK.join(excel_lines[start:end])
                if i > 0:
                    excel_to_send = f"{excel_header.strip()}{excel_constants.EXCEL_LINE_BREAK}" + excel_to_send
                
                logging.info(f"# ExcelContentModifierAgent # {i} ####################### excel_header = {excel_header.strip()}")
                logging.info(f"# ExcelContentModifierAgent # {i} ####################### {end - start} lines [{start}:{end}]. excel_to_send = {excel_to_send}")

                try:
                    agent_response = self.ask_ai(excel_to_send, system_prompt, example_prompts, file_name).strip() + excel_constants.EXCEL_LINE_BREAK
                except Exception as e:
                    logging.error(f"AI ExcelContentModifierAgent: Error communicating with AI: {e}")
                    raise

                if i > 0:
                    agent_response = self.remove_header(agent_response, excel_header.strip())
                
                logging.info(f"# ExcelContentModifierAgent # {i} ####################### agent_response = {agent_response}")
                excel_content_modifier_agent_response.append(agent_response)
        else:
            try:
                excel_content_modifier_agent_response.append(self.ask_ai(excel_data, system_prompt, example_prompts, file_name))
            except Exception as e:
                logging.error(f"AI ExcelContentModifierAgent: Error communicating with AI: {e}")
                raise

        try:
            ExcelService.save_excel_csv_data_into_file(output_excel_file_path, excel_constants.EXCEL_LINE_BREAK.join(excel_content_modifier_agent_response))
        except Exception as e:
            logging.error(f"AI ExcelContentModifierAgent: Error saving modified content to Excel file: {e}")
            raise

    def remove_header(self, excel_data: str, excel_header: str) -> str:
        """
        Remove the header from the Excel data.

        Args:
            excel_data (str): The Excel data to be used.
            excel_header (str): The header to be removed.

        Returns:
            str: The Excel data without the header.
        """
        lines = excel_data.splitlines()
        excel_header_titles = excel_header.split(",")
        title = excel_header_titles[0] if excel_header_titles else excel_header

        # Identifica o índice da linha que contém o cabeçalho
        header_index = next((i for i, line in enumerate(lines) if title in line), -1)

        # Retorna apenas as linhas após o cabeçalho
        return excel_constants.EXCEL_LINE_BREAK.join(lines[header_index + 1:]) if header_index != -1 else excel_data