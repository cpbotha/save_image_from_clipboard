#!/usr/bin/python3

"""save_image_from_clipboard

Save any image from the X11 clipboard to disk in the format of your choice.

I made this because xclip by itself can only save out in the same format that
it was copied, whereas my Emacs org-download-screenshot expects to be able
to write out a PNG from the clipboard.

Copyright 2020 by Charl P. Botha <info@charlbotha.com>

P.S. This script uses the walrus operator, and so requires Python 3.8 at a
minimum. Yay walrus!

"""

from pathlib import Path
import re
import subprocess
import sys
import tempfile

def main():
    if len(sys.argv) < 2:
        print("save_image_from_clipboard output_filename.png")
        return

    result = subprocess.run(["xclip", "-selection", "clipboard", "-t", "TARGETS", "-o"], stdout=subprocess.PIPE)
    xc_output = result.stdout.decode("utf-8")

    output_path = Path(sys.argv[1])
    # suffix is e.g. ".png" or "" if no extension was supplied
    # remove the dot at the start
    ext = output_path.suffix[1:]

    # xc_output can look something like:
    # image/png
    # image/bmp
    # TARGETS

    # if we have an image/ext that matches the output file's ext, then call
    # xclip and be done with it.
    if xc_output.find(desired_type := f"image/{ext}") >= 0:
        with output_path.open("w") as output_file:
            subprocess.run(["xclip", "-selection", "clipboard", "-t", desired_type, "-o"], stdout=output_file)

    # if we don't have the desired output format, dump what we do have, then convert
    elif mo := re.search("image/(.*)$", xc_output, re.MULTILINE):
        # this will be e.g. bmp
        ext_avail = mo.group(1)

        # dump out to temporary file with the correct extension
        with tempfile.NamedTemporaryFile(suffix=f".{ext_avail}", delete=False) as temp_file:
            subprocess.run(["xclip", "-selection", "clipboard", "-t", f"image/{ext_avail}", "-o"], stdout=temp_file)

        # then use imagemagick to convert that to the desired output type
        subprocess.run(["convert", temp_file.name, output_path])

    else:
        raise RuntimeError("Clipboard has no image/ types available.")

if __name__ == "__main__":
    main()
