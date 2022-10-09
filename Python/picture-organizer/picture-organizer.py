import os
import random
import shutil
import string
from colorama import Fore
from pathlib import Path

CHARACTERS = string.ascii_letters + string.digits
EXTENSIONS = [ ".jpg", ".jpeg", ".png", ".mp4", ".mov", ".heic" ]

def generate_random_string(length):
    return "".join(random.choice(CHARACTERS) for _ in range(length))

def contains_invalid_characters(string, characters):
    for character in string:
        if character in characters:
           return True
    return False

def main():

    print("Select Target Directory")
    target_directory_path = input(">>> ")
    print()

    print("Select Destination Directory")
    destination_directory_path = input(">>> ")
    print()

    os.makedirs(target_directory_path, exist_ok=True)
    os.makedirs(destination_directory_path, exist_ok=True)

    count = 0

    for _, _, file_paths in os.walk(target_directory_path):
        for file_path in file_paths:
            count += 1
            file = Path(file_path)
            extension = file.suffix.lower()
            if extension in EXTENSIONS:
                print(f"[{Fore.BLUE}#{count}{Fore.RESET}] ", end="")
                if contains_invalid_characters(file.name, CHARACTERS):
                    new_file_name = generate_random_string(16) + extension
                    print(f"{Fore.YELLOW}{file.name}{Fore.RESET} -> {Fore.GREEN}{new_file_name}{Fore.RESET}")
                    shutil.copy2(
                        os.path.join(target_directory_path, file_path),
                        os.path.join(destination_directory_path, new_file_name)
                    )
                else:
                    print(f"{Fore.GREEN}{file.name}{Fore.RESET}")
                    shutil.copy2(
                        os.path.join(target_directory_path, file_path),
                        os.path.join(destination_directory_path, file_path)
                    )

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()