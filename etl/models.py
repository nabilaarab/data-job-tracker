from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class ETLConfig:
    """
    Paramètres lus depuis config.txt 
    """
    # Parameter of extract phase
    search_term: str = ""
    site_names: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    location_countries: Dict[str, str] = field(default_factory=dict)
    radius_km: int = 0
    max_results_per_platform: int = 50
    posted_within_days: int = 30
    max_workers: int = 4
    use_proxies: bool = False
    proxies: List[str] | str | None = field(default_factory=list)
    job_type: str = "all"
