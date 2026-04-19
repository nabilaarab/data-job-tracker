from abc import ABC, abstractmethod
from analysis.analyzer import Analyzer
from analysis.models import AnalyzerConfig
from dotenv import load_dotenv
from groq import Groq
import os

class Analyzer(ABC):
    def __init__(self, config: AnalyzerConfig):
        self._config = config

    @abstractmethod
    def run(self):
        """
        Launch the analyze by the strategy chose.
        """
        pass

class AnalyzerKeyWord(Analyzer):
    def run(self):
        pass

class AnalyzerLLM(Analyzer):

    # function: __init__ --------------------------------------------------------------------------------------------------
    def __init__(self, config: AnalyzerConfig):
        super().__init__(config)
        load_dotenv()
        self.__client = Groq(api_key=os.environ["GROQ_API_KEY"])
    
    # function: run --------------------------------------------------------------------------------------------------
    def run(self):
        self.__launch_one_request()
    
    # function: __launch_one_request ---------------------------------------------------------------------------------
    def __launch_one_request(self):
        extra_parameters = {}
        
        output_desired = self._config.prompt_output_desired
        if output_desired is not None:
            extra_parameters["response_format"] = output_desired

        response = self.__client.chat.completions.create(
            model=self._config.ai_model,
            messages=self.__build_messages(),
            **extra_parameters
        )

        print(response.choices[0].message.content)

    # function: __build_messages -------------------------------------------------------------------------------------
    def __build_messages(self):
        parameters_prompt = []

        for role, content in [
            ("system", self._config.prompt_system_content),
            ("user",   self._config.prompt_user_content)
        ]:
            if content is not None:
                parameters_prompt.append(
                    {
                        "role": role, 
                        "content": content
                     }
                )

        return parameters_prompt
    
    # function: update_config ----------------------------------------------------------------------------------------
    def update_config(self, analyzer_config: AnalyzerConfig):
        self._config = analyzer_config
