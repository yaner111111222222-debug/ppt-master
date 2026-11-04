#!/usr/bin/env python3
"""Regression: the Source Han CN subsets resolve as East Asian faces."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from svg_to_pptx.drawingml.utils import parse_font_family  # noqa: E402


class SourceHanCnFontFamilyTest(unittest.TestCase):
    def test_sans_cn_fills_both_slots_as_named(self) -> None:
        fonts = parse_font_family('"Source Han Sans CN", sans-serif', 'zh-CN')
        self.assertEqual(fonts, {'latin': 'Source Han Sans CN', 'ea': 'Source Han Sans CN'})

    def test_serif_cn_fills_ea_slot(self) -> None:
        fonts = parse_font_family('Georgia, "Source Han Serif CN"', 'zh-CN')
        self.assertEqual(fonts, {'latin': 'Georgia', 'ea': 'Source Han Serif CN'})

    def test_existing_yahei_stack_unchanged(self) -> None:
        fonts = parse_font_family('"Microsoft YaHei", Arial, sans-serif', 'zh-CN')
        self.assertEqual(fonts, {'latin': 'Arial', 'ea': 'Microsoft YaHei'})

