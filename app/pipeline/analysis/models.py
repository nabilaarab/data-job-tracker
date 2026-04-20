from dataclasses import dataclass

@dataclass
class AnalyzerConfig:
    keywords: list[str] | None
    text: str | None
    ai_model: str | None
    prompt_system_content: str | None
    prompt_user_content: str | None
    prompt_output_desired: str | None
