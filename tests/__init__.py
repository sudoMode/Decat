from pathlib import Path
from decat import decat
from decat.core import DecatResponse, bulk_decat
from decat.core.parallel import parallelize
from decat.parsers import load_inputs, parse_user_args
import json
from unittest import TestCase, main

BASE_DIR = Path(__file__).resolve().parent
EXTRACTOR_INPUT = BASE_DIR / "extractor_input.json"
PASSAGE_INPUT = BASE_DIR / "passage_input.json"
INPUT_PAYLOAD = BASE_DIR / "input_payload.json"


class DecatTester(TestCase):
    @classmethod
    def setUpClass(cls):
        with open(EXTRACTOR_INPUT, "r") as f:
            cls.extractor_input = json.loads(f.read())

        with open(PASSAGE_INPUT, "r") as f:
            cls.passage_input = json.loads(f.read())

        with open(INPUT_PAYLOAD, "r") as f:
            cls.input_payload = json.loads(f.read())

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_decat(self):
        for key, value in self.extractor_input.items():
            out = decat(key)
            self.assertEqual(out, value)

    def test_passage_decat(self):
        for passage in self.passage_input:
            out = decat(passage["input"])
            self.assertEqual(out, passage["output"])

    def test_presevervation_of_special_characters(self):
        input_ = {
            "stringwithoutspace,andwithacomma": [
                "string",
                "without",
                "space,",
                "and",
                "with",
                "a",
                "comma",
            ]
        }
        for key, value in input_.items():
            out = decat(key, preserve_special_characters=True)
            self.assertEqual(out, value)

    def test_bulk_decat_via_public_function(self):
        strings = list(self.extractor_input.keys())
        out = decat(strings)
        self.assertIsInstance(out, dict)
        self.assertEqual(set(out.keys()), set(strings))
        for key, value in self.extractor_input.items():
            self.assertIn("results", out[key])
            self.assertIn("confidence", out[key])
            self.assertIn("elapsed", out[key])
            self.assertEqual(out[key]["results"], value)
            self.assertGreaterEqual(out[key]["confidence"], 0)
            self.assertLessEqual(out[key]["confidence"], 1)

    def test_bulk_decat_matches_single_string_results(self):
        strings = self.input_payload
        out = decat(strings, threads=2)
        for string in strings:
            self.assertEqual(out[string]["results"], decat(string))

    def test_bulk_decat_using_process_executor(self):
        strings = self.input_payload
        out = decat(strings, threads=2, executor="process")
        for string in strings:
            self.assertEqual(out[string]["results"], decat(string))

    def test_bulk_decat_direct_import(self):
        strings = self.input_payload
        out = bulk_decat(strings, workers=2)
        for string in strings:
            self.assertEqual(out[string]["results"], decat(string))

    def test_decat_response_to_dict_is_extensible(self):
        response = DecatResponse(
            results=["a"], confidence=1.0, elapsed=0.1, extra={"custom_metric": 42}
        )
        payload = response.to_dict()
        self.assertEqual(payload["results"], ["a"])
        self.assertEqual(payload["custom_metric"], 42)

    def test_parallelize_decorator_is_generic(self):
        @parallelize()
        def square(number):
            return number * number

        # direct/single-item invocation keeps working unmodified
        self.assertEqual(square(4), 16)

        # bulk invocation, fanned out concurrently
        out = square.parallel([1, 2, 3], workers=2)
        self.assertEqual(out, {1: 1, 2: 4, 3: 9})

    def test_cli_loads_multiple_raw_inputs(self):
        args = parse_user_args(["-i", "somerandomtext", "somebettertext"])
        inputs = load_inputs(args)
        self.assertEqual(inputs, ["somerandomtext", "somebettertext"])

    def test_cli_loads_single_raw_input_preserves_old_behaviour(self):
        args = parse_user_args(["-i", "somerandomtext"])
        inputs = load_inputs(args)
        self.assertEqual(inputs, "somerandomtext")

    def test_cli_loads_inputs_from_json_file(self):
        args = parse_user_args(["-i", str(INPUT_PAYLOAD), "-f", "json", "-t", "4"])
        inputs = load_inputs(args)
        self.assertEqual(inputs, self.input_payload)
        self.assertEqual(args.threads, 4)


if __name__ == "__main__":
    main()
