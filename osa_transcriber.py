import tkinter
from tkinter import messagebox, PhotoImage, filedialog, scrolledtext
from math import ceil
from textwrap import dedent
from tkinter import scrolledtext


def _generate_svg(lines: list) -> str:
    longest_line = 30
    for eachline in lines[1:]:
        linelength = len(str(eachline)) - 8
        if linelength > longest_line:
            longest_line = linelength
    width = (longest_line * 6) + 60
    height = 18 + ((len(lines)) * 24)
    if longest_line == 30:
        centerline = 115.5
    else:
        centerline = round(
            width / 2.1
        )  # centerline isn’t 1/2 because the transliterations are generally slightly wider than the transcriptions
    leftx = centerline - 25
    rightx = centerline + 25
    svg = dedent(
        f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
        <style>
            text {{font-family: "Times New Roman", serif; font-size: 12pt; white-space: pre; text-anchor: start; fill: black}}
            .header {{font-style: italic}}
            .left {{text-anchor: end}}
            .transcription {{font-family: sans-serif; direction: rtl; unicode-bidi: bidi-override}}
            .linenumber {{font-style: italic; text-anchor: middle}}
            .bracket {{font-family: "Times New Roman", serif; font-size: 16pt; font-weight: 100}}
            .ltr {{text-anchor: end}}
        </style>
        <text class="header left" x="{leftx}" y="12">transcription</text><text class="header" x="{rightx}" y="12">transliteration</text>
        """
    )
    i = 0
    badcodes = []
    for eachline in lines:
        i += 1
        if "⚠️" in eachline[0]:
            badcodes.append(str(i))
        y = (i * 24) + 12
        cleanedtranscription = (
            eachline[0]
            .replace("[", '<tspan class="bracket">[</tspan>')
            .replace("]", '<tspan class="bracket">]</tspan>')
        )
        cleanedtranliteration = (
            eachline[1]
            .replace("[", '<tspan class="bracket">[</tspan>')
            .replace("]", '<tspan class="bracket">]</tspan>')
        )
        if eachline[2]:
            svg += f'<text class="transcription ltr" x="{-1 * leftx}" y="{y}" transform="scale(-1,1)">{cleanedtranscription}</text><text class="linenumber" x="{centerline}" y="{y}">{i}</text><text class="transliteration" x="{rightx}" y="{y}">{cleanedtranliteration}</text>\n'
        else:
            svg += f'<text class="transcription" x="{leftx}" y="{y}">{cleanedtranscription}</text><text class="linenumber" x="{centerline}" y="{y}">{i}</text><text class="transliteration" x="{rightx}" y="{y}">{cleanedtranliteration}</text>\n'
    svg += "</svg>"
    if badcodes:
        if len(badcodes) == 1:
            message = f"Invalid code(s) in line {badcodes[0]}."
        elif len(badcodes) == 2:
            message = f"Invalid codes in lines {' and '.join(badcodes)}."
        elif len(badcodes) > 2:
            message = f"Invalid codes in lines {', '.join(badcodes[:-1])}, and {badcodes[-1]}."
        if not messagebox.askyesno(
            "Invalid Codes",
            f"{message} Do you still wish to save the SVG file?",
            icon="warning",
            parent=window,
        ):
            return
    return svg


def _transcribe_line(line: str) -> tuple:
    alphabet = {
        "h": ("𐩠", "H"),
        "l": ("𐩡", "L"),
        "ha": ("𐩢", "Ḥ"),  # hh
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
        "ss": ("𐩮", "Ṣ"),
        "s3": ("𐩯", "S³"),
        "f": ("𐩰", "F"),
        "a": ("𐩱", "ʾ"),
        "3": ("𐩲", "ʿ"),
        "dd": ("𐩳", "Ḍ"),
        "j": ("𐩴", "J"),
        "d": ("𐩵", "D"),
        "gh": ("𐩶", "Ġ"),
        "tt": ("𐩷", "Ṭ"),
        "z": ("𐩸", "Z"),
        "dh": ("𐩹", "Ḏ"),
        "y": ("𐩺", "Y"),
        "th": ("𐩻", "Ṯ"),
        "zz": ("𐩼", "Ẓ"),
        "|": ("𐩽", "  "),
        "_": ("   ", "   "),
        "?": ("[ … ]", "[ … ]"),
        "??": ("[ … … ]", "[ … … ]"),
    }
    left = []
    right = []
    ltr = False
    if not line:
        left.append("")
        right.append("")
    else:
        if line[0] == ">":
            ltr = True
            line = line[1:].strip()
        characters = line.lower().split()
        for each_character in characters:
            if "?" not in each_character:
                try:
                    left.append(alphabet[each_character][0])
                    right.append(alphabet[each_character][1])
                except KeyError:
                    left.append("⚠️")
                    right.append("⚠️")
            else:
                try:
                    left.append(f"[ {alphabet[each_character[:-1]][0]} ]")
                    right.append(f"[ {alphabet[each_character[:-1]][1]} ]")
                except KeyError:
                    left.append(f"[ ⚠️ ]")
                    right.append(f"[ ⚠️ ]")
    transcription = f"{' '.join(left)}"
    transliteration = f"{' '.join(right)}"
    return (transcription, transliteration, ltr)


def transcribe() -> None:
    text = code.get("1.0", tkinter.END).strip()
    if len(text) > 0:
        lines = []
        for each_line in text.split("\n"):
            lines.append(_transcribe_line(each_line.strip()))
        svg = _generate_svg(lines)
        if svg:
            svg_file = tkinter.filedialog.asksaveasfile(
                mode="w",
                defaultextension="svg",
                filetypes=(("SVG Files", "*.svg"),),
                title="Save Transcription",
            )
            svg_file.write(svg)
            svg_file.close()
    else:
        messagebox.showwarning("No Code", "No code was entered.", parent=window)
    return


if __name__ == "__main__":
    window = tkinter.Tk()
    window.title("OSA Transcriber")
    window.geometry("700x580")
    window.minsize(width=700, height=580)
    table_image = PhotoImage(file="Table.png")
    character_table = tkinter.Label(window, image=table_image)
    character_table.grid(row=0, column=0, padx=(20, 15), pady=(15, 0), sticky="ne")
    code_frame = tkinter.LabelFrame(window, text="Enter Codes")
    code_frame.grid(row=0, column=1, padx=(15, 20), pady=(10, 0), sticky="news")
    code = scrolledtext.ScrolledText(code_frame, font=("Times New Roman", 16))
    code.grid(row=0, column=0, sticky="news")
    code.focus()
    spacer = tkinter.Frame(window)
    spacer.grid(row=1, column=0)
    button = tkinter.Button(window, text="Transcribe", command=transcribe)
    button.grid(row=1, column=0, columnspan=2, sticky="se", padx=(0, 20), pady=(5, 15))
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=0)
    window.columnconfigure(1, weight=1)
    code_frame.rowconfigure(0, weight=1)
    code_frame.columnconfigure(0, weight=1)
    window.mainloop()
