
def calculate_keyword_density(text: str, target_word: str) -> dict:
    if not text or not target_word:
        return {"density": 0.0, "count": 0}
    words = text.lower().split()
    count = words.count(target_word.lower())
    density = count / len(words) if len(words) > 0 else 0.0
    return {
        "density": density,
        "count": count,
        "total_words": len(words)
    }
