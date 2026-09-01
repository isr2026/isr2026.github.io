# Changelog

All notable changes to the IEEE ISR/SIAS 2026 website are recorded here.
Newest entries first. Dates are in JST (YYYY-MM-DD).

## 2026-09-01

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
