#!/usr/bin/env python3
"""Regression: newly authored shape ids never repeat across slides."""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from svg_to_pptx import convert_svg_to_slide_shapes  # noqa: E402

_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">'
    '<rect x="40" y="40" width="300" height="120" rx="16" fill="#D4A24C"/>'
    '<rect x="40" y="200" width="300" height="120" fill="#2B1416"/>'
    '<text x="60" y="400" font-size="24" font-family="Arial" fill="#111111">A</text>'
    '</svg>'
)


def _shape_ids(xml: str) -> list[int]:
    """Authored shape ids; id 1 is the spTree root every slide repeats."""
    ids = [int(value) for value in re.findall(r'<p:cNvPr id="(\d+)"', xml)]
    return [value for value in ids if value != 1]


class SlideShapeIdUniquenessTest(unittest.TestCase):
    def test_same_page_on_two_slides_shares_no_shape_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            svg = folder / "page.svg"
            svg.write_text(_SVG, encoding="utf-8")
            per_slide = []
            for slide_num in (1, 2):
                xml, *_ = convert_svg_to_slide_shapes(
                    svg, resource_root=folder, slide_num=slide_num, slide_count=2,
                )
                ids = _shape_ids(xml)
                self.assertTrue(ids)
                self.assertEqual(len(ids), len(set(ids)))
                per_slide.append(set(ids))
        self.assertEqual(min(per_slide[0]), 2)
        self.assertFalse(per_slide[0] & per_slide[1])
