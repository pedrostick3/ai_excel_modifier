from modules.ai.core.enums.file_category import FileCategory

CATEGORIZER_SYSTEM_PROMPT = f"""You are an assistant that handles Excel files.
When someone asks to categorize a file, your task is to return only the category name of the file.
1. Name categorization:
1.1. If the filename contains 'Execution_data', then it belongs to the '{FileCategory.EXECUCAO.value}' category and ignore the rest of the rules;
1.2. If the filename contains 'Test_Execution_data', then it belongs to the '{FileCategory.TESTE_EXECUCAO.value}' category and ignore the rest of the rules;
1.3. If the filename does not contain any of the text indicated above, then a categorization should be made by its content;
2. Content categorization:
2.1. If the file has a blank first line and in the second line must have the exact columns 'ExecutionId, ExecutionStartDate, ExecutionEndDate, TaskWorkload, CaseStartDate, CaseEndDate, IsSuccessful, RunTimeSeconds, AverageRunTimeSeconds', then category is '{FileCategory.EXECUCAO.value}'.
2.2. If the file has in column A line 1 the label 'Test execution', in column A line 2 the label 'Total run time' and in line 4 must have the exact columns 'ExecutionId, IsSuccessful, RunTimeSeconds, ExecutionStartDate, ExecutionEndDate, TaskWorkload, CaseStartDate, CaseEndDate, AverageRunTimeSeconds', then category is '{FileCategory.TESTE_EXECUCAO.value}'.
2.3. If the file does not comply with the indicated cases, then category is '{FileCategory.INVALIDO.value}'.

Additional rules:
No code-blocks or MARKDOWN are allowed in the response.
Your response should only include one JSON with the following format: {{"category": "<category_name>"}}"""

CATEGORIZER_PROMPTS_CATEGORY_EXECUCAO = [
    {
        "role": "system",
        "content": CATEGORIZER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize the following file:
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
        "content": f'{{"category": "{FileCategory.EXECUCAO.value}"}}',
    },
]

