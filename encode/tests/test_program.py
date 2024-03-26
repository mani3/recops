import json
import os

import pytest
from src.program import Program

DUMMY_JSON_FILE = "test_program_data.json"


@pytest.fixture
def setup_dummy_json():
  dummy_data = [
    {
      "id": "BS_101",
      "programs": [
        {
          "channel": "BS_101",
          "title": "アニメ",
          "detail": "詳細",
          "start": 1707056400000,
          "end": 1707059400000,
          "duration": 3000,
        }
      ],
    },
    {
      "id": "BS_103",
      "programs": [
        {
          "channel": "BS_103",
          "title": "テスト　＃1",
          "detail": "詳細",
          "start": 1711281600000,
          "end": 1711281600000,
          "duration": 9000,
        }
      ],
    },
  ]
  with open(DUMMY_JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(dummy_data, f, ensure_ascii=False, indent=4)

  yield

  os.remove(DUMMY_JSON_FILE)


def test_program(setup_dummy_json):
  filename = "2024年03月24日21時00分00秒-アニメ　テスト＃１「テスト」.m2ts"
  program = Program(DUMMY_JSON_FILE, filename)
  directory_name, output_filename = program.get_output_info()

  assert directory_name == "テスト"
  assert output_filename == "テスト　＃1_詳細_2024年03月24日21時00分00秒.mp4"
  assert output_filename == "テスト　＃1_詳細_2024年03月24日21時00分00秒.mp4"
  assert output_filename == "テスト　＃1_詳細_2024年03月24日21時00分00秒.mp4"
