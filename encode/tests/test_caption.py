import pytest
from src.caption import Caption

DUMMY_M2TS_FILE = "test_data/test_video.m2ts"
OUTPUT_DIR = "test_output"


def mock_subprocess_run(*args, **kwargs):
  pass


@pytest.fixture
def monkeypatch_subprocess_run(monkeypatch):
  monkeypatch.setattr("subprocess.run", mock_subprocess_run)


def test_extract_ass(monkeypatch_subprocess_run):
  caption = Caption(DUMMY_M2TS_FILE, OUTPUT_DIR)
  output_file = caption.extract_ass()

  expected_output_file = f"{OUTPUT_DIR}/test_video.ass"
  assert output_file == expected_output_file, "Not Found caption file"
