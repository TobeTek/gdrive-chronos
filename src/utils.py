import os


def write_output_variable(name, value):
    # print(f"::set-output name={variable_name}::{variable_value}")
    with open(os.getenv("GITHUB_OUTPUT"), "a") as env:
        print(f"{name}={value}", file=env)


def set_env(name, value):
    with open(os.getenv("GITHUB_ENV"), "a") as env:
        print(f"{name}={value}", file=env)
