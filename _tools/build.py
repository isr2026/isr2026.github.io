# -*- coding: utf-8 -*-
"""Emits plain static HTML for isr2026.github.io. Output needs no build step."""
import os, io

# Repo root: this script lives in _tools/, so write one level up.
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_URL   = "https://isr2026.github.io/"
CONF_TITLE = "IEEE ISR/SIAS 2026"
CONF_FULL  = ("2026 IEEE International Conference on Intelligence and Safety for Robotics / "
              "Safety of Industrial Automated Systems")
CONF_DATES = "December 2–4, 2026"
CONF_VENUE = "INTEX Osaka, Osaka, Japan"
CFP_PDF    = "assets/docs/ISRSIAS2026_cfp_2st.pdf"
# Generic IEEE RAS PaperPlaza entry page. Replace with the conference-specific
# URL when the Program Chair supplies it (see the note on the submission page).
SUBMIT_URL = "https://ras.papercept.net/conferences/scripts/start.pl"
CONTACT_EMAIL = "M-isrsias2026-info-ml@aist.go.jp"

NAV = [
    ("index.html",        "Home"),
    ("about.html",        "About"),
    ("dates.html",        "Important Dates"),
    ("registration.html", "Registration"),
    ("submission.html",   "Submission"),
    ("poster.html",       "Poster"),
    ("program.html",      "Program"),
    ("venue.html",        "Venue"),
    ("accommodation.html","Accommodation"),
    ("committee.html",    "Committee"),
    ("contact.html",      "Contact"),
]

# Header navigation. A third element groups pages under a dropdown; the first
# child is the parent section's own page. NAV above stays flat and drives the
# footer, so every page is still one click away if the dropdowns never open.
HEADER_NAV = [
    ("index.html",        "Home",             None),
    (None,                "About",            [("about.html",        "About the Conference"),
                                               ("committee.html",    "Committee")]),
    ("dates.html",        "Important Dates",  None),
    ("registration.html", "Registration",     None),
    (None,                "Submission",       [("submission.html",   "Paper Submission"),
                                               ("poster.html",       "Poster Presentation")]),
    ("program.html",      "Program",          None),
    (None,                "Venue",            [("venue.html",        "Venue & Access"),
                                               ("accommodation.html","Accommodation")]),
    ("contact.html",      "Contact",          None),
]

def _nav(page):
    out = []
    for href, label, children in HEADER_NAV:
        if not children:
            cur = ' aria-current="page"' if href == page else ''
            out.append('        <a href="%s"%s>%s</a>' % (href, cur, label))
            continue
        gid = "navmenu-" + label.lower().replace(" ", "-")
        active = ' is-active' if any(h == page for h, _ in children) else ''
        out.append('        <div class="nav-group">')
        out.append('          <button type="button" class="nav-toggle%s" aria-expanded="false" aria-controls="%s">%s<span class="nav-caret" aria-hidden="true"></span></button>'
                   % (active, gid, label))
        out.append('          <div class="nav-menu" id="%s">' % gid)
        for h, l in children:
            cur = ' aria-current="page"' if h == page else ''
            out.append('            <a href="%s"%s>%s</a>' % (h, cur, l))
        out.append('          </div>')
        out.append('        </div>')
    return "\n".join(out)

def head(page, title, desc):
    nav = _nav(page)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | {CONF_TITLE}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{SITE_URL}{'' if page == 'index.html' else page}" />

  <!-- Social sharing -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{CONF_TITLE}" />
  <meta property="og:title" content="{title} | {CONF_TITLE}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{SITE_URL}{'' if page == 'index.html' else page}" />
  <meta property="og:image" content="{SITE_URL}assets/img/Osaka.png" />
  <meta name="twitter:card" content="summary_large_image" />

  <link rel="stylesheet" href="assets/css/style.css" />
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>

  <header class="site-header">
    <div class="header-inner">
      <a class="site-logo" href="index.html" aria-label="{CONF_TITLE} home">
        <span class="logo-mark" aria-hidden="true">ISR<br />SIAS</span>
        <span>{CONF_TITLE}</span>
      </a>

      <nav class="site-nav" aria-label="Main navigation">
{nav}
      </nav>
    </div>
  </header>
"""

def foot():
    links = "\n".join('        <li><a href="%s">%s</a></li>' % (h, l) for h, l in NAV)
    return f"""
  <footer class="site-footer">
    <div class="footer-inner">
      <ul class="footer-nav">
{links}
      </ul>

      <p>
        <strong>{CONF_TITLE}</strong><br />
        {CONF_DATES} &nbsp;&middot;&nbsp; {CONF_VENUE}
      </p>

      <div class="footer-logos">
        <a href="https://www.ieee.org/" target="_blank" rel="noopener noreferrer">
          <img class="logo-white" src="https://upload.wikimedia.org/wikipedia/commons/2/21/IEEE_logo.svg"
               alt="IEEE" width="110" height="38" />
        </a>
        <a href="https://www.neca.or.jp/" target="_blank" rel="noopener noreferrer">
          <img class="logo-white" src="assets/img/NECA_LOGO.png" alt="NECA" width="110" height="38" />
        </a>
      </div>

      <p>
        &copy; 2026 {CONF_TITLE}.
      </p>
    </div>
  </footer>

  <script>
    // Header dropdowns. Without this the menus still open on hover and on
    // keyboard focus (CSS), and every page is reachable from the footer.
    (function () {{
      var groups = [].slice.call(document.querySelectorAll('.nav-group'));
      if (!groups.length) return;

      function close(g) {{
        g.removeAttribute('data-open');
        var b = g.querySelector('.nav-toggle');
        if (b) b.setAttribute('aria-expanded', 'false');
      }}
      function closeAll(except) {{
        groups.forEach(function (g) {{ if (g !== except) close(g); }});
      }}

      groups.forEach(function (g) {{
        var btn = g.querySelector('.nav-toggle');
        if (!btn) return;
        btn.addEventListener('click', function () {{
          var open = g.getAttribute('data-open') === 'true';
          closeAll(g);
          if (open) {{
            close(g);
          }} else {{
            g.setAttribute('data-open', 'true');
            btn.setAttribute('aria-expanded', 'true');
          }}
        }});
        g.addEventListener('keydown', function (e) {{
          if (e.key === 'Escape' && g.getAttribute('data-open') === 'true') {{
            close(g);
            btn.focus();
          }}
        }});
      }});

      document.addEventListener('click', function (e) {{
        if (!e.target.closest('.nav-group')) closeAll(null);
      }});
    }})();
  </script>
