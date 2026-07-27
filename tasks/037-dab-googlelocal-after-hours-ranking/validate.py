import re

ground_truth = [
    (
        "TACOS LA CABANA",
        [
            ['Thursday', 'Closed'],
            ['Friday', '5–11PM'],
            ['Saturday', '5–11PM'],
            ['Sunday', '5–11PM'],
            ['Monday', '5–11PM'],
            ['Tuesday', 'Closed'],
            ['Wednesday', 'Closed']
        ],
        5.0
    ),
    (
        "White Barn Candle Co",
        [
            ['Thursday', '10AM–9PM'],
            ['Friday', '10AM–9PM'],
            ['Saturday', '10AM–9PM'],
            ['Sunday', '11AM–7PM'],
            ['Monday', '10AM–9PM'],
            ['Tuesday', '10AM–9PM'],
            ['Wednesday', '10AM–9PM']
        ],
        5.0
    ),
    (
        "Mariscos el poblano",
        [
            ['Thursday', 'Open 24 hours'],
            ['Friday', '8AM–3:30PM'],
            ['Saturday', '8AM–3:30PM'],
            ['Sunday', '8AM–3:30PM'],
            ['Monday', '9AM–3:30AM'],
            ['Tuesday', '8AM–3:30PM'],
            ['Wednesday', '8AM–3:30PM']
        ],
        5.0
    ),
    (
        "Beauty Divine Artistry",
        [
            ['Thursday', '9AM–8PM'],
            ['Friday', '9AM–8PM'],
            ['Saturday', '10AM–7PM'],
            ['Sunday', '11AM–6PM'],
            ['Monday', '9AM–8PM'],
            ['Tuesday', '9AM–8PM'],
            ['Wednesday', '9AM–8PM']
        ],
        5.0
    ),
    (
        "Taba Rug Gallery",
        [
            ['Thursday', '10AM–7PM'],
            ['Friday', '10AM–7PM'],
            ['Saturday', '10AM–7PM'],
            ['Sunday', '11AM–6PM'],
            ['Monday', '10AM–7PM'],
            ['Tuesday', '10AM–7PM'],
            ['Wednesday', '10AM–7PM']
        ],
        5.0
    )
]


_DAY_ORDER = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
_DAY_RANGE_RE = re.compile(
    r'\b(mon|tue|wed|thu|fri|sat|sun)-(mon|tue|wed|thu|fri|sat|sun)\b', re.I
)


def _abbr_covered_by_range(abbr, norm_window):
    """Corner case: 'Tue-Thu' implies 'wed' even though 'wed' isn't written out."""
    if abbr not in _DAY_ORDER:
        return False
    target = _DAY_ORDER.index(abbr)
    for m in _DAY_RANGE_RE.finditer(norm_window):
        start = _DAY_ORDER.index(m.group(1).lower())
        end = _DAY_ORDER.index(m.group(2).lower())
        if start <= end:
            covered = start <= target <= end
        else:  # wrap-around: e.g. Sun-Tue covers Sun(6), Mon(0), Tue(1)
            covered = target >= start or target <= end
        if covered:
            return True
    return False


def _norm(s):
    """Normalize time tokens so surface-form variants match:
      - 24-hour variants ("Open 24 hours" / "24/7" / "24 hrs") → "24h"
      - en-dash / em-dash / hyphen all collapse to "-"
      - spaces inside a "5 - 11 PM" style range collapse
      - "11 PM" → "11PM"
    """
    s = re.sub(r"\b(?:open\s+)?24\s*(?:/\s*7|hours?|hrs?|h)\b", "24h", s, flags=re.I)
    s = s.replace("–", "-").replace("—", "-")
    s = re.sub(r"\s*-\s*", "-", s)
    s = re.sub(r"\s+(am|pm|AM|PM)\b", r"\1", s)
    s = re.sub(r"\s+", " ", s)
    return s


def validate(llm_output: str):
    """Validate LLM output for query3:
    - Business names must appear
    - All hours (day + hours) must appear in a 500-char window after the name
      (after surface-form normalization — en-dash/space variants accepted)
    - The business's score must appear somewhere in that window
    """
    llm_lower = llm_output.lower()

    for name, hours_list, score in ground_truth:
        name_lower = name.lower()
        idx = llm_lower.find(name_lower)
        if idx == -1:
            return False, f"Missing business name: {name}"

        window = llm_output[idx:idx+500].lower()
        norm_window = _norm(window)

        for day, hours in hours_list:
            day_l = day.lower()
            abbr = day_l[:3]
            hours_l = _norm(hours.lower())
            day_present = (day_l in norm_window) or (abbr in norm_window) or _abbr_covered_by_range(abbr, norm_window)
            if not (day_present and hours_l in norm_window):
                return False, f"Missing hours [{day}, {hours}] for business: {name}"

        matches = re.findall(r"(\d+(?:\.\d+)?)", window)
        if not matches:
            return False, f"No score found after hours info for business: {name}"

        gt_score_rounded = round(score, 2)
        found = False
        for m in matches:
            try:
                if round(float(m), 2) == gt_score_rounded:
                    found = True
                    break
            except Exception:
                continue
        if not found:
            return False, f"Score mismatch for business: {name}, expected ~{gt_score_rounded:.2f}"

    return True, "All businesses validated successfully."
