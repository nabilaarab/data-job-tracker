from dataclasses import dataclass, field
from typing import Dict, List, Self
from utils import load_key_words

@dataclass
class ETLConfig:
    """
    Paramètres lus depuis config.txt 
    """
    # Parameter of extract phase
    key_words: List[str] = field(default_factory=list)
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

    # function: load_config -------------------------------------------------------------------------------------------------------------
    @staticmethod
    def load_config(
        filepath_config: str = "etl/input/config.local.txt", 
        filepath_keywords: str = "etl/input/key_words_job_offers.txt"
    ) -> Self:
        
        # Read the file of configuration
        raw = ETLConfig.__read_config_file(filepath_config)

        # Read the file of key words
        raw["key_words"] = load_key_words(filepath_keywords)

        # Extract locations and country for each location
        locations, location_countries = ETLConfig.__extract_locations_countries_from(raw.get("locations", ""))

        # Extract proxies
        proxies = ETLConfig.__extract_proxies_from(raw.get("proxies"))

        # Create and return the object
        return ETLConfig(
            key_words=raw.get("key_words", []),
            site_names=[s.strip() for s in raw.get("site_names", "").split(",") if s.strip()],
            locations=locations,
            location_countries=location_countries,
            radius_km=int(raw.get("radius_km", 0) or 0),
            max_results_per_platform=int(raw.get("max_results_per_platform", 50)),
            posted_within_days=int(raw.get("posted_within_days", 30)),
            max_workers=int(raw.get("max_workers", 4)),
            use_proxies=raw.get("use_proxies", "false").lower() == "true",
            proxies=proxies,
            job_type=raw.get("job_type", "all"),
        )
    
    def __read_config_file(filepath_config: str) -> dict[str, str]:
        raw = {}
        with open(filepath_config, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.split("#")[0].strip()  # ignore commentaires inline
                raw[key] = value

        return raw

    # function: __extract_locations_countries_from -------------------------------------------------------------------------------------
    def __extract_locations_countries_from(raw_locations) -> tuple[list[str], dict[str, str]]:
        locations = []
        location_countries = {}
        for item in raw_locations.split(","):
            item = item.strip()
            if not item:
                continue
            if ":" in item:
                city, country = item.split(":", 1)
                city, country = city.strip(), country.strip()
                locations.append(city)
                location_countries[city] = country
            else:
                locations.append(item)

        return locations, location_countries

    # function: __extract_proxies_from -------------------------------------------------------------------------------------------------
    def __extract_proxies_from(raw_proxies) -> list[str]:
        proxies = []
        if raw_proxies:
            for p in raw_proxies.split(","):
                p = p.strip()
                if p:
                    proxies.append(p)

        return proxies
