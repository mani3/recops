import pytest
from src.program import Program


def test_program():
  program = Program("tests/test.json", "2024年03月24日21時00分00秒-アニメ　テスト＃１「テスト」.m2ts")
  directory_name, output_filename = program.get_output_info()
  assert directory_name == "テスト"
  assert output_filename == "テスト　＃1_詳細_2024年03月24日21時00分00秒.mp4"