</body>
</html>
"""

def hero(kicker, h1, lead, extra=""):
    return f"""
  <section class="hero compact">
    <div class="hero-inner">
      <div class="eyebrow">{kicker}</div>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      {extra}
    </div>
  </section>
"""

def tba(what, note=""):
    return f"""      <div class="tba">
        <h3>To be announced</h3>
        <p>{what}{(' ' + note) if note else ''}</p>
      </div>
"""

def write(page, title, desc, body):
    with io.open(os.path.join(OUT, page), "w", encoding="utf-8") as f:
        f.write(head(page, title, desc) + body + foot())
    print("wrote", page)

# ---------------------------------------------------------------- Home

write("index.html", "Home",
      f"{CONF_FULL}. {CONF_DATES}, {CONF_VENUE}.",
f"""
  <section class="hero">
    <div class="hero-inner split">
      <div>
        <div class="eyebrow">{CONF_DATES} &middot; Osaka, Japan</div>
        <h1>{CONF_TITLE}</h1>
        <p class="lead">
          {CONF_FULL}
        </p>
        <p class="lead"><em>Where robotics meets intelligence, safety, and wellbeing.</em></p>

        <div class="hero-meta">
          <span class="meta-pill">{CONF_DATES}</span>
          <span class="meta-pill">{CONF_VENUE}</span>
          <span class="meta-pill">IEEE Conference</span>
        </div>

        <div class="hero-actions">
          <a class="btn btn-primary" href="poster.html">Submit a Poster &rarr;</a>
          <a class="btn btn-outline" href="submission.html">Submission Information</a>
          <a class="btn btn-outline" href="{CFP_PDF}" target="_blank" rel="noopener noreferrer">
            Call for Papers (PDF)
          </a>
        </div>
      </div>

      <aside class="hero-card" aria-labelledby="next-deadline">
        <div class="status-label">Next milestone</div>
        <h2 id="next-deadline">October 18, 2026</h2>
        <p>Notification of paper acceptance. Submission closed on September 5, 2026.</p>
        <p><strong><a href="poster.html">Poster abstracts</a> are open until October 25, 2026.</strong></p>
        <p style="margin-bottom:0;">
          Camera-ready final papers are due November 2, 2026.
          <a href="dates.html">See all dates</a>
        </p>
      </aside>
    </div>
  </section>

  <main id="main">

    <section class="section" aria-labelledby="announcements">
      <div class="section-heading">
        <span class="kicker">Latest</span>
        <h2 id="announcements">Announcements</h2>
      </div>

      <div class="card">
        <ul class="announcement-list">
          <li class="announcement-item" data-date="2026-10-03">
            <span class="announcement-date">October 3, 2026</span>
            <a href="poster.html">
              Poster presentations &mdash; abstract submission is open until October 25, 2026
            </a>
          </li>

          <li class="announcement-item" data-date="2026-09-05">
            <span class="announcement-date">September 5, 2026</span>
            <a href="submission.html">
              Paper submission is now closed &mdash; notification of acceptance by October 18, 2026
            </a>
          </li>

          <li class="announcement-item" data-date="2026-09-01">
            <span class="announcement-date">September 1, 2026</span>
            <a href="dates.html">
              Paper submission deadline extended to September 5, 2026
            </a>
          </li>

          <li class="announcement-item" data-date="2026-08-06">
            <span class="announcement-date">August 6, 2026</span>
            <a href="submission.html">
              Paper submission is now open &mdash; submit via IEEE RAS PaperPlaza
            </a>
          </li>

          <li class="announcement-item" data-date="2026-07-31">
            <span class="announcement-date">July 31, 2026</span>
            <a href="dates.html">
              Important dates updated &mdash; paper submission deadline extended to August 28, 2026
            </a>
          </li>

          <li class="announcement-item">
            <span class="announcement-date">July 31, 2026</span>
            <a href="{CFP_PDF}" target="_blank" rel="noopener noreferrer">
              <span class="badge badge-pdf">PDF</span>
              Download the Call for Papers
            </a>
          </li>
        </ul>
      </div>

      <script>
        // Show the NEW badge only on announcements from the last 30 days.
        (function () {{
          var MAX_DAYS = 30;
          var today = new Date();
          document.querySelectorAll('.announcement-item[data-date]').forEach(function (item) {{
            var posted = new Date(item.getAttribute('data-date') + 'T00:00:00');
            var ageDays = (today - posted) / 86400000;
            if (ageDays < 0 || ageDays > MAX_DAYS) return;
            var link = item.querySelector('a');
            if (!link || link.querySelector('.badge-new')) return;
            var badge = document.createElement('span');
            badge.className = 'badge badge-new';
            badge.textContent = 'NEW';
            link.insertBefore(badge, link.firstChild);
          }});
        }})();
      </script>
    </section>

    <section class="section" aria-label="Conference imagery">
      <div class="image-strip">
        <img src="assets/img/ConceptImage1.png" alt="Robot and human collaboration concept" loading="lazy" />
        <img src="assets/img/Intex_Osaka.png" alt="INTEX Osaka convention centre" loading="lazy" />
        <img src="assets/img/ConceptImage2.png" alt="Industrial automation concept" loading="lazy" />
      </div>
    </section>

    <section class="section" aria-labelledby="about-short">
      <div class="section-heading">
        <span class="kicker">About</span>
        <h2 id="about-short">Intelligence, Safety, and Wellbeing</h2>
      </div>

      <div class="prose">
        <p>
          Humans and robot systems coexist with each other in various domains. Robots assist humans in
          both public and private spaces for transportation and servant purposes, where the environments
          including humans need to be recognised for autonomous and safe operations. Workers perform
          collaborative operations with industrial robots in factories, where autonomy is a major concern
          for manpower saving under workers' safety.
        </p>
        <p>
          {CONF_TITLE} brings together an international community of experts to discuss a way forward in
          robot systems for the future of safety and security with intelligence.
          <a href="about.html">Read more about the conference</a>.
        </p>
      </div>
    </section>

    <section class="section" aria-labelledby="key-dates">
      <div class="section-heading">
        <span class="kicker">Important Dates</span>
        <h2 id="key-dates">Key Deadlines</h2>
      </div>

      <div class="grid-4">
        <article class="card date-card">
          <div class="label">Paper Submission</div>
          <div class="date">September 5, 2026</div>
        </article>
        <article class="card date-card highlight">
          <div class="label">Notification</div>
          <div class="date">October 18, 2026</div>
        </article>
        <article class="card date-card">
          <div class="label">Camera-ready</div>
          <div class="date">November 2, 2026</div>
        </article>
        <article class="card date-card">
          <div class="label">Conference</div>
          <div class="date">Dec 2&ndash;4, 2026</div>
        </article>
      </div>
    </section>

    <section class="footer-cta">
      <div>
        <h2>Papers are under review</h2>
        <p>Submission closed September 5, 2026. Authors will be notified by October 18, 2026.</p>
      </div>
      <div class="hero-actions">
        <a class="btn btn-primary" href="submission.html">Submission Guide</a>
        <a class="btn btn-outline" href="{CFP_PDF}" target="_blank" rel="noopener noreferrer">Download CFP</a>
      </div>
    </section>

  </main>
