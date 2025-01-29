HEADER_FINDER_SYSTEM_PROMPT = """You are an assistant that handles Excel files.
When someone asks to find the header of a table, your task is to identify where the table starts by finding the row with the column names.
Your response should only include one JSON with the following format:
{
    "row_number": "<row_number>",
    "row_content": "<row_content>"
}

Additional rules:
No code-blocks or MARKDOWN are allowed in the response."""

HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO = [
    {
        "role": "system",
        "content": HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Find the header of the following file:
,,,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,1,20,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,33,33""",
    },
    {
        "role": "assistant",
        "content": """{
    "row_number": "2",
    "row_content": "ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds"
}""",
    },
]

HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO = [
    {
        "role": "system",
        "content": HEADER_FINDER_SYSTEM_PROMPT,
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