CATEGORIZER_PROMPTS_CATEGORY_TESTE_EXECUCAO = [
    {
        "role": "system",
        "content": CATEGORIZER_SYSTEM_PROMPT,
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

CATEGORIZER_PROMPTS_CATEGORY_INVALIDO = [
    {
        "role": "system",
        "content": CATEGORIZER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize the following file:
Filename = 'ParameterizationFile_testes_13112024.xlsx'
```csv
Template,Nome,Quota,Pivot,Sheet,NIF,Nsocio,SeparadorMilhar,SeparadorDecimal,Moeda,Remover linhas com,RemoverLinhaFinal,IgnorarLinhasSemValorDesconto,Taxa,MesReferencia
AqueleGrande,Nome,Quota SAMS sócio,A1,Sheet1,Nº identif.fiscal,Número de sócio,",",.,,,,,,
CA Coimbra,Nome ,Valor do Desconto,A3,Folha1,NIF,,,.,,,,,,
CA Generico,NOME,QUOTA,A8,Mapa,,Nº SÓCIO SINDICATO,",",.,€,Total,Sim,,,
Complicado,NOME,DESCONTO,A1,Folha1,NIF,Nº PARTIC.,,.,€,Total;TOTAL;Factura,,Sim,,
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_PROMPTS_CATEGORY_INVALIDO_1 = [
    {
        "role": "system",
        "content": CATEGORIZER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize the following file:
Filename = 'E_unnamed_inv.xlsx'
```csv
,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,1,20,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,1,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,1,33,33
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_PROMPTS_CATEGORY_INVALIDO_2 = [
    {
        "role": "system",
        "content": CATEGORIZER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize the following file:
Filename = 'TE_unnamed_inv.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,
Total run time,3910,,,,,
,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,AverageRunTimeSeconds
153,1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,20
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_PROMPTS_CATEGORY_INVALIDO_3 = [
    {
        "role": "system",
        "content": CATEGORIZER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize the following file:
Filename = 'file-73.xlsx'
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

CATEGORIZER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME = [
    {
        "role": "system",
        "content": CATEGORIZER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize the following file:
Filename = 'new file.xlsx'
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
        "content": f'{{"category": "{FileCategory.EXECUCAO.value}"}}',
    },
]

CATEGORIZER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME = [
    {
        "role": "system",
        "content": CATEGORIZER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize the following file:
Filename = 'copy of edited file.xlsx'
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

CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT = f"""You are an assistant that handles Excel files.
When someone asks to categorize a file and find the header of a table, your task is to return the category name of the file and identify where the table starts by finding the row with the column names.
1. Name categorization:
1.1. If the filename contains 'Execution_data', then it belongs to the '{FileCategory.EXECUCAO.value}' category and ignore the next '2.' step;
1.2. If the filename contains 'Test_Execution_data', then it belongs to the '{FileCategory.TESTE_EXECUCAO.value}' category and ignore the next '2.' step;
1.3. If the filename does not contain any of the text indicated above, then a categorization should be made by its content;
2. Content categorization:
2.1. If the file has a blank first line and in the second line must have the exact columns 'ExecutionId, ExecutionStartDate, ExecutionEndDate, TaskWorkload, CaseStartDate, CaseEndDate, IsSuccessful, RunTimeSeconds, AverageRunTimeSeconds', then category is '{FileCategory.EXECUCAO.value}'.
2.2. If the file has in column A line 1 the label 'Test execution', in column A line 2 the label 'Total run time' and in line 4 must have the exact columns 'ExecutionId, IsSuccessful, RunTimeSeconds, ExecutionStartDate, ExecutionEndDate, TaskWorkload, CaseStartDate, CaseEndDate, AverageRunTimeSeconds', then category is '{FileCategory.TESTE_EXECUCAO.value}'.
2.3. If the file does not comply with the indicated cases, then category is '{FileCategory.INVALIDO.value}'.

Additional rules:
No code-blocks or MARKDOWN are allowed in the response.
Your response should only include one JSON with the following format:
{{
    "category": "<category_name>",
    "header": {{
        "row_number": "<row_number>",
        "row_content": "<row_content>"
    }}
}}"""

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

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'ParameterizationFile_testes_13112024.xlsx'
```csv
Template,Nome,Quota,Pivot,Sheet,NIF,Nsocio,SeparadorMilhar,SeparadorDecimal,Moeda,Remover linhas com,RemoverLinhaFinal,IgnorarLinhasSemValorDesconto,Taxa,MesReferencia
AqueleGrande,Nome,Quota SAMS sócio,A1,Sheet1,Nº identif.fiscal,Número de sócio,",",.,,,,,,
CA Coimbra,Nome ,Valor do Desconto,A3,Folha1,NIF,,,.,,,,,,
CA Generico,NOME,QUOTA,A8,Mapa,,Nº SÓCIO SINDICATO,",",.,€,Total,Sim,,,
Complicado,NOME,DESCONTO,A1,Folha1,NIF,Nº PARTIC.,,.,€,Total;TOTAL;Factura,,Sim,,
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_1 = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'E_unnamed_inv.xlsx'
```csv
,,,,,,
ExecutionId,ExecutionStartDate,ExecutionEndDate,TaskWorkload,IsSuccessful,RunTimeSeconds,AverageRunTimeSeconds
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,1,20,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,1,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,1,33,33
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_2 = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'TE_unnamed_inv.xlsx'
```csv
Test execution date,2024-10-30 12:15:38.947,,,,,
Total run time,3910,,,,,
,,,,,,
ExecutionId,IsSuccessful,RunTimeSeconds,ExecutionStartDate,ExecutionEndDate,TaskWorkload,AverageRunTimeSeconds
153,1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,20
```""",
    },
    {
        "role": "assistant",
        "content": f'{{"category": "{FileCategory.INVALIDO.value}"}}',
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_INVALIDO_3 = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'file-73.xlsx'
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

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_FILENAME = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'new file.xlsx'
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

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_FILENAME = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'copy of edited file.xlsx'
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

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_EXECUCAO_WITHOUT_HEADER = [
    {
        "role": "system",
        "content": CATEGORIZER_AND_HEADER_FINDER_SYSTEM_PROMPT,
    },
    {
        "role": "user",
        "content": """Categorize and find the header of the following file:
Filename = 'Execution_data Template.xlsx'
```csv
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,33,33
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,1,20,20
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:16:14.750,2024-10-30 12:18:40.463,1,146,146
153,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,1.00000,2024-10-30 12:18:41.737,2024-10-30 12:19:14.870,1,23,93
```""",
    },
    {
        "role": "assistant",
        "content": f"""{{
    "category": "{FileCategory.EXECUCAO.value}",
    "header": None
}}""",
    },
]

CATEGORIZER_AND_HEADER_FINDER_PROMPTS_CATEGORY_TESTE_EXECUCAO_WITHOUT_HEADER = [
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
153,1,15,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20
153,1,20,2024-10-30 12:15:38.947,2024-10-30 12:19:15.973,2.00000,2024-10-30 12:15:41.433,2024-10-30 12:16:01.763,20
```""",
    },
    {
        "role": "assistant",
        "content": f"""{{
    "category": "{FileCategory.TESTE_EXECUCAO.value}",
    "header": None
}}""",
    },
]

PRE_HEADER_MODIFIER_SYSTEM_PROMPT = f"""You are an assistant that handles Excel files.
When someone asks to modify the pre-header of a file with the '{FileCategory.EXECUCAO.value}' category, your tasks are:
1. Remove row 1 if it is empty.

When someone asks to modify the pre-header of a file with the '{FileCategory.TESTE_EXECUCAO.value}' category, your tasks are:
1. Remove row 3 if it is empty.
2. Add a new blank row above row 1.

Additional rules:
Return the complete modified file with all rows and columns.
You should not add extra commas.
Your response must not include code-blocks or MARKDOWN."""

PRE_HEADER_MODIFIER_PROMPTS_CATEGORY_EXECUCAO = [
    {
        "role": "system",
        "content": PRE_HEADER_MODIFIER_SYSTEM_PROMPT,
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

PRE_HEADER_MODIFIER_PROMPTS_CATEGORY_TESTE_EXECUCAO = [
    {
        "role": "system",
        "content": PRE_HEADER_MODIFIER_SYSTEM_PROMPT,
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