""")

# ---------------------------------------------------------------- About

write("about.html", "About",
      f"About {CONF_TITLE}: scope, aims, and topics of interest.",
hero("About", "About the Conference",
     "An international forum on intelligence and safety for robotics and industrial automated systems.") +
f"""
  <main id="main">

    <section class="section">
      <div class="prose">
        <p>
          Humans and robot systems coexist with each other in various domains. Robots assist humans in both
          public and private spaces for transportation and servant purposes, where the environments including
          humans need to be recognised again for autonomous and safe operations. Workers perform collaborative
          operations with industrial robots in factories, where autonomy is a major concern for manpower saving
          under workers' safety. These examples show that intelligence and safety are indispensable for
          human&ndash;robot coexistence, and that they need to be elaborately integrated.
        </p>
        <p>
          The concept of safety has evolved from the goal of eliminating accidents &mdash; reducing negatives to
          zero &mdash; to a new approach focused on contributing to human health, productivity in the workplace,
          and job satisfaction through safety. In other words, research and development of technologies that
          connect safety to well-being, along with their effective application, are now paramount.
        </p>
        <p>
          {CONF_TITLE} brings together an international community of experts to discuss a way forward in robot
          systems for the future of safety and security with intelligence, by provisions of new research results
          and perspectives of future developments as well as achievements of social implementation.
        </p>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Scope</span>
        <h2>Topics of Interest</h2>
        <p>Topics of interest include, but are not limited to, the following areas.</p>
      </div>

      <div class="grid-2">
        <article class="card topic-card">
          <h3>System Integration for Safety and Health</h3>
          <ul>
            <li>Control technologies</li>
            <li>Robotics</li>
            <li>Network systems</li>
            <li>Integration platform</li>
            <li>Software design, hardware design</li>
            <li>Active and passive safety systems</li>
          </ul>
        </article>

        <article class="card topic-card">
          <h3>Artifacts</h3>
          <ul>
            <li>Mechatronics systems</li>
            <li>Automation</li>
            <li>Virtual reality</li>
            <li>Entertainment systems</li>
          </ul>
        </article>

        <article class="card topic-card">
          <h3>Health and Safety, Human Centered, Human in the Loop</h3>
          <ul>
            <li>Welfare systems</li>
            <li>Human factors</li>
            <li>Environment / ecological systems</li>
            <li>Bio systems</li>
            <li>Intelligent transportation systems</li>
          </ul>
        </article>

        <article class="card topic-card">
          <h3>Assistive Technologies</h3>
          <ul>
            <li>Large-scale system simulation</li>
            <li>Software systems</li>
            <li>Networking systems</li>
            <li>Decision making systems</li>
            <li>Recognition</li>
            <li>Human&ndash;robot interaction / collaboration</li>
          </ul>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Contribute</span>
        <h2>Workshops, Tutorials, and Special Sessions</h2>
      </div>

      <div class="grid-2">
        <article class="card">
          <h3>Workshops and Tutorials</h3>
          <p>
            Proposals for half-day or full-day workshops or tutorials should include the title, organisers,
            an abstract, a brief description of the area of interest, and a list of prospective speakers.
          </p>
          <p><strong>Proposal deadline:</strong> July 1, 2026 (closed)</p>
        </article>

        <article class="card">
          <h3>Special Sessions</h3>
          <p>
            Special sessions provide the opportunity to focus in detail on particular emerging topics which are
            not reflected in the list of conference tracks, or which represent a specific working field where
            researchers would like to meet and discuss advances.
          </p>
          <p><strong>Proposal deadline:</strong> July 1, 2026 (closed)</p>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Reference</span>
        <h2>Call for Papers</h2>
      </div>
      <div class="notice-box info">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>The CFP PDF is the official reference document.</strong>
          <p>
            <a href="{CFP_PDF}" target="_blank" rel="noopener noreferrer">Download the Call for Papers (PDF)</a>
          </p>
        </div>
      </div>
    </section>

  </main>
