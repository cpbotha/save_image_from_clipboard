#!/usr/bin/python3

"""save_image_from_clipboard

Save any image from the X11 clipboard to disk in the format of your choice.

I made this because xclip by itself can only save out in the same format that
it was copied, whereas my Emacs org-download-screenshot expects to be able
to write out a PNG from the clipboard.

Copyright 2020-2022 by Charl P. Botha <info@charlbotha.com>

P.S. This script uses the walrus operator, and so requires Python 3.8 at a
minimum. Yay walrus!

"""

import argparse
from pathlib import Path
import re
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_filename", help="Output filename, e.g. bleh.png")
    # https://docs.python.org/3/howto/argparse.html#introducing-optional-arguments
    # action=store_true sets this as an on/off flag
    parser.add_argument("--wayland", help="Use Wayland clipboard instead of X clipboard", action="store_true")
    args = parser.parse_args()

    if args.wayland:
        CLIP_CMD = "wl-paste"
        LIST_CMD = f"{CLIP_CMD} --list"
        # double { means we want single in the output, so we can interpolate desired_type later
        SAVE_CMD = f"{CLIP_CMD} -t {{desired_type}}"
    else:
        # use xclip by default
        CLIP_CMD = "xclip -selection clipboard"
        LIST_CMD = f"{CLIP_CMD} -t TARGETS -o"
        SAVE_CMD = f"{CLIP_CMD} -t {{desired_type}} -o"

    result = subprocess.run(LIST_CMD.split(), stdout=subprocess.PIPE)
    xc_output = result.stdout.decode("utf-8")

    output_path = Path(args.output_filename)
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
            subprocess.run(SAVE_CMD.format(desired_type=desired_type).split(), stdout=output_file)

    # if we don't have the desired output format, dump what we do have, then convert
    elif mo := re.search("image/(.*)$", xc_output, re.MULTILINE):
        # this will be e.g. bmp
        ext_avail = mo.group(1)

        # dump out to temporary file with the correct extension
        with tempfile.NamedTemporaryFile(suffix=f".{ext_avail}", delete=False) as temp_file:
            subprocess.run(SAVE_CMD.format(desired_type=f"image/{ext_avail}").split(), stdout=temp_file)

        # then use imagemagick to convert that to the desired output type
        subprocess.run(["convert", temp_file.name, output_path])

    else:
        raise RuntimeError("Clipboard has no image/* types available.")


if __name__ == "__main__":
    main()
