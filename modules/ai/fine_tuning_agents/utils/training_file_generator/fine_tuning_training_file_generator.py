import json
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_categorizer_agent_prompts
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_header_finder_agent_prompts
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_categorizer_and_header_finder_agent_prompts
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_pre_header_modifier_agent_prompts
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_content_modifier_with_code_agent_prompts
from modules.ai.fine_tuning_agents.excel_generic_agent.prompts import excel_content_modifier_with_function_calling_agent_prompts
import logging


class FinetuningTrainingFileGenerator:
    """
    Class to generate a JSONL file for fine-tuning an AI model.
    """

    # Dados a serem convertidos para JSONL
    all_poc3_prompt_data = [
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_INVALIDO},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_INVALIDO_1},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_INVALIDO_2},
        {"messages": excel_categorizer_agent_prompts.CATEGORIZER_PROMPTS_CATEGORY_INVALIDO_3},
        {"messages": excel_header_finder_agent_prompts.HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_header_finder_agent_prompts.HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_HEADER},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_HEADER},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_1},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_2},
        {"messages": excel_categorizer_and_header_finder_agent_prompts.CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_3},
        {"messages": excel_pre_header_modifier_agent_prompts.PRE_HEADER_MODIFIER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_pre_header_modifier_agent_prompts.PRE_HEADER_MODIFIER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_content_modifier_with_code_agent_prompts.CONTENT_MODIFIER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_content_modifier_with_code_agent_prompts.CONTENT_MODIFIER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
        {"messages": excel_content_modifier_with_function_calling_agent_prompts.CONTENT_MODIFIER_PROMPTS_CATEGORY_EXECUCAO},
        {"messages": excel_content_modifier_with_function_calling_agent_prompts.CONTENT_MODIFIER_PROMPTS_CATEGORY_TESTE_EXECUCAO},
    ]

    training_file = "./modules/ai/fine_tuning_agents/utils/training_file_generator/generated_training_files/excel_fine_tuning_data.jsonl"

    @staticmethod
    def generate_training_file(
        data: dict = all_poc3_prompt_data,
        force_rewrite: bool = False,
    ) -> None:
        """
        Generate a JSONL file for fine-tuning an AI model.

        Args:
            data (dict): The data to be used.
            force_rewrite (bool): If True, the output file will be overwritten.
        """
        if not force_rewrite:
            try:
                with open(FinetuningTrainingFileGenerator.training_file, "r", encoding="utf-8") as file:
                    logging.info(f"Ficheiro JSONL já existe em: {FinetuningTrainingFileGenerator.training_file}")
                    return
            except FileNotFoundError:
                pass

        with open(FinetuningTrainingFileGenerator.training_file, "w", encoding="utf-8") as file:
            for entry in data:
                json_line = json.dumps(entry, ensure_ascii=False)
                file.write(json_line + "\n")

        logging.info(f"Ficheiro JSONL gerado em: {FinetuningTrainingFileGenerator.training_file}")
