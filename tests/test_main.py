"""Tests for THE DAY IN WORLD NEWS (18 Nov 2026). Stdlib unittest only.

Run from the entry directory:  python3 -m unittest discover -s tests -v
"""
import hashlib
import os
import struct
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import main


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    w, h = struct.unpack(">II", head[16:24])
    return w, h


class TestData(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(main.STORIES), 13)
        self.assertEqual([s["n"] for s in main.STORIES], list(range(1, 14)))
        self.assertEqual(len(main.BRIEFS), 32)
        self.assertEqual([b[0] for b in main.BRIEFS], list(range(14, 46)))
        self.assertEqual(len(main.NUMBERS), 6)

    def test_stories_complete(self):
        kinds = set()
        for s in main.STORIES:
            self.assertTrue(s["headline"].strip())
            self.assertTrue(s["deck"].strip())
            self.assertTrue(s["kicker"].strip())
            self.assertTrue(s["kind"].strip())
            kinds.add(s["kind"])
            self.assertTrue(-90 <= s["lat"] <= 90)
            self.assertTrue(-180 <= s["lon"] <= 180)
        # every illustrated story has its own distinct motif
        self.assertEqual(len(kinds), 13)

    def test_summary_and_numbers(self):
        self.assertIn("18 November", main.DATE_LINE)
        self.assertTrue(main.SUMMARY.strip())
        self.assertLessEqual(len(main.SUMMARY), 280)
        for val, lab in main.NUMBERS:
            self.assertTrue(val and lab)

    def test_map_pins_in_bounds(self):
        for s in main.STORIES:
            x = (s["lon"] + 180) / 360
            y = (90 - s["lat"]) / 180
            self.assertTrue(0 <= x <= 1 and 0 <= y <= 1)

    def test_no_nonstdlib_imports(self):
        with open(os.path.join(ROOT, "main.py"), encoding="utf-8") as fh:
            src = fh.read()
        for bad in ("numpy", "pandas", "requests", "matplotlib"):
            self.assertNotIn(bad, src)

    def test_text_fits_its_box(self):
        """Headlines/decks/briefs/summary must fit without truncation."""
        from PIL import Image, ImageDraw, ImageFont
        fonts = main.find_fonts()
        self.assertIsNotNone(fonts, "Pillow/DejaVu needed for fit test")
        img = Image.new("RGB", (8, 8))
        d = ImageDraw.Draw(img)

        def F(name, size):
            return ImageFont.truetype(fonts[name], size)

        serif_b = F("DejaVuSerif-Bold.ttf", 20)
        serif_b_sm = F("DejaVuSerif-Bold.ttf", 15)
        serif_b_xs = F("DejaVuSerif-Bold.ttf", 12)
        sans = F("DejaVuSans.ttf", 10)
        sans_sm = F("DejaVuSans.ttf", 9)
        sans_b_sm = F("DejaVuSans-Bold.ttf", 8)
        serif_i_sm = F("DejaVuSerif.ttf", 13)
        # summary: one typographic line
        self.assertEqual(
            len(main.wrap(d, main.SUMMARY, serif_i_sm, 1024 - 48 - 20)), 1)
        # stories: headline <= 3 lines, deck <= its tier's line budget
        for i, s in enumerate(main.STORIES):
            if i == 0:
                hf, hw, df, dw, dl = serif_b, 294, sans, 294, 3
            elif i < 7:
                hf, hw, df, dw, dl = serif_b_sm, 229, sans_sm, 229, 2
            else:
                hf, hw, df, dw, dl = serif_b_xs, 140, sans_sm, 140, 2
            self.assertLessEqual(len(main.wrap(d, s["headline"], hf, hw)), 3,
                                 f"story {s['n']} headline too long")
            self.assertLessEqual(len(main.wrap(d, s["deck"], df, dw)), dl,
                                 f"story {s['n']} deck too long")
        # briefs: number + tag + text fits one line in its column (245px)
        for n, tag, text in main.BRIEFS:
            w = (d.textlength(f"{n}.", font=sans_b_sm) + 22
                 + d.textlength(tag, font=sans_b_sm) + 4
                 + d.textlength(text, font=sans_sm))
            self.assertLessEqual(w, 245, f"brief {n} too wide: {w:.0f}px")


