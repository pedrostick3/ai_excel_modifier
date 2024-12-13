SYSTEM_PROMPT_CATEGORY_EXECUTION = """
You are an assistant for editing Excel files. Your tasks are:
1. Move the 'IsSuccessful' column to column A, shifting the remaining columns to the right.
2. Remove the 'AverageRunTimeSeconds' column.
3. Add a new column 'RunTimeMinutes' at the last position of the table and set each value to 'RunTimeSeconds/60'.
4. Change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000).
5. Change the format of the columns 'ExecutionStartDate', 'ExecutionEndDate', 'CaseStartDate', and 'CaseEndDate' to 'dd-MM-yyyy HH:mm:ss.mmm'.
6. Return the complete modified file with the same amount of rows (even if they are the same).
7. Your response must not include code-blocks or MARKDOWN.
8. You should not add extra commas.
"""

EXAMPLE_PROMPTS_CATEGORY_EXECUTION = [
    {
        "role": "user",
        "content": """ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,1,20,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,33,33""",
    },
    {
        "role": "assistant",
        "content": """IsSuccessful,ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,RunTimeSeconds,RunTimeMinutes
1,153,30-10-2024 12:15:38.947,30-10-2024 12:19:15.973,"2,00000",30-10-2024 12:15:41.433,30-10-2024 12:16:01.763,20,0.33
1,153,30-10-2024 12:15:38.947,30-10-2024 12:19:15.973,"1,00000",30-10-2024 12:16:14.750,30-10-2024 12:18:40.463,146,2.43
1,153,30-10-2024 12:15:38.947,30-10-2024 12:19:15.973,"1,00000",30-10-2024 12:18:41.737,30-10-2024 12:19:14.870,33,0.55""",
    },
]

SYSTEM_PROMPT_CATEGORY_TEST_EXECUTION = """
You are an assistant for editing Excel files. Your tasks are:
1. Reorder the columns to: 'ExecutionId', 'ExecutionStartDate', 'ExecutionEndDate', 'TaskWorkload', 'CaseStartDate', 'CaseEndDate', 'IsSuccessful', 'RunTimeSeconds', 'AverageRunTimeSeconds'.
2. Change each value in the 'TaskWorkload' column by replacing '.' with ',' (e.g., 2.00000 becomes 2,00000).
3. Return the complete modified file with the same amount of rows (even if they are the same).
4. Your response must not include code-blocks or MARKDOWN.
5. You should not add extra commas.
"""
# Não consegue fazer contas com precisão nem consistência # "Add the sum of the data at the end of the 'RunTimeSeconds' and 'TaskWorkload' columns."

EXAMPLE_PROMPTS_CATEGORY_TEST_EXECUTION = [
    {
        "role": "user",
        "content": """,,,,,,,,
Test execution date,2024-10-30 12:15:38.947,,,,,,,
Total run time,3910,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds
153,1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20
153,1,146,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,146
153,1,33,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,33""",
    },
    {
        "role": "assistant",
        "content": """,,,,,,,,
Test execution date,2024-10-30 12:15:38.947,,,,,,,
Total run time,3910,,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,"2,00000",2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,1,20,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,"1,00000",2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,"1,00000",2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,33,33""",
    },
]