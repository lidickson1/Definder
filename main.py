import requests
import shutil
import sys
from bs4 import BeautifulSoup

with open("words.txt", "r") as file:
    for word in file.readlines():
        word = word.rstrip('\n')
        soup = BeautifulSoup(
            requests.get(f"https://www.lexico.com/definition/{word}").content,
            'html.parser')
        parts_of_speech = soup.find_all("section", class_="gramb")
        if parts_of_speech:
            print(word.capitalize().center(shutil.get_terminal_size().columns, '-'))
            for pos in parts_of_speech:
                print(pos.find("span", class_="pos").getText().upper())

                for index, definition in enumerate(
                        pos.find("ul", class_="semb").find_all("li", recursive=False)):
                    print(f"{index + 1}. {definition.find('span', class_='ind').getText()}")

                    example = definition.find("div", class_="ex")
                    if example is not None:
                        print(example.find("em").getText())

                    sub_definitions = definition.find("ol")
                    if sub_definitions is not None:
                        for sub_index, sub_def in enumerate(
                                sub_definitions.find_all("li", recursive=False)):
                            print(
                                f"{index + 1}.{sub_index + 1}. {sub_def.find('span', class_='ind').getText()}")

                            example = sub_def.find("div", class_="ex")
                            if example is not None:
                                print(example.find("em").getText())
        else:
            sys.stderr.write(f"{word.capitalize()} not found. Maybe check the spelling and try again.")
