# Changelog

All notable changes to the IEEE ISR/SIAS 2026 website are recorded here.
Newest entries first. Dates are in JST (YYYY-MM-DD).

## 2026-10-03 (later)

- **Navigation regrouped into dropdowns.** Eleven top-level links needed 1155px
  of header against a 1180px container — one line on a wide desktop with 25px
  to spare, and wrapped to two lines on anything narrower. Now eight: Committee
  sits under About, Poster under Submission, Accommodation under Venue. The
  header needs 937px. Important Dates deliberately stayed top-level; it is one
  of the most-visited pages on a conference site and does not belong behind
  About.
  - The footer keeps all eleven links flat, so every page is one click away.
  - Below 980px, where the header already stacks, the dropdowns flatten back
    into a plain inline list and the toggles disappear. No JavaScript is needed
    at that width.
  - On wider screens the menus open on hover, on keyboard focus, and on click.
    The click handler adds Escape-to-close and click-outside-to-close. With
    JavaScript off, hover and focus still work, and the footer is the backstop.
  - Removed two dead rules, `.nav-toggle` and `.nav-toggle-label`, left over
    from a mobile menu that was never built. The first collided with the new
    toggle button.
- **Poster submission needs a one-page PDF after all.** An earlier reading of
  the General Chair's reply took "the system does not handle poster data" to
  mean no upload at all. It refers to the A0 poster. Authors submit both the
  abstract (2,000 characters, in the form) and a one-page PDF carrying the
  abstract and one representative figure.
- **Home page** now leads with the poster deadline: "Submit a Poster" is the
  primary call to action, the hero card carries the October 25 date, and a
  dated announcement was added. Paper submission has closed, so the poster is
  the only thing authors can still act on.

## 2026-10-03

- **Poster presentation page added** (`poster.html`), linked from the navigation
  and footer of every page. Content confirmed by the General Chair and checked
  against the live PaperPlaza entry (ConfID 586), which shows a "Poster Paper"
  track open from September 22 to October 25, 2026. Submission is the abstract
  only, typed into the PaperPlaza form, maximum 2,000 characters (400-500 words
  is a guide, not the limit). No peer review, no file upload, no IEEE Xplore.
  A0 single sheet, agreed with INTEX Osaka. Registration fee is the same as for
  oral presenters. The abstract book lists poster number, title and authors.
  Authors of regular papers that are not accepted are invited to present as
  posters and do not resubmit.
- **Deadline time zone corrected.** Important Dates claimed "23:59 Anywhere on
  Earth". PaperPlaza enforces 23:59:59 Pacific Time, which is about 17 hours
  earlier, so the site had been promising authors most of an extra day. This
  was flagged as unverified in the README from the start; PaperPlaza settles it.
- **Important Dates** gained the October 25 poster deadline row.

## 2026-09-29

- **Submission closed.** The site had been telling authors that submission was
  open for 24 days after the September 5 deadline passed, with a live "Submit
  Your Paper" button. `submission.html` now states that submission is closed and
  papers are under review; the PaperPlaza link is kept, relabelled "Open IEEE
  RAS PaperPlaza", so authors can still sign in and view their own submission.
  The "Where do I submit my paper?" FAQ became "Can I still submit a paper?".
- **Important Dates:** The page notice no longer announces the extension to
  September 5; it now states that submission is closed and gives the next two
  milestones. The paper-submission row's status changed from "Extended" to
  "Closed" and its struck-out August 28 date was dropped, the extension history
  having stopped being useful once the deadline passed.
- **Home page:** Hero card switched from "Next deadline — September 5" to
  "Next milestone — October 18, 2026" (notification of acceptance). The
  highlight on the Key Deadlines row moved from Paper Submission to
  Notification. The closing call to action changed from "Call for Papers is
  open" to "Papers are under review". Added a September 5 announcement that
  submission has closed.
- **`_tools/build.py`** updated in step; all ten pages verified to regenerate
  byte-identical.

## 2026-09-01

- **Key dates strike-through:** Changed the previous-deadline (struck-out) date
  on the home Key Deadlines card and the Important Dates table from August 1 to
  August 28, to match the corrected hero subtitle.
- **Home hero:** Corrected the deadline subtitle to "extended from August 28,
  2026" (the deadline authors were working to), instead of August 1.
- **Deadline extended to September 5, 2026.** Updated every operative mention of
  the paper submission deadline (home hero, key dates, CFP line, dates page,
  submission page) from August 28 to September 5. Added a new dated announcement
  at the top of the home page; the historical July 31 announcement is left as-is.
  HP-only change — PaperPlaza already accepts submissions until September 5.

## 2026-08-07


- **Home:** The "NEW" badge on announcements is now automatic. Each dated
  announcement carries a `data-date`, and a small script shows the NEW badge
  only while the item is within the last 30 days, so it expires on its own.
  Applied in both `index.html` and `_tools/build.py`.

- **Home:** Reordered the "Latest Announcements" list to newest-first. The
  "Paper submission is now open" item (August 6) now sits at the top, above the
  two July 31 items (important dates, then Call for Papers). Applied in both
  `index.html` and the `_tools/build.py` template so they stay in sync.

## 2026-08-06

- **Submission open:** The submission system button on `submission.html` now links
  to IEEE RAS PaperPlaza (https://ras.papercept.net/conferences/scripts/start.pl)
  and is styled as a large primary call to action. The page notice changed from
  "will be announced shortly" to "now open", and the "Where do I submit?" FAQ
  answer was updated. The home page announcement changed from SOON to NEW.
  Note: this is the generic RAS PaperPlaza entry page listing all open RAS
  conferences, so both places tell authors to select "ISR-SIAS 2026" from the
  list. Replace with the conference-specific URL when it is available.
- **Contact:** `contact.html` now publishes the conference mailing list,
  M-isrsias2026-info-ml@aist.go.jp. The "address to be confirmed" warning was
  replaced with an informational note, and the three separate enquiry cards
  (General enquiries / Paper submission / Website) were removed, since all
  three resolved to the same address. Their subject wording was folded into
  the note so authors still know the one address covers submission questions.
  The "Where to Find Us" section was also removed: after the AIST gateway card
  went, its only remaining card linked to this site from this site.
- **AIST gateway link removed sitewide.** The AIST page now redirects here, so
  the footer link on all ten pages sent readers away and straight back. Removed
  from every footer and from `contact.html`.
- **`_tools/build.py` repaired and resynced.** It had a hardcoded absolute
  output path from the machine that generated it, so it crashed on any other
  computer; `OUT` is now derived from the script's own location. Its templates
  were also months out of date — running it would have wiped the registration
  fee table added on 2026-08-03 and reverted today's changes. All ten pages now
  regenerate byte-identical to what is committed.

## 2026-08-03

- **Registration:** Added the registration fee table (early-bird and on-site rates
  for IEEE member, non-member, and student categories, in JPY). Early-bird
  deadline marked as "to be announced". Updated the page notice accordingly.
- **Site launch:** Published the full conference site to GitHub Pages
  (https://isr2026.github.io/) — Home, About, Important Dates, Registration,
  Submission, Program, Venue, Accommodation, Committee, and Contact pages,
  plus assets, sitemap, robots.txt, and `.nojekyll`.
