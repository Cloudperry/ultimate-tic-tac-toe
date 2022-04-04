#!/usr/bin/python3
import secrets

def generate_key_if_not_exist():
    has_secret_key = False
    with open(".env") as env_file:
        for line in env_file:
            if line.startswith("SECRET_KEY"):
                has_secret_key = True

    with open(".env", "a") as env_file:
        if not has_secret_key:
            env_file.write(f"SECRET_KEY={secrets.token_hex(32)}")
