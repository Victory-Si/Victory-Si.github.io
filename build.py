#!/usr/bin/env python3
"""Rebuild the static academic homepage using Python 3's standard library."""
from pathlib import Path
from collections import Counter
from datetime import date
from html import escape
from urllib.parse import quote, urlsplit
import json
import re

ROOT = Path(__file__).resolve().parent

def read_data(name):
    return json.loads((ROOT / 'assets' / 'data' / (name + '.json')).read_text(encoding='utf-8'))

def safe_url(value):
    if urlsplit(value).scheme not in ('', 'https', 'http', 'mailto') or value.startswith('//'):
        raise ValueError('Unsupported URL: ' + value)
    return escape(value, quote=True)

def render(template, values):
    result = re.sub(r'\{\{([a-z_0-9]+)\}\}', lambda m: str(values[m[1]]), template)
    if '<?php' in result or '{{' in result:
        raise ValueError('Unconverted PHP or unresolved placeholder in template')
    return result

def build():
    profile = read_data('profile')
    values = {k: escape(str(v), quote=True) for k, v in profile.items()}
    for k in ('github', 'scholar', 'cv', 'portrait'):
        values[k] = safe_url(profile[k])
    values['year'] = date.today().year
    papers = read_data('publications')
    counts = Counter(p['kind'] for p in papers)
    labels = {'first': 'First-author journal', 'coauthor': 'Co-author journal', 'conference': 'Conference paper', 'preprint': 'Preprint · Not peer-reviewed'}
    articles = []
    for paper in sorted(papers, key=lambda p: int(p['year']), reverse=True):
        kind = paper['kind']
        if kind not in labels:
            raise ValueError('Invalid publication kind: ' + kind)
        e = {k: escape(str(v), quote=True) for k, v in paper.items()}
        if not paper.get('link') or 'scholar.google.com/scholar' in paper['link']:
            raise ValueError('Verified paper page required: ' + paper['title'])
        url = safe_url(paper['link'])
        status = '<span class="pub-status">' + e['status'] + '</span>' if paper.get('status') else ''
        articles.append(f'''<article class="publication-item" data-kind="{kind}" data-category="{e.get('category', 'localization')}">
<span class="pub-year">{e['year']}</span><div class="pub-content"><div class="pub-type">{labels[kind]} <b>/</b> {e['venue']}{status}</div>
<h2><a href="{url}" target="_blank" rel="noopener noreferrer">{e['title']}</a></h2><p class="pub-authors">{e['authors']}</p></div>
<a class="pub-link" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Open paper: {e['title']}">↗</a></article>''')
    filters = ''.join(f'<button type="button" data-filter="{kind}" aria-pressed="false">{label} ({count})</button>' for kind,label,count in [('first','First author',counts['first']),('all','All',len(papers)),('coauthor','Co-author',counts['coauthor']),('conference','Conference',counts['conference']),('preprint','Preprints',counts['preprint'])])
    publications = f'''<div class="container"><header class="inner-header"><h1>Publications</h1><p>Journal articles, conference papers and separately labeled preprints, based on the supplied CV, Scholar snapshot, and available publisher records. First-author publications are shown by default.</p></header>
<div class="inner-content"><div class="pub-intro"><span>{len(papers)} entries · {counts['first']} first-author journal articles · {counts['coauthor']} co-author journal articles · {counts['conference']} conference papers · {counts['preprint']} preprint</span>
<div class="pub-filters" role="group" aria-label="Filter publications" hidden>{filters}</div></div><div class="publication-list">{''.join(articles)}</div>
<div class="pub-bottom"><p>Bibliography is based on the supplied CV, Scholar snapshot, and available publisher records. Preprints are not peer-reviewed journal publications. Paper titles link directly to verified publisher or preprint pages; the Google Scholar profile remains available separately.</p><a href="{values['cv']}" target="_blank" rel="noopener noreferrer">Download complete CV ↗</a></div></div></div>'''
    news = []
    for index, item in enumerate(sorted(read_data('news'),key=lambda n:n['date_order'],reverse=True)):
        # News is trusted owner-authored HTML, just as in the original supplied source.
        news.append(f'<li class="news-item" data-older="{str(index >= 5).lower()}"><time class="news-date">{escape(item["date"])}</time><div class="news-detail">{item["html"]}</div></li>')
    values['news']='\n'.join(news)
    pages = [('index.html','Home','front-page'),('research.html','Research','page-research'),('publications.html','Publications',None),('experience-honors.html','Experience & Honors','page-experience-honors')]
    for filename, title, template in pages:
        v = values | {'page_title':escape(title),'description':escape(profile['intro'],quote=True)}
        header = render((ROOT/'templates/header.html').read_text(),v)
        header = header.replace(f'href="{filename}" ',f'href="{filename}" aria-current="page" ',1 if filename != 'index.html' else 0) if filename != 'index.html' else header.replace('href="index.html" >','href="index.html" aria-current="page">')
        body = render((ROOT/'templates'/f'{template}.html').read_text(),v) if template else publications
        (ROOT/filename).write_text(header+body+render((ROOT/'templates/footer.html').read_text(),v),encoding='utf-8')
    (ROOT/'.nojekyll').touch()
    print(f'Built {len(pages)} pages; {len(papers)} publications ({dict(counts)}); {len(news)} news items.')

if __name__ == '__main__':
    build()
