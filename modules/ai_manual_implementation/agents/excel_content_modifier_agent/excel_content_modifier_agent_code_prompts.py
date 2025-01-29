SYSTEM_CODE_PROMPT_CATEGORY_EXECUTION = """You are an assistant for editing Excel files. Your tasks are:
1. Move the 'IsSuccessful' column to column A, shifting the remaining columns to the right.
2. Remove the 'AverageRunTimeSeconds' column.
3. Add a new column 'RunTimeMinutes' at the last position of the table and set each value to 'RunTimeSeconds/60'. Careful with the division and try to convert the values to numeric before dividing.
4. Change the format of the columns 'ExecutionStartDate', 'ExecutionEndDate', 'CaseStartDate', and 'CaseEndDate' to 'dd-MM-yyyy HH:mm:ss.mmm'. Mitigate possible warnings.
5. Return the python code to modify the complete file and save it.
6. Your response must not include code-blocks or MARKDOWN.
7. Initialize the given variables in the beginning of the code.
8. Use concat() function to join dataframes.
9. Don't use xlswriter to save the file."""
# AI don't have a consistent behavior for this task. This task was seperated from this ExcelContentModifierAgent prompt and it's being handled as a specific case by the ExcelGenericContentModifierAgent.
#5. In the end, change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Make sure that every cell of 'TaskWorkload' column have 5 decimal places after the ','.

EXAMPLE_CODE_PROMPTS_CATEGORY_EXECUTION = [
    {
        "role": "user",
        "content": """input_excel_file_path = './assets/docs_input/Execution_data Template.xlsx'
output_excel_file_path = './assets/docs_output/Execução - 16_12_2024 - Execution_data Template.xlsx'
excel_header_row_index = 1""",
    },
    {
        "role": "assistant",
        "content": open('./modules/ai_manual_implementation/agents/excel_content_modifier_agent/code_examples_for_code_prompts/code_example_category_execution_main.py', 'r', encoding='utf-8').read(),
    },
]

SYSTEM_CODE_PROMPT_CATEGORY_TEST_EXECUTION = """You are an assistant for editing Excel files. Your tasks are:
1. Reorder the columns to: 'ExecutionId', 'ExecutionStartDate', 'ExecutionEndDate', 'TaskWorkload', 'CaseStartDate', 'CaseEndDate', 'IsSuccessful', 'RunTimeSeconds', 'AverageRunTimeSeconds'.
2. Add the sum of 'RunTimeSeconds' and 'TaskWorkload' columns at the end of the table. Convert the values to numeric before calculating.
3. Return the python code to modify the complete file and save it.
4. Your response must not include code-blocks or MARKDOWN.
5. Initialize the given variables in the beginning of the code.
6. Use concat() function to join dataframes.
7. Don't use xlswriter to save the file.
8. Don't add unnecessary columns."""
# AI don't have a consistent behavior for this task. This task was seperated from this ExcelContentModifierAgent prompt and it's being handled as a specific case by the ExcelGenericContentModifierAgent.
#3. In the end, change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Make sure that every cell of 'TaskWorkload' column have 5 decimal places after the ','.

EXAMPLE_CODE_PROMPTS_CATEGORY_TEST_EXECUTION = [
    {
        "role": "user",
        "content": """input_excel_file_path = './assets/docs_input/Test_Execution_data Template.xlsx'
output_excel_file_path = './assets/docs_output/Teste Execução - 13_12_2024 - Test_Execution_data Template.xlsx'
excel_header_row_index = 3""",
    },
    {
        "role": "assistant",
        "content": open('./modules/ai_manual_implementation/agents/excel_content_modifier_agent/code_examples_for_code_prompts/code_example_category_test_execution_main.py', 'r', encoding='utf-8').read(),
    },
]