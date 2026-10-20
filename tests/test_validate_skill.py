import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skill import check_frontmatter  # noqa: E402

GOOD = '---\nname: kiss\ndescription: "Short and valid."\nmetadata:\n  version: "1.0.0"\n---\n\nBody.\n'


class FrontmatterTests(unittest.TestCase):
    def test_good(self):
        self.assertEqual(check_frontmatter(GOOD), [])

    def test_long_description_ok_if_first_sentence_is_short(self):
        self.assertEqual(check_frontmatter(GOOD.replace("Short and valid.", "Short. " + "More words here. " * 19 + "End.")), [])

    def test_bad_cases(self):
        bad = {
            "unknown field": GOOD.replace("metadata:", "version: 1\nmetadata:"),
            "name mismatch": GOOD.replace("name: kiss", "name: other"),
            "uppercase name": GOOD.replace("name: kiss", "name: Kiss"),
            "long description": GOOD.replace("Short and valid.", "x" * 61 + "."),
            "unquoted colon": GOOD.replace('"Short and valid."', "KISS: oops."),
            "bare number in metadata": GOOD.replace('"1.0.0"', "1.0"),
            "no frontmatter": "# just a heading\n",
            "empty body": "---\nname: kiss\ndescription: A.\n---\n",
        }
        for label, text in bad.items():
            with self.subTest(label):
                self.assertTrue(check_frontmatter(text), label)


if __name__ == "__main__":
    unittest.main()