""")

# ---------------------------------------------------------------- Dates

write("dates.html", "Important Dates",
      f"Deadlines and key dates for {CONF_TITLE}.",
hero("Important Dates", "Important Dates",
     "Submission deadlines close at 23:59:59 Pacific Time, as enforced by PaperPlaza.") +
f"""
  <main id="main">

    <section class="section">
      <div class="notice-box info">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>Paper submission closed on September 5, 2026.</strong>
          <p>
            Papers are under peer review. The next milestone is notification of acceptance on
            <strong>October 18, 2026</strong>, followed by camera-ready final papers on
            <strong>November 2, 2026</strong>. The
            <a href="{CFP_PDF}" target="_blank" rel="noopener noreferrer">CFP PDF</a>
            is the official reference document.
          </p>
        </div>
      </div>

      <div class="table-wrap">
        <table class="date-table">
          <caption>Schedule for IEEE ISR/SIAS 2026</caption>
          <thead>
            <tr>
              <th scope="col">Date</th>
              <th scope="col">Milestone</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>July 1, 2026</td>
              <td>Deadline for proposals for Special Sessions</td>
              <td>Closed</td>
            </tr>
            <tr>
              <td>July 1, 2026</td>
              <td>Deadline for proposals for Workshops / Tutorials</td>
              <td>Closed</td>
            </tr>
            <tr>
              <td>September 5, 2026</td>
              <td>Deadline for paper submission (2&ndash;4 page extended abstract)</td>
              <td>Closed</td>
            </tr>
            <tr>
              <td><span class="date-old">September 30, 2026</span><br /><span class="date-new">October 18, 2026</span></td>
              <td>Notification of paper acceptance</td>
              <td>Updated</td>
            </tr>
            <tr>
              <td>October 25, 2026</td>
              <td>Deadline for <a href="poster.html">poster abstract</a> submission</td>
              <td>Open</td>
            </tr>
            <tr>
              <td><span class="date-old">October 13, 2026</span><br /><span class="date-new">November 2, 2026</span></td>
              <td>Deadline for camera-ready final papers</td>
              <td>Updated</td>
            </tr>
            <tr>
              <td>December 2&ndash;4, 2026</td>
              <td>Conference at {CONF_VENUE}</td>
              <td>Scheduled</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Registration</span>
        <h2>Registration Deadlines</h2>
      </div>
{tba('Author and early-bird registration deadlines will be published together with the registration fees.',
     'See the <a href="registration.html">Registration</a> page.')}
    </section>

  </main>
""")

# ---------------------------------------------------------------- Registration

write("registration.html", "Registration",
      f"Registration information and fees for {CONF_TITLE}.",
hero("Registration", "Registration",
     "Registration rates, categories, and the online registration system will be announced here.") +
f"""
  <main id="main">

    <section class="section">
      <div class="notice-box">
        <div class="notice-icon" aria-hidden="true">!</div>
        <div>
          <strong>Online registration is not yet open.</strong>
          <p>
            Registration fees are listed below. The early-bird deadline and the online
            registration system will be announced on this page shortly.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Fees</span>
        <h2>Registration Fees</h2>
        <p>
          All fees are shown in Japanese yen (JPY) and include applicable taxes. The
          early-bird registration deadline will be announced soon.
        </p>
      </div>

      <div class="table-wrap">
        <table class="date-table">
          <caption>IEEE ISR/SIAS 2026 registration fees (JPY)</caption>
          <thead>
            <tr>
              <th scope="col">Category</th>
              <th scope="col">Early-bird</th>
              <th scope="col">On-site</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>IEEE Member</td>
              <td>&yen;70,000</td>
              <td>&yen;80,000</td>
            </tr>
            <tr>
              <td>Non-member</td>
              <td>&yen;80,000</td>
              <td>&yen;90,000</td>
            </tr>
            <tr>
              <td>IEEE Member (Student)</td>
              <td>&yen;40,000</td>
              <td>&yen;50,000</td>
            </tr>
            <tr>
              <td>Non-member (Student)</td>
              <td>&yen;50,000</td>
              <td>&yen;60,000</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p style="color: var(--muted); font-size: 14px; margin-top: 14px;">
        Early-bird rates apply until the early registration deadline (to be announced).
        On-site rates apply thereafter, including registration at the venue.
      </p>
    </section>

    <section class="section">
      <div class="notice-box info">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>At least one author of each accepted paper is normally required to register.</strong>
          <p>Exact requirements will be confirmed when registration opens.</p>
        </div>
      </div>
    </section>

  </main>
