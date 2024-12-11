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

Como saber quais os modelos disponiveis:
```python
import openai
openai.api_key = "OPENAI_API_KEY"

models=openai.models.list()
print(f"######## Modelos disponíveis: {models}")
```

### Modelos disponíveis para o plano Free da API da OpenAI:
- **dall-e-2** (created: 1698798177 (01/11/2023), owned by: system)
- **whisper-1** (created: 1677532384 (27/02/2023), owned by: openai-internal)
- **gpt-3.5-turbo-instruct** (created: 1692901427 (24/08/2023) , owned by: system)
- **gpt-3.5-turbo** (created: 1677610602 (28/02/2023), owned by: openai)
- **gpt-3.5-turbo-0125** (created: 1706048358 (23/01/2024), owned by: system)
- **babbage-002** (created: 1692634615 (21/08/2023), owned by: system)
- **davinci-002** (created: 1692634301 (21/08/2023), owned by: system)
- **dall-e-3** (created: 1698785189 (31/10/2023), owned by: system)
- **gpt-3.5-turbo-16k** (created: 1683758102 (10/05/2023), owned by: openai-internal)
- **tts-1-hd-1106** (created: 1699053533 (03/11/2023), owned by: system)
- **text-embedding-ada-002** (created: 1671217299 (16/12/2022), owned by: openai-internal)
- **text-embedding-3-small** (created: 1705948997 (22/01/2024), owned by: system)
- **text-embedding-3-large** (created: 1705953180 (22/01/2024), owned by: system)
- **tts-1-hd** (created: 1699046015 (03/11/2023), owned by: system)
- **gpt-3.5-turbo-1106** (created: 1698959748 (02/11/2023), owned by: system)
- **gpt-4o-mini-2024-07-18** (created: 1721172717 (16/07/2024), owned by: system)
- **gpt-4o-mini** (created: 1721172741 (16/07/2024), owned by: system)
- **tts-1** (created: 1681940951 (19/04/2023), owned by: openai-internal)
- **tts-1-1106** (created: 1699053241 (03/11/2023), owned by: system)
- **gpt-3.5-turbo-instruct-0914** (created: 1694122472 (07/09/2023), owned by: system)