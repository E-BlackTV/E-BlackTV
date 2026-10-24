#!/usr/bin/env python3
"""Render the technologies and tools listed in the original profile."""
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',monospace"
ORANGE = '#ff6b35'
CREAM = '#f6f2e9'
GROUPS = [
    ('WEB', ['TypeScript', 'JavaScript', 'Angular', 'HTML', 'CSS', 'PHP']),
    ('APPS & LANGUAGES', ['Flutter', 'Dart', 'Kotlin', 'Swift', 'Java', 'C#']),
    ('DATA & SYSTEMS', ['Python', 'SQL', 'Deluge', 'Linux', 'Git', 'GitHub']),
    ('DESIGN & TOOLS', ['Figma', 'Postman', 'IntelliJ IDEA', 'VS Code', 'Unity', 'Notion']),
]


def monogram(label, size=29, background=ORANGE, color='#111310'):
    return f'<rect width="58" height="58" rx="7" fill="{background}"/><text x="29" y="39" text-anchor="middle" font-family="{MONO}" font-size="{size}" font-weight="700" fill="{color}">{escape(label)}</text>'


ICONS = {
    'TypeScript': monogram('TS'),
    'JavaScript': monogram('JS'),
    'Angular': '<path d="M29 0L58 10 53 45 29 60 5 45 0 10Z" fill="none" stroke="#ff6b35" stroke-width="3"/><path d="M14 43L29 12 44 43M20 32H38" fill="none" stroke="#f6f2e9" stroke-width="5"/>',
    'HTML': '<path d="M5 2H53L49 51 29 58 9 51Z" fill="#ff6b35"/><path d="M17 14H42M17 14L19 29H39L37 42 29 45 21 42" fill="none" stroke="#111310" stroke-width="5"/>',
    'CSS': '<path d="M5 2H53L49 51 29 58 9 51Z" fill="none" stroke="#ff9662" stroke-width="3"/><path d="M16 15H42L39 42 29 46 19 42M22 28H40" fill="none" stroke="#ff6b35" stroke-width="5"/>',
    'PHP': '<ellipse cx="29" cy="29" rx="29" ry="20" fill="#ff6b35"/><text x="29" y="36" text-anchor="middle" font-family="Helvetica,sans-serif" font-size="23" font-weight="700" font-style="italic" fill="#111310">php</text>',
    'Flutter': '<path d="M36 0H58L20 38 9 27Z" fill="#ff9662"/><path d="M36 24H58L32 50 21 39Z" fill="#ff6b35"/><path d="M32 50L43 39 58 54H36Z" fill="#a64b29"/>',
    'Dart': '<path d="M8 8L36 1 58 25V58H25L1 36Z" fill="#a64b29"/><path d="M8 8H34L58 32V58Z" fill="#ff9662"/><path d="M8 8L58 58H32L8 34Z" fill="#ff6b35"/>',
    'Kotlin': '<path d="M0 0H58L29 29 58 58H0Z" fill="#ff6b35"/><path d="M0 0H29L0 29Z" fill="#ffb58a"/>',
    'Swift': '<path d="M4 17L27 35 10 8 39 31Q44 22 38 7Q59 22 50 42L58 54Q48 48 42 51Q20 61 5 40Q20 48 31 42Z" fill="#ff9662"/>',
    'Java': '<path d="M11 29H43L40 45Q27 54 14 45Z" fill="none" stroke="#ff9662" stroke-width="3"/><path d="M43 31H49Q58 40 42 43M7 54H48" fill="none" stroke="#ff9662" stroke-width="3"/><path d="M24 23C9 13 40 15 25 2M34 24C22 17 45 16 37 8" fill="none" stroke="#ff6b35" stroke-width="3"/>',
    'C#': '<path d="M29 1L55 16V44L29 59 3 44V16Z" fill="#ff6b35"/><text x="29" y="39" text-anchor="middle" font-family="Helvetica,sans-serif" font-size="28" font-weight="700" fill="#111310">C#</text>',
    'Python': '<path d="M12 22V10Q12 1 26 1H35Q47 1 47 12V26H26V31H8Q0 31 0 23V22Z" fill="#ff6b35"/><path d="M47 37V49Q47 58 33 58H24Q12 58 12 47V33H33V28H51Q59 28 59 36V37Z" fill="#f6f2e9"/><circle cx="22" cy="10" r="3" fill="#111310"/><circle cx="37" cy="49" r="3" fill="#111310"/>',
    'SQL': '<path d="M7 12V46C7 61 51 61 51 46V12M7 28C7 43 51 43 51 28M7 42C7 57 51 57 51 42" fill="none" stroke="#ff9662" stroke-width="3"/><ellipse cx="29" cy="12" rx="22" ry="9" fill="#ff6b35"/>',
    'Deluge': monogram('D', background='#273023', color='#ff9662'),
    'Linux': '<rect width="60" height="54" y="3" rx="8" fill="none" stroke="#46503f" stroke-width="2"/><path d="M12 18L24 30 12 42M33 42H49" fill="none" stroke="#ff9662" stroke-width="4"/>',
    'Git': '<rect x="8" y="8" width="42" height="42" rx="4" transform="rotate(45 29 29)" fill="#ff6b35"/><path d="M19 9V36M19 18L38 37" fill="none" stroke="#111310" stroke-width="4"/><g fill="#111310"><circle cx="19" cy="18" r="5"/><circle cx="19" cy="37" r="5"/><circle cx="38" cy="37" r="5"/></g>',
    'GitHub': '<circle cx="29" cy="29" r="29" fill="#ff9662"/><path d="M15 23L14 12 25 17Q29 15 34 17L44 12 43 25Q50 46 30 46Q8 46 15 23Z" fill="#111310"/><path d="M24 44V58M35 44V58M25 49Q11 53 9 44" fill="none" stroke="#111310" stroke-width="5"/>',
    'Figma': '<path d="M29 2H18A9 9 0 0 0 18 20H29Z" fill="#ff6b35"/><path d="M29 2H40A9 9 0 0 1 40 20H29Z" fill="#ffb58a"/><path d="M29 20H18A9 9 0 0 0 18 38H29Z" fill="#a64b29"/><circle cx="38" cy="29" r="9" fill="#f6f2e9"/><path d="M29 38H18A9 9 0 1 0 29 47Z" fill="#ff9662"/>',
    'Postman': '<circle cx="29" cy="29" r="29" fill="#ff6b35"/><path d="M13 45L24 24 43 10 49 16 34 35Z" fill="#f6f2e9"/><path d="M17 42L42 17M25 25L34 34" stroke="#111310" stroke-width="2"/>',
    'IntelliJ IDEA': '<rect width="58" height="58" rx="5" fill="#ff6b35"/><rect x="8" y="8" width="42" height="42" fill="#111310"/><text x="15" y="31" font-family="Helvetica,sans-serif" font-size="23" font-weight="700" fill="#f6f2e9">IJ</text><path d="M15 43H30" stroke="#f6f2e9" stroke-width="3"/>',
    'VS Code': '<path d="M42 0L58 7V51L42 58 13 36 4 44 0 40V18L4 14 13 22ZM42 15L23 29 42 43Z" fill="#ff9662" fill-rule="evenodd"/>',
    'Unity': '<path d="M29 2L54 17V43L29 58 4 43V17Z" fill="none" stroke="#ff9662" stroke-width="3"/><path d="M29 16L42 23V38L29 46 16 38V23ZM4 17L16 23M54 17L42 23M29 46V58" fill="none" stroke="#f6f2e9" stroke-width="3"/>',
    'Notion': '<rect x="3" y="3" width="52" height="52" rx="4" fill="#f6f2e9"/><text x="29" y="44" text-anchor="middle" font-family="Georgia,serif" font-size="43" font-weight="700" fill="#111310">N</text>',
}


