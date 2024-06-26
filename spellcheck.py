import hunspell
import string
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import re

# Initialize the Hunspell object with Polish dictionaries
h = hunspell.HunSpell('/usr/share/hunspell/pl_PL.dic', '/usr/share/hunspell/pl_PL.aff')

def misspell_handler(misspelled_word: str):
    suggestions = h.suggest(misspelled_word)

    for word in suggestions:
        if misspelled_word == word:
            return word

    if not suggestions:
        print(f"Word '{misspelled_word}' not found in the dictionary.")
        return misspelled_word

    return suggestions

def strip_punctuation(text: str) -> str:
    # Define regex pattern to match and remove unwanted characters
    pattern = r'[^\w\s]'  # Match any character that is not a word character or whitespace

    # Substitute non-word characters with an empty string
    stripped_text = re.sub(pattern, ' ', text)

    # Also remove newlines and digits
    stripped_text = re.sub(r'[\n\d]', ' ', stripped_text)

    return stripped_text

def split_text_into_words(text: str) -> list:
    # Split text into words considering various delimiters
    return re.findall(r'\b\w+\b', text)

def spell_check(original_text: str) -> (str, list[tuple[str, str]]):
    fixed_text = []
    mistakes = []

    # Clean up the text before processing
    cleaned_text = strip_punctuation(original_text)

    # Split the cleaned text into words
    words = split_text_into_words(cleaned_text)

    for word in words:
        try:
            lang = detect(word)
        except LangDetectException:
            lang = 'unknown'

        print(f"Detected language: {lang}, word: {word}")

        if h.spell(word):
            fixed_text.append(word)
        else:
            corrected = misspell_handler(word)
            fixed_text.append(corrected[0])
            mistakes.append((word, corrected))
        #if lang == 'pl':  # Only check Polish words
              # Append non-Polish words as they are
        # else:
        #    fixed_text.append(word)

    # Join the list of words back into a single string
    corrected_text = ' '.join(fixed_text)

    print(mistakes)
    return corrected_text, mistakes
