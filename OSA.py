alphabet = {
    "h": ("𐩠", "H"),
    "l": ("𐩡", "L"),
    "ha": ("𐩢", "Ḥ"),
    "m": ("𐩣", "M"),
    "q": ("𐩤", "Q"),
    "w": ("𐩥", "W"),
    "sh": ("𐩦", "Š"),
    "r": ("𐩧", "R"),
    "b": ("𐩨", "B"),
    "t": ("𐩩", "T"),
    "s": ("𐩪", "S"),
    "k": ("𐩫", "K"),
    "n": ("𐩬", "N"),
    "kh": ("𐩭", "Ḫ"),
    "s2": ("𐩮", "Ṣ"),
    "s3": ("𐩯", "S³"),
    "f": ("𐩰", "F"),
    "alef": ("𐩱", "ʾ"),
    "ayn": ("𐩲", "ʿ"),
    "dad": ("𐩳", "Ḍ"),
    "j": ("𐩴", "J"),
    "d": ("𐩵", "D"),
    "ghayn": ("𐩶", "Ġ"),
    "ta": ("𐩷", "Ṭ"),
    "z": ("𐩸", "Z"),
    "dh": ("𐩹", "Ḏ"),
    "y": ("𐩺", "Y"),
    "th": ("𐩻", "Ṯ"),
    "za": ("𐩼", "Ẓ"),
    "|": ("𐩽", "  "),
    "?": ("[ … ]", "[ … ]"),
    "??": ("[ … … ]", "[ … … ]"),
}

STARTR2L = "\u2069"
ENDR2L = "\u2067"


def _transcribe_line(line: str, linenum: int) -> str:
    left = []
    right = []
    characters = line.split(" ")
    for each_character in characters:
        if each_character not in ("?", "??"):
            if each_character[-1] == "?":
                left.append(f"[ {alphabet[each_character[:-1]][0]} ]")
                right.append(f"[ {alphabet[each_character[:-1]][1]} ]")
            else:
                left.append(alphabet[each_character][0])
                right.append(alphabet[each_character][1])
        else:
            left.append(alphabet[each_character][0])
            right.append(alphabet[each_character][1])
    transcription = f"{' '.join(left)}"
    transliteration = f"{' '.join(right)}"
    return f"{ENDR2L}{transcription}{STARTR2L}  {linenum}  {transliteration}"


def _ul(text: str) -> str:
    return f"\033[4m{text}\033[0m"


def transcribe(text: str = None) -> None:
    output = ["transcription     transliteration"]
    if not text:
        print("\n")
        print("-" * 45)
        print(f"\n{_ul('Char')}\t{_ul('Code')}\t\t{_ul('Char')}\t{_ul('Code')}")
        for i in range(16):
            print(
                f"{list(alphabet.items())[i][1][0]}\t{list(alphabet.items())[i][0]}\t\t{list(alphabet.items())[i+16][1][0]}\t{list(alphabet.items())[i+16][0]}"
            )
        print("\n- Using character codes above, enter each line")
        print("  of the Musnad text and press return.")
        print("- Append a question mark (?) to the character code")
        print("  to indicate that the reading is questionable.")
        print("- Separate each character code by a single space.")
        print("- Press return twice to output the transcription.\n")
        i = 1
        line = input(f"Line {i}: ").strip()
        output.append(_transcribe_line(line, i))
        while line != "":
            i += 1
            line = input(f"Line {i}: ").strip()
            if line != "":
                output.append(_transcribe_line(line, i))
    print("\nCopy the following into your word processor of choice:\n")
    longest_line = len(max(output, key=len))
    for each_formatted_line in output:
        padding = " " * round((longest_line - len(each_formatted_line)) / 2)
        print(f"{padding}{each_formatted_line}")
    print()


if __name__ == "__main__":
    transcribe()
