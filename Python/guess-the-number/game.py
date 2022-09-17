import os
import time
import random

from colorama import Fore # pip install colorama

MINIMUM_VALUE = 1
MAXIMUM_VALUE = 100

def clear():
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)

def check_int(input):
    try:
        int(input)
        return True
    except ValueError:
        return False

def main():

    value = random.randint(MINIMUM_VALUE, MAXIMUM_VALUE)
    tried_values = []

    while True:

        time.sleep(1)
        clear()

        print(f"Guess The Number! Tries: {len(tried_values)}")
        print()

        if len(tried_values) > 0:

            print("Tried Values:", end="")
            for tried_value in tried_values:
                value_difference = abs(value - tried_value)
                color = Fore.GREEN
                if value_difference > 25:
                    color = Fore.YELLOW
                if value_difference > 50:
                    color = Fore.RED
                print(f" {color}{tried_value}", end="")
            print(Fore.RESET)
            print()

        guess_value_string = input(">>> ")
        print()

        if not check_int(guess_value_string):
            print("Invalid Input!")
            continue
        guess_value = int(guess_value_string)
        tried_values.append(guess_value)
        if guess_value == value:
            print("You guessed it!")
            value = random.randint(MINIMUM_VALUE, MAXIMUM_VALUE)
            tried_values = []
        elif guess_value < value:
            print("Go higher!")
        elif guess_value > value:
            print("Go lower!")
        else:
            print("I don't know...")

main()