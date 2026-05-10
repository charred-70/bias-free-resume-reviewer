GENDERED_LANGUAGE = {
    "aggressive": "masculine-coded",
    "dominant": "masculine-coded",
    "assertive": "masculine-coded",
    "supportive": "feminine-coded",
    "nurturing": "feminine-coded",
    "rockstar": "masculine-coded",
    "ninja": "masculine-coded",
    "guru": "masculine-coded",
    "led team": "masculine-coded",
    "competitive": "masculine-coded",
    "passionate": "feminine-coded",
    "collaborative": "feminine-coded",
}

PRESTIGE_TERMS = {
    "google": "tech prestige bias",
    "microsoft": "tech prestige bias",
    "stanford": "elite institution bias",
    "harvard": "elite institution bias",
    "ivy league": "elite institution bias",
    "amazon": "tech prestige bias",
    "meta": "tech prestige bias",
    "apple": "tech prestige bias",
    "san jose state": "institution reference",
    "university": "institution reference",
    "top university": "elite institution bias",
    "tier 1": "elite institution bias",
}

AGE_INDICATORS = [
    "10 years experience",
    "20 years experience",
    "30 years experience",
    "veteran",
    "retired",
    "seasoned",
    "digital native",
    "recent graduate",
    "graduation may",  # catches graduation dates that imply age
    "class of",
]

RACE_INDICATORS = {
    "diversity hire": "sensitive demographic reference",
    "minority": "sensitive demographic reference",
    "african american": "racial identifier",
    "latino": "racial identifier",
    "asian": "racial identifier",
    "underrepresented": "demographic reference",
}

DISABILITY_INDICATORS = {
    "wheelchair": "accessibility reference",
    "hearing impaired": "disability reference",
    "visually impaired": "disability reference",
    "autism": "neurodiversity reference",
    "disabled": "general disability reference",
}