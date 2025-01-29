from modules.ai.enums.file_category import FileCategory
from modules.ai.function_calls_agent.enums.functions_to_call import FunctionsToCall

CONTENT_MODIFIER_SYSTEM_PROMPT = f"""You are an assistant responsible for choosing the right function to call (tools - function calling).
When someone asks to return the function to call that modifies the content of a file, if the category is:
- '{FileCategory.EXECUCAO.value}', return the 'modify_excel_content_for_execution_category' function.
- '{FileCategory.TESTE_EXECUCAO.value}', return the 'modify_excel_content_for_test_execution_category' function."""

# Functions must be separated from messegaes in the training file. [Official Function Calling Documentation](https://platform.openai.com/docs/guides/fine-tuning#fine-tuning-examples)
FUNCTIONS = [
    FunctionsToCall.MODIFY_EXCEL_CONTENT_FOR_EXECUTION_CATEGORY.value["tools"][0]["function"],
    FunctionsToCall.MODIFY_EXCEL_CONTENT_FOR_TEST_EXECUTION_CATEGORY.value["tools"][0]["function"],
]

CONTENT_MODIFIER_PROMPTS_CATEGORY_EXECUCAO = [
    {
        "role": "system",
        "content": CONTENT_MODIFIER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": f"""Return the function to call that modifies the content of the following file that belongs to the '{FileCategory.EXECUCAO.value}' category:
input_excel_file_path = './assets/docs_input/Execution_data Template.xlsx'
output_excel_file_path = './assets/docs_output/Execução - 16_12_2024 - Execution_data Template.xlsx'
excel_header_row_index = 1""",
    },
    {
        "role": "assistant",
        "function_call": {
            "name": "modify_excel_content_for_execution_category",
            "arguments": "{\"input_excel_file_path\":\"./assets/docs_input/Execution_data Template.xlsx\",\"output_excel_file_path\":\"./assets/docs_output/Execução - 16_12_2024 - Execution_data Template.xlsx\",\"excel_header_row_index\":1}",
        },
    },
]

CONTENT_MODIFIER_PROMPTS_CATEGORY_TESTE_EXECUCAO = [
    {
        "role": "system",
        "content": CONTENT_MODIFIER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": f"""Return the function to call that modifies the content of the following file that belongs to the '{FileCategory.TESTE_EXECUCAO.value}' category:
input_excel_file_path = './assets/docs_input/Test_Execution_data Template.xlsx'
output_excel_file_path = './assets/docs_output/Teste Execução - 13_12_2024 - Test_Execution_data Template.xlsx'
excel_header_row_index = 3""",
    },
    {
        "role": "assistant",
        "function_call": {
            "name": "modify_excel_content_for_test_execution_category",
            "arguments": "{\"input_excel_file_path\":\"./assets/docs_input/Test_Execution_data Template.xlsx\",\"output_excel_file_path\":\"./assets/docs_output/Teste Execução - 13_12_2024 - Test_Execution_data Template.xlsx\",\"excel_header_row_index\":3}",
        },
    },
]
