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
REGISTRATION_URL = "https://amarys-jtb.jp/isr2026/"
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

# Site-wide strip above the header pointing to the poster call. It hides
# itself once PaperPlaza closes. Extended to October 30 on 2026-10-25;
# 23:59:59 Pacific Time is PDT here (DST ends November 1), so 2026-10-31
# 06:59:59 UTC. Not shown on the poster page itself.
POSTER_CLOSES_UTC = "2026-10-31T07:00:00Z"

def poster_banner(page):
    if page == "poster.html":
        return ""
    return """
  <div class="site-banner" id="poster-banner">
    <div class="site-banner-inner">
      <span><strong>Call for Posters</strong> &mdash; abstracts are open until <strong>October 30, 2026</strong></span>
      <a class="site-banner-link" href="poster.html">Submit a Poster &rarr;</a>
    </div>
  </div>
  <script>
    if (Date.now() > Date.parse('%s')) document.getElementById('poster-banner').hidden = true;
  </script>
""" % POSTER_CLOSES_UTC

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
{poster_banner(page)}
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
          <a class="btn btn-outline" href="submission.html">Submission Information</a>
          <a class="btn btn-outline" href="{CFP_PDF}" target="_blank" rel="noopener noreferrer">
            Call for Papers (PDF)
          </a>
        </div>
      </div>

      <aside class="hero-card poster-cta" aria-labelledby="poster-cta-title">
        <img class="poster-cta-photo" src="assets/img/poster-session-1.jpg" width="1400" height="1050"
             alt="Attendees discussing posters with presenters at a poster session" />
        <div class="poster-cta-body">
          <div class="status-label">&#9679; Call for Posters &mdash; open now</div>
          <h2 id="poster-cta-title">Poster Session</h2>
          <p class="poster-cta-deadline">Submit by <strong>October 30, 2026</strong></p>
          <p>Work in progress, late-breaking results and industrial case studies. Abstract + one-page PDF, no peer review.</p>
          <a class="btn btn-accent btn-lg btn-block" href="poster.html">Submit a Poster &rarr;</a>
          <p class="poster-cta-next">
            Accepted papers: camera-ready due <strong>November 2, 2026</strong> &middot;
            <a href="dates.html">All dates</a>
          </p>
        </div>
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
          <li class="announcement-item" data-date="2026-10-25">
            <span class="announcement-date">October 25, 2026</span>
            <a href="program.html">
              Program at a glance published &mdash; session schedule and rooms for all three days
            </a>
          </li>

          <li class="announcement-item" data-date="2026-10-25">
            <span class="announcement-date">October 25, 2026</span>
            <a href="poster.html">
              Poster submission deadline extended to October 30, 2026
            </a>
          </li>

          <li class="announcement-item" data-date="2026-10-20">
            <span class="announcement-date">October 20, 2026</span>
            <a href="submission.html">
              Notifications of paper acceptance have been sent &mdash; camera-ready final papers are due November 2, 2026
            </a>
          </li>

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
        <article class="card date-card">
          <div class="label">Notification</div>
          <div class="date">October 20, 2026</div>
        </article>
        <article class="card date-card highlight">
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
        <h2>Notifications have been sent</h2>
        <p>Authors of accepted papers: please submit your camera-ready paper by November 2, 2026.</p>
      </div>
      <div class="hero-actions">
        <a class="btn btn-primary" href="submission.html">Paper Submission</a>
        <a class="btn btn-outline" href="poster.html">Submit a Poster</a>
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
            Notifications of acceptance were sent on <strong>October 20, 2026</strong>.
            The next milestones are <a href="poster.html">poster abstracts</a> on
            <strong>October 30, 2026</strong> and camera-ready final papers on
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
              <td>October 20, 2026</td>
              <td>Notification of paper acceptance</td>
              <td>Sent</td>
            </tr>
            <tr>
              <td><span class="date-old">October 25, 2026</span><br /><span class="date-new">October 30, 2026</span></td>
              <td>Deadline for <a href="poster.html">poster abstract</a> submission</td>
              <td>Extended</td>
            </tr>
            <tr>
              <td><span class="date-old">October 13, 2026</span><br /><span class="date-new">November 2, 2026</span></td>
              <td>Deadline for camera-ready final papers</td>
              <td>Updated</td>
            </tr>
            <tr>
              <td>December 2&ndash;4, 2026</td>
              <td><a href="program.html">Conference</a> at {CONF_VENUE}</td>
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
      <div class="table-wrap">
        <table class="date-table">
          <caption>Registration deadlines (Japan Standard Time)</caption>
          <thead>
            <tr>
              <th scope="col">Date</th>
              <th scope="col">Milestone</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>October 31, 2026</td>
              <td>Online <a href="registration.html">registration</a> opens</td>
              <td>Scheduled</td>
            </tr>
            <tr>
              <td>November 6, 2026</td>
              <td>Early-bird registration deadline (23:59 JST)</td>
              <td>Scheduled</td>
            </tr>
            <tr>
              <td>November 20, 2026</td>
              <td>Regular registration deadline (23:59 JST)</td>
              <td>Scheduled</td>
            </tr>
            <tr>
              <td>December 2&ndash;4, 2026</td>
              <td>On-site registration at INTEX Osaka</td>
              <td>Scheduled</td>
            </tr>
          </tbody>
        </table>
      </div>
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
      <!--
        ==========================================================================
        WEB CHAIR NOTE - revised fees, 2026-10-26 (confirmed 2026-10-28)
        Figures and notice wording supplied by the Program Chair, who then
        confirmed two points: the IEEE Member (non-student) rate is unchanged
        because the member rate is the baseline the others are set against,
        and the structure is three tiers, Early / Regular / On-site, with
        Regular and On-site priced the same.
        REGISTRATION_URL is the JTB Amarys site. Before it opened it redirected
        to a Japanese session-error page, which is why the opening date sits
        next to the link.
        ==========================================================================
      -->
      <div class="notice-box">
        <div class="notice-icon" aria-hidden="true">!</div>
        <div>
          <strong>Notice of Revised Registration Fees &mdash; October 26, 2026</strong>
          <p>
            The registration fees previously published on this page have been revised to reflect
            IEEE requirements regarding member and non-member rates. Student registration fees have
            also been revised. The updated fees are shown in the table below.
          </p>
          <p>
            We apologize for any confusion these changes may cause.
          </p>
          <p>
            Registration deadlines are now confirmed and shown with the fees below.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="two-column">
        <div>
          <div class="section-heading">
            <span class="kicker">Register</span>
            <h2>Online Registration</h2>
          </div>
          <div class="prose">
            <p>
              Registration is handled through the conference registration site, operated by JTB.
              It is <strong>scheduled to open on October 31, 2026</strong>. We apologize for the
              delay.
            </p>
            <p>
              Early-bird registration closes at <strong>23:59 JST on November 6, 2026</strong>, and
              regular registration at <strong>23:59 JST on November 20, 2026</strong>.
            </p>
          </div>
        </div>

        <div class="card">
          <h3>Registration site</h3>
          <p>Opens <strong>October 31, 2026</strong>.</p>
          <p>
            <a class="btn btn-primary btn-lg btn-block" href="{REGISTRATION_URL}"
               target="_blank" rel="noopener noreferrer">
              Go to Registration &rarr;
            </a>
          </p>
          <p style="color: var(--muted); font-size: 14px; margin-bottom: 0;">
            <a href="{REGISTRATION_URL}" target="_blank" rel="noopener noreferrer">{REGISTRATION_URL}</a>
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Fees</span>
        <h2>Registration Fees</h2>
        <p>
          All fees are shown in Japanese yen and include Japanese consumption tax. Deadlines are
          Japan Standard Time.
        </p>
      </div>

      <div class="table-wrap">
        <table class="date-table fee-table">
          <caption>IEEE ISR/SIAS 2026 registration fees (JPY)</caption>
          <thead>
            <tr>
              <th scope="col">Category</th>
              <th scope="col">Early Bird<br /><span class="fee-when">on or before 23:59, November 6, 2026</span></th>
              <th scope="col">Regular<br /><span class="fee-when">on or before 23:59, November 20, 2026</span></th>
              <th scope="col">On-Site<br /><span class="fee-when">08:30 December 2 to 18:00 December 4, 2026</span></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">IEEE Member</th>
              <td>&yen;70,000</td>
              <td>&yen;80,000</td>
              <td>&yen;80,000</td>
            </tr>
            <tr>
              <th scope="row">NECA Member</th>
              <td>&yen;70,000</td>
              <td>&yen;80,000</td>
              <td>&yen;80,000</td>
            </tr>
            <tr>
              <th scope="row">Non-member</th>
              <td>&yen;85,000</td>
              <td>&yen;95,000</td>
              <td>&yen;95,000</td>
            </tr>
            <tr>
              <th scope="row">IEEE Life Member</th>
              <td>Free</td>
              <td>Free</td>
              <td>Free</td>
            </tr>
            <tr>
              <th scope="row">IEEE Member (Student)</th>
              <td>&yen;35,000</td>
              <td>&yen;40,000</td>
              <td>&yen;40,000</td>
            </tr>
            <tr>
              <th scope="row">Non-member (Student)</th>
              <td>&yen;43,000</td>
              <td>&yen;48,000</td>
              <td>&yen;48,000</td>
            </tr>
            <tr>
              <th scope="row">Accompanying person</th>
              <td colspan="3">&yen;10,000 &mdash; same at every stage</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p style="color: var(--muted); font-size: 14px; margin-top: 14px;">
        Regular and On-Site registration are charged at the same amount.
      </p>
    </section>

    <section class="section">
      <div class="grid-2">
        <article class="card">
          <h3>What registration includes</h3>
          <ul class="info-list">
            <li><span class="check" aria-hidden="true">&#10003;</span><span>Access to all sessions</span></li>
            <li><span class="check" aria-hidden="true">&#10003;</span><span>Banquet</span></li>
            <li><span class="check" aria-hidden="true">&#10003;</span><span>Welcome party</span></li>
            <li><span class="check" aria-hidden="true">&#10003;</span><span>Coffee breaks and lunch</span></li>
          </ul>
        </article>

        <article class="card">
          <h3>Accompanying person</h3>
          <p>&yen;10,000. Includes the social and catering program:</p>
          <ul class="info-list">
            <li><span class="check" aria-hidden="true">&#10003;</span><span>Banquet</span></li>
            <li><span class="check" aria-hidden="true">&#10003;</span><span>Welcome party</span></li>
            <li><span class="check" aria-hidden="true">&#10003;</span><span>Coffee breaks and lunch</span></li>
          </ul>
          <p style="color: var(--muted); font-size: 14px; margin-bottom: 0;">
            <strong>Does not include access to the sessions.</strong>
          </p>
        </article>
      </div>

      <div class="notice-box info" style="margin-top: 24px;">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>Receipts and the Japanese invoice system.</strong>
          <p>
            The IEEE ISR/SIAS 2026 Organizing Committee is not a registered invoice issuer, so
            receipts issued by the committee do not carry a Registration Number.
          </p>
        </div>
      </div>
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
        Notifications of acceptance were sent on October 20, 2026 (confirmed by
        the Program Chair; originally scheduled for October 18). Camera-ready
        deadline unchanged: November 2, 2026.
        ==========================================================================
      -->
      <div class="notice-box info">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>Paper submission is closed.</strong>
          <p>
            The submission deadline was <strong>September 5, 2026</strong>. Notifications of
            acceptance were sent on <strong>October 20, 2026</strong>. Camera-ready final papers are due
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
        <div class="flow-item"><strong>Notification</strong><span>October 20, 2026</span></div>
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
            have been reviewed, and notifications of acceptance were sent on October 20, 2026.
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
      opened 2026-09-22, closes 2026-10-30 (extended from 2026-10-25 by the
      Program Chair on 2026-10-25), deadlines 23:59:59 Pacific Time.

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
            Submit through IEEE RAS PaperPlaza by <strong>October 30, 2026</strong>
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
          <del>Authors whose regular paper is not accepted will be invited to present their work as a
          poster instead. If that applies to you, your title and author list are already on file and
          you do not need to submit again &mdash; you will be contacted directly.</del>
        </p>
        <p>
          <strong>Updated October 22, 2026.</strong> Authors of a paper that was not accepted who
          wish to take part in the poster session must make a <strong>new poster submission</strong>.
        </p>
        <p>
          There is currently a problem in the submission system affecting resubmission of
          non-accepted papers to the poster session. Once it is resolved, the Program Committee will
          contact the affected authors individually.
        </p>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">At the venue</span>
        <h2>What the Poster Session Looks Like</h2>
        <p>
          Each presenter stands by their A0 poster board and talks visitors through the work.
          Sessions are informal and conversation-driven &mdash; a good way to meet researchers and
          industry engineers working on robot safety.
        </p>
      </div>

      <div class="photo-grid">
        <img src="assets/img/poster-session-1.jpg" width="1400" height="1050" loading="lazy"
             alt="Attendees discussing posters with presenters at a poster session" />
        <img src="assets/img/poster-session-2.jpg" width="916" height="582" loading="lazy"
             alt="A presenter explaining a poster to a group of visitors" />
      </div>
      <p class="photo-caption">What a poster session looks like.</p>
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
            The poster track is open until <strong>October 30, 2026</strong>.
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
              <td><span class="date-old">October 25, 2026</span><br /><span class="date-new">October 30, 2026</span></td>
              <td>Deadline for poster abstract submission</td>
              <td>Extended</td>
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
            Yes, but you must make a new poster submission. Your earlier paper entry is not carried
            over into the poster session.
          </p>
          <p>
            There is currently a problem in the submission system affecting this. Once it is
            resolved, the Program Committee will contact the affected authors individually.
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
      f"Program at a glance, session schedule and rooms for {CONF_TITLE}.",
