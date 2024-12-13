import logging
import pandas as pd
import re
import os
import constants.configs as configs
from modules.analytics.models.ai_files_analytics_model import AiFilesAnalyticsModel
from modules.analytics.models.ai_agent_analytics_model import AiAgentAnalyticsModel

class AiAnalytics:
    ai_files_analytics: AiFilesAnalyticsModel = AiFilesAnalyticsModel()

    @staticmethod
    def add_file_agent_request(
        file_name: str,
        agent_name: str,
        ai_model: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        execution_time_in_seconds: float,
        extra_info: str = None,
        log: bool = False,
    ) -> None:
        """
        Adds an AI Agent Analytics Model to the list of agent requests.

        Args:
            file_name (str): The name of the file.
            agent_name (str): The name of the agent.
            ai_model (str): The AI model.
            prompt_tokens (int): The number of tokens in the prompt.
            completion_tokens (int): The number of tokens in the completion.
            total_tokens (int): The total number of tokens.
            execution_time_in_seconds (float): The execution time.
            extra_info (str, optional): Extra information. Defaults to None.
        """
        agent_request = AiAgentAnalyticsModel(
            name=agent_name,
            ai_model=ai_model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            execution_time_in_seconds=execution_time_in_seconds,
            extra_info=extra_info,
        )

        AiAnalytics.ai_files_analytics.add_agent_request(file_name, agent_request)

        if log:
            logging.info(f"Added agent request: {agent_request}")

    @staticmethod
    def export_str_ai_analytics_data_to_excel(
        data: str = None,
        output_file_path: str = f"./assets/ai_analytics/{pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M-%S')}_ai_analytics.xlsx",
    ) -> None:
        """
        Exports the AI Analytics to an Excel file.

        Args:
            data (str, optional): The data to be exported. Defaults to None.
            output_file_path (str): The output file path. Defaults to a timestamped path.
        """
        data = data if data else str(AiAnalytics.ai_files_analytics)
        if not data or "#####" not in data:
            raise ValueError("O formato do texto fornecido não é válido. Verifique os delimitadores '#####'.")

        # Configurações fixas para o Excel
        pricing = {
            "AI Model": "gpt-4o-mini",
            "Pricing Input per 1M Tokens": 0.15,
            "Pricing Output per 1M Tokens": 0.6,
            "1 Million Tokens": 1000000,
            "MAX_EXCEL_LINES_PER_AI_REQUEST": configs.MAX_EXCEL_LINES_PER_AI_REQUEST,
        }

        # Função para processar os dados
        def process_data_per_section(raw_section: str, pricing: dict[str, any] = pricing) -> list[dict[str, any]]:
            try:
                section_lines = raw_section.strip().split("\n")
                section_title = section_lines[0].strip()
                file_name, total_duration = map(str.strip, section_title.split(" - Demorou "))
                data_lines = section_lines[1:]
                rows = []

                for line in data_lines:
                    match = re.search(
                        r"(\w+) - ai_model=([\w\-]+) CompletionUsage\(prompt_tokens=(\d+), completion_tokens=(\d+), total_tokens=(\d+)\) - Demorou ([\d\.]+s)",
                        line,
                    )
                    if not match:
                        continue

                    agent, ai_model, prompt_tokens, completion_tokens, total_tokens, duration = match.groups()
                    prompt_tokens_cost = int(prompt_tokens) * pricing["Pricing Input per 1M Tokens"] / pricing["1 Million Tokens"]
                    completion_tokens_cost = int(completion_tokens) * pricing["Pricing Output per 1M Tokens"] / pricing["1 Million Tokens"]
                    total_tokens_cost = prompt_tokens_cost + completion_tokens_cost

                    rows.append({
                        "File": file_name,
                        "Agent": agent,
                        "AI Model": ai_model,
                        "prompt_tokens used": int(prompt_tokens),
                        "prompt_tokens cost": prompt_tokens_cost,
                        "completion_tokens used": int(completion_tokens),
                        "completion_tokens cost": completion_tokens_cost,
                        "total_tokens used": int(total_tokens),
                        "total_tokens cost": total_tokens_cost,
                        "Duration": duration,
                        "Average Duration": "-",
                    })
                
                # Calcular totais por Agent
                for agent in set(row["Agent"] for row in rows):
                    agent_rows = [row for row in rows if row["Agent"] == agent]
                    total_prompt_tokens_used = sum(row["prompt_tokens used"] for row in agent_rows)
                    total_prompt_tokens_cost = sum(row["prompt_tokens cost"] for row in agent_rows)
                    total_completion_tokens_used = sum(row["completion_tokens used"] for row in agent_rows)
                    total_completion_tokens_cost = sum(row["completion_tokens cost"] for row in agent_rows)
                    total_tokens_used = sum(row["total_tokens used"] for row in agent_rows)
                    total_tokens_cost = sum(row["total_tokens cost"] for row in agent_rows)
                    total_duration = sum(float(row["Duration"][:-1]) for row in agent_rows) # [:-1] remove o caracter final, i.e. o 's'
                    average_duration = total_duration / len(agent_rows)
                    rows.append({
                        "File": file_name,
                        "Agent": agent,
                        "AI Model": "Total",
                        "prompt_tokens used": total_prompt_tokens_used,
                        "prompt_tokens cost": total_prompt_tokens_cost,
                        "completion_tokens used": total_completion_tokens_used,
                        "completion_tokens cost": total_completion_tokens_cost,
                        "total_tokens used": total_tokens_used,
                        "total_tokens cost": total_tokens_cost,
                        "Duration": f"{total_duration:.3f}s",
                        "Average Duration": f"{average_duration:.3f}s",
                    })

                # Calcular totais
                total_prompt_tokens_used = sum(row["prompt_tokens used"] for row in rows if row["AI Model"] != "Total")
                total_prompt_tokens_cost = sum(row["prompt_tokens cost"] for row in rows if row["AI Model"] != "Total")
                total_completion_tokens_used = sum(row["completion_tokens used"] for row in rows if row["AI Model"] != "Total")
                total_completion_tokens_cost = sum(row["completion_tokens cost"] for row in rows if row["AI Model"] != "Total")
                total_tokens_used = sum(row["total_tokens used"] for row in rows if row["AI Model"] != "Total")
                total_tokens_cost = sum(row["total_tokens cost"] for row in rows if row["AI Model"] != "Total")
                total_duration = sum(float(row["Duration"][:-1]) for row in rows if row["AI Model"] != "Total") # [:-1] remove o caracter final, i.e. o 's'
                rows.append({
                    "File": file_name,
                    "Agent": "-",
                    "AI Model": "Total",
                    "prompt_tokens used": total_prompt_tokens_used,
                    "prompt_tokens cost": total_prompt_tokens_cost,
                    "completion_tokens used": total_completion_tokens_used,
                    "completion_tokens cost": total_completion_tokens_cost,
                    "total_tokens used": total_tokens_used,
                    "total_tokens cost": total_tokens_cost,
                    "Duration": f"{total_duration:.3f}s",
                    "Average Duration": "-",
                })

                return rows
            except Exception as e:
                raise ValueError(f"Erro ao processar os dados: {e}")

        # Processar os dados
        rows = []
        sections = data.split("#####")[1:]  # Ignorar qualquer texto antes da primeira seção
        for section in sections:
            rows.extend(process_data_per_section(section))
        
        # Adicionar linha com totais de todos os ficheiros
        total_prompt_tokens_used = sum(row["prompt_tokens used"] for row in rows if row["AI Model"] != "Total")
        total_prompt_tokens_cost = sum(row["prompt_tokens cost"] for row in rows if row["AI Model"] != "Total")
        total_completion_tokens_used = sum(row["completion_tokens used"] for row in rows if row["AI Model"] != "Total")
        total_completion_tokens_cost = sum(row["completion_tokens cost"] for row in rows if row["AI Model"] != "Total")
        total_tokens_used = sum(row["total_tokens used"] for row in rows if row["AI Model"] != "Total")
        total_tokens_cost = sum(row["total_tokens cost"] for row in rows if row["AI Model"] != "Total")
        total_duration = sum(float(row["Duration"][:-1]) for row in rows if row["AI Model"] != "Total")
        rows.append({
            "File": "All Files",
            "Agent": "-",
            "AI Model": "Total",
            "prompt_tokens used": total_prompt_tokens_used,
            "prompt_tokens cost": total_prompt_tokens_cost,
            "completion_tokens used": total_completion_tokens_used,
            "completion_tokens cost": total_completion_tokens_cost,
            "total_tokens used": total_tokens_used,
            "total_tokens cost": total_tokens_cost,
            "Duration": f"{total_duration:.3f}s",
            "Average Duration": "-",
        })

        # Exportar para Excel
        try:
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with pd.ExcelWriter(output_file_path, engine="openpyxl") as writer:
                # Escrever configurações
                pd.DataFrame({
                    "Description": [key for key in pricing.keys()],
                    "Value": [value for value in pricing.values()],
                }).to_excel(writer, index=False, header=False, startrow=1, startcol=1)

                # Escrever dados principais
                pd.DataFrame(rows).to_excel(writer, index=False, startrow=len(pricing)+2, startcol=1)
        except Exception as e:
            raise IOError(f"Erro ao exportar os dados para Excel: {e}")


    @staticmethod
    def __str__() -> str:
        return f"""
#################################### AI Analytics ####################################

{str(AiAnalytics.ai_files_analytics)}
######################################################################################
"""