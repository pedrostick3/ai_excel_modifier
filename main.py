import constants.configs as configs
from modules.enums.ai_implementation import AiImplementation
from modules.ai_manual_implementation.enums.ai_type import AiType
from modules.ai_manual_implementation.ai_manual_implementation import AiManualImplementation
from modules.ai_langchain_implementation.ai_langchain_implementation import AiLangChainImplementation

AI_IMPLEMENTATION = AiImplementation.LANGCHAIN

def main():
    print("Main START")

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

    if AI_IMPLEMENTATION == AiImplementation.MANUAL:
        print("Main AI_IMPLEMENTATION == AiImplementation.MANUAL")
        AiManualImplementation.run(
            input_files=input_files,
            ai_type=AiType.FINE_TUNING,
            custom_ai_service_base_url=configs.GITHUB_BASE_URL,
            custom_ai_service_key=configs.GITHUB_KEY,
            custom_ai_service_model=configs.GITHUB_MODEL,
            finetuning_base_model=configs.OPENAI_FINE_TUNING_BASE_MODEL,
            finetuning_model=configs.OPENAI_FINE_TUNING_MODEL_29_01_2025_WITH_VALIDATION_FILE
        )
    elif AI_IMPLEMENTATION == AiImplementation.LANGCHAIN:
        print("Main AI_IMPLEMENTATION == AiImplementation.LANGCHAIN")
        AiLangChainImplementation.run(
            input_files=input_files,
            finetuning_model=configs.OPENAI_FINE_TUNING_MODEL_29_01_2025_WITH_VALIDATION_FILE,
        )
        
    print("Main END")


if __name__ == "__main__":
    main()
