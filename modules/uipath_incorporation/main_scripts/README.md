Crate .env folder for virtual environment:

```bash
python -m venv .env
```

Activate virtual environment:

```bash
source .env/bin/activate
```
OR
```bash
.env/Scripts/activate
```

Install dependencies:

```bash
pip install -r dependencies_to_install.txt
```

Run the application on F5 (run button) or:

```bash
python main.py
```

Check available OpenAI models:
```python
import openai
openai.api_key = "OPENAI_API_KEY"

models=openai.models.list()
print(f"Available Models: {models}")
```

### OpenAI Models:
- **ft:gpt-4o-mini-2024-07-18:inspireit::AqjmD7gd (fine-tuning model)**
- **gpt-4o-mini-2024-07-18 (fine-tuning base model)**

### Agent Prompts:
- **ExcelGenericFineTuningAgent**: modules/ai/fine_tuning_agents/excel_generic_agent/excel_generic_fine_tuning_agent_prompts.py

### AI Services & Utils:
- **OpenAiAiService**: modules/ai/services/openai_ai_service.py
- **TokenUtils**: modules/ai/utils/token_utils.py

### Excel Services:
- **ExcelService**: modules/excel/services/excel_service.py

### AiAnalytics Services:
- **AiAnalytics**: modules/analytics/services/ai_analytics.py

### Python version used for UiPath compatibility:
- **Python 3.9** - you can check it by running `python --version` in your terminal