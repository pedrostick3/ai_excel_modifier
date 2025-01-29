from modules.ai_manual_implementation.fine_tuning_agents.excel_generic_agent.prompts.excel_categorizer_and_header_finder_agent_prompts import CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT
from modules.ai_manual_implementation.enums.file_category import FileCategory

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'Execution_data Template.xlsx'
```csv
,,,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,1,20,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,33,33
```""",
    },
    {
        "role": "assistant",
        "content": f"""{{
    "category": "{FileCategory.EXECUCAO.value}",
    "header": {{
        "row_number": "2",
        "row_content": "ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds"
    }}
}}""",
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_1_E = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'under.xlsx'
```csv
,,,,,,,
ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,1,20,20
2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146,146
2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,33,33
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_2_E = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'or.xlsx'
```csv
,,,,,,,
ExecutionId,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,1,20,20
153,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146,146
153,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,33,33
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_3_E = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'older.xlsx'
```csv
,,,,,,,
ExecutionId,ExecutionStartDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,1,20,20
153,2024-10-30 12:15:38.947,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146,146
153,2024-10-30 12:15:38.947,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,33,33
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_4_E = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'microsoft.xlsx'
```csv
,,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,1,20,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,33,33
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_5_E = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'angus.xlsx'
```csv
,,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseEndDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:16:01.763,1,20,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:40.463,1,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:19:14.870,1,33,33
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_6_E = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'new.xlsx'
```csv
,,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,1,20,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,1,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,1,33,33
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_7_E = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'quartz.xlsx'
```csv
,,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,33,33
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_8_E = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'leverage.xlsx'
```csv
,,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,1,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,33
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_9_E = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'random template.xlsx'
```csv
,,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,IsSuccessful,RunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,1,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,33
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
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
        "content": f"""{{
    "category": "{FileCategory.TESTE_EXECUCAO.value}",
    "header": {{
        "row_number": "4",
        "row_content": "ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds"
    }}
}}""",
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_10_TE = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'other template.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,,
Total run time,3910,,,,,,
,,,,,,,
IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds
1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_11_TE = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'wearable excel.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,,
Total run time,3910,,,,,,
,,,,,,,
ExecutionId,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds
153,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_12_TE = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'real true.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,,
Total run time,3910,,,,,,
,,,,,,,
ExecutionId,IsSuccessful,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds
153,1,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_13_TE = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'ok.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,,
Total run time,3910,,,,,,
,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds
153,1,20,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_14_TE = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'heavy number of lines.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,,
Total run time,3910,,,,,,
,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds
153,1,20,2024-10-30 12:15:38.947,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_15_TE = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'complex file.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,,
Total run time,3910,,,,,,
,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,CaseStartDate,CaseEndDate,AverageRunTimeSeconds
153,1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_16_TE = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'ok file copied.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,,
Total run time,3910,,,,,,
,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseEndDate,AverageRunTimeSeconds
153,1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:16:01.763,20
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_17_TE = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'understandable template.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,,
Total run time,3910,,,,,,
,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,AverageRunTimeSeconds
153,1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,20
```""",
    },
    {
        "role": "assistant",
        "content": f"""{{
    "category": "{FileCategory.TESTE_EXECUCAO.value}",
    "header": {{
        "row_number": "4",
        "row_content": "ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds"
    }}
}}""",
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_18_TE = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'private.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,,
Total run time,3910,,,,,,
,,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate
153,1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763
```""",
    },
    {
        "role": "assistant",
        "content": f"""{{
    "category": "{FileCategory.TESTE_EXECUCAO.value}",
    "header": {{
        "row_number": "4",
        "row_content": "ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,CaseStartDate,CaseEndDate,AverageRunTimeSeconds"
    }}
}}""",
    },
]