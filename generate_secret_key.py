#!/usr/bin/python3
import secrets
env_file_name = ".env"

def generate_key_if_not_exist():
    open(env_file_name, 'a').close()
    has_secret_key = False
    with open(env_file_name) as env_file:
        for line in env_file:
            if line.startswith("SECRET_KEY"):
                has_secret_key = True

    with open(env_file_name, "a") as env_file:
        if not has_secret_key:
            env_file.write(f"SECRET_KEY={secrets.token_hex(32)}")
