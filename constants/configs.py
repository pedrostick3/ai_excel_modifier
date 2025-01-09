# Paths
INPUT_FOLDER = "./assets/docs_input"
OUTPUT_FOLDER = "./assets/docs_output"
TEST_EXECUTION_EXAMPLE_FILE = "./assets/example_test_execution_main.py"
MAX_EXCEL_LINES_PER_AI_REQUEST = 5

# Free AI APIs: https://github.com/zukixa/cool-ai-stuff

# GitHub Configs
# Quick Start Guide: https://github.com/marketplace/models/azure-openai/o1-mini
# Limitações: https://docs.github.com/pt/github-models/prototyping-with-ai-models#rate-limits
GITHUB_BASE_URL = "https://models.inference.ai.azure.com"
GITHUB_KEY = "<your_key>"
GITHUB_MODEL = "gpt-4o-mini" # https://github.com/marketplace/models

# FresedGPT Configs
# Discord invite to config: https://discord.gg/JecEC5my4T
# Discord channel to config: https://discord.com/channels/1232622371249192970/1234913876693221426
# Quick Start Guide: https://fresed-api.gitbook.io/fresed-api/getting-started
FRESEDGPT_BASE_URL = "https://fresedgpt.space/v1"
FRESEDGPT_KEY = "<your_key>"
FRESEDGPT_MODEL = "gpt-4o-mini" # https://fresedgpt.space/v1/models

# Zukijourney Configs
# Discord invite to config: https://discord.com/invite/Y4J6XXnmQ6
# Discord channel to config: https://discord.com/channels/1090022628946886726/1305777445852545024
# Quick Start Guide: https://docs.zukijourney.com/ai
ZUKIJOURNEY_BASE_URL = "https://api.zukijourney.com/v1"
ZUKIJOURNEY_KEY = "<your_key>"
ZUKIJOURNEY_MODEL = "gpt-4o-mini" # https://proxy.blackgaypornis.fun/v1/models

# OpenAI Configs
OPENAI_API_KEY = "<your_key>"
OPENAI_MODEL = "gpt-4o-mini" # https://platform.openai.com/docs/models OR https://openai.com/api/pricing

# Azure OpenAI Configs
# [Fine-tuning models Regions](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#fine-tuning-models)
# [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
# [Chat Quick Start Guide](https://learn.microsoft.com/pt-pt/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line%2Ckeyless%2Cjavascript-keyless%2Ctypescript-keyless%2Cpython-new&pivots=programming-language-python#create-a-new-python-application)
AZURE_ENDPOINT = "https://<your_azure_openai_resource_name>.openai.azure.com/" # Can be found in: Azure AI Foundry > Home > Azure OpenAI Endpoint (https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning?tabs=azure-openai%2Cturbo%2Cpython-new&pivots=programming-language-python#create-a-customized-model)
AZURE_API_KEY_1 = "<your_key>" # Can be found in: Azure AI Foundry > Home > API key 1 (https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning?tabs=azure-openai%2Cturbo%2Cpython-new&pivots=programming-language-python#create-a-customized-model)
AZURE_MODEL = "gpt-4o-mini" # Can be found in: Azure AI Foundry > Deployments > specific_model. It's the 'Name' propriety (not the 'Model Name' propriety). (https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning?tabs=azure-openai%2Cturbo%2Cpython-new&pivots=programming-language-python#create-a-customized-model)
AZURE_API_VERSION = "2024-08-01-preview" # Can be found in: Azure AI Foundry > Deployments > specific_model > Endpoint > Target URI (https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning)