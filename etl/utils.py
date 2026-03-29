from etl.models import ETLConfig

def load_config(
        filepath_config: str = "input/config.txt", 
        filepath_keywords: str = "input/key_words_job_offers.txt"
    ) -> ETLConfig:
    raw = {}

    # Read the file of key words
    with open(filepath_keywords, "r", encoding="utf-8") as f:
        key_words = []
        for line in f:
            key_words.append(line.strip())
        raw["key_words"] = key_words

    # Read the file of configuration
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

    # --- locations + location_countries ---
    locations = []
    location_countries = {}
    for item in raw.get("locations", "").split(","):
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

    # --- proxies ---
    proxies = []
    if raw.get("proxies"):
        for p in raw["proxies"].split(","):
            p = p.strip()
            if p:
                proxies.append(p)

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
