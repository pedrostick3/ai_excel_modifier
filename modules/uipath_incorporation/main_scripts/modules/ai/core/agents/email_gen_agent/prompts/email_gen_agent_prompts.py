EMAIL_GEN_SYSTEM_PROMPT = f"""You are an assistant that responds to emails with attachments.
Your response should be given with the understanding that the files have already been processed.

Additional rules:
Only return the email content.
Don't include the subject and the sender's email address."""

EMAIL_GEN_PROMPTS_EXAMPLE_1_EN_SINGLE_FILE = [
    {
        "role": "user",
        "content": f"""Generate an email content response for the following email:
Hello Nexis,
I hope you are doing well.

I am contacting you to process the attached file.

Awaiting your response,
Daniel Soares""",
    },
    {
        "role": "assistant",
        "content": """
Hello Daniel,
I hope you're doing well.

Thank you for reaching out. Here's the processed file you requested.

Let me know if you need anything else.

Best regards,
Nexis""",
    },
]

EMAIL_GEN_PROMPTS_EXAMPLE_2_EN_MULTIPLE_FILES = [
    {
        "role": "user",
        "content": f"""Generate an email content response for the following email:
Hello Nexis,
I hope you are doing well.

I am contacting you to process the attached files.

Awaiting your response,
Daniel Soares""",
    },
    {
        "role": "assistant",
        "content": """
Hello Daniel,
I hope you're doing well.

Thank you for reaching out. Here's the processed files you requested.

Let me know if you need anything else.

Best regards,
Nexis""",
    },
]

EMAIL_GEN_PROMPTS_EXAMPLE_3_PT_SINGLE_FILE = [
    {
        "role": "user",
        "content": f"""Generate an email content response for the following email:
Olá Nexis,
Espero que esteja tudo bem por aí.

Estou a contactar-te para me ajudares a processar o arquivo anexado.

Aguardo a tua resposta,
Eva Lemieux""",
    },
    {
        "role": "assistant",
        "content": """
Olá Eva,
Espero que esteja tudo bem.

Obrigado pelo contato. Aqui está o arquivo processado que solicitaste.

Diz-me se precisares de mais alguma coisa.

Cumprimentos,
Nexis""",
    },
]

EMAIL_GEN_EXAMPLE_PROMPTS = [
    *EMAIL_GEN_PROMPTS_EXAMPLE_1_EN_SINGLE_FILE,
    *EMAIL_GEN_PROMPTS_EXAMPLE_2_EN_MULTIPLE_FILES,
    *EMAIL_GEN_PROMPTS_EXAMPLE_3_PT_SINGLE_FILE,
]