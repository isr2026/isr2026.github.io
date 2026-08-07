# IEEE ISR/SIAS 2026 — conference website

Source for <https://isr2026.github.io/>.

Plain static HTML. No build step, no dependencies. What is in this repo is exactly what is served.

## Deploying to GitHub Pages

The org name must be `isr2026` and the repo name must be `isr2026.github.io` — that exact pair is what produces the URL `https://isr2026.github.io/`. Any other repo name gives you `https://isr2026.github.io/repo-name/`.

1. **Create the organization.** github.com → your avatar → *Your organizations* → *New organization* → Free plan. Name it `isr2026`.
   - If the name is taken you cannot have this URL. Pick an alternative (`isrsias2026`, `ieee-isrsias2026`) and tell everyone the new address before anything is printed.
2. **Create the repository** inside the org, named exactly `isr2026.github.io`. Public. Do not add a README (this repo has one).
3. **Push the contents of this folder** to the `main` branch:

   ```bash
   cd isr2026.github.io
   git init -b main
   git add .
   git commit -m "Initial conference website"
   git remote add origin https://github.com/isr2026/isr2026.github.io.git
   git push -u origin main
   ```

   Or use GitHub's web uploader: repo → *Add file* → *Upload files* → drag everything in, including the `assets` folder.

4. **Enable Pages.** Repo → *Settings* → *Pages* → Source: *Deploy from a branch* → Branch: `main`, folder `/ (root)` → *Save*.
5. Wait 1–2 minutes, then open <https://isr2026.github.io/>.

**Add co-maintainers.** Org → *People* → invite the other chairs. If only one person can publish, the site stalls whenever that person is away. Give at least two people write access.

## Files

| Path | What it is |
|---|---|
| `index.html` | Home — hero, announcements, key dates |
| `about.html` | Scope, topics of interest, workshops/special sessions |
| `dates.html` | Full deadline table |
| `registration.html` | Fees and categories (awaiting content) |
| `submission.html` | Paper requirements, templates, FAQ |
| `program.html` | Technical program (awaiting content) |
| `venue.html` | INTEX Osaka, access, about the city |
| `accommodation.html` | Hotels (awaiting content) |
| `committee.html` | Organizing committee |
| `contact.html` | Contact addresses (awaiting content) |
| `404.html` | Shown for bad URLs |
| `assets/css/style.css` | **All** styling. Change colours and spacing here only. |
| `assets/img/` | Images |
| `assets/docs/` | Call for Papers PDF |
| `.nojekyll` | Tells GitHub Pages to serve files as-is |
| `robots.txt`, `sitemap.xml` | Search engine hints |
| `_tools/build.py` | Optional generator that produced these pages — see below |

## Editing

For text changes, edit the `.html` file directly. The pages are ordinary HTML; you do not need to run anything.

**One caveat:** the navigation menu and the footer are duplicated in all ten pages. If you add or rename a page you must update all ten, or run the optional generator:

```bash
python3 _tools/build.py
```

`_tools/build.py` regenerates every page from a single template. It **overwrites** all ten HTML files, so if you have hand-edited a page, put the change into `build.py` first or your edit will be lost. Using it is optional — if you prefer to hand-edit, just delete `_tools/`.

As of 2026-08-06 the generator is in sync: running it reproduces all ten committed pages byte-for-byte. Verify that after any hand-edit, so the generator never silently reverts published content:

```bash
cp -R . /tmp/buildcheck && (cd /tmp/buildcheck && python3 _tools/build.py) && diff -rq --exclude=.git --exclude=_tools . /tmp/buildcheck
```

## Blockers — confirm with the General Chair before publishing

1. **The extended deadlines are not on the live AIST site.** As of this writing, <https://unit.aist.go.jp/ircwb/isrsias2026> still shows the *original* dates (submission Aug 1, notification Sep 30, camera-ready Oct 13). The extended dates (Aug 28 / Oct 18 / Nov 2) appear only in the local `index.html` draft and in the CFP PDF. This site uses the **extended** dates throughout. Confirm the extension is official before publishing, or the two sites will contradict each other in public.
2. **The CFP PDF is internally inconsistent.** The file is named `ISRSIAS2026_cfp_2st.pdf` but its heading reads "1st Call for Papers", while its content carries the extended dates. Ask for a corrected PDF; it is linked from four places on this site.
3. **Submission link is the generic PaperPlaza page.** Submissions opened 2026-08-06 and the button is live, but it points at `https://ras.papercept.net/conferences/scripts/start.pl` — the generic IEEE RAS entry page listing every open RAS conference. ISR-SIAS 2026 is on that list and is accepting submissions, so the link works, but authors must find the conference themselves; both the button caption and the FAQ tell them to. Ask the Program Chair for the conference-specific PaperPlaza URL and replace the two `href`s, both in `submission.html` (the portal button and the "Where do I submit?" FAQ answer).
   - **Deadline mismatch:** the PaperPlaza listing shows a submission deadline of **August 20, 2026**, while this site says **August 28** everywhere. One of the two is wrong and authors will see both. Resolve with the Program Chair.
4. **IEEE logo is hot-linked from Wikimedia Commons** (inherited from the original site, in every page footer). Wikimedia discourages hotlinking, and IEEE has its own trademark usage rules for conference sites. Request the official IEEE master brand file and host it locally in `assets/img/`.

## Before launch — placeholders to replace

Search the repo for `TBA` and `to be announced`. The items below need real content:

- [x] **Contact e-mail addresses** (`contact.html`) — done 2026-08-06. One address, `M-isrsias2026-info-ml@aist.go.jp`, covers every enquiry type. A separate website address was offered by the General Chair's office but declined in favour of one shared list, so the three per-topic cards were removed as duplicates.
- [ ] **Registration fees and categories** (`registration.html`)
- [ ] **Hotel list** (`accommodation.html`)
- [ ] **Program** (`program.html`) — after October 18 notification
- [ ] **Program Committee list** (`committee.html`)
- [ ] **Deadline time zone** (`dates.html`) — states "23:59 Anywhere on Earth"; this was *not* in any source document. Confirm with the Program Chair or remove it.
- [ ] **Registration requirement** (`registration.html`) — says at least one author "is normally required to register". Confirm the actual policy.
- [ ] **Indicative program structure** (`program.html`) and **registration categories** (`registration.html`) are labelled as indicative and were invented as scaffolding. Replace or delete them.
- [ ] **Sponsor logos** — only IEEE and NECA were on the original site. Add IEEE society co-sponsors (RAS, IES) if applicable.

Venue access details in `venue.html` (station walking times, journey times) were taken from the official INTEX Osaka access page and are accurate as of this writing. The postal address matches INTEX Osaka's own listing.

## The AIST gateway page

A separate `aist-gateway/index.html` (one folder up from this repo) is a small standalone page for the AIST server that redirects here. Send it to the General Chair. It is not part of this repo and should not be uploaded to GitHub.
