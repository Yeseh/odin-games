#!/usr/bin/env python3
"""
Generate a 3-frame 16x16 dog idle animation sprite sheet.
The dog stands still while its tail wags through three positions.

Output (relative to project root):
  sprites/dog_idle.png         — 48x16 sprite sheet (native)
  sprites/dog_idle_preview.png — 384x128 preview (8x scaled)
  sprites/dog_idle_frame_0-2.png — individual frames (8x scaled)

Usage:
  python3 sprites/scripts/gen_dog_idle.py
"""

from PIL import Image
import os

# ---------------------------------------------------------------------------
# Color palette (RGBA)
# ---------------------------------------------------------------------------
T = (0, 0, 0, 0)        # transparent
D = (55, 28, 8, 255)     # dark outline
B = (158, 98, 46, 255)   # brown body
L = (208, 160, 98, 255)  # light tan (belly / snout)
K = (15, 12, 8, 255)     # black (eye, nose)
S = (100, 60, 22, 255)   # shadow / far-side legs


def draw_dog_idle(frame_idx: int) -> Image.Image:
    """Return a 16x16 RGBA Image for the given idle frame (0–2).

    Tail positions:
      0 — high:   tip curls up and to the right
      1 — mid:    tail points straight up
      2 — low:    tail droops to the left / outward
    """
    img = Image.new('RGBA', (16, 16), T)

    def p(x, y, c):
        if 0 <= x < 16 and 0 <= y < 16:
            img.putpixel((x, y), c)

    # ---- BODY (cols 3-10, rows 4-8) ------------------------------------ #
    for x in range(3, 11): p(x, 4, D)          # top edge
    for x in range(3, 11): p(x, 8, D)          # bottom edge
    for y in range(5, 8):  p(3, y, D)          # left side
    for y in range(5, 8):  p(10, y, D)         # right side
    for y in range(5, 7):                       # body fill
        for x in range(4, 10): p(x, y, B)
    for x in range(4, 10): p(x, 7, L)          # belly (lighter)

    # ---- TAIL ---------------------------------------------------------- #
    if frame_idx == 0:
        # High: tail curls upward, tip angled right
        #   . . d d
        #   . d b d
        #   d b b d
        p(2, 1, D); p(3, 1, D)
        p(1, 2, D); p(2, 2, B); p(3, 2, D)
        p(0, 3, D); p(1, 3, B); p(2, 3, B); p(3, 3, D)

    elif frame_idx == 1:
        # Mid: tail points straight up, slightly left of high
        #   . d d .
        #   d b b d
        #   . d b d
        p(1, 1, D); p(2, 1, D)
        p(0, 2, D); p(1, 2, B); p(2, 2, B); p(3, 2, D)
        p(1, 3, D); p(2, 3, B); p(3, 3, D)

    else:
        # Low: tail droops outward to the left
        #   d d . .
        #   . d b d
        #   . . d b d
        p(0, 2, D); p(1, 2, D)
        p(0, 3, D); p(1, 3, B); p(2, 3, D)
        p(1, 4, D); p(2, 4, B); p(3, 4, D)

    # ---- HEAD (cols 10-15, rows 1-6) ----------------------------------- #
    p(11, 1, D); p(12, 1, B)                           # ear
    p(11, 2, B); p(12, 2, D); p(13, 2, D)             # head top
    p(10, 3, D); p(11, 3, B); p(12, 3, B); p(13, 3, B); p(14, 3, D)  # upper head
    p(10, 4, D); p(11, 4, B); p(12, 4, B); p(13, 4, L); p(14, 4, L); p(15, 4, D)  # snout
    p(10, 5, D); p(11, 5, B); p(12, 5, L); p(13, 5, L); p(14, 5, D)  # lower head
    p(11, 6, D); p(12, 6, D)                           # chin
    p(13, 3, K)                                        # eye
    p(15, 4, K)                                        # nose

    # ---- LEGS (neutral / standing still) ------------------------------- #
    bl_x, fl_x = 4, 8   # back-leg and front-leg column (outline pixel)

    # Far (shadow) legs — drawn first so near legs paint over them
    fbl_x, ffl_x = bl_x + 1, fl_x - 1
    for dy in range(4):
        p(fbl_x,   9 + dy, S); p(fbl_x + 1, 9 + dy, S)
        p(ffl_x,   9 + dy, S); p(ffl_x + 1, 9 + dy, S)
    p(fbl_x, 13, D); p(fbl_x + 1, 13, D)
    p(ffl_x, 13, D); p(ffl_x + 1, 13, D)

    # Near legs
    for dy in range(4):
        p(bl_x,   9 + dy, D); p(bl_x + 1, 9 + dy, B)
        p(fl_x,   9 + dy, D); p(fl_x + 1, 9 + dy, B)
    p(bl_x, 13, D); p(bl_x + 1, 13, D)
    p(fl_x, 13, D); p(fl_x + 1, 13, D)

    return img


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.normpath(os.path.join(script_dir, '..'))

    # Sprite sheet: 3 frames side-by-side → 48×16
    sheet = Image.new('RGBA', (48, 16), T)
    for i in range(3):
        sheet.paste(draw_dog_idle(i), (i * 16, 0))
    sheet.save(os.path.join(out_dir, 'dog_idle.png'))

    # 8× scaled preview: 384×128
    preview = sheet.resize((384, 128), Image.NEAREST)
    preview.save(os.path.join(out_dir, 'dog_idle_preview.png'))

    # Individual frames at 8× scale
    for i in range(3):
        frame = draw_dog_idle(i).resize((128, 128), Image.NEAREST)
        frame.save(os.path.join(out_dir, f'dog_idle_frame_{i}.png'))

    print(f"Saved sprite sheet and frames to: {out_dir}")


if __name__ == '__main__':
    main()
