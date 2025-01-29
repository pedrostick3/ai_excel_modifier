import json
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_categorizer_agent_prompts
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_header_finder_agent_prompts
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_categorizer_and_header_finder_agent_prompts
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_pre_header_modifier_agent_prompts
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_content_modifier_with_code_agent_prompts
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_content_modifier_with_function_calling_agent_prompts
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts_validators import excel_categorizer_and_header_finder_agent_prompts_validators
import logging


class FinetuningFileGenerator:
    """
    Class to generate a JSONL file for fine-tuning an AI model.
    """

    ALL_POC3_PROMPT_DATA = [
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_EXECUCAO_CASE_INSENSITIVE},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME_CASE_INSENSITIVE},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_TESTE_EXECUCAO_CASE_INSENSITIVE},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME_CASE_INSENSITIVE},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_INVALIDO},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_INVALIDO_1},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_INVALIDO_2},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_INVALIDO_3},
        {"messages": excel_header_finder_agent_prompts.HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_header_finder_agent_prompts.HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_CASE_INSENSITIVE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME_WITH_EMPTY_COLS},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME_CASE_INSENSITIVE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_HEADER},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_CASE_INSENSITIVE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME_WITH_EMPTY_COLS},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME_CASE_INSENSITIVE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_HEADER},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_1_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_2_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_3_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_4_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_5_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_6_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_7_TE},
        {"messages": excel_pre_header_modifier_agent_prompts.PRE_HEADER_MODIFIER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_pre_header_modifier_agent_prompts.PRE_HEADER_MODIFIER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_content_modifier_with_code_agent_prompts.CONTENT_MODIFIER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_content_modifier_with_code_agent_prompts.CONTENT_MODIFIER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_content_modifier_with_function_calling_agent_prompts.CONTENT_MODIFIER_PROMPTS_CATEGORY_EXECUCAO, "functions": excel_content_modifier_with_function_calling_agent_prompts.FUNCTIONS},
        {"messages": excel_content_modifier_with_function_calling_agent_prompts.CONTENT_MODIFIER_PROMPTS_CATEGORY_TESTE_EXECUCAO, "functions": excel_content_modifier_with_function_calling_agent_prompts.FUNCTIONS},
    ]
    
    CLEAN_POC3_PROMPT_DATA = [
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_CASE_INSENSITIVE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME_WITH_EMPTY_COLS},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME_CASE_INSENSITIVE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_HEADER},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_CASE_INSENSITIVE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME_WITH_EMPTY_COLS},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME_CASE_INSENSITIVE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_HEADER},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_1_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_2_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_3_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_4_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_5_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_6_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_7_TE},
        {"messages": excel_pre_header_modifier_agent_prompts.PRE_HEADER_MODIFIER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_pre_header_modifier_agent_prompts.PRE_HEADER_MODIFIER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_content_modifier_with_function_calling_agent_prompts.CONTENT_MODIFIER_PROMPTS_CATEGORY_EXECUCAO, "functions": excel_content_modifier_with_function_calling_agent_prompts.FUNCTIONS},
        {"messages": excel_content_modifier_with_function_calling_agent_prompts.CONTENT_MODIFIER_PROMPTS_CATEGORY_TESTE_EXECUCAO, "functions": excel_content_modifier_with_function_calling_agent_prompts.FUNCTIONS},
    ]
    
    CLEAN_POC3_PROMPT_DATA_VALIDATION = [
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_1_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_2_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_3_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_4_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_5_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_6_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_7_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_8_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_9_E},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_10_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_11_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_12_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_13_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_14_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_15_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_16_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_17_TE},
        {"messages": excel_categorizer_and_header_finder_agent_prompts_validators.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_18_TE},
    ]

    TRAINING_FILE_PATH = "./modules/ai/fine_tuning_agents/utils/fine_tuning_file_generator/generated_files/excel_fine_tuning_data.jsonl"
    VALIDATION_FILE_PATH = "./modules/ai/fine_tuning_agents/utils/fine_tuning_file_generator/generated_files/excel_fine_tuning_data_validation.jsonl"

    @staticmethod
    def generate_training_file(
        data: dict = CLEAN_POC3_PROMPT_DATA,
        force_rewrite: bool = False,
    ) -> None:
        """
        Generate a JSONL file for fine-tuning an AI model.

        Args:
            data (dict): The data to be used.
            force_rewrite (bool): If True, the output file will be overwritten.
        """
        FinetuningFileGenerator._generate_file(
            data=data,
            file_path=FinetuningFileGenerator.TRAINING_FILE_PATH,
            force_rewrite=force_rewrite,
        )
    
    @staticmethod
    def generate_validation_file(
        data: dict = CLEAN_POC3_PROMPT_DATA_VALIDATION,
        force_rewrite: bool = False,
    ) -> None:
        """
        Generate a JSONL file for validation when fine-tuning an AI model.

        Args:
            data (dict): The data to be used.
            force_rewrite (bool): If True, the output file will be overwritten
        """
        FinetuningFileGenerator._generate_file(
            data=data,
            file_path=FinetuningFileGenerator.VALIDATION_FILE_PATH,
            force_rewrite=force_rewrite,
        )
    
    @staticmethod
    def _generate_file(
        data: dict,
        file_path: str,
        force_rewrite: bool,
    ) -> None:
        """
        Generate a JSONL file for fine-tuning an AI model.

        Args:
            data (dict): The data to be used.
            file_path (str): The path to the output file.
            force_rewrite (bool): If True, the output file will be overwritten.
        """
        if not force_rewrite:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    logging.info(f"Ficheiro JSONL já existe em: {file_path}")
                    return
            except FileNotFoundError:
                pass

        with open(file_path, "w", encoding="utf-8") as file:
            for entry in data:
                json_line = json.dumps(entry, ensure_ascii=False)
                file.write(json_line + "\n")

        logging.info(f"Ficheiro JSONL gerado em: {file_path}")