""")

# ---------------------------------------------------------------- Submission

write("submission.html", "Submission",
      f"Paper submission guidelines and deadlines for {CONF_TITLE}.",
hero("Paper Submission", "Paper Submission",
     "Paper format, length requirements, and the submission process for IEEE ISR/SIAS 2026.") +
f"""
  <main id="main">

    <section class="section">
      <!--
        ==========================================================================
        WEB CHAIR NOTE - submission system
        Opened August 6, 2026; closed September 5, 2026. SUBMIT_URL is the
        GENERIC IEEE RAS PaperPlaza entry page, which lists every open RAS
        conference. The link is kept so authors can sign in and view their own
        submission; it is no longer presented as a call to action.
        Next milestone: notification of acceptance, October 18, 2026. When
        results go out, update this notice, the FAQ answer below, the hero card
        and key-date cards on index.html, and the status column in dates.html.
        ==========================================================================
      -->
      <div class="notice-box info">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>Paper submission is closed.</strong>
          <p>
            The submission deadline was <strong>September 5, 2026</strong>. Papers are now under
            peer review, and authors will be notified of the outcome by
            <strong>October 18, 2026</strong>. Camera-ready final papers are due
            <strong>November 2, 2026</strong>.
          </p>
        </div>
      </div>

      <div class="two-column">
        <div>
          <div class="section-heading">
            <span class="kicker">Requirements</span>
            <h2>Paper Requirements</h2>
          </div>

          <div class="card">
            <h3>At a glance</h3>
            <ul class="info-list">
              <li><span class="check" aria-hidden="true">&#10003;</span><span>The conference working language is <strong>English</strong>.</span></li>
              <li><span class="check" aria-hidden="true">&#10003;</span><span>Papers must be submitted electronically in <strong>PDF</strong> format.</span></li>
              <li><span class="check" aria-hidden="true">&#10003;</span><span>Initial submissions: <strong>2&ndash;4 page extended abstracts</strong>.</span></li>
              <li><span class="check" aria-hidden="true">&#10003;</span><span>Final manuscripts: <strong>4&ndash;6 pages</strong>, with up to two extra pages for an additional fee.</span></li>
              <li><span class="check" aria-hidden="true">&#10003;</span><span>All papers are <strong>peer-reviewed</strong>.</span></li>
              <li><span class="check" aria-hidden="true">&#10003;</span><span>Accepted papers will be submitted for inclusion in <strong>IEEE Xplore</strong>, subject to meeting IEEE Xplore's scope and quality requirements.</span></li>
            </ul>
          </div>
        </div>

        <div class="card">
          <h3>Submission portal</h3>
          <p>
            Submission through <strong>IEEE RAS PaperPlaza</strong> closed on
            <strong>September 5, 2026</strong>. Authors can still sign in to PaperPlaza to view
            their own submission; select <strong>ISR-SIAS 2026</strong> from the conference list.
          </p>
          <p>
            <a class="btn btn-blue btn-block"
               href="{SUBMIT_URL}"
               target="_blank" rel="noopener noreferrer">
              Open IEEE RAS PaperPlaza
            </a>
          </p>
          <p>
            <a class="btn btn-blue btn-block" href="{CFP_PDF}" target="_blank" rel="noopener noreferrer">
              Download Call for Papers (PDF)
            </a>
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Templates</span>
        <h2>Manuscript Preparation</h2>
        <p>
          Authors should prepare manuscripts using the standard IEEE conference paper format.
        </p>
      </div>

      <div class="grid-3">
        <article class="card">
          <h3>IEEE templates</h3>
          <p>Use the official IEEE conference proceedings templates (LaTeX and Word).</p>
          <p>
            <a href="https://www.ieee.org/conferences/publishing/templates.html"
               target="_blank" rel="noopener noreferrer">IEEE author templates</a>
          </p>
        </article>

        <article class="card">
          <h3>Initial submission</h3>
          <p>
            A 2&ndash;4 page extended abstract in PDF, prepared in the IEEE conference format and written
            in English.
          </p>
        </article>

        <article class="card">
          <h3>Final manuscript</h3>
          <p>
            4&ndash;6 pages. Up to two additional pages are permitted for an extra fee, payable at
            registration.
          </p>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Process</span>
        <h2>From Submission to Presentation</h2>
      </div>

      <div class="publication-flow">
        <div class="flow-item"><strong>Prepare</strong><span>Extended abstract, IEEE format</span></div>
        <div class="flow-item"><strong>Submit</strong><span>By September 5, 2026</span></div>
        <div class="flow-item"><strong>Review</strong><span>Peer review</span></div>
        <div class="flow-item"><strong>Notification</strong><span>October 18, 2026</span></div>
        <div class="flow-item"><strong>Camera-ready</strong><span>November 2, 2026</span></div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">FAQ</span>
        <h2>Frequently Asked Questions</h2>
      </div>

      <div class="faq">
        <details>
          <summary>How long should my initial submission be?</summary>
          <p>Initial submissions are 2&ndash;4 page extended abstracts in PDF format.</p>
        </details>

        <details>
          <summary>How long is the final manuscript?</summary>
          <p>
            Final manuscripts are 4&ndash;6 pages. Up to two extra pages are allowed for an additional fee.
          </p>
        </details>

        <details>
          <summary>Can I still submit a paper?</summary>
          <p>
            No. Submission closed on September 5, 2026. Papers already submitted through
            <a href="{SUBMIT_URL}" target="_blank" rel="noopener noreferrer">IEEE RAS PaperPlaza</a>
            are under review, with notification of acceptance by October 18, 2026.
          </p>
        </details>

        <details>
          <summary>Will accepted papers be published in IEEE Xplore?</summary>
          <p>
            Accepted papers will be submitted for inclusion in IEEE Xplore, subject to meeting IEEE Xplore's
            scope and quality requirements.
          </p>
        </details>

        <details>
          <summary>Who should I contact with submission questions?</summary>
          <p>Please see the <a href="contact.html">Contact</a> page.</p>
        </details>
      </div>
    </section>

  </main>
