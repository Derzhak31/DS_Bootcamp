#!/bin/python
import os

if __name__ == "__main__":
    env_name = os.getenv("VIRTUAL_ENV")
    if env_name:
        print(f"Your current virtual env is {env_name}")
    else:
        print("Virtual environment not activated")
