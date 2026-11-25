"""Colour study notes (A4 PDF) for the Jolly Phonics teacher course — Claude's own explanations."""
import sys, html
from playwright.sync_api import sync_playwright

CSS = """
@page { size: A4; margin: 14mm 14mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', 'Noto Sans', Arial, 'Lohit Bengali', sans-serif; color: #1f2340; font-size: 11pt; line-height: 1.45; margin: 0; }
.cover { background: linear-gradient(135deg, #5b3fd8, #1d8fff 55%, #2fe0b5); color: #fff; border-radius: 18px; padding: 22px 26px; margin-bottom: 16px; }
.cover .tag { text-transform: uppercase; letter-spacing: 2px; font-size: 9pt; opacity: .9; font-weight: 700; }
.cover h1 { margin: 6px 0 4px; font-size: 24pt; line-height: 1.15; }
.cover p { margin: 0; opacity: .95; }
h2 { font-size: 14.5pt; margin: 18px 0 8px; padding: 6px 12px; border-radius: 10px; color: #fff; break-after: avoid; }
.c1 { background: #1d8fff; } .c2 { background: #8b5cf6; } .c3 { background: #16a86a; } .c4 { background: #f59e0b; }
.c5 { background: #e8364a; } .c6 { background: #0ea5b7; } .c7 { background: #db2777; }
ul, ol { margin: 4px 0 8px 20px; padding: 0; } li { margin: 2px 0; }
.box { border-radius: 12px; padding: 10px 14px; margin: 10px 0; break-inside: avoid; }
.key { background: #fff7e0; border-left: 6px solid #f59e0b; }
.tip { background: #e8f6ff; border-left: 6px solid #1d8fff; }
.warn { background: #fdecef; border-left: 6px solid #e8364a; }
.home { background: #e9fbf4; border-left: 6px solid #16a86a; }
.box b.t { display: block; margin-bottom: 3px; }
table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 8px 0; font-size: 10.5pt; break-inside: avoid; }
th { background: #2a2470; color: #fff; text-align: left; padding: 6px 8px; }
th:first-child { border-top-left-radius: 8px; } th:last-child { border-top-right-radius: 8px; }
td { padding: 6px 8px; border-bottom: 1px solid #e3e5f2; vertical-align: top; }
tr:nth-child(even) td { background: #f6f7fd; }
.chips span { display: inline-block; min-width: 34px; text-align: center; padding: 4px 8px; margin: 2px; border-radius: 8px; font-weight: 800; font-size: 12pt; color: #fff; }
.g1 { background:#e8364a } .g2 { background:#f59e0b } .g3 { background:#16a86a } .g4 { background:#1d8fff } .g5 { background:#8b5cf6 } .g6 { background:#db2777 } .g7 { background:#0ea5b7 }
.quiz { background: #f3efff; border: 2px dashed #8b5cf6; }
.foot { margin-top: 16px; font-size: 8.5pt; color: #6b6f8f; border-top: 1px solid #e3e5f2; padding-top: 6px; }
"""

FOOT = ("Study notes written by Claude for Azizlpe's own study of the Jolly Phonics teacher course. "
        "These are explanations in our own words, not the course material. Jolly Phonics is a trademark of Jolly Learning Ltd.")


def build(src_html, out_pdf):
    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{src_html}<div class='foot'>{FOOT}</div></body></html>"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.set_content(doc); pg.pdf(path=out_pdf, format="A4", print_background=True,
            display_header_footer=True, header_template="<span></span>",
            footer_template="<div style='font-size:8px;width:100%;text-align:center;color:#888'><span class='pageNumber'></span> / <span class='totalPages'></span></div>",
            margin={"top": "14mm", "bottom": "16mm", "left": "14mm", "right": "14mm"})
        b.close()

if __name__ == "__main__":
    build(open(sys.argv[1], encoding="utf-8").read(), sys.argv[2])
