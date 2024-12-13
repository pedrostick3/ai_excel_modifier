# Esta prompt teve de ser alterada para JSON devido à AI retornar constantemente "None" como resposta por achar que 'Execução' é uma palavra violenta.
SYSTEM_PROMPT_JSON = """
You are an assistant for analyzing Excel files.
You need to identify where the table starts by finding the row with the column names.
Your response should only include one JSON with the following format:
{
    "row_number": "<row_number>",
    "row_content": "<row_content>"
}
No code-blocks or MARKDOWN are allowed in the response.
"""

EXAMPLE_PROMPTS_JSON = [
    {
        "role": "user",
        "content": """Test execution date,2024-10-30 12:15:38.947,,,,,,,
Total run time,3910,,,,,,,
,,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds
153,1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20""",
    },
    {
        "role": "assistant",
        "content": """
{
    "row_number": "4",
    "row_content": "ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds"
}
""",
    },
]
