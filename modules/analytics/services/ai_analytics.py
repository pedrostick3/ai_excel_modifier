import logging
from datetime import timedelta
from modules.analytics.models.ai_files_analytics_model import AiFilesAnalyticsModel
from modules.analytics.models.ai_agent_analytics_model import AiAgentAnalyticsModel

class AiAnalytics:
    ai_files_analytics: AiFilesAnalyticsModel = AiFilesAnalyticsModel()

    @staticmethod
    def add_file_agent_request(
        file_name: str,
        agent_name: str,
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
            prompt_tokens (int): The number of tokens in the prompt.
            completion_tokens (int): The number of tokens in the completion.
            total_tokens (int): The total number of tokens.
            execution_time_in_seconds (float): The execution time.
            extra_info (str, optional): Extra information. Defaults to None.
        """
        agent_request = AiAgentAnalyticsModel(
            name=agent_name,
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
    def __str__() -> str:
        return f"""
#################################### AI Analytics ####################################

{str(AiAnalytics.ai_files_analytics)}
######################################################################################
"""