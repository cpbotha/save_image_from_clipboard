# save_image_from_clipboard

Save any image from the X11 clipboard to disk in the format of your choice.

I made this because xclip by itself can only save out in the same format than
was copied, whereas my Emacs
[`org-download-screenshot`](https://github.com/abo-abo/org-download) setup
expects to be able to write out a PNG from the clipboard.

On macOS, I used to use [pngpaste](https://github.com/jcsalterego/pngpaste),
which is also the default for org-download's `M-x org-download-clipboard` on
that platform.

On October 13, 2021, I added optional Wayland clipboard support behind the flag
`--wayland`. I use this as part of my Emacs setup on XWayland on WSLg to store
screenshots made on the Windows side.

Copyright 2020 by Charl P. Botha <info@charlbotha.com>

## Usage

After having copied any image to the clipboard, invoke the script with the
desired output filename. The script will ensure that the image from the
clipboard is converted to the format you specified.

```shell
# dump to jpg
save_image_from_clipboard /some/directory/your_desired_filename.jpg
# dump to png
save_image_from_clipboard /another/directory/your_desired_filename.png
```

## To install

- This script requires Python 3.8 or higher, because I used the walrus operator.
- Make sure that you have `xclip` and ImageMagick `convert` installed. These are
  available in most modern Linux distributions.
- If you are planning to use the Wayland clipboard, make sure that
  `wl-clipboard` is installed.

There are at least two options to install:

### Option 1

```shell
# make sure you have the latest pip
# NOTE: you HAVE to do this upgrade, else pip install won't know what to do without setup.py!
pip3 install --user --upgrade pip
# install xdg-open-wsl using your latest pip
pip install --user git+https://github.com/cpbotha/save_image_from_clipboard.git
# ensure that the newly installed xdg-open is active
# the following command should show something like /home/username/.local/bin/xdg-open
which save_image_from_clipboard
```

### Option 2

Download just the `save_image_from_clipboard.py` script, and put it somewhere in
your path.

## Use with org-download

In my `init.el` in the [org-download](https://github.com/abo-abo/org-download)
`use-package` clause, I have:

```emacs-lisp
(setq org-download-screenshot-method "save_image_from_clipboard %s")
```

My workflow is that I use whichever system tool to make a screenshot and copy
it to the clipboard, and then in Emacs Orgmode I invoke `M-x
org-download-screenshot` to attach the screenshot to the current heading.

(I just learned that org-download now has an `org-download-clipboard` function,
but that just temporarily binds `org-download-screenshot-method` to the basic
`xclip ... -t image/png` command, which will fail if you copied a graphic of a
different format. The setup documented here is required for multi-format support.)
