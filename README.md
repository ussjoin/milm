# Maternal Integrated Lactation Marking system (MILM)

## Purpose

Producing timestamped human breast milk medical labels to apply to milk storage units (e.g., bags, bottles).

## What? Why?

Everyone who is currently lactating with the intent to feed needs to timestamp milk to ensure it's used oldest-to-newest. (If you need to know why that's important, go Google it.) Some people need to be able to do that *and* apply labels that are readable by a hospital's scanning system.

If you don't need to do the medical thing, then this is probably a bit overkill, but feel free to customize it for your own uses. Replace the barcodes with a Star Wars pun!

## No, srsly though, why?

I'm a cis male, so the support I can provide in the lactation process is somewhat limited: I can bring food and beverages, and I can handle supplies. As part of the latter, I needed to add time and date stamping to a (otherwise pre-printed) label. I did this using a Sharpie.

As any good technologist knows, however: why use a $0.30 Sharpie when you can use a $100 label printer, a Raspberry Pi, a [three-key USB keyboard](https://www.amazon.com/Ecarke-Mechanical-Keyboard-Programming-Software/dp/B08P1GY3GN/), and various bits and bobs?

If you get that keyboard, by the way, the keys default to `1` `2` and `3` respectively, so you don't need to bother with reprogramming it.

## License

BSD license, except for `Roboto-Medium.ttf` which is released under the Apache license: <https://fonts.google.com/specimen/Roboto>

## Usage

Get the non-Python requirements:
`sudo apt install ghostscript imagemagick` (or as necessary for your environment)

Get the python requirements:
`sudo pip3 install -r requirements.txt`

To run:

`./milm.py`

Press CTRL-C to quit, or any other key to print a label.

To deploy in a useful way: set a Raspberry Pi to boot *logged-in* to the command line (you can use raspi-config to do that) and then put the invocation in `.bashrc`.
