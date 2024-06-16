import hunspell
import string

h = hunspell.HunSpell('/usr/share/hunspell/pl_PL.dic', '/usr/share/hunspell/pl_PL.aff')


def misspell_handler(misspelled_word: str):
    suggestions = h.suggest(misspelled_word)

    for word in suggestions:
        if misspelled_word == word:
            return word

    if not suggestions:
        print(f"Word '{misspelled_word}' not found in the dictionary.")
        return misspelled_word

    return suggestions[0]


def strip_punctuation(text: str) -> str:
    return ''.join([char for char in text if char not in string.punctuation + "\n"])


def spell_check(original_text: str) -> (list[str], list[tuple[str, str]]):
    fixed_text = []
    mistakes = []
    original_text = strip_punctuation(original_text).split()

    for word in original_text:
        if h.spell(word):
            fixed_text.append(word)
        else:
            corrected = misspell_handler(word)
            fixed_text.append(corrected)
            mistakes.append((word, corrected))

    return (fixed_text, mistakes)