""")

# ---------------------------------------------------------------- Program

write("poster.html", "Poster Presentation",
      f"Poster presentation submission and presentation details for {CONF_TITLE}.",
hero("Poster Presentation", "Poster Presentation",
     "Submit a short abstract through PaperPlaza and present your work on an A0 poster board in Osaka.") +
f"""
  <main id="main">

    <!--
      ==========================================================================
      WEB CHAIR NOTE - poster page
      Content confirmed by the General Chair (Tanigawa) on 2026-10-03, and
      checked against the live PaperPlaza entry for ISR-SIAS 2026 (ConfID 586)
      on the same day. PaperPlaza shows the "Poster Paper" track as open:
      opened 2026-09-22, closes 2026-10-25, deadlines 23:59:59 Pacific Time.

      CONFIRMED by the General Chair:
        - Submission goes through PaperPlaza, same as regular papers. A poster
          track already exists there; the website only needs to link to it.
        - Abstract limit is 2,000 characters. That is the hard limit of the
          PaperPlaza form. 400-500 words is only a rough guide.
        - No peer review. Titles, authors and abstracts are checked for sanity
          only.
        - Authors of regular papers that are not accepted (IEEE asked for a
          70-80% acceptance rate) will be offered a poster slot.
        - Registration fee is identical to oral presentation. No new category.
        - A0, one sheet. Already agreed with INTEX Osaka.
        - Abstract book carries poster number, title and authors only.

      TWO ITEMS ARE SUBMITTED: the abstract, typed into the PaperPlaza form
      (2,000 character limit), and a one-page PDF carrying the abstract and one
      representative figure. Confirmed by the Website Chair 2026-10-03.
      The General Chair's phrase "the system does not handle poster data"
      refers to the A0 poster itself, which the author prints and brings to the
      venue; it does not exempt the one-page PDF.
      ==========================================================================
    -->

    <section class="section">
      <div class="notice-box success">
        <div class="notice-icon" aria-hidden="true">&#10003;</div>
        <div>
          <strong>Poster submission is open.</strong>
          <p>
            Submit through IEEE RAS PaperPlaza by <strong>October 25, 2026</strong>
            (23:59:59 Pacific Time). On the PaperPlaza page, select
            <strong>ISR-SIAS 2026</strong>, then choose <strong>Poster Paper</strong> from the list
            of submission types.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Overview</span>
        <h2>About the Poster Session</h2>
      </div>

      <div class="prose">
        <p>
          The poster session is for <strong>presentation and discussion</strong> rather than archival
          publication. It gives researchers a way to share work in progress, late-breaking results
          and industrial case studies, and to talk them through face to face with an audience in Osaka.
        </p>
        <p>
          Poster contributions are <strong>not peer-reviewed</strong>. Submitted titles, authors and
          abstracts are checked for scope and suitability only. Authors bring and mount their own
          poster at the venue; the A0 poster itself is never uploaded.
        </p>
        <p>
          Authors whose regular paper is not accepted will be invited to present their work as a
          poster instead. If that applies to you, your title and author list are already on file and
          you do not need to submit again &mdash; you will be contacted directly.
        </p>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">What to submit</span>
        <h2>Submission Requirements</h2>
      </div>

      <div class="grid-2">
        <article class="card">
          <h3>1. Poster abstract</h3>
          <p>
            Typed directly into the PaperPlaza submission form, in English.
          </p>
          <ul class="info-list">
            <li><span class="check" aria-hidden="true">&#10003;</span><span><strong>Maximum 2,000 characters</strong> &mdash; a hard limit set by the form</span></li>
            <li><span class="check" aria-hidden="true">&#10003;</span><span><strong>400&ndash;500 words</strong> as a rough guide</span></li>
            <li><span class="check" aria-hidden="true">&#10003;</span><span>Title and full author list</span></li>
          </ul>
        </article>

        <article class="card">
          <h3>2. One-page PDF</h3>
          <p>
            Uploaded with the submission: a single page carrying the abstract and one figure.
          </p>
          <ul class="info-list">
            <li><span class="check" aria-hidden="true">&#10003;</span><span><strong>About one page</strong>, free format</span></li>
            <li><span class="check" aria-hidden="true">&#10003;</span><span><strong>One representative figure</strong> or diagram</span></li>
            <li><span class="check" aria-hidden="true">&#10003;</span><span>PDF only</span></li>
          </ul>
        </article>
      </div>

      <div class="notice-box info" style="margin-top: 24px;">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>No IEEE template is required.</strong>
          <p>
            The one-page PDF is free format &mdash; it is read to check the content of your
            contribution, not typeset for publication, so it does not have to follow the IEEE
            conference paper format. Your A0 poster is a separate thing: print it yourself and bring
            it to the venue. Posters are not published in IEEE Xplore.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">How to submit</span>
        <h2>Submission Portal</h2>
      </div>

      <div class="two-column">
        <div>
          <div class="card">
            <h3>Step by step</h3>
            <ul class="info-list">
              <li><span class="check" aria-hidden="true">&#10003;</span><span>Open <strong>IEEE RAS PaperPlaza</strong> using the button</span></li>
              <li><span class="check" aria-hidden="true">&#10003;</span><span>Find <strong>ISR-SIAS 2026</strong> in the conference list</span></li>
              <li><span class="check" aria-hidden="true">&#10003;</span><span>Follow <strong>Submit a contribution to ISR-SIAS 2026</strong></span></li>
              <li><span class="check" aria-hidden="true">&#10003;</span><span>Choose the <strong>Poster Paper</strong> submission type</span></li>
            </ul>
          </div>
        </div>

        <div class="card">
          <h3>Submit your poster abstract</h3>
          <p>
            The poster track is open until <strong>October 25, 2026</strong>.
          </p>
          <p>
            <a class="btn btn-primary btn-lg btn-block"
               href="{SUBMIT_URL}"
               target="_blank" rel="noopener noreferrer">
              Submit Your Poster &rarr;
            </a>
          </p>
          <p style="color: var(--muted); font-size: 14px; margin-bottom: 0;">
            You do not need to log in to make a first submission.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Schedule</span>
        <h2>Poster Deadlines</h2>
      </div>

      <div class="table-wrap">
        <table class="date-table">
          <caption>Poster schedule for IEEE ISR/SIAS 2026</caption>
          <thead>
            <tr>
              <th scope="col">Date</th>
              <th scope="col">Milestone</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>September 22, 2026</td>
              <td>Poster submission opens on PaperPlaza</td>
              <td>Open</td>
            </tr>
            <tr>
              <td>October 25, 2026</td>
              <td>Deadline for poster abstract submission</td>
              <td>Open</td>
            </tr>
            <tr>
              <td>December 2&ndash;4, 2026</td>
              <td>Poster session at INTEX Osaka</td>
              <td>Scheduled</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p style="color: var(--muted); font-size: 14px; margin-top: 14px;">
        All PaperPlaza deadlines are 23:59:59 Pacific Time. Posters are not peer-reviewed, so there is
        no separate acceptance notification. See <a href="dates.html">Important Dates</a> for the
        full-paper schedule.
      </p>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">At the venue</span>
        <h2>Presenting Your Poster</h2>
        <p>
          Poster boards are provided at INTEX Osaka. Presenters bring and mount their own poster and
          stand with it during the session.
        </p>
      </div>

      <div class="grid-3">
        <article class="card">
          <h3>Poster size</h3>
          <p><strong>A0, one sheet</strong> per contribution.</p>
          <p style="color: var(--muted); font-size: 14px;">841 &times; 1189 mm. Agreed with INTEX Osaka.</p>
        </article>

        <article class="card">
          <h3>Bring your own poster</h3>
          <p>The A0 poster is not uploaded and not printed for you. Print it in advance and bring it with you.</p>
        </article>

        <article class="card">
          <h3>Registration</h3>
          <p>Poster presenters pay the <a href="registration.html">same registration fee</a> as oral presenters.</p>
          <p style="color: var(--muted); font-size: 14px;">There is no poster-only category.</p>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Publication</span>
        <h2>Abstract Book</h2>
      </div>

      <div class="notice-box info">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>Posters are listed by number, title and authors.</strong>
          <p>
            The conference abstract book carries the poster number, the title and the author list for
            each poster. Poster contributions are not peer-reviewed full papers and are
            <strong>not submitted to IEEE Xplore</strong>. Authors who want an archival publication
            should use the <a href="submission.html">regular paper track</a>.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">FAQ</span>
        <h2>Frequently Asked Questions</h2>
      </div>

      <div class="faq">
        <details>
          <summary>How long should the poster abstract be?</summary>
          <p>
            The PaperPlaza form accepts at most 2,000 characters, and that is the real limit.
            400&ndash;500 words is given as a rough guide, but if your text exceeds 2,000 characters
            the form will not accept it.
          </p>
        </details>

        <details>
          <summary>Are poster submissions peer-reviewed?</summary>
          <p>
            No. Titles, authors and abstracts are checked for scope and suitability only. There is no
            review process and no separate acceptance notification.
          </p>
        </details>

        <details>
          <summary>My regular paper was not accepted. Can I present a poster?</summary>
          <p>
            Yes. Authors of regular papers that are not accepted are invited to present as posters.
            Your title and author list are already on file, so you do not need to submit again; the
            organizers will contact you.
          </p>
        </details>

        <details>
          <summary>Do I upload my A0 poster to the submission system?</summary>
          <p>
            No. You upload a one-page PDF with your abstract and one figure. The A0 poster itself is
            never uploaded &mdash; print it yourself and bring it to INTEX Osaka.
          </p>
        </details>

        <details>
          <summary>Will my poster be published in IEEE Xplore?</summary>
          <p>
            No. The conference abstract book lists the poster number, title and authors. Posters are
            not submitted to IEEE Xplore.
          </p>
        </details>

        <details>
          <summary>Is the registration fee lower for poster presenters?</summary>
          <p>
            No. Registration is for attending the conference, so the fee is the same whether you
            present orally, present a poster, or do not present at all. See
            <a href="registration.html">Registration</a>.
          </p>
        </details>

        <details>
          <summary>Who should I contact about poster submissions?</summary>
          <p>
            Write to <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>
            and state that your enquiry concerns the poster session.
          </p>
        </details>
      </div>
    </section>

  </main>
