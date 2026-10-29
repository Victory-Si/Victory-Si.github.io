# Haonan Si — static academic homepage

A GitHub Pages-compatible conversion of the supplied Haonan Academic WordPress theme. The original typography, colors, layout, photographs, research text, experience and bibliography are retained. No WordPress/PHP, database, JavaScript framework, paid service or external font is required. This package is prepared for the confirmed `Victory-Si/Victory-Si.github.io` repository; publication status must be checked separately.

## Preview

Requires Python 3.9+ (standard library only for building):

```sh
python3 build.py
python3 -m http.server 8000
```

Open http://localhost:8000. HTML is already generated, so rebuilding is only needed after editing data/templates.

## Update publications, news and CV

1. Edit `assets/data/publications.json`. Keep existing papers; add a JSON object with `title`, `authors`, `venue`, `year`, `kind`, `category`, `status`, and `link`. `kind` must be `first` (first-author journal), `coauthor` (co-author journal), `conference`, or `preprint` (not peer-reviewed). Counts are computed automatically, and newest years sort first. Provide a verified actual publisher or preprint page URL in `link`. Missing links fail the static build; do not substitute a Scholar search. Preserve verified author order and publication status; do not infer acceptance from Scholar indexing.
2. Edit `assets/data/news.json` to add news. `date_order` is `YYYY-MM`; `date` is its displayed label. `html` permits trusted owner-authored HTML. Do not paste untrusted scripts. Items sort newest first; the first five appear initially.
3. Replace `assets/Haonan_Si_CV.pdf` with the verified current PDF using exactly the same filename. Every CV link uses that path. Website data and PDF are separate: updating one does not automatically rewrite the other.
4. Edit `assets/data/profile.json` for affiliation, bio, contact information, Scholar/GitHub URLs or image/CV paths. The GitHub account `Victory-Si` and existing `Victory-Si.github.io` repository were confirmed through the connected account; availability must still be checked after each deployment.
5. Research and experience text live in `templates/page-research.html` and `templates/page-experience-honors.html`; homepage layout in `templates/front-page.html`; shared navigation/footer in `templates/header.html` and `templates/footer.html`. `style.css` controls appearance; `assets/js/site.js` controls mobile navigation, news expansion and publication filters.
6. Run `python3 build.py`, preview, verify changes, then commit both edited source/data and regenerated HTML. Do not edit generated root HTML directly: the next build overwrites it.

All publications and news remain readable without JavaScript; filters and mobile menu are enhancements. Printing includes all publications, not only the active filter.

## Publish to the confirmed GitHub repository

First verify the intended GitHub account and repository. No account/repository identity is assumed by this package and there is no CNAME or hard-coded deployment origin.

- Put the **contents** of this folder in the repository root, including `.nojekyll` and generated `index.html`.
- In the repository's **Settings → Pages**, select **Deploy from a branch**, the branch containing these files, and **/(root)**, then Save.
- For an account site, the repository must be named `<confirmed-username>.github.io`; a normal repository can serve a project site. All site assets/navigation use relative links, so either layout is supported.
- Wait for GitHub's Pages deployment to finish, open the actual URL reported by GitHub, and verify Home, Research, Publications, Experience & Honors, the PDF download, and mobile navigation.
- GitHub Pages is public hosting in the normal public-repository configuration. Publishing exposes the bundled CV, photographs, contact details, JSON and template sources; review them before publishing. Do not upload private notes or credentials.

Official instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Scope and provenance

The bibliography combines the owner-supplied CV and Scholar snapshot with available publisher records. Not every entry has independently verified full publisher metadata. Preprints are kept separate from journal papers. All 40 paper links now use verified actual publisher or preprint pages; the Scholar profile link is preserved separately. This is a static homepage: WordPress admin editing, generic blog/archive/search templates, custom post types and server-side behavior are intentionally not deployed. There was no supplied database export or individual blog-post content to migrate. The four real academic pages are preserved. The original theme declares GNU GPL v2 or later; its license declaration is retained in `style.css`.

### Metadata still requiring confirmation

- The TASE paper's supplied author information currently supports the first four authors plus `et al.`; confirm the remaining author names against the full publisher record before expanding the list.
- The PIMRC 2026 addition retains the supplied title and six authors; no unconfirmed DOI, page range or event location is invented.
- Citation figures in the CV are explicitly a user-supplied October 2026 snapshot, not a live Google Scholar count. The static site does not scrape or automatically refresh Scholar.
