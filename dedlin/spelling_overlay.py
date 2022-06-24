"""
Create overlay of spelling markers
"""
from spellchecker import SpellChecker


spell = SpellChecker()

def check(line:str):
    """
    Add a 'did you mean' suggestion to each incorrect word
    """
    # find those words that may be misspelled
    misspelled = spell.unknown(spell.split_words(line))
    new_line = line
    for word in misspelled:
        correction = spell.correction(word)
        if correction != word:
            replacement = f"{word} (did you mean {correction}?"
            new_line = new_line.replace(word, replacement)
    return new_line

if __name__ == '__main__':
    line = "So it goes and 'what' and then the other So! wow. rieciept and cieling."
    print(line)
    print(check(line))