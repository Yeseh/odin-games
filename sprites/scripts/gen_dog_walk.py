#!/usr/bin/env python3
"""
Generate a 4-frame 16x16 dog walk animation sprite sheet.

Output (relative to project root):
  sprites/dog_walk.png         — 64x16 sprite sheet (native)
  sprites/dog_walk_preview.png — 512x128 preview (8x scaled)
  sprites/dog_frame_0-3.png    — individual frames (8x scaled)

Usage:
  python3 sprites/scripts/gen_dog_walk.py
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


def draw_dog(frame_idx: int) -> Image.Image:
    """Return a 16x16 RGBA Image for the given walk-cycle frame (0–3)."""
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

    # ---- TAIL (upper-left; wags down on frames 2 & 3) ------------------ #
    if frame_idx in (0, 1):
        p(2, 1, D); p(3, 1, D)
        p(1, 2, D); p(2, 2, B); p(3, 2, D)
        p(1, 3, D); p(2, 3, B); p(3, 3, D)
    else:
        p(1, 2, D); p(2, 2, D)
        p(0, 3, D); p(1, 3, B); p(2, 3, B); p(3, 3, D)
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

    # ---- LEGS ---------------------------------------------------------- #
    # Walk cycle: diagonal leg pairs alternate forward/back each frame.
    #   bl_x  = near back-leg column (outline pixel)
    #   fl_x  = near front-leg column (outline pixel)
    cycle = [
        (4, 8),   # frame 0: neutral
        (3, 8),   # frame 1: back leg swings forward
        (4, 9),   # frame 2: front leg swings forward
        (5, 8),   # frame 3: back leg pushes off
    ]
    bl_x, fl_x = cycle[frame_idx]

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
    out_dir = os.path.join(script_dir, '..') # sprites/
    out_dir = os.path.normpath(out_dir)

    # Sprite sheet: 4 frames side-by-side → 64×16
    sheet = Image.new('RGBA', (64, 16), T)
    for i in range(4):
        sheet.paste(draw_dog(i), (i * 16, 0))
    sheet.save(os.path.join(out_dir, 'dog_walk.png'))

    # 8× scaled preview: 512×128
    preview = sheet.resize((512, 128), Image.NEAREST)
    preview.save(os.path.join(out_dir, 'dog_walk_preview.png'))

    # Individual frames at 8× scale
    for i in range(4):
        frame = draw_dog(i).resize((128, 128), Image.NEAREST)
        frame.save(os.path.join(out_dir, f'dog_frame_{i}.png'))

    print(f"Saved sprite sheet and frames to: {out_dir}")


if __name__ == '__main__':
    main()