class TestIllustrations(unittest.TestCase):
    """v3c: supersampled illustration tiles (3x lead, 4x thin strips)."""

    def test_tiles_correct_size_and_distinct(self):
        from PIL import Image
        tiles = {}
        for s in main.STORIES:
            w, h = (150, 130) if s["n"] == 1 else (229, 44) if s["n"] < 8 else (140, 34)
            tile = main.illus_tile(s["kind"], w, h, s["bg"])
            self.assertEqual(tile.size, (w, h), s["kind"])
            self.assertEqual(tile.mode, "RGB")
            tiles[s["kind"]] = tile.tobytes()
        # every motif is its own picture
        self.assertEqual(len(set(tiles.values())), 13)

    def test_tiles_deterministic_and_filled(self):
        from PIL import Image
        for s in main.STORIES:
            w, h = (150, 130) if s["n"] == 1 else (229, 44) if s["n"] < 8 else (140, 34)
            bg = tuple(int(s["bg"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
            t1 = main.illus_tile(s["kind"], w, h, s["bg"])
            t2 = main.illus_tile(s["kind"], w, h, s["bg"])
            self.assertEqual(t1.tobytes(), t2.tobytes(), s["kind"])
            non_bg = sum(1 for p in t1.getdata() if p != bg)
            self.assertGreater(non_bg, 0.05 * w * h,
                               f"{s['kind']} motif fills <5% of its panel")

    def test_tile_is_supersampled_not_1x(self):
        """The tile must differ from a direct 1x draw of the same motif:
        the LANCZOS-downscaled path is what lands on the page."""
        from PIL import Image, ImageDraw
        for s in main.STORIES[:3] + main.STORIES[7:8]:
            w, h = (150, 130) if s["n"] == 1 else (229, 44) if s["n"] < 8 else (140, 34)
            bg = tuple(int(s["bg"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
            tile = main.illus_tile(s["kind"], w, h, s["bg"])
            raw = Image.new("RGB", (w, h), bg)
            main._motif_raw(ImageDraw.Draw(raw), s["kind"], 0, 0, w, h, bg)
            self.assertNotEqual(tile.tobytes(), raw.tobytes(), s["kind"])

    def test_illus_pastes_tile_onto_page(self):
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (300, 100), (247, 243, 232))
        d = ImageDraw.Draw(img)
        main.illus(d, "chip", 10, 10, 100, 44, "#15803d")
        region = img.crop((10, 10, 110, 54))
        self.assertTrue(any(p == (21, 128, 61) for p in region.getdata()))
        self.assertTrue(any(p == (34, 197, 94) for p in region.getdata()))

    def test_render_panels_hold_motifs(self):
        """On the rendered page, every illustration panel holds its motif."""
        from PIL import Image
        fonts = main.find_fonts()
        self.assertIsNotNone(fonts, "Pillow/DejaVu needed for render test")
        img = main.render(fonts)
        zones = [(32, 230, 150, 130), (510, 230, 229, 44), (763, 230, 229, 44),
                 (32, 384, 222, 44), (278, 384, 222, 44), (524, 384, 222, 44),
                 (770, 384, 222, 44), (32, 538, 140, 34), (196, 538, 140, 34),
                 (360, 538, 140, 34), (524, 538, 140, 34), (688, 538, 140, 34),
                 (852, 538, 140, 34)]
        for (x, y, w, h), s in zip(zones, main.STORIES):
            bg = tuple(int(s["bg"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
            panel = img.crop((x, y, x + w, y + h))
            non_bg = sum(1 for p in panel.getdata() if p != bg)
            self.assertGreater(non_bg, 0.05 * w * h, f"story {s['n']} panel empty")


class TestRender(unittest.TestCase):
    def test_check_mode(self):
        r = subprocess.run([sys.executable, "main.py", "--check"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("13 illustrated stories", r.stdout)

    def test_render_produces_1024_png(self):
        out = os.path.join(ROOT, "output.png")
        r = subprocess.run([sys.executable, "main.py", "--output", out],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(png_size(out), (1024, 1024))

    def test_bundled_entry_matches_render(self):
        """entry.png must be exactly what main.py renders (deterministic)."""
        entry = os.path.join(ROOT, "entry.png")
        out = os.path.join(ROOT, "output.png")
        self.assertTrue(os.path.isfile(entry), "entry.png missing")
        self.assertEqual(png_size(entry), (1024, 1024))
        if os.path.isfile(out):
            with open(entry, "rb") as a, open(out, "rb") as b:
                self.assertEqual(hashlib.sha256(a.read()).hexdigest(),
                                 hashlib.sha256(b.read()).hexdigest(),
                                 "entry.png differs from a fresh render")

    def test_fallback_copies_entry_byte_for_byte(self):
        """Simulate a machine with no Pillow: find_fonts -> None."""
        import main as m
        orig = m.find_fonts
        m.find_fonts = lambda: None
        try:
            out = os.path.join(ROOT, "fallback-test.png")
            self.assertEqual(m.main(["--output", out]), 0)
            with open(os.path.join(ROOT, "entry.png"), "rb") as a, \
                    open(out, "rb") as b:
                self.assertEqual(a.read(), b.read())
        finally:
            m.find_fonts = orig
            if os.path.exists(os.path.join(ROOT, "fallback-test.png")):
                os.remove(os.path.join(ROOT, "fallback-test.png"))


if __name__ == "__main__":
    unittest.main()
