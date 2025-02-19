#!/bin/python
import os
import shutil

if __name__ == "__main__":
    try:
        if os.environ["VIRTUAL_ENV"][-8:] == "sharellc":
            os.system("pip install beautifulsoup4 pytest")
            os.system("pip freeze > requirements.txt")
            archive_name = "env_archive"
            env_path = "../sharellc"
            shutil.make_archive(archive_name, "zip", env_path)
            print(f"Virtual environment archived to {archive_name}.zip")
    except KeyError:
        print("ENV не sharellc")
