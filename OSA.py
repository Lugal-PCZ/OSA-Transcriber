from math import ceil
from textwrap import dedent

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


def _generate_svg(lines: list) -> str:
    longest_line = 30
    for eachline in lines[1:]:
        linelength = ceil(len(str(eachline)) * 1.2) - 8
        if linelength > longest_line:
            longest_line = linelength
    width = (longest_line * 6) + 60
    height = 18 + ((len(lines) - 1) * 24)
    if longest_line == 30:
        centerline = 115.5
    else:
        centerline = width / 2
    leftx = centerline - 25
    rightx = centerline + 25
    svg = dedent(
        f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
        <style>
            text {{font-family: "Times New Roman", serif; font-size: 12pt; white-space: pre; fill: white}}
            .left {{text-anchor: end}}
            .right {{text-anchor: start}}
            .header {{font-style: italic}}
            .linenumber {{font-style: italic; text-anchor: middle}}
            .transcription {{font-family: sans-serif}}
            .bracket {{font-size: 16pt; font-weight: 100}}
        </style>
        <text class="header left" x="{leftx}" y="12">transcription</text><text class="header right" x="{rightx}" y="12">transliteration</text>
        """
    )
    i = 1
    for eachline in lines[1:]:
        y = (i * 24) + 12
        cleanedleft = (
            eachline[0]
            .replace("[", '<tspan class="bracket">[</tspan>')
            .replace("]", '<tspan class="bracket">]</tspan>')
        )
        cleanedright = (
            eachline[1]
            .replace("[", '<tspan class="bracket">[</tspan>')
            .replace("]", '<tspan class="bracket">]</tspan>')
        )
        svg += f'<text class="transcription left" x="{leftx}" y="{y}">{cleanedleft}</text><text class="linenumber" x="{centerline}" y="{y}">{i}</text><text class="transliteration right" x="{rightx}" y="{y}">{cleanedright}</text>\n'
        i += 1
    svg += "</svg>"
    return svg


def _transcribe_line(line: str) -> tuple:
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
    return (transcription, transliteration)


def _ul(text: str) -> str:
    return f"\033[4m{text}\033[0m"


def transcribe(text: str = None) -> None:
    lines = [("transcription", "transliteration")]
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
        print("  to indicate that that character’s reading is unsure.")
        print("- Separate each character code by a single space.")
        print("- Press return twice to output the transcription.\n")
        i = 1
        line = input(f"Line {i}: ").strip()
        lines.append(_transcribe_line(line))
        while line != "":
            i += 1
            line = input(f"Line {i}: ").strip()
            if line != "":
                lines.append(_transcribe_line(line))
    # print("\nCopy the following into your word processor of choice:\n")
    print(_generate_svg(lines))


if __name__ == "__main__":
    transcribe()

# TODO: save svg file
# TODO: catch when nothing is entered for line 1
# TODO: catch when bad characters are entered
