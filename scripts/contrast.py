#!/usr/bin/env python3
"""WCAG contrast ratios between colors.

Usage:
  python3 contrast.py "#0B2530" "#FF6B4A"          one pair
  python3 contrast.py --grid "#F4F7F7" "#FFFFFF" "#0B2530" "#FF6B4A"   every pair

AA needs 4.5:1 for body text and 3:1 for large text (24 px, or 19 px bold).
"""
import itertools, sys


def lum(hex_):
    h = hex_.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def verdict(r):
    return "AA text" if r >= 4.5 else "AA large only" if r >= 3 else "fails"


def main():
    args = sys.argv[1:]
    grid = args and args[0] == "--grid"
    colors = args[1:] if grid else args
    if len(colors) < 2:
        sys.exit(__doc__)
    pairs = itertools.combinations(colors, 2) if grid else [colors[:2]]
    for a, b in pairs:
        r = ratio(a, b)
        print(f"{a} on {b}: {r:.2f}:1  {verdict(r)}")


if __name__ == "__main__":
    main()
