LLM_MODEL = "llama-3.1-8b-instant"

LLM_PROMPT_SYSTEM = \
    """Tu es un expert en recrutement. Tu vas recevoir les mots-clés d'un CV et une fiche de poste.
    Évalue les chances de ce CV en donnant un score de pertinence allant de 0 à 100.
    Réponds UNIQUEMENT avec ce JSON, sans texte avant ni après : {\"score\": <entier 0-100>}"""


LLM_PROMPT_USER = \
    """Voici le CV : {resume}
    Voici la fiche de poste : {job_description}"""

LLM_PROMPT_OUTPUT = {
    "type": "json_object"
}
