import io
import sys
import unittest
from contextlib import redirect_stdout
from unittest import mock

from uztext.cli import main


def run(argv, stdin=""):
    out = io.StringIO()
    with mock.patch.object(sys, "stdin", io.StringIO(stdin)), redirect_stdout(out):
        code = main(argv)
    return code, out.getvalue()


class CliTest(unittest.TestCase):
    def test_args(self):
        self.assertEqual(run(["to-latin", "Ўзбекистон", "Республикаси"]), (0, "Oʻzbekiston Respublikasi\n"))
        self.assertEqual(run(["to-cyrillic", "O'zbekiston"]), (0, "Ўзбекистон\n"))
        self.assertEqual(run(["to-new", "Oʻzbekiston"]), (0, "Özbekiston\n"))
        self.assertEqual(run(["from-new", "Özbekiston"]), (0, "Oʻzbekiston\n"))
        self.assertEqual(run(["normalize", "O'zbekiston"]), (0, "Oʻzbekiston\n"))
        self.assertEqual(run(["search-key", "Ўзбекистон"]), (0, "özbekiston\n"))

    def test_stdin(self):
        self.assertEqual(run(["to-latin"], "Шаҳар\nҚишлоқ\n"), (0, "Shahar\nQishloq\n"))

    def test_sum_words(self):
        self.assertEqual(
            run(["sum-words", "1 250 000,50"]),
            (0, "bir million ikki yuz ellik ming soʻm ellik tiyin\n"),
        )
        self.assertEqual(run(["sum-words", "--script", "cyrillic", "7"]), (0, "етти сўм\n"))
        self.assertEqual(run(["sum-words"], "1\n\n2\n"), (0, "bir soʻm\nikki soʻm\n"))
        self.assertEqual(run(["sum-words", "--currency", "dollar", "--subunit", "sent", "1.05"]),
                         (0, "bir dollar besh sent\n"))

    def test_sum_words_error(self):
        err = io.StringIO()
        with mock.patch.object(sys, "stderr", err):
            code, _ = run(["sum-words", "abc"])
        self.assertEqual(code, 2)
        self.assertIn("not an amount", err.getvalue())


if __name__ == "__main__":
    unittest.main()
