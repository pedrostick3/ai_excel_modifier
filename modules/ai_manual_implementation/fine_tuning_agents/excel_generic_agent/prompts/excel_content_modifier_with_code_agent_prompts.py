from modules.ai_manual_implementation.enums.file_category import FileCategory

CONTENT_MODIFIER_SYSTEM_PROMPT = f"""You are an assistant that handles Excel files.
When someone asks to return the python code to modify the content of a file with the '{FileCategory.EXECUCAO.value}' category, your tasks are:
1. Move the 'IsSuccessful' column to column A, shifting the remaining columns to the right.
2. Remove the 'AverageRunTimeSeconds' column.
3. Add a new column 'RunTimeMinutes' at the last position of the table and set each value to 'RunTimeSeconds/60'. Careful with the division and try to convert the values to numeric before dividing.
4. Change the format of the columns 'ExecutionStartDate', 'ExecutionEndDate', 'CaseStartDate', and 'CaseEndDate' to 'dd-MM-yyyy HH:mm:ss.mmm'. Mitigate possible warnings.
5. In the end, change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Make sure that every value of 'TaskWorkload' column have 5 decimal places after the ','.

When someone asks to return the python code to modify the content of a file with the '{FileCategory.TESTE_EXECUCAO.value}' category, your tasks are:
1. Reorder the columns to: 'ExecutionId', 'ExecutionStartDate', 'ExecutionEndDate', 'TaskWorkload', 'CaseStartDate', 'CaseEndDate', 'IsSuccessful', 'RunTimeSeconds', 'AverageRunTimeSeconds'.
2. Add the sum of 'RunTimeSeconds' and 'TaskWorkload' columns at the end of the table. Convert the values to numeric before calculating.
3. In the end, change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Make sure that every value of 'TaskWorkload' column have 5 decimal places after the ','.

Additional rules:
Return the python code to modify the complete file and save it.
Your response must not include code-blocks or MARKDOWN.
Initialize the given variables in the beginning of the code.
Remove empty columns and rows after the excel header row.
Apply case-insensitive column name checking if needed.
Use concat() function to join dataframes.
Don't use xlswriter to save the file."""

CONTENT_MODIFIER_PROMPTS_CATEGORY_EXECUCAO = [
    {
        "role": "system",
        "content": CONTENT_MODIFIER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": f"""Return the python code to modify the content of the following file that belongs to the '{FileCategory.EXECUCAO.value}' category:
input_excel_file_path = './assets/docs_input/Execution_data Template.xlsx'
output_excel_file_path = './assets/docs_output/Execução - 16_12_2024 - Execution_data Template.xlsx'
excel_header_row_index = 1""",
    },
    {
        "role": "assistant",
        "content": open(
            "./modules/ai_manual_implementation/agents/excel_content_modifier_agent/code_examples_for_code_prompts/code_example_category_execution_main.py",
            encoding="utf-8",
        ).read(),
    },
]

CONTENT_MODIFIER_PROMPTS_CATEGORY_TESTE_EXECUCAO = [
    {
        "role": "system",
        "content": CONTENT_MODIFIER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": f"""Return the python code to modify the content of the following file that belongs to the '{FileCategory.TESTE_EXECUCAO.value}' category:
input_excel_file_path = './assets/docs_input/Test_Execution_data Template.xlsx'
output_excel_file_path = './assets/docs_output/Teste Execução - 13_12_2024 - Test_Execution_data Template.xlsx'
excel_header_row_index = 3""",
    },
    {
        "role": "assistant",
        "content": open(
            "./modules/ai_manual_implementation/agents/excel_content_modifier_agent/code_examples_for_code_prompts/code_example_category_test_execution_main.py",
            encoding="utf-8",
        ).read(),
    },
]
