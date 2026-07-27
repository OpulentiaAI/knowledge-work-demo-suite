def validate(llm_output: str):
    """Accept either the buy-and-hold ranking or the genuine DCA ranking.

    The question asks about "regular monthly investments since 2000 …
    highest overall returns". That phrase admits two standard readings:

      * Buy-and-hold total return (last_close / first_close − 1).
      * Monthly dollar-cost-average return (sum $1/month, value at end).

    Under buy-and-hold the top-5 is {399001.SZ, NSEI, IXIC, 000001.SS, NYA};
    under real DCA it's {IXIC, NSEI, 399001.SZ, GDAXI, TWII}. Both are
    defensible interpretations of the prompt, so either set is accepted.
    For each set, each ticker must appear within 100 chars of its country
    (or an alias).
    """
    country_aliases = {
        "china": ["china", "cn"],
        "india": ["india", "in"],
        "united states": ["united states", "us", "usa", "u.s."],
        "germany": ["germany", "de", "deutschland"],
        "taiwan": ["taiwan", "tw"],
    }
    candidate_sets = [
        [("399001.SZ", "China"), ("NSEI", "India"), ("IXIC", "United States"),
         ("000001.SS", "China"), ("NYA", "United States")],
        [("IXIC", "United States"), ("NSEI", "India"), ("399001.SZ", "China"),
         ("GDAXI", "Germany"), ("TWII", "Taiwan")],
    ]

    llm_lower = llm_output.lower()
    failures = []
    for pairs in candidate_sets:
        ok = True
        reason = ""
        for name, country in pairs:
            name_lower = name.lower()
            idx = llm_lower.find(name_lower)
            if idx == -1:
                ok = False
                reason = f"Missing name: {name}"
                break
            aliases = country_aliases.get(country.lower(), [country.lower()])
            lo = max(0, idx - 100)
            hi = min(len(llm_lower), idx + len(name_lower) + 100)
            window = llm_lower[lo:hi]
            if not any(a in window for a in aliases):
                ok = False
                reason = (f"Country '{country}' not within ±100 chars "
                          f"of '{name}'")
                break
        if ok:
            return True, "All name-country pairs matched."
        failures.append(reason)
    return False, "Neither candidate ranking matched: " + " | ".join(failures)
