import os
from analysis.analyzer import Analyzer
from groq import Groq

class AnalyzerLLM(Analyzer):

    # function: __init__ --------------------------------------------------------------------------------------------------
    def __init__(self):
        self.__client = Groq(api_key=os.environ["GROQ_API_KEY"])
        self.__MODEL = "llama-3.1-8b-instant"
        self.__PROMPT_SYSTEM = (
            "Tu es un expert en recrutement. Tu vas recevoir les mots-clés d'un CV et une fiche de poste. "
            "Évalue les chances de ce CV en donnant un score de pertinence allant de 0 à 100. "
            "Réponds UNIQUEMENT avec ce JSON, sans texte avant ni après : {\"score\": <entier 0-100>}"
        )
        self.__PROMPT_USER: str = (
            "Voici le CV : {resume}" \
            "Voici la fiche de poste : {job_description}"
        )

    # function: run --------------------------------------------------------------------------------------------------
    def run(self):
        pass
    
    # function: __launch_one_request ---------------------------------------------------------------------------------
    def __launch_one_request(self, messages):
        response = self.__client.chat.completions.create(
            model=self.__MODEL,
            messages=messages,
            response_format={"type": "json_object"}
        )

        print(response.choices[0].message.content)

    # function: __build_messages -------------------------------------------------------------------------------------
    def __build_messages(self, resume, job_description):
        return [
            {
                "role": "system",
                "content": self.__PROMPT_SYSTEM
            },
            {
                "role": "user",
                "content": self.__PROMPT_USER.format(
                    resume=resume, 
                    job_description=job_description
                )
            }
        ]
    