"""
Create overlay of spelling markers
"""
from spellchecker import SpellChecker

spell = SpellChecker()


def check(line: str) -> str:
    """
    Add a 'did you mean' suggestion to each incorrect word
    """
    # find those words that may be misspelled
    misspelled = spell.unknown(spell.split_words(line))
    new_line = line
    for word in misspelled:
        correction = spell.correction(word)
        if correction != word and correction:
            replacement = f"{word} (did you mean {correction}?)"
            new_line = new_line.replace(word, replacement)
    return new_line
