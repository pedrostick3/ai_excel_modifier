Crate .venv folder for virtual environment:

```bash
python -m venv .venv
```
OR
```bash
python3.9 -m venv .venv
```

Activate virtual environment:

```bash
source .venv/bin/activate
```
OR
```bash
.venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r dependencies_to_install.txt
```
OR
```bash
python3.9 -m pip install -r dependencies_to_install.txt
```
OR
```bash
.venv/Scripts/python.exe -m pip install -r dependencies_to_install.txt
```

Run the application on F5 (run button) or:

```bash
python main.py
```
OR
```bash
python3.9 main.py
```
OR
```bash
.venv/Scripts/python.exe main.py
```

Check available OpenAI models:
```python
import openai
openai.api_key = "OPENAI_API_KEY"

models=openai.models.list()
print(f"Available Models: {models}")
```

### Tested Models:
- **o1-preview**
- **o1-mini**
- **gpt-4o**
- **gpt-4o-mini (most used since it's the best option for this PoC comparing cost & quality)**

### Agent Prompts:
- **ExcelCategorizerAgent**: modules/ai/agents/excel_categorizer_agent/excel_categorizer_agent_prompts.py
- **ExcelHeaderFinderAgent**: modules/ai/agents/excel_header_finder_agent/excel_header_finder_agent_prompts.py
- **ExcelPreHeaderModifierAgent**: modules/ai/agents/excel_pre_header_modifier_agent/excel_pre_header_modifier_agent_prompts.py
- **ExcelContentModifierAgent**: modules/ai/agents/excel_content_modifier_agent/excel_content_modifier_agent_prompts.py
- **ExcelGenericContentModifierAgent**: modules/ai/agents/excel_generic_content_modifier_agent/excel_generic_content_modifier_agent_code_prompts.py
- **CodeInterpreterAgent (not tested yet)**: modules/ai/code_interpreter_agent/code_interpreter_agent/code_interpreter_agent.py
- **FileSearchAgent (not tested yet)**: modules/ai/file_search_agent/file_search_agent/file_search_agent.py
- **ExcelSumColumnsAgent**: modules/ai/function_calls_agent/excel_sum_columns_agent/excel_sum_columns_agent.py
- **ExcelGenericFineTuningAgent**: modules/ai/fine_tuning_agents/excel_generic_agent/excel_generic_fine_tuning_agent_prompts.py

### AI Services & Utils:
- **AzureAiService**: modules/ai/services/azure_ai_service.py
- **OpenAiAiService**: modules/ai/services/openai_ai_service.py
- **CustomAiService**: modules/ai/services/custom_ai_service.py
- **TokenUtils**: modules/ai/utils/token_utils.py

### Excel Services:
- **ExcelService**: modules/excel/services/excel_service.py

### AiAnalytics Services:
- **AiAnalytics**: modules/analytics/services/ai_analytics.py

### Python Project Modules:
- **ai**: Module responsible for handling everything related to AI;
- **analytics**: Module responsible for analyzing the AI Agents behavior;
- **excel**: Module responsible for processing excel files;
- **uipath_incorporation**: Independent module developed to test the [incorporation](https://youtu.be/Zar8wrhT0Dk?si=cCyvklLRAEGq7eOU) of the python project into UiPath Activities;

### Python version used:
- **Python 3.11.5** - you can check it by running `python --version` in your terminal