""")

write("program.html", "Program",
      f"Technical program, keynotes, and schedule for {CONF_TITLE}.",
hero("Program", "Conference Program",
     "The technical program, keynote speakers, and session schedule will be published here.") +
f"""
  <main id="main">

    <section class="section">
      <div class="notice-box">
        <div class="notice-icon" aria-hidden="true">!</div>
        <div>
          <strong>The program will be published after paper notification.</strong>
          <p>
            Notification of acceptance is scheduled for <strong>October 18, 2026</strong>. The detailed
            program is expected to follow in November 2026.
          </p>
        </div>
      </div>

{tba('The technical program, including oral and poster sessions, special sessions, workshops, tutorials, and keynote speakers, will be published on this page.')}
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Structure</span>
        <h2>Planned Program Structure</h2>
        <p>Indicative only. The final structure will be confirmed with the detailed program.</p>
      </div>

      <div class="grid-3">
        <article class="card">
          <div class="step-number" aria-hidden="true">1</div>
          <h3>Day 1 &mdash; December 2</h3>
          <p>Workshops and tutorials, opening, keynote.</p>
        </article>
        <article class="card">
          <div class="step-number" aria-hidden="true">2</div>
          <h3>Day 2 &mdash; December 3</h3>
          <p>Technical sessions, special sessions, poster session.</p>
        </article>
        <article class="card">
          <div class="step-number" aria-hidden="true">3</div>
          <h3>Day 3 &mdash; December 4</h3>
          <p>Technical sessions, awards, closing.</p>
        </article>
      </div>
    </section>

  </main>
""")

# ---------------------------------------------------------------- Venue

write("venue.html", "Venue",
      f"Venue and access information for {CONF_TITLE} at {CONF_VENUE}.",
hero("Venue", "INTEX Osaka",
     f"{CONF_TITLE} will be held at INTEX Osaka, Osaka, Japan, {CONF_DATES}.") +
f"""
  <main id="main">

    <section class="section">
      <div class="two-column">
        <div>
          <div class="section-heading">
            <span class="kicker">Location</span>
            <h2>INTEX Osaka</h2>
          </div>
          <div class="prose">
            <p>
              INTEX Osaka is one of Japan's largest international exhibition and convention centres, located
              on Sakishima Island in Osaka Bay. It regularly hosts large international conferences and
              exhibitions.
            </p>
            <p>
              <strong>Address:</strong> 1-5-102 Nanko-kita, Suminoe-ku, Osaka 559-0034, Japan<br />
              <strong>Website:</strong>
              <a href="https://www.intex-osaka.com/en/" target="_blank" rel="noopener noreferrer">intex-osaka.com</a>
            </p>
            <p>
              The specific halls and meeting rooms used by {CONF_TITLE} will be confirmed with the
              conference program.
            </p>
          </div>
        </div>

        <div>
          <img src="assets/img/Intex_Osaka.png" alt="INTEX Osaka convention centre"
               style="border-radius:var(--radius-lg);" />
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Getting there</span>
        <h2>Access</h2>
        <p>
          INTEX Osaka is served by three stations. Walking times below are from the venue operator; please
          confirm current timetables before travelling.
        </p>
      </div>

      <div class="grid-3">
        <article class="card">
          <h3>Nakafuto Station</h3>
          <p>
            Osaka Metro New Tram (Nanko Port Town Line). Approximately <strong>5 minutes on foot</strong> &mdash;
            the closest station to the venue.
          </p>
        </article>

        <article class="card">
          <h3>Trade Center-mae Station</h3>
          <p>
            Osaka Metro New Tram (Nanko Port Town Line). Approximately <strong>8 minutes on foot</strong>.
          </p>
        </article>

        <article class="card">
          <h3>Cosmosquare Station</h3>
          <p>
            Osaka Metro Chuo Line. Approximately <strong>9 minutes on foot</strong>, or transfer to the
            New Tram.
          </p>
        </article>
      </div>

      <div class="notice-box info" style="margin-top:22px;">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>INTEX Osaka advises Chuo Line passengers to use Cosmosquare rather than Nakafuto</strong>,
          as Nakafuto becomes very crowded during large events.
          <p>
            Indicative journey times: approximately 40 minutes from Osaka (Umeda) or Namba, 45 minutes from
            Shin-Osaka, and 50 minutes from Kobe (Sannomiya). See the
            <a href="https://www.intex-osaka.com/en/access/train/" target="_blank" rel="noopener noreferrer">official
            access page</a> for full routes, fares, and access by car, plane, or ferry.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Airports</span>
        <h2>Arriving by Air</h2>
      </div>

      <div class="grid-2">
        <article class="card">
          <h3>Kansai International Airport (KIX)</h3>
          <p>
            The main international gateway to the Kansai region, connected to central Osaka by rail and
            limousine bus.
          </p>
        </article>

        <article class="card">
          <h3>Osaka International Airport (Itami, ITM)</h3>
          <p>
            Handles domestic flights, connected to central Osaka by limousine bus and the Osaka Monorail.
          </p>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Osaka</span>
        <h2>About the City</h2>
      </div>
      <div class="two-column">
        <div class="prose">
          <p>
            Osaka is Japan's second-largest metropolitan area, known for its food culture, historic sites
            including Osaka Castle, and its role as a centre for manufacturing and robotics research.
          </p>
          <p>
            December in Osaka is cool and generally dry. Visitors should bring warm clothing and check the
            forecast before travelling.
          </p>
        </div>
        <div>
          <img src="assets/img/Osaka.png" alt="View of Osaka" style="border-radius:var(--radius-lg);" loading="lazy" />
        </div>
      </div>
    </section>

    <section class="section">
      <div class="notice-box info">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>Visa support</strong>
          <p>
            Participants who require a visa to enter Japan should apply well in advance. Information on
            invitation letters for visa applications will be published with registration details.
          </p>
        </div>
      </div>
    </section>

  </main>
