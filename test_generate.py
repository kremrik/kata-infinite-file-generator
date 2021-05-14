from generate import inf_csv, inf_json_lines, inf_text

import io
import unittest
from typing import IO, List


class test_csv(unittest.TestCase):

    data = [
        "foo,bar,baz\n",
        "1,2,3\n",
        "4,5,6\n",
        "7,8,9\n"
    ]
    
    def test_with_header(self):
        handler = mock_handler(self.data)
        gold = [
            list("123"),
            list("456"),
            list("789"),
            list("123")
        ]
        data = inf_csv(handler, header=True)
        output = [next(data) for _ in range(4)]
        self.assertEqual(gold, output)

    def test_without_header(self):
        handler = mock_handler(self.data)
        gold = [
            "foo,bar,baz".split(","),
            list("123"),
            list("456"),
            list("789"),
            "foo,bar,baz".split(","),
            list("123")
        ]
        data = inf_csv(handler, header=False)
        output = [next(data) for _ in range(6)]
        self.assertEqual(gold, output)


class test_json(unittest.TestCase):

    data = [
        '{"foo": 1, "bar": 2, "baz": 3}\n',
        '{"foo": 4, "bar": 5, "baz": 6}\n',
        '{"foo": 7, "bar": 8, "baz": 9}\n'
    ]

    def test(self):
        handler = mock_handler(self.data)
        gold = [
            {"foo": 1, "bar": 2, "baz": 3},
            {"foo": 4, "bar": 5, "baz": 6},
            {"foo": 7, "bar": 8, "baz": 9},
            {"foo": 1, "bar": 2, "baz": 3},
        ]
        data = inf_json_lines(handler)
        output = [next(data) for _ in range(4)]
        self.assertEqual(gold, output)


class test_text(unittest.TestCase):

    data = [
        "hello world\n",
        "foo bar baz\n",
        "goodbye\n"
    ]

    def test(self):
        handler = mock_handler(self.data)
        gold = [
            "hello world",
            "foo bar baz",
            "goodbye",
            "hello world"
        ]
        data = inf_text(handler)
        output = [next(data) for _ in range(4)]
        self.assertEqual(gold, output)


def mock_handler(lines: List[str]) -> IO:
    output = io.BytesIO()
    wrapper = io.TextIOWrapper(
        output, encoding="utf-8", line_buffering=True
    )
    for line in lines:
        wrapper.write(line)
    wrapper.seek(0, 0)
    return wrapper


if __name__ == "__main__":
    unittest.main()
