import json
from modules.ai.fine_tuning_agents.excel_generic_agent import excel_generic_fine_tuning_agent_prompts


class FinetuningTrainingFileGenerator:
    """
    Class to generate a JSONL file for fine-tuning an AI model.
    """

    # Dados a serem convertidos para JSONL
    all_poc3_prompt_data = [
        {"messages": excel_generic_fine_tuning_agent_prompts.CATEGORIZER_PROMPTS},
        {"messages": excel_generic_fine_tuning_agent_prompts.HEADER_FINDER_PROMPTS},
        {"messages": excel_generic_fine_tuning_agent_prompts.PRE_HEADER_MODIFIER_CATEGORY_EXECUTION_PROMPTS},
        {"messages": excel_generic_fine_tuning_agent_prompts.PRE_HEADER_MODIFIER_CATEGORY_TEST_EXECUTION_PROMPTS},
        {"messages": excel_generic_fine_tuning_agent_prompts.CONTENT_MODIFIER_CATEGORY_EXECUTION_PROMPTS},
        {"messages": excel_generic_fine_tuning_agent_prompts.CONTENT_MODIFIER_CATEGORY_TEST_EXECUTION_PROMPTS},
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
                    print(f"Ficheiro JSONL já existe em: {FinetuningTrainingFileGenerator.training_file}")
                    return
            except FileNotFoundError:
                pass

        with open(FinetuningTrainingFileGenerator.training_file, "w", encoding="utf-8") as file:
            for entry in data:
                json_line = json.dumps(entry, ensure_ascii=False)
                file.write(json_line + "\n")

        print(f"Ficheiro JSONL gerado em: {FinetuningTrainingFileGenerator.training_file}")
