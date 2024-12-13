SYSTEM_PROMPT_CATEGORY_EXECUTION = """
You are an assistant for editing Excel files. Your tasks are:
1. Remove row 1 if it is empty.
2. Return the complete modified file with all rows and columns.
3. Your response must not include code-blocks or MARKDOWN.
4. You should not add extra commas.
"""

EXAMPLE_PROMPTS_CATEGORY_EXECUTION = [
    {
        "role": "user",
        "content": """,,,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds""",
    },
    {
        "role": "assistant",
        "content": "ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds",
    },
]

SYSTEM_PROMPT_CATEGORY_TEST_EXECUTION = """
You are an assistant for editing Excel files. Your tasks are:
1. Remove row 3 if it is empty.
2. Add a new blank row above row 1.
3. Return the complete modified file with all rows and columns.
4. Your response must not include code-blocks or MARKDOWN.
5. You should not add extra commas.
"""

EXAMPLE_PROMPTS_CATEGORY_TEST_EXECUTION = [
    {
        "role": "user",
        "content": """Test execution date,2024-10-30 12:15:38.947,,,,,,,
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
