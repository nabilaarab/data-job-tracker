from dataclasses import dataclass

@dataclass
class AnalyzerConfig:
    keywords: list[str]
    ai_model: str
    prompt_system_content: str | None
    prompt_user_content: str | None
    prompt_output_desired: str | None