hero("Program", "Conference Program",
     "Program at a glance for the three conference days at INTEX Osaka.") +
f"""
  <main id="main">

    <!--
      ==========================================================================
      WEB CHAIR NOTE - program at a glance
      Built from the Program Chair's workbook conference_program_rooms_r6.xlsx,
      tab "公開用Program-at-glance", received 2026-10-25. The tables below are
      generated from that grid, not typed by hand.

      Session labels only (A11, B21, ...). Paper titles and authors are not in
      that file and are still to come; the notice below says so.

      Two things in the source grid to re-check with the Program Chair if the
      displayed times look wrong:
        - The time column skips 16:40 (it runs ... 16:00, 16:20, 17:00 ...),
          which is why Dec 2 Poster Session 1 reads 16:00-17:20 and the Dec 3
          afternoon break reads 16:20-17:00.
        - December 4 has nothing between 12:00 and 12:40, where the combined
          Lunch / Award / Closing block starts.
      ==========================================================================
    -->
    <section class="section">
      <div class="notice-box info">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>Program at a glance is now available.</strong>
          <p>
            The session structure and room allocation for all three days are below. The detailed
            session program &mdash; paper titles, authors and presentation order within each session
            &mdash; will be published on this page once it is finalised.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Schedule</span>
        <h2>Program at a Glance</h2>
        <p>
          All sessions take place at <a href="venue.html">INTEX Osaka</a>. Times are local
          (Japan Standard Time).
        </p>
      </div>

      <h3 id="day1">Day 1 &mdash; Wednesday, December 2, 2026</h3>
      <div class="table-wrap">
        <table class="date-table program-grid">
          <caption>Program at a glance &mdash; December 2, 2026</caption>
          <thead>
            <tr><th scope="col">Time</th><th scope="col">Room A</th><th scope="col">Room B</th><th scope="col">Conference Hall</th><th scope="col">Party Hall</th></tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">13:20&ndash;14:00</th>
              <td></td>
              <td></td>
              <td>Opening ceremony</td>
              <td></td>
            </tr>
            <tr>
              <th scope="row">14:20&ndash;15:40</th>
              <td>Session A11</td>
              <td>Session B11</td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <th scope="row">15:40&ndash;16:00</th>
              <td colspan="4" class="slot-break">Break</td>
            </tr>
            <tr>
              <th scope="row">16:00&ndash;17:20</th>
              <td></td>
              <td></td>
              <td>Poster Session 1</td>
              <td></td>
            </tr>
            <tr>
              <th scope="row">18:00&ndash;20:00</th>
              <td></td>
              <td></td>
              <td></td>
              <td>Welcome Party</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h3 id="day2">Day 2 &mdash; Thursday, December 3, 2026</h3>
      <div class="table-wrap">
        <table class="date-table program-grid">
          <caption>Program at a glance &mdash; December 3, 2026</caption>
          <thead>
            <tr><th scope="col">Time</th><th scope="col">Room A</th><th scope="col">Room B</th><th scope="col">Conference Hall</th><th scope="col">Party Hall</th></tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">09:00&ndash;10:20</th>
              <td>Session A21</td>
              <td>Session B21</td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <th scope="row">10:20&ndash;10:40</th>
              <td colspan="4" class="slot-break">Break</td>
            </tr>
            <tr>
              <th scope="row">10:40&ndash;12:00</th>
              <td>Session A22</td>
              <td>Session B22</td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <th scope="row">12:00&ndash;13:20</th>
              <td></td>
              <td></td>
              <td></td>
              <td class="slot-break">Lunch</td>
            </tr>
            <tr>
              <th scope="row">13:20&ndash;15:00</th>
              <td>Session A23</td>
              <td>Session B23</td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <th scope="row">15:00&ndash;15:20</th>
              <td colspan="4" class="slot-break">Break</td>
            </tr>
            <tr>
              <th scope="row">15:20&ndash;16:20</th>
              <td></td>
              <td></td>
              <td>Poster Session 2</td>
              <td></td>
            </tr>
            <tr>
              <th scope="row">16:20&ndash;17:00</th>
              <td colspan="4" class="slot-break">Break</td>
            </tr>
            <tr>
              <th scope="row">17:00&ndash;18:00</th>
              <td></td>
              <td></td>
              <td>Plenary Talk 1</td>
              <td></td>
            </tr>
            <tr>
              <th scope="row">19:00&ndash;21:00</th>
              <td></td>
              <td></td>
              <td></td>
              <td>Banquet</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h3 id="day3">Day 3 &mdash; Friday, December 4, 2026</h3>
      <div class="table-wrap">
        <table class="date-table program-grid">
          <caption>Program at a glance &mdash; December 4, 2026</caption>
          <thead>
            <tr><th scope="col">Time</th><th scope="col">Room A</th><th scope="col">Room B</th><th scope="col">Conference Hall</th><th scope="col">Party Hall</th></tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">09:20&ndash;10:20</th>
              <td></td>
              <td></td>
              <td>Plenary Talk 2</td>
              <td></td>
            </tr>
            <tr>
              <th scope="row">10:20&ndash;10:40</th>
              <td colspan="4" class="slot-break">Break</td>
            </tr>
            <tr>
              <th scope="row">10:40&ndash;12:00</th>
              <td>Session A31</td>
              <td>Session B31</td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <th scope="row">12:40&ndash;14:00</th>
              <td></td>
              <td></td>
              <td></td>
              <td>Lunch &middot; Award ceremony &middot; Closing ceremony</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section">
      <div class="grid-3">
        <article class="card">
          <h3>Parallel sessions</h3>
          <p>
            Oral sessions run in parallel in <strong>Room A</strong> and <strong>Room B</strong>.
            Session codes follow the pattern A11, B21 and so on.
          </p>
        </article>
        <article class="card">
          <h3>Poster sessions</h3>
          <p>
            Two poster sessions are held in the Conference Hall, on December 2 and December 3.
            See the <a href="poster.html">poster page</a> for submission and presentation details.
          </p>
        </article>
        <article class="card">
          <h3>Social program</h3>
          <p>
            A Welcome Party on December 2 and the Banquet on December 3, both in the Party Hall.
            Details will follow with the detailed program.
          </p>
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
      f"Where to stay for {CONF_TITLE} at INTEX Osaka.",
hero("Accommodation", "Accommodation",
     "Where to stay for IEEE ISR/SIAS 2026 at INTEX Osaka.") +
f"""
  <main id="main">

    <!--
      ==========================================================================
      WEB CHAIR NOTE - accommodation, written 2026-10-28
      Deliberately short: attendees are mostly domestic and do not need to be
      told how to book a hotel in Osaka. The useful part is that INTEX sits on
      an artificial island, so the walk-to-venue option is worth naming.

      Only hotels verified against their own official sites are named.
      Do NOT re-add Sakishima Cosmo Tower Hotel: Osaka Prefecture published a
      closure notice for it, although INTEX Osaka's own accommodation page
      still listed it. That page was down for maintenance when this was
      written, so re-check it before adding anything from there.
      ==========================================================================
    -->
    <section class="section">
      <div class="notice-box info">
        <div class="notice-icon" aria-hidden="true">i</div>
        <div>
          <strong>No conference hotel block has been arranged.</strong>
          <p>
            Participants book their own accommodation. Early December is a busy travel period in
            Japan, so please book early. The areas below are the ones conference participants
            normally use; naming a hotel here is guidance, not an endorsement or a booking
            arrangement.
          </p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-heading">
        <span class="kicker">Where to stay</span>
        <h2>Three Options</h2>
        <p>
          INTEX Osaka is on Sakishima, an artificial island in Osaka Bay. Staying on the island means
          walking to the venue; staying in the city means about 40 minutes each way.
        </p>
      </div>

      <div class="grid-3">
        <article class="card">
          <h3>Bayside &mdash; walk to the venue</h3>
          <p>
            A handful of hotels sit beside INTEX Osaka. Convenient, but quiet in the evening with few
            places to eat.
          </p>
          <p>
            <a href="https://www.princehotels.com/osakabay/" target="_blank" rel="noopener noreferrer">Grand
            Prince Hotel Osaka Bay</a> is roughly a 3-minute walk from the venue.
          </p>
        </article>

        <article class="card">
          <h3>Bentencho &mdash; 3 stops away</h3>
          <p>
            On the Chuo Line, three stops from Cosmosquare with no transfer, and also on the JR Osaka
            Loop Line. A reasonable middle ground.
          </p>
          <p>
            <a href="https://iconia.co.jp/en-us/hotel-art-hotel-osaka-bay-tower-osaka" target="_blank" rel="noopener noreferrer">ART
            HOTEL Osaka Bay Tower</a> is next to Bentencho Station.
          </p>
        </article>

        <article class="card">
          <h3>City centre &mdash; most choice</h3>
          <p>
            Namba, Shinsaibashi and Umeda have by far the widest choice of hotels and restaurants,
            and the best onward connections to Kyoto, Kobe and Kansai Airport.
          </p>
          <p>
            About 40 minutes to the venue, changing to the Chuo Line at Hommachi.
          </p>
        </article>
      </div>

      <p style="color: var(--muted); font-size: 14px; margin-top: 18px;">
        See the <a href="venue.html">Venue</a> page for full access details and journey times.
      </p>
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
