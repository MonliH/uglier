import unicodedata
import re

# Used to generate the horrible characters.txt, from the confusables file
# see https://util.unicode.org/UnicodeJsps/confusables.jsp
def generate_chars():
    match = re.compile("^[a-zA-Z]*$")
    characters = ""
    with open("./uglier/confusables.txt", "r") as f:
        for line in f.readlines():
            if line[0] in "←\t":
                char = line.split("\u200e")[1][1:-1]
                normalized = unicodedata.normalize("NFKC", char)
                if re.match(match, normalized) is not None:
                    characters += char
