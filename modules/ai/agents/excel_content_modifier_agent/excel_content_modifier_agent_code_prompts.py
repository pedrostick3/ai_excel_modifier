SYSTEM_CODE_PROMPT_CATEGORY_EXECUTION = """You are an assistant for editing Excel files. Your tasks are:
1. Move the 'IsSuccessful' column to column A, shifting the remaining columns to the right.
2. Remove the 'AverageRunTimeSeconds' column.
3. Add a new column 'RunTimeMinutes' at the last position of the table and set each value to 'RunTimeSeconds/60'. Careful with the division and try to convert the values to numeric before dividing.
4. Change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Must have 5 decimal places.
5. Change the format of the columns 'ExecutionStartDate', 'ExecutionEndDate', 'CaseStartDate', and 'CaseEndDate' to 'dd-MM-yyyy HH:mm:ss.mmm'. Mitigate possible warnings.
6. Return the python code to modify the complete file and save it.
7. Your response must not include code-blocks or MARKDOWN.
8. Initialize the given variables in the beginning of the code.
9. Use concat() function to join dataframes.
10. Don't use xlswriter to save the file."""

EXAMPLE_CODE_PROMPTS_CATEGORY_EXECUTION = [
    {
        "role": "user",
        "content": """input_excel_file_path = './assets/docs_input/Execution_data Template.xlsx'
output_excel_file_path = './assets/docs_output/Execução - 16_12_2024 - Execution_data Template.xlsx'
excel_header_row_index = 1""",
    },
    {
        "role": "assistant",
        "content": open('./modules/ai/agents/excel_content_modifier_agent/code_examples_for_code_prompts/code_example_category_execution_main.py', 'r', encoding='utf-8').read(),
    },
]

SYSTEM_CODE_PROMPT_CATEGORY_TEST_EXECUTION = """You are an assistant for editing Excel files. Your tasks are:
1. Reorder the columns to: 'ExecutionId', 'ExecutionStartDate', 'ExecutionEndDate', 'TaskWorkload', 'CaseStartDate', 'CaseEndDate', 'IsSuccessful', 'RunTimeSeconds', 'AverageRunTimeSeconds'.
2. Add the sum of 'RunTimeSeconds' and 'TaskWorkload' columns at the end of the table. Convert the values to numeric before calculating.
3. Only after the sum, change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Must have 5 decimal places.
4. Return the python code to modify the complete file and save it.
5. Your response must not include code-blocks or MARKDOWN.
6. Initialize the given variables in the beginning of the code.
7. Use concat() function to join dataframes.
8. Don't use xlswriter to save the file.
9. Don't add unnecessary columns."""

EXAMPLE_CODE_PROMPTS_CATEGORY_TEST_EXECUTION = [
    {
        "role": "user",
        "content": """input_excel_file_path = './assets/docs_input/Execution_data Template.xlsx'
output_excel_file_path = './assets/docs_output/Teste Execução - 13_12_2024 - Test_Execution_data Template.xlsx'
excel_header_row_index = 3""",
    },
    {
        "role": "assistant",
        "content": open('./modules/ai/agents/excel_content_modifier_agent/code_examples_for_code_prompts/code_example_category_test_execution_main.py', 'r', encoding='utf-8').read(),
    },
]