import datetime
import json
import re


class Program:
  def __init__(self, json_file, raw_filename):
    self.json_file = json_file
    self.raw_filename = raw_filename
    self.title = ""
    self.detail = ""
    self.date = ""
    self.start_time = None
    self.start_epoch = 0  # milliseconds
    self.directory_name = ""
    self.output_filename = ""
    self.channel = None
    self.extract_info()

  def extract_info(self):
    match = re.search(r"(\d{4}年\d{2}月\d{2}日\d{2}時\d{2}分\d{2}秒)-(.+).m2ts", self.raw_filename)
    if match:
      self.date, self.title = match.groups()
      self.start_time = datetime.datetime.strptime(self.date, "%Y年%m月%d日%H時%M分%S秒")
      self.start_epoch = int(self.start_time.timestamp() * 1000)
      self.directory_name = self.extract_directory_name(self.title)
    else:
      raise ValueError(f"Invalid filename: {self.raw_filename}")

    with open(self.json_file, "r") as file:
      data = json.load(file)

    for program in data:
      programs = program["programs"]
      for program in programs:
        if program["start"] == self.start_epoch and self.directory_name in program["title"]:
          self.channel = program["channel"]
          self.title = program["title"]
          self.detail = program["detail"]
          break

    if self.title and self.date:
      self.output_filename = f"{self.title}_{self.date}.mp4"
    else:
      raise ValueError(f"Program not found: {self.raw_filename}")

  def extract_directory_name(self, title):
    name = title.replace("アニメ", "", 1).strip()
    name = re.sub(r"\[(.{1,2})\]", "", name).strip()
    name = name.split("「")[0].strip()
    name = name.split("第")[0].strip()
    name = name.split("#")[0].strip()
    name = name.split("♯")[0].strip()
    name = name.split("＃")[0].strip()
    name = name.split("　")[0].strip()
    return name

  def get_output_info(self):
    return self.directory_name, self.output_filename
