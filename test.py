import unittest
from spellcheck import spell_check, strip_punctuation


from Levenshtein import distance as levenshtein_distance

def calculate_similarity(text1: str, text2: str) -> float:
    levenshtein_dist = levenshtein_distance(text1, text2)
    max_len = max(len(text1), len(text2))
    similarity = 1 - levenshtein_dist / max_len if max_len > 0 else 0
    return similarity



class MyTestCase(unittest.TestCase):
    def test_spell_check_and_similarity(self):
        with open('correct_text.txt', 'r', encoding='utf-8') as file:
            correct_text = file.read()

        with open('incorrect_text.txt', 'r', encoding='utf-8') as file:
            incorrect_text = file.read()

        correct_text = strip_punctuation(correct_text)

        fixed_text, _ = spell_check(incorrect_text)
        corrected_text = ' '.join(fixed_text)

        print(f"\nCorrect text: {correct_text}")
        print(f"\nCorrected text: {corrected_text}")

        similarity = calculate_similarity(correct_text, corrected_text)
        print(f"Similarity: {similarity * 100:.2f}%")

        self.assertGreaterEqual(similarity * 100, 80)


if __name__ == '__main__':
    unittest.main()