def render(mobile=False):
    width, height = (600, 1380) if mobile else (1200, 840)
    margin = 32 if mobile else 48
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
             '<title id="title">The toolkit — 24 technologies and tools</title>',
             '<desc id="desc">' + escape('; '.join(title + ': ' + ', '.join(names) for title, names in GROUPS)) + '.</desc>',
             f'<rect width="{width}" height="{height}" rx="20" fill="#111310"/>',
             f'<text x="{margin}" y="50" font-family="{MONO}" font-size="20" fill="#ff9662" letter-spacing="2">02 / TOOLKIT</text>',
             f'<text x="{width-margin}" y="50" text-anchor="end" font-family="{MONO}" font-size="16" fill="#85917d">24 / TOOLS</text>']
    for group_index, (title, names) in enumerate(GROUPS):
        group_y = 94 + group_index * (310 if mobile else 175)
        parts.append(f'<text x="{margin}" y="{group_y}" font-family="{MONO}" font-size="16" letter-spacing="1.5" fill="#bac1b3">{escape(title)}</text>')
        for i, name in enumerate(names):
            col, row = (i % 3, i // 3) if mobile else (i, 0)
            x = margin + col * (184 if mobile else 186)
            y = group_y + 18 + row * 132
            parts += [f'<g transform="translate({x} {y})">',
                      '<rect width="164" height="118" rx="12" fill="#1a1e18" stroke="#30372b"/>',
                      '<path d="M16 1H48" stroke="#ff6b35" stroke-width="2"/>',
                      f'<g transform="translate(59 13) scale(.8)">{ICONS[name]}</g>',
                      f'<text x="82" y="92" text-anchor="middle" font-family="{MONO}" font-size="{17 if len(name)>10 else 19}" fill="#e0e4d9">{escape(name)}</text>',
                      '</g>']
    parts += [f'<path d="M{margin} {height-55}H{width-margin}" stroke="#343a2f"/>',
              f'<text x="{margin}" y="{height-24}" font-family="{MONO}" font-size="16" fill="#85917d">DESIGN → BUILD → REFINE</text>',
              f'<text x="{width-margin}" y="{height-24}" text-anchor="end" font-family="{MONO}" font-size="18" fill="#ff9662">&lt;/&gt;</text>', '</svg>']
    result = '\n'.join(parts) + '\n'
    ET.fromstring(result)
    return result


def main():
    for mobile in (False, True):
        name = 'toolkit-mobile.svg' if mobile else 'toolkit.svg'
        (ROOT / 'assets' / name).write_text(render(mobile), encoding='utf-8')


if __name__ == '__main__':
    main()