""")

# ---------------------------------------------------------------- Accommodation

write("accommodation.html", "Accommodation",
      f"Hotel and accommodation information for {CONF_TITLE} in Osaka.",
hero("Accommodation", "Accommodation",
     "Recommended hotels and booking information for conference participants.") +
f"""
  <main id="main">

    <section class="section">
      <div class="notice-box">
        <div class="notice-icon" aria-hidden="true">!</div>
        <div>
          <strong>Hotel information is being prepared.</strong>
          <p>
            Recommended hotels and any negotiated conference rates will be published on this page.
            December is a busy travel period in Japan, so participants are encouraged to plan early.
          </p>
        </div>
      </div>

{tba('A list of recommended hotels near INTEX Osaka and in central Osaka, together with booking instructions and any conference rates, will be published here.')}
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Guidance</span>
        <h2>Where to Stay</h2>
        <p>
          While the official hotel list is being prepared, the areas below are commonly used by conference
          participants. This is general guidance, not an endorsement or a booking arrangement.
        </p>
      </div>

      <div class="grid-3">
        <article class="card">
          <h3>Osaka Bay / Cosmosquare</h3>
          <p>
            Closest to INTEX Osaka, with a small number of hotels. Convenient for the venue but quieter in
            the evenings.
          </p>
        </article>

        <article class="card">
          <h3>Namba / Shinsaibashi</h3>
          <p>
            Central Osaka, with the widest choice of hotels, restaurants, and direct rail access to Kansai
            International Airport.
          </p>
        </article>

        <article class="card">
          <h3>Umeda / Osaka Station</h3>
          <p>
            The main transport hub, well connected to the wider Kansai region including Kyoto and Kobe.
          </p>
        </article>
      </div>
    </section>

  </main>
""")

# ---------------------------------------------------------------- Committee

COMMITTEE = [
    ("General Chair",           "Tamio Tanikawa",   "AIST, Japan"),
    ("General Co-Chair",        "Akio Noda",        "Osaka Institute of Technology, Japan"),
    ("Program Chair",           "Kazutsugu Suita",  "Daido University, Japan"),
    ("Program Co-Chair",        "Kuniaki Kawabata", "JAEA, Japan"),
    ("Finance Chair",           "Kenichi Ohara",    "Meijo University, Japan"),
    ("Local Arrangement Chair", "Tomohito Takubo",  "Osaka Metropolitan University, Japan"),
]

cards = "\n".join(f"""        <article class="card person-card">
          <div class="role">{role}</div>
          <div class="name">{name}</div>
          <div class="affil">{affil}</div>
        </article>""" for role, name, affil in COMMITTEE)

write("committee.html", "Committee",
      f"Organizing committee of {CONF_TITLE}.",
hero("Committee", "Organizing Committee",
     "The organizing committee of IEEE ISR/SIAS 2026.") +
f"""
  <main id="main">

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Organizing Committee</span>
        <h2>Conference Leadership</h2>
      </div>

      <div class="grid-3">
{cards}
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Program Committee</span>
        <h2>International Program Committee</h2>
      </div>
{tba('The full list of International Program Committee members and reviewers will be published here.')}
    </section>

    <section class="section">
      <div class="notice-box info">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>Committee updates</strong>
          <p>
            Additional chairs and committee members will be added as appointments are confirmed. For
            corrections, please use the <a href="contact.html">Contact</a> page.
          </p>
        </div>
      </div>
    </section>

  </main>
""")

# ---------------------------------------------------------------- Contact

write("contact.html", "Contact",
      f"Contact information for {CONF_TITLE}.",
hero("Contact", "Contact Us",
     "How to reach the IEEE ISR/SIAS 2026 organizing committee.") +
f"""
  <main id="main">

    <section class="section">
      <!--
        WEB CHAIR NOTE: one address covers every kind of enquiry. If separate
        addresses are created later, this is the only block to change.
      -->
      <div class="notice-box info">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>All enquiries go to the conference mailing list.</strong>
          <p>
            Questions about the conference, registration, paper submission, the review process,
            or this website should all be sent to
            <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.
            Please state the subject of your enquiry. Messages are handled by the organizing committee.
          </p>
        </div>
      </div>
    </section>

  </main>
""")

print("done")
