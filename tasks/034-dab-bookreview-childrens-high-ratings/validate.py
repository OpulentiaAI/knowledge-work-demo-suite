import re


def _normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _gt_short(s: str) -> str:
    # for the GT side only: also drop subtitle (after first ':') so abbreviated
    # agent answers still match.
    s = s.lower().split(":", 1)[0]
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def validate(llm_output: str):
    ground_truth_books = [
        "Around the World Mazes",
        "Behind the Wheel (Choose Your Own Adventure #35)(Paperback/Revised)",
        "Benny Goes To The Moon: The great new book from Top Children's entertainer Gerry Ogilvie (1)",
        "Cheer Up, Ben Franklin! (Young Historians)",
        "Favorite Thorton W. Burgess Stories: 6 Books",
        "Egypt (Enchantment of the World)",
        "Pokémon: Sun & Moon, Vol. 8 (8)",
        "The Library Book",
        "LunaLu the Llamacorn",
        "Monstrous Stories #4: The Day the Mice Stood Still",
        "The Old Man and the Pirate Princess",
        "Trouble in the CTC!: The Terra Prime Adventures Book 2",
        "Clark the Shark: Tooth Trouble, No. 1",
        "Cleo Porter and the Body Electric",
    ]
    llm_norm = _normalize(llm_output)
    for book in ground_truth_books:
        if _gt_short(book) not in llm_norm:
            return False, f"Missing book title in LLM output: {book}"
    return True, "All book titles found in LLM output."
