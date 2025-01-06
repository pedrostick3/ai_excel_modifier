from modules.ai.enums.file_category import FileCategory

CATEGORIZER_PROMPTS = [
    {
        "role": "system",
        "content": f"""You are an assistant that handles Excel files.
When someone asks to categorize a file, your task is to return only the category name of the file.
1. Name categorization:
1.1. If the filename contains 'Execution_data', then it belongs to the '{FileCategory.EXECUCAO.value}' category and ignore the rest of the rules;
1.2. If the filename contains 'Test_Execution_data', then it belongs to the '{FileCategory.TESTE_EXECUCAO.value}' category and ignore the rest of the rules;
1.3. If the filename does not contain any of the text indicated above, then a categorization should be made by its content;
2. Content categorization:
2.1. If the file has a blank first line and then the columns 'ExecutionId, ExecutionStartDate, ExecutionEndDate, TaskWorkload, CaseStartDate, CaseEndDate, IsSuccessful, RunTimeSeconds, AverageRunTimeSeconds', then category is '{FileCategory.EXECUCAO.value}'.
2.2. If the file has in column A line 1 the label 'Test execution', in column A line 2 the label 'Total run time' and in list 4 the columns 'ExecutionId, IsSuccessful, RunTimeSeconds, ExecutionStartDate, ExecutionEndDate, TaskWorkload, CaseStartDate, CaseEndDate, AverageRunTimeSeconds', then category is '{FileCategory.TESTE_EXECUCAO.value}'.
2.3. If the file does not comply with the indicated cases, then category is '{FileCategory.INVALIDO.value}'.

Additional rules:
No code-blocks or MARKDOWN are allowed in the response.
Your response should only include one JSON with the following format: {{"category": "<category_name>"}}""",
    },
    {
        "role": "user",
        "content": """Categorize the following file:
Filename = 'Test_Execution_data Template.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,,,
Total run time,3910,,,,,,,
,,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds
153,1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.TESTE_EXECUCAO.value}"}}',
    },
]

HEADER_FINDER_PROMPTS = [
    {
        "role": "system",
        "content": """You are an assistant that handles Excel files.
When someone asks to find the header of a table, your task is to identify where the table starts by finding the row with the column names.
Your response should only include one JSON with the following format:
{
    "row_number": "<row_number>",
    "row_content": "<row_content>"
}

Additional rules:
No code-blocks or MARKDOWN are allowed in the response.""",
    },
    {
        "role": "user",
        "content": """Find the header of the following file:
Test execution date,2024-10-30 12:15:38.947,,,,,,,
Total run time,3910,,,,,,,
,,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds
153,1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20""",
    },
    {
        "role": "assistant",
        "content": """{
    "row_number": "4",
    "row_content": "ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds"
}""",
    },
]

PRE_HEADER_MODIFIER_CATEGORY_EXECUTION_PROMPTS = [
    {
        "role": "system",
        "content": f"""You are an assistant that handles Excel files.
When someone asks to modify the pre-header of a file with the '{FileCategory.EXECUCAO.value}' category, your tasks are:
1. Remove row 1 if it is empty.

Additional rules:
Return the complete modified file with all rows and columns.
You should not add extra commas.
Your response must not include code-blocks or MARKDOWN.""",
    },
    {
        "role": "user",
        "content": f"""Modify the pre-header of the following file that belongs to the '{FileCategory.EXECUCAO.value}' category:
,,,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds""",
    },
    {
        "role": "assistant",
        "content": "ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds",
    },
]

PRE_HEADER_MODIFIER_CATEGORY_TEST_EXECUTION_PROMPTS = [
    {
        "role": "system",
        "content": f"""You are an assistant that handles Excel files.
When someone asks to modify the pre-header of a file with the '{FileCategory.TESTE_EXECUCAO.value}' category, your tasks are:
1. Remove row 3 if it is empty.
2. Add a new blank row above row 1.

Additional rules:
Return the complete modified file with all rows and columns.
You should not add extra commas.
Your response must not include code-blocks or MARKDOWN.""",
    },
    {
        "role": "user",
        "content": f"""Modify the pre-header of the following file that belongs to the '{FileCategory.TESTE_EXECUCAO.value}' category:
Test execution date,2024-10-30 12:15:38.947,,,,,,,
Total run time,3910,,,,,,,
,,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds""",
    },
    {
        "role": "assistant",
        "content": """,,,,,,,,
Test execution date,2024-10-30 12:15:38.947,,,,,,,
Total run time,3910,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds""",
    },
]

CONTENT_MODIFIER_CATEGORY_EXECUTION_PROMPTS = [
    {
        "role": "system",
        "content": f"""You are an assistant that handles Excel files.
When someone asks to return the python code to modify the content of a file with the '{FileCategory.EXECUCAO.value}' category, your tasks are:
1. Move the 'IsSuccessful' column to column A, shifting the remaining columns to the right.
2. Remove the 'AverageRunTimeSeconds' column.
3. Add a new column 'RunTimeMinutes' at the last position of the table and set each value to 'RunTimeSeconds/60'. Careful with the division and try to convert the values to numeric before dividing.
4. Change the format of the columns 'ExecutionStartDate', 'ExecutionEndDate', 'CaseStartDate', and 'CaseEndDate' to 'dd-MM-yyyy HH:mm:ss.mmm'. Mitigate possible warnings.
5. In the end, change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Make sure that every value of 'TaskWorkload' column have 5 decimal places after the ','.

Additional rules:
Return the python code to modify the complete file and save it.
Your response must not include code-blocks or MARKDOWN.
Initialize the given variables in the beginning of the code.
Use concat() function to join dataframes.
Don't use xlswriter to save the file.""",
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
            "./modules/ai/agents/excel_content_modifier_agent/code_examples_for_code_prompts/code_example_category_execution_main.py",
            encoding="utf-8",
        ).read(),
    },
]

CONTENT_MODIFIER_CATEGORY_TEST_EXECUTION_PROMPTS = [
    {
        "role": "system",
        "content": f"""You are an assistant that handles Excel files.
When someone asks to return the python code to modify the content of a file with the '{FileCategory.TESTE_EXECUCAO.value}' category, your tasks are:
1. Reorder the columns to: 'ExecutionId', 'ExecutionStartDate', 'ExecutionEndDate', 'TaskWorkload', 'CaseStartDate', 'CaseEndDate', 'IsSuccessful', 'RunTimeSeconds', 'AverageRunTimeSeconds'.
2. Add the sum of 'RunTimeSeconds' and 'TaskWorkload' columns at the end of the table. Convert the values to numeric before calculating.
3. In the end, change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000). Make sure that every value of 'TaskWorkload' column have 5 decimal places after the ','.

Additional rules:
Return the python code to modify the complete file and save it.
Your response must not include code-blocks or MARKDOWN.
Initialize the given variables in the beginning of the code.
Use concat() function to join dataframes.
Don't use xlswriter to save the file.
Don't add unnecessary columns.""",
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
            "./modules/ai/agents/excel_content_modifier_agent/code_examples_for_code_prompts/code_example_category_test_execution_main.py",
            encoding="utf-8",
        ).read(),
    },
]
