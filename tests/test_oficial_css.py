"""Catch invalid CSS hex alpha syntax before browser smoke tests."""
import re
import unittest
from pathlib import Path

CSS = (Path(__file__).resolve().parents[1] / 'oficial/site.css').read_text()

class OfficialCssTests(unittest.TestCase):
    def test_hex_colors_use_supported_lengths(self):
        css = re.sub(r'/\*.*?\*/', '', CSS, flags=re.S)
        colors = re.findall(r'(?<![\w-])#([0-9a-fA-F]+)(?![\w-])', css)
        self.assertTrue(colors)
        self.assertEqual([], [f'#{color}' for color in colors if len(color) not in (3, 4, 6, 8)])

    def test_hero_fade_standard_and_webkit_match(self):
        blocks = re.findall(r'\.hero-art-composition \.hero-composition\s*\{([^}]+)\}', CSS)
        fade = next(block for block in blocks if 'mask-image:' in block)
        standard = re.search(r'(?<![-\w])mask-image\s*:\s*([^;}]+)', fade).group(1).strip()
        webkit = re.search(r'-webkit-mask-image\s*:\s*([^;}]+)', fade).group(1).strip()
        self.assertEqual(standard, webkit)
        self.assertIn('linear-gradient(', standard)
        self.assertIn('transparent 100%', standard)

if __name__ == '__main__':
    unittest.main()
