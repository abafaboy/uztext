"""Run every case in corpus/cases.json against the Python package.

One test method per case, so the summary line counts corpus cases.
"""

import json
import pathlib
import unittest

import uztext
from uztext import _data

CORPUS = pathlib.Path(__file__).resolve().parents[2] / "corpus" / "cases.json"
CASES = json.loads(CORPUS.read_text(encoding="utf-8"))["cases"]

TEXT_FNS = {
    "to_latin": uztext.to_latin,
    "to_cyrillic": uztext.to_cyrillic,
    "to_new": uztext.to_new,
    "from_new": uztext.from_new,
    "normalize": uztext.normalize,
    "search_key": uztext.search_key,
}


def run_case(case):
    if case["fn"] == "sum_words":
        return uztext.sum_words(case["input"], **case.get("args", {}))
    return TEXT_FNS[case["fn"]](case["input"])


class CorpusTest(unittest.TestCase):
    pass


def _make(case):
    def test(self):
        if case.get("error"):
            with self.assertRaises((ValueError, TypeError)):
                run_case(case)
        else:
            self.assertEqual(run_case(case), case["expected"], case.get("note"))

    return test


for _case in CASES:
    setattr(CorpusTest, "test_" + _case["id"].replace("-", "_"), _make(_case))


class CorpusShapeTest(unittest.TestCase):
    def test_ids_unique(self):
        ids = [c["id"] for c in CASES]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_function_covered(self):
        self.assertEqual({c["fn"] for c in CASES}, set(TEXT_FNS) | {"sum_words"})

    def test_every_exception_exercised(self):
        inputs = [str(c["input"]).lower() for c in CASES if c["fn"] in ("to_latin", "to_cyrillic")]
        stems = [s for s, _ in _data.LAT_PREFIX_EXCEPTIONS] + list(_data.LAT_EXACT_EXCEPTIONS)
        stems += [s for s, _ in _data.CYR_PREFIX_EXCEPTIONS]
        for stem in stems:
            self.assertTrue(any(stem in i for i in inputs), stem)

    def test_no_stem_is_prefix_of_another(self):
        for table in (_data.LAT_PREFIX_EXCEPTIONS, _data.CYR_PREFIX_EXCEPTIONS):
            stems = [s for s, _ in table]
            for a in stems:
                for b in stems:
                    self.assertFalse(a != b and b.startswith(a), (a, b))


class ApiTest(unittest.TestCase):
    def test_all_exports(self):
        self.assertEqual(
            sorted(uztext.__all__),
            ["from_new", "normalize", "search_key", "sum_words", "to_cyrillic", "to_latin", "to_new"],
        )

    def test_decimal_and_bool(self):
        from decimal import Decimal

        self.assertEqual(uztext.sum_words(Decimal("15.05")), "oʻn besh soʻm besh tiyin")
        with self.assertRaises(TypeError):
            uztext.sum_words(True)
        with self.assertRaises(TypeError):
            uztext.sum_words(None)

    def test_version_matches_pyproject(self):
        pyproject = (pathlib.Path(__file__).resolve().parents[1] / "pyproject.toml").read_text()
        self.assertIn(f'version = "{uztext.__version__}"', pyproject)


if __name__ == "__main__":
    unittest.main()
