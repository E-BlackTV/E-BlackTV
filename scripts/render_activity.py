#!/usr/bin/env python3
"""Render only the anonymous contribution counts already visible on GitHub.

No PAT, private repository API, repository names or commit messages are used.
Private activity appears when enabled in the account's Contribution settings.
"""
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROFILE = 'E-BlackTV'
COLORS = ['#242922', '#583321', '#a64b29', '#e56a37', '#ff9662']
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',monospace"
DISPLAY = "Impact,'Arial Narrow',sans-serif"


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.labels = {}
        self.tooltip = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'td' and 'data-date' in attrs:
            key = attrs['id']
            if key in self.cells:
                raise ValueError('Duplicate calendar cell')
            self.cells[key] = (date.fromisoformat(attrs['data-date']), int(attrs['data-level']))
        if tag == 'tool-tip':
            self.tooltip = attrs.get('for')
            if self.tooltip:
                self.labels[self.tooltip] = ''

    def handle_data(self, data):
        if self.tooltip:
            self.labels[self.tooltip] += data

    def handle_endtag(self, tag):
        if tag == 'tool-tip':
            self.tooltip = None


def parse_calendar(markup):
    parser = CalendarParser()
    parser.feed(markup)
    days = []
    for key, (day, level) in parser.cells.items():
        label = parser.labels.get(key, '').strip()
        match = re.match(r'^(No|[\d,]+) contributions? on ', label)
        if not match or level not in range(5):
            raise ValueError('GitHub calendar format changed; keeping the existing artwork')
        count = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
        if (count == 0) != (level == 0):
            raise ValueError('Calendar count and level disagree')
        days.append((day, count, level))
    days.sort()
    if not 350 <= len(days) <= 378:
        raise ValueError('Expected a complete year of contribution data')
    if any(b[0] - a[0] != timedelta(days=1) for a, b in zip(days, days[1:])):
        raise ValueError('Missing or duplicate calendar date')
    heading = re.search(r'([\d,]+)\s+contributions?\s+in the last year', markup)
    if not heading or sum(d[1] for d in days) != int(heading[1].replace(',', '')):
        raise ValueError('Daily counts do not match the public contribution total')
    return days


def text(x, y, value, size=18, color='#bac1b3', font=MONO, **attrs):
    attributes = ''.join(f' {k.replace("_", "-")}="{escape(str(v), quote=True)}"' for k, v in attrs.items())
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}"{attributes}>{escape(str(value))}</text>'


def heatmap(days, x, y, step, cell):
    start = days[0][0] - timedelta(days=(days[0][0].weekday() + 1) % 7)
    svg = []
    previous_month = None
    for day, count, level in days:
        column, row = divmod((day - start).days, 7)
        if row == 0 and day.month != previous_month:
            # Leave enough space between month labels, including the first partial month.
            if column > 1:
                svg.append(text(x + column * step, y - 16, day.strftime('%b').upper(), 14))
            previous_month = day.month
        px, py = x + column * step, y + row * step
        svg.append(f'<rect x="{px}" y="{py}" width="{cell}" height="{cell}" rx="3" fill="{COLORS[level]}"><title>{day}: {count} contributions</title></rect>')
    return ''.join(svg)


def render(days, mobile=False):
    total = sum(d[1] for d in days)
    active = sum(d[1] > 0 for d in days)
    peak = max(d[1] for d in days)
    end = days[-1][0]
    width, height = (600, 620) if mobile else (1200, 490)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">GitHub contribution activity</title>',
           f'<desc id="desc">{total:,} contributions, {active} active days and a peak of {peak} contributions in one day over the past year. Updated {end}. Only anonymous daily counts are displayed.</desc>',
           f'<rect width="{width}" height="{height}" rx="20" fill="#111310"/>',
           f'<path d="M32 1H{width-32}" stroke="#ff6b35" stroke-width="2"/>']
    if mobile:
        svg += [text(32, 49, '01 / ACTIVITY', 20, '#ff9662'),
                text(32, 152, f'{total:,}', 100, '#f6f2e9', DISPLAY),
                text(32, 190, 'CONTRIBUTIONS / PAST YEAR', 18),
                '<path d="M32 222H568" stroke="#343a2f"/>',
                text(32, 280, active, 48, '#f6f2e9', DISPLAY),
                text(114, 277, 'ACTIVE DAYS', 17),
                text(340, 280, peak, 48, '#f6f2e9', DISPLAY),
                text(422, 277, 'BEST DAY', 17),
                text(32, 338, 'LAST 26 WEEKS', 17, '#f6f2e9')]
        week_start = end - timedelta(days=(end.weekday() + 1) % 7) - timedelta(weeks=25)
        visible = [d for d in days if d[0] >= week_start]
        svg.append(heatmap(visible, 53, 386, 19, 14))
        svg += [text(32, 570, 'GITHUB / ANONYMOUS DAILY COUNTS', 15),
                text(32, 598, 'UPDATED ' + str(end), 15, '#85917d')]
    else:
        svg += [text(48, 51, '01 / ACTIVITY', 18, '#ff9662', letter_spacing=2),
                text(1152, 51, 'PAST 12 MONTHS', 16, text_anchor='end'),
                text(48, 170, f'{total:,}', 108, '#f6f2e9', DISPLAY),
                text(48, 209, 'CONTRIBUTIONS', 19),
                '<path d="M570 104V216M870 104V216" stroke="#343a2f"/>',
                text(620, 169, active, 68, '#f6f2e9', DISPLAY),
                text(620, 207, 'ACTIVE DAYS', 17),
                text(920, 169, peak, 68, '#f6f2e9', DISPLAY),
                text(920, 207, 'BEST DAY', 17)]
        svg.append(heatmap(days, 72, 277, 20, 15))
        svg += [text(48, 454, 'GITHUB / ANONYMOUS DAILY COUNTS', 15),
                text(1152, 454, 'UPDATED ' + str(end), 15, '#85917d', text_anchor='end')]
    svg.append('</svg>')
    result = '\n'.join(svg)
    ET.fromstring(result)
    return result


def main():
    request = urllib.request.Request(
        f'https://github.com/users/{PROFILE}/contributions',
        headers={'User-Agent': f'{PROFILE}-profile-artwork', 'Accept-Language': 'en-US'})
    with urllib.request.urlopen(request, timeout=30) as response:
        days = parse_calendar(response.read().decode('utf-8'))
    # Validate both images before writing either file. On any error, fail closed.
    images = {'activity.svg': render(days), 'activity-mobile.svg': render(days, mobile=True)}
    for name, content in images.items():
        target = ROOT / 'assets' / name
        temporary = target.with_suffix('.svg.tmp')
        temporary.write_text(content, encoding='utf-8')
        temporary.replace(target)
    print(f'Rendered {sum(d[1] for d in days)} anonymous contributions across {len(days)} days.')


if __name__ == '__main__':
    main()
