#!/usr/bin/env python3
"""Builds the SD Solutions static site from shared layout + page bodies.

Run:  python3 build.py
Edit SITE_URL below before publishing so canonical links and the sitemap are right.
"""
import os
import json

OUT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://www.sdsolutions.example"
EMAIL = "arvinmishraji@gmail.com"
PHONE = "+91 95555 86890"
PHONE_HREF = "+919555586890"
PHONE2 = "+91 88514 02921"
PHONE2_HREF = "+918851402921"
WHATSAPP_HREF = "919555586890"

# ------------------------------------------------------------------ icons
def icon(path, stroke=2.6):
    return ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (stroke, path))

I = {
    "doc": icon('<rect x="10" y="5" width="28" height="38" rx="5"/><path d="M17 16h14M17 23h14M17 30h8"/>'),
    "target": icon('<circle cx="24" cy="24" r="18"/><circle cx="24" cy="24" r="10"/><circle cx="24" cy="24" r="2.5" fill="currentColor"/><path d="M24 2v7M24 39v7M2 24h7M39 24h7"/>'),
    "send": icon('<path d="M6 22L42 6 26 42l-6-14z"/><path d="M42 6L20 28"/>'),
    "video": icon('<rect x="4" y="12" width="28" height="24" rx="6"/><path d="M32 21l12-7v20l-12-7"/><circle cx="14" cy="24" r="3" fill="currentColor"/>'),
    "check": icon('<path d="M9 25l10 10 20-22"/>', 3.4),
    "plus": icon('<path d="M24 8v32M8 24h32"/>', 4),
    "person": icon('<circle cx="24" cy="15" r="9"/><path d="M6 43c2-11 9-16 18-16s16 5 18 16"/><path d="M33 5l3 3 6-6"/>'),
    "reel": icon('<rect x="5" y="9" width="38" height="30" rx="7"/><path d="M20 18l11 6-11 6z" fill="currentColor"/>'),
    "role": icon('<rect x="5" y="14" width="38" height="26" rx="6"/><path d="M17 14V9a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v5"/><path d="M5 26h38"/>'),
    "mail": icon('<rect x="4" y="9" width="40" height="30" rx="6"/><path d="M6 13l18 14 18-14"/>'),
    "phone": icon('<path d="M10 5h8l3 10-5 3a24 24 0 0 0 14 14l3-5 10 3v8a4 4 0 0 1-4.4 4A38 38 0 0 1 6 9.4 4 4 0 0 1 10 5z"/>'),
    "chat": icon('<path d="M8 8h32a4 4 0 0 1 4 4v18a4 4 0 0 1-4 4H22l-10 8v-8H8a4 4 0 0 1-4-4V12a4 4 0 0 1 4-4z"/><path d="M14 18h20M14 25h12"/>'),
    "pin": icon('<path d="M24 44C12 30 10 24 10 19a14 14 0 0 1 28 0c0 5-2 11-14 25z"/><circle cx="24" cy="19" r="5"/>'),
    "cap": icon('<path d="M3 18L24 8l21 10-21 10z"/><path d="M11 23v11c0 3 6 6 13 6s13-3 13-6V23"/><path d="M45 18v13"/>'),
    "switch": icon('<path d="M6 15h31M29 7l8 8-8 8"/><path d="M42 33H11M19 25l-8 8 8 8"/>'),
    "back": icon('<circle cx="25" cy="26" r="16"/><path d="M25 17v9l6 4"/><path d="M5 14l2 9 9-2"/>'),
    "globe": icon('<circle cx="24" cy="24" r="18"/><path d="M6 24h36"/><path d="M24 6c-9 9-9 27 0 36M24 6c9 9 9 27 0 36"/>'),
    "lock": icon('<rect x="8" y="21" width="32" height="22" rx="6"/><path d="M14 21v-6a10 10 0 0 1 20 0v6"/><circle cx="24" cy="32" r="2.6" fill="currentColor"/>'),
    "up": icon('<path d="M24 41V9M10 23L24 9l14 14"/>', 3.6),
    "prev": icon('<path d="M30 10L16 24l14 14"/>', 3.6),
    "next": icon('<path d="M18 10l14 14-14 14"/>', 3.6),
}

SOC = [
    ("LinkedIn", '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M8 10.5V16M8 7.8v.01M12 16v-3a2.2 2.2 0 0 1 4.4 0v3M12 10.5V16"/>'),
    ("Instagram", '<rect x="3" y="3" width="18" height="18" rx="5.5"/><circle cx="12" cy="12" r="4"/><path d="M17.2 6.8v.01"/>'),
    ("X", '<path d="M5 4.5l14 15M19 4.5l-14 15"/>'),
    ("YouTube", '<rect x="3" y="6" width="18" height="12" rx="4"/><path d="M10.5 9.5l4 2.5-4 2.5z"/>'),
    ("WhatsApp", '<path d="M4 20l1.2-4.1A8 8 0 1 1 8.2 18.8z"/><path d="M9.2 8.8c.3 2.4 2.4 4.6 5 5.2l1.1-1.2-1.9-1-.9.7c-.7-.3-1.5-1.1-1.9-1.9l.7-.9-1-1.9z"/>'),
]

LOGO = ('<svg viewBox="0 0 36 36" aria-hidden="true"><rect x="2" y="2" width="32" height="32" rx="11" '
        'fill="#3678D4" stroke="#16324F" stroke-width="2.4"/><path d="M9 24l6-8 5 5 7-10" fill="none" '
        'stroke="#A8D8F0" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="27.5" cy="10.5" r="2.6" fill="#5BA7D1"/></svg>')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 36 36'%3E%3Crect x='2' y='2' "
           "width='32' height='32' rx='11' fill='%235B3CFF' stroke='%2315112B' stroke-width='2.4'/%3E%3Cpath d='M9 24l6-8 "
           "5 5 7-10' fill='none' stroke='%23FFD23F' stroke-width='3.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")

# ------------------------------------------------------------------ layout
NAV = [("index.html", "Home"), ("services.html", "Services"), ("process.html", "Process"),
       ("interview-coaching.html", "Interview prep"), ("about.html", "About"),
       ("reviews.html", "Reviews"), ("contact.html", "Contact")]


def header(active):
    links = "".join('<a href="%s"%s>%s</a>' % (h, ' class="active" aria-current="page"' if h == active else "", t)
                    for h, t in NAV)
    links += '<a class="nav-cta-mobile" href="contact.html">Get my free resume audit</a>'
    return ('<header class="site-header">\n  <nav class="nav" aria-label="Main">\n'
            '    <a href="index.html" class="logo" aria-label="SD Solutions home">' + LOGO + '<span>SD Solutions</span></a>\n'
            '    <div class="nav-links" id="site-menu">' + links + '</div>\n'
            '    <div class="nav-right">\n'
            '      <a href="contact.html" class="btn btn-sun btn-sm"><span class="btn-label">Free resume audit</span></a>\n'
            '      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-menu"><span></span><span></span><span></span></button>\n'
            '    </div>\n  </nav>\n</header>')


def footer():
    soc = "".join('<a href="#" aria-label="%s" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></a>' % (n, p)
                  for n, p in SOC)
    return '''<footer class="site-footer">
  <div class="foot-top">
    <span class="foot-glow g1" aria-hidden="true"></span><span class="foot-glow g2" aria-hidden="true"></span>
    <div class="wrap">
      <div class="foot-cta">
        <div>
          <h3>One career tip a week. No spam.</h3>
          <p>Short, practical notes on resumes, applications and interviews, from the people who read them for a living.</p>
        </div>
        <form class="sub-form" data-form="newsletter" novalidate aria-label="Newsletter signup">
          <div class="field">
            <label class="sr-only" for="sub-email">Email address</label>
            <input id="sub-email" name="email" type="email" placeholder="you@email.com" autocomplete="email" required data-required-msg="Add your email to subscribe.">
            <span class="err" role="alert"></span>
          </div>
          <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
          <button type="submit" class="btn btn-violet"><span class="btn-label">Send me the tips</span></button>
          <p class="sub-msg" role="status" aria-live="polite"></p>
        </form>
      </div>

      <div class="foot-grid">
        <div class="foot-brand">
          <a href="index.html" class="logo">''' + LOGO + '''<span>SD Solutions</span></a>
          <p>We rebuild your resume, point you at the right jobs, apply for you, and get you ready for the interview.</p>
          <div class="socials">''' + soc + '''</div>
        </div>
        <nav class="foot-col" aria-label="Services">
          <h4>Services</h4>
          <a href="services.html#resume">Resume rebuild</a>
          <a href="services.html#platform">Where to apply</a>
          <a href="services.html#submission">We hit submit</a>
          <a href="interview-coaching.html">Interview prep</a>
          <a href="services.html#plans">Packages</a>
        </nav>
        <nav class="foot-col" aria-label="Company">
          <h4>Company</h4>
          <a href="process.html">How it works</a>
          <a href="about.html">About us</a>
          <a href="reviews.html">Reviews</a>
          <a href="contact.html">Contact</a>
        </nav>
        <div class="foot-col">
          <h4>Say hi</h4>
          <ul class="foot-contact">
            <li>''' + I["mail"] + '''<a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a></li>
            <li>''' + I["phone"] + '''<a href="tel:''' + PHONE_HREF + '''">''' + PHONE + '''</a><br><a href="tel:''' + PHONE2_HREF + '''">''' + PHONE2 + '''</a></li>
            <li>''' + I["pin"] + '''<span>Jaipur, Rajasthan<br>Mon to Sat, 9 AM to 7 PM IST</span></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div class="foot-base">
    <span class="foot-glow g3" aria-hidden="true"></span><span class="foot-glow g4" aria-hidden="true"></span>
    <div class="wrap">
      <div class="wordmark" aria-hidden="true">SD Solutions</div>
      <div class="foot-legal">
        <span>&copy; 2026 SD Solutions. All rights reserved.</span>
        <nav class="legal-links" aria-label="Legal"><a href="privacy.html">Privacy policy</a><a href="terms.html">Terms of service</a><a href="contact.html">Contact</a></nav>
      </div>
    </div>
  </div>
</footer>'''


def page(filename, title, desc, body, active=None, three=False, schema=None, noindex=False):
    url = SITE_URL + "/" + ("" if filename == "index.html" else filename)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ''
    ld = ('<script type="application/ld+json">' + json.dumps(schema) + '</script>\n') if schema else ''
    scripts = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n' if three else '')
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta name="theme-color" content="#3678D4">
__ROBOTS__<link rel="canonical" href="__URL__">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SD Solutions">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="__URL__">
<meta name="twitter:card" content="summary">
<script>document.documentElement.classList.add('js')</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap" rel="stylesheet">
<link rel="icon" href="__FAVICON__">
<link rel="stylesheet" href="assets/css/styles.css">
__LD__</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><i></i></div>
__HEADER__
<main id="main">
__BODY__
</main>
__FOOTER__
<button class="to-top" type="button" aria-label="Back to top">__UP__</button>
__SCRIPTS__<script src="assets/js/main.js"></script>
</body>
</html>
'''
    for k, v in [("__TITLE__", title), ("__DESC__", desc), ("__ROBOTS__", robots), ("__URL__", url),
                 ("__FAVICON__", FAVICON), ("__LD__", ld), ("__HEADER__", header(active or filename)),
                 ("__BODY__", body), ("__FOOTER__", footer()), ("__UP__", I["up"]), ("__SCRIPTS__", scripts)]:
        html = html.replace(k, v)
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        html = html.replace('</body>', '<a class="whatsapp-float" href="https://wa.me/' + WHATSAPP_HREF + '" target="_blank" rel="noopener" aria-label="Chat on WhatsApp with ' + PHONE + '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20l1.2-4.5A8.5 8.5 0 1 1 20.5 11.5Z"/><path d="M8.5 8.5c.3 2.7 2.3 4.7 5 5l1.1-1.1-1.8-1-.8.7c-.7-.3-1.4-1-1.8-1.7l.7-.9-.9-1.8z"/></svg><span>Chat on WhatsApp</span></a>\n</body>')
        f.write(html)


# ------------------------------------------------------------------ components
DECO = '''<svg class="deco" viewBox="0 0 380 300" aria-hidden="true">
  <circle cx="250" cy="110" r="84" fill="#A8D8F0" stroke="#16324F" stroke-width="3"/>
  <path d="M40 250c30-44 60 44 90 0s60 44 90 0 60 44 90 0" fill="none" stroke="#5BA7D1" stroke-width="12" stroke-linecap="round"/>
  <path d="M118 30c3 22 17 36 38 38-21 2-35 16-38 38-3-22-17-36-38-38 21-2 35-16 38-38z" fill="#fff" stroke="#16324F" stroke-width="3" stroke-linejoin="round"/>
</svg>'''


def page_hero(crumb, title, lede):
    return ('<section class="page-hero">\n  <div class="wrap">\n'
            '    <div class="crumb"><a href="index.html">Home</a> / ' + crumb + '</div>\n'
            '    <h1>' + title + '</h1>\n    <p class="lede">' + lede + '</p>\n  </div>\n  ' + DECO + '\n</section>')


def cta(title, text, button="Book my free audit"):
    return ('<section class="section-tight">\n  <div class="wrap">\n    <div class="cta reveal" data-reveal="zoom">\n'
            '      <div><h2>' + title + '</h2><p>' + text + '</p></div>\n'
            '      <a href="contact.html" class="btn btn-ink"><span class="btn-label">' + button + '</span></a>\n'
            '    </div>\n  </div>\n</section>')


def ticks(items):
    return '<ul class="ticks">' + "".join("<li>" + I["check"] + t + "</li>" for t in items) + '</ul>'


def checks(items):
    return '<ul class="checks">' + "".join("<li>" + I["check"] + "<span>" + t + "</span></li>" for t in items) + '</ul>'


def quote(cls, text, initials, name, role, avatar_bg="#fff"):
    return ('<figure class="quote %s reveal"><blockquote>&ldquo;%s&rdquo;</blockquote>'
            '<figcaption class="by"><span class="avatar" style="background:%s">%s</span><span><b>%s</b><span>%s</span></span></figcaption></figure>'
            % (cls, text, avatar_bg, initials, name, role))


STEPS = [
    ("Audit", "A 30-minute call. We tell you what's working in your search and what isn't."),
    ("Rebuild", "Your new resume in three business days, with two rounds of edits."),
    ("Aim", "We match you to the job boards where people like you actually get replies."),
    ("Apply", "Five to ten tailored applications a week. You send them, or we do."),
    ("Rehearse", "Two recorded mock interviews and a written scorecard before the real one."),
]


def stairs():
    return '<div class="stairs">' + "".join(
        '<div class="step"><div class="n">%d</div><h3>%s</h3><p>%s</p></div>' % (i + 1, t, d)
        for i, (t, d) in enumerate(STEPS)) + '</div>'


def stats_band():
    return '''<section class="section band-grad">
  <div class="wrap">
    <div class="stats" data-stagger>
      <div class="stat reveal"><b data-count="1200" data-suffix="+">1,200+</b><span>Resumes rewritten</span></div>
      <div class="stat reveal"><b data-count="68" data-suffix="%">68%</b><span>Average callback rate</span></div>
      <div class="stat reveal"><b data-count="14">14</b><span>Job platforms tracked</span></div>
      <div class="stat reveal"><b data-count="40" data-suffix=" hrs">40 hrs</b><span>Saved per client on average</span></div>
    </div>
  </div>
</section>'''


# ================================================================== HOME
PLATFORMS = ["LinkedIn", "Naukri", "Indeed", "Glassdoor", "Wellfound", "Foundit", "Instahyre", "Cutshort",
             "Hirist", "Internshala", "Apna", "Google Jobs", "Company career pages", "Referral networks"]
marq_set = "".join("<li>%s</li>" % p for p in PLATFORMS)

SITUATIONS = [
    ("cap", "Fresh graduate", "No experience? Your resume still has to say something.",
     "Recruiters know you are early in your career. They still want proof that you can do the work.",
     ["We turn projects, internships and coursework into real evidence", "A list of boards and campus-to-career programs that actually hire freshers", "Entry-level interview drills, so the first one is not your first one"]),
    ("role", "Experienced professional", "You have the track record. It needs to read that way.",
     "Years of work get flattened into a list of duties. We bring the results back to the front.",
     ["Achievements rewritten with numbers and scope", "Senior-role targeting and recruiter outreach", "Mock interviews with the tougher questions"]),
    ("switch", "Career switcher", "Different field, same you.",
     "Your skills travel further than your last job title suggests. The resume has to make that obvious.",
     ["We translate your experience into the language of the new field", "Roles and companies that hire switchers", "Answers for the &ldquo;why the change?&rdquo; question"]),
    ("back", "Returning after a break", "A gap is not a red flag when it is explained well.",
     "Whether it was family, health, study or a hard year, you can tell it plainly and move on.",
     ["Honest, confident wording for the break", "A refreshed skills section so you look current", "Mock interviews to rebuild your confidence"]),
    ("globe", "Applying abroad", "Different country, different rules.",
     "Resume formats, job boards and interview styles change from one country to the next.",
     ["Your resume reformatted to the local norms", "The right job boards for your target country", "A walk-through of how interviews differ there"]),
]
tab_btns = "".join(
    '<button class="tab" role="tab" id="tab-%d" aria-controls="panel-%d" aria-selected="%s" tabindex="%s" type="button">%s<span>%s</span></button>'
    % (i, i, "true" if i == 0 else "false", "0" if i == 0 else "-1", I[ic], name)
    for i, (ic, name, *_r) in enumerate(SITUATIONS))
tab_panels = "".join(
    '<div class="tabpanel" role="tabpanel" id="panel-%d" aria-labelledby="tab-%d"%s><h3>%s</h3><p>%s</p>%s'
    '<a href="contact.html" class="btn btn-sun"><span class="btn-label">Talk to us about this</span></a></div>'
    % (i, i, "" if i == 0 else " hidden", head, body, checks(items))
    for i, (ic, name, head, body, items) in enumerate(SITUATIONS))

HERO_FALLBACK = '''<div class="hero-fallback" aria-hidden="true"><svg viewBox="0 0 400 400">
  <circle cx="200" cy="200" r="120" fill="none" stroke="#3678D4" stroke-width="64"/>
  <circle cx="200" cy="200" r="152" fill="none" stroke="#16324F" stroke-width="3" opacity=".3"/>
  <circle cx="330" cy="120" r="22" fill="#A8D8F0" stroke="#16324F" stroke-width="3"/>
  <rect x="52" y="262" width="40" height="40" rx="8" fill="#63C7B2" stroke="#16324F" stroke-width="3" transform="rotate(14 72 282)"/>
  <circle cx="80" cy="110" r="16" fill="#5BA7D1" stroke="#16324F" stroke-width="3"/>
</svg></div>'''

home = '''
<section class="hero">
  <span class="blob b1" aria-hidden="true"></span><span class="blob b2" aria-hidden="true"></span><span class="blob b3" aria-hidden="true"></span>
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <h1><span class="line"><span>Get hired.</span></span><span class="line"><span>Not ghosted.</span></span></h1>
        <p class="lede fade-in d1">We rebuild your resume, tell you exactly where to apply, hit submit for you, and put you through recorded mock interviews until the real one feels easy.</p>
        <div class="hero-actions fade-in d2">
          <a href="contact.html" class="btn btn-sun"><span class="btn-label">Get my free resume audit</span></a>
          <a href="process.html" class="btn btn-white"><span class="btn-label">See how it works</span></a>
        </div>
        <p class="proof fade-in d3"><b>1,200 resumes rewritten</b> so far, with an average callback rate of <b>68%</b>.</p>
      </div>
      <div class="hero-visual">
        <canvas id="hero-canvas" aria-hidden="true"></canvas>
        ''' + HERO_FALLBACK + '''
        <div class="chip chip-a"><span class="dot" style="background:#63C7B2">''' + I["check"] + '''</span><span>Resume rewritten<small>Passes the ATS filter</small></span></div>
        <div class="chip chip-b"><span class="dot" style="background:#A8D8F0">''' + I["send"] + '''</span><span>3 callbacks this week<small>From 8 applications</small></span></div>
        <div class="chip chip-c"><span class="dot" style="background:#5BA7D1">''' + I["video"] + '''</span><span>Mock interview recorded<small>Scorecard ready</small></span></div>
      </div>
    </div>
  </div>
</section>

<div class="marquee-band" aria-label="Job platforms we cover">
  <p class="marquee-title">Where we look for your next job</p>
  <div class="marquee">
    <div class="marquee-track">
      <ul class="marquee-set">''' + marq_set + '''</ul>
      <ul class="marquee-set" aria-hidden="true">''' + marq_set + '''</ul>
    </div>
  </div>
</div>

''' + stats_band() + '''

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>Four ways we get you closer to the offer</h2>
      <p>Pick one, or hand us the whole search.</p>
    </div>
    <div class="bento" data-stagger>
      <article class="tile t1 tilt reveal">
        <span class="tile-icon">''' + I["doc"] + '''</span>
        <h3>Resume rebuild</h3>
        <p>We take your resume apart and rebuild it for the job you actually want. It gets through the applicant-tracking filters and reads well to a human.</p>
        <a class="tile-link" href="services.html#resume">What's included</a>
      </article>
      <article class="tile t2 tilt reveal">
        <span class="tile-icon">''' + I["target"] + '''</span>
        <h3>Know where to apply</h3>
        <p>There are dozens of job boards. We tell you which ones fit your role and give you a ranked list every week.</p>
        <a class="tile-link" href="services.html#platform">How it works</a>
      </article>
      <article class="tile t3 tilt reveal">
        <span class="tile-icon">''' + I["send"] + '''</span>
        <h3>We hit submit</h3>
        <p>No time to apply? We send tailored applications for you. You approve every one first.</p>
        <a class="tile-link" href="services.html#submission">See the details</a>
      </article>
      <article class="tile t4 tilt reveal">
        <span class="tile-icon">''' + I["video"] + '''</span>
        <h3>Camera-ready interviews</h3>
        <p>Two recorded mock interviews, a written scorecard, and a plain guide to lighting, framing and profile photos. Watch yourself, fix it, walk in calm.</p>
        <a class="tile-link" href="interview-coaching.html">Explore interview prep</a>
      </article>
    </div>
  </div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>Whatever your situation, we have done it before</h2>
      <p>Pick the one that sounds like you.</p>
    </div>
    <div class="tabs reveal" data-tabs>
      <div class="tablist" role="tablist" aria-label="Your situation" aria-orientation="vertical">''' + tab_btns + '''</div>
      <div>''' + tab_panels + '''</div>
    </div>
  </div>
</section>

<section class="section band-ink">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>Five steps from stuck to hired</h2>
      <p>Same order every time, because each step sets up the next.</p>
    </div>
    ''' + stairs() + '''
    <p style="margin-top:36px"><a class="link-u" href="process.html" style="color:var(--sun)">Read the full process</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal" data-reveal="left">
      <h2>We fix the parts of a job search nobody else touches.</h2>
      <p style="margin-top:20px;font-size:19px">Most advice stops at &ldquo;polish your resume.&rdquo; We stay with you through the applications and the interview, because that is where offers are won or lost.</p>
    </div>
    <div class="facts" data-stagger>
      <div class="fact reveal">''' + I["person"] + '''<div><h3>Real recruiters read your resume</h3><p>Everything we write is checked by someone who has screened hundreds of them.</p></div></div>
      <div class="fact reveal">''' + I["reel"] + '''<div><h3>Everything is on video</h3><p>Mock interviews are recorded and yours to keep. Watch them the night before.</p></div></div>
      <div class="fact reveal">''' + I["role"] + '''<div><h3>Built around your target role</h3><p>No templates. Every resume and apply list is written for the jobs you are chasing.</p></div></div>
    </div>
  </div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="section-head reveal"><h2>People who stopped getting ghosted</h2></div>
    <div class="carousel reveal" data-carousel role="region" aria-roledescription="carousel" aria-label="Client stories">
      <div class="viewport">
        <div class="track">
          <figure class="slide" aria-label="Story 1 of 3">
            <blockquote>&ldquo;The apply list alone was worth it. I was sending fifteen applications a week that were never going to land. Once they changed where I applied, I had three first-round calls in eight days.&rdquo;</blockquote>
            <figcaption class="by"><span class="avatar">AR</span><span><b>Ananya R.</b><span>Data analyst</span></span></figcaption>
          </figure>
          <figure class="slide" aria-label="Story 2 of 3" aria-hidden="true">
            <blockquote>&ldquo;Watching my own mock interview was uncomfortable and exactly what I needed. The real one felt like a rerun.&rdquo;</blockquote>
            <figcaption class="by"><span class="avatar">RK</span><span><b>Rohit K.</b><span>Product manager</span></span></figcaption>
          </figure>
          <figure class="slide" aria-label="Story 3 of 3" aria-hidden="true">
            <blockquote>&ldquo;I sent them a resume I was embarrassed by. Three days later I wanted to hand it to a recruiter.&rdquo;</blockquote>
            <figcaption class="by"><span class="avatar">MS</span><span><b>Meera S.</b><span>UX designer</span></span></figcaption>
          </figure>
        </div>
      </div>
      <div class="car-controls">
        <div class="dots">
          <button type="button" aria-label="Show story 1" aria-current="true"></button>
          <button type="button" aria-label="Show story 2" aria-current="false"></button>
          <button type="button" aria-label="Show story 3" aria-current="false"></button>
        </div>
        <div class="arrows">
          <button type="button" class="arrow" data-prev aria-label="Previous story">''' + I["prev"] + '''</button>
          <button type="button" class="arrow" data-next aria-label="Next story">''' + I["next"] + '''</button>
        </div>
      </div>
    </div>
    <p style="margin-top:30px"><a class="link-u" href="reviews.html">Read more stories</a></p>
  </div>
</section>

''' + cta("Applying everywhere and hearing nothing?", "Book a free 20-minute audit. We will tell you exactly what is holding your applications back.")

schema = {
    "@context": "https://schema.org", "@type": "ProfessionalService", "name": "SD Solutions",
    "description": "Career consultancy that rebuilds resumes, advises on job platforms, submits applications and coaches interviews.",
    "url": SITE_URL, "email": EMAIL, "telephone": PHONE,
    "address": {"@type": "PostalAddress", "addressLocality": "Jaipur", "addressRegion": "Rajasthan", "addressCountry": "IN"},
}
page("index.html", "SD Solutions | Get hired. Not ghosted.",
     "SD Solutions rebuilds your resume, tells you where to apply, submits applications for you and coaches you through recorded mock interviews.",
     home, three=True, schema=schema)

# ================================================================== SERVICES
def svc(cls, id_, label, icon_key, title, desc, items):
    return ('<article class="svc %s reveal" id="%s"><div class="svc-side">%s<b>%s</b></div>'
            '<div class="svc-main"><h3>%s</h3><p class="desc">%s</p>%s</div></article>'
            % (cls, id_, I[icon_key], label, title, desc, ticks(items)))


def plan(name, blurb, items, featured=False):
    return ('<article class="plan%s reveal">%s<h3>%s</h3><p class="for">%s</p><div class="quote-line">Custom quote</div>%s'
            '<a href="contact.html" class="btn %s"><span class="btn-label">Get a quote</span></a></article>'
            % (" featured" if featured else "", '<span class="ribbon">Most popular</span>' if featured else "",
               name, blurb, checks(items), "btn-sun" if featured else "btn-white"))


services = page_hero("Services", "Pick a service. Or hand us the whole search.",
    "Every engagement starts with a free audit, then goes wherever your search is stuck: the resume, the applications or the interview.") + '''
<section class="section">
  <div class="wrap-narrow" style="max-width:1000px">
''' + svc("s1", "resume", "Resume", "doc", "Resume rebuild",
    "We take your current resume apart line by line and rebuild it around the roles you want. It clears the applicant-tracking filters, matches the language in your target job descriptions, and gets checked by a recruiter who has read the real thing.",
    ["Full rewrite, not a template swap", "ATS-safe formatting check", "Two rounds of edits", "LinkedIn headline and summary", "Delivered in 3 business days", "Cover letter template"]) \
  + svc("s2", "platform", "Where to apply", "target", "Know where to apply",
    "Most people apply everywhere and get seen nowhere. We tell you which platforms fit your role and seniority, including the niche boards nobody thinks to check, then give you a ranked list each week so your time goes to jobs you can win.",
    ["Review of 14+ job platforms", "Weekly ranked apply list", "Fit score against your resume", "Niche board picks", "Recruiter outreach templates", "Application tracker set up for you"]) \
  + svc("s3", "submission", "Submission", "send", "We hit submit",
    "Job hunting while employed? The problem is usually hours, not strategy. We submit tailored applications for you, track every reply, and flag the ones that need a nudge from you.",
    ["5 to 10 tailored applications a week", "Custom note for each role", "Reply tracking dashboard", "Follow-up reminders", "Weekly summary", "You approve every send"]) \
  + svc("s4", "interview", "Interviews", "video", "Camera-ready interviews",
    'Live mock interviews, recorded and reviewed with you: pacing, structure, body language and what you actually say. Plus a plain guide to your camera setup and profile photos. <a class="link-u" href="interview-coaching.html">See the full interview prep page</a>.',
    ["Two recorded mock interviews", "Question bank for your role", "Written scorecard", "Video and photo guide", "Lighting and framing checklist", "Recordings are yours to keep"]) + '''
  </div>
</section>

<section class="section band" id="plans">
  <div class="wrap">
    <div class="section-head center reveal">
      <h2>Three ways to work with us</h2>
      <p>Prices depend on your role and seniority, so we quote after the free audit. You never pay for the audit.</p>
    </div>
    <div class="plans" data-stagger>
''' + plan("Resume only", "A strong search is already running and the resume needs to catch up.",
           ["Full resume rebuild", "ATS-safe formatting check", "LinkedIn headline and summary", "Two rounds of edits", "Cover letter template"]) \
    + plan("Job search plan", "You want a resume and a clear plan for where to apply.",
           ["Everything in Resume only", "Review of 14+ job platforms", "Weekly ranked apply list", "Recruiter outreach templates", "Application tracker set up for you"], True) \
    + plan("Full runway", "You want us on the whole search, all the way to the interview.",
           ["Everything in Job search plan", "We submit 5 to 10 applications a week", "Two recorded mock interviews", "Written scorecard", "Video and photo guide"]) + '''
    </div>
  </div>
</section>
''' + cta("Not sure which one you need?", "Start with the free audit. We will tell you which step is holding your search back.", "Get my free audit")

page("services.html", "Services | SD Solutions",
     "Resume rebuild, job platform strategy, done-for-you applications and recorded interview prep from SD Solutions.", services)

# ================================================================== PROCESS
details = [
    ("1", "Audit", "We start with a 30-minute call about your resume, LinkedIn profile and the roles you want. You leave with a plain-language read on what is working, what is not, and which of our services will actually help.", "Takes 30 minutes. Notes the same day."),
    ("2", "Rebuild", "We rebuild your resume for the roles you are targeting, with formatting that passes applicant-tracking filters and wording a recruiter will read past the first six seconds.", "Ready in 3 business days, with 2 rounds of edits."),
    ("3", "Aim", "We match your new profile to the platforms where you have the best odds, from the big boards to niche communities and direct recruiter networks, so you stop spreading effort across places that never reply.", "Takes 2 business days. You get a ranked list."),
    ("4", "Apply", "Now the applying starts: five to ten targeted roles a week, walked through with you or sent for you, depending on your plan. Every application is tailored. Nothing is copy-pasted.", "Weekly rhythm. Every reply is logged."),
    ("5", "Rehearse", "Once calls start landing, we run two full recorded mock interviews against questions for your role, then send a written scorecard on structure, clarity and delivery.", "Two sessions, plus a scorecard."),
]
detail_html = "".join('<div class="detail reveal"><div class="big">%s</div><div><h3>%s</h3><p>%s</p><span class="when">%s</span></div></div>' % d for d in details)

faqs = [
    ("How long does the whole thing take?", "Most people go from audit to a first interview in three to five weeks. It depends on how fast roles open up in your field and how many hours a week you can give to applying."),
    ("Can I skip ahead if my resume is already strong?", "Yes. The audit tells us whether your resume needs a rebuild or a light polish. If it is already strong, we go straight to aiming and applying."),
    ("Do you guarantee an offer?", "No, and be wary of anyone who does. A company you have never met makes that decision. We control the quality of your resume, where you apply, and how ready you are for the interview."),
    ("Who sees my resume?", "You and our team. We only share it with an employer or recruiter after you have said yes to that specific application."),
    ("What if I need to pause?", "Go ahead. The process runs at your pace. If you land an offer or hit a busy stretch at work, we hold your place and restart when you are ready."),
]
faq_html = "".join(
    '<div class="faq-item%s reveal"><button class="faq-q" type="button" aria-expanded="%s">%s<span class="plus">%s</span></button>'
    '<div class="faq-a"><p>%s</p></div></div>' % (" open" if i == 0 else "", "true" if i == 0 else "false", q, I["plus"], a)
    for i, (q, a) in enumerate(faqs))

process = page_hero("Process", "Five steps. Same order, every time.",
    "We have run this with over a thousand people. It works because it is sequential: each step feeds the next, instead of resume, applications and interview prep all happening at once.") + '''
<section class="section band-ink">
  <div class="wrap">''' + stairs() + '''</div>
</section>

<section class="section">
  <div class="wrap-narrow">
    <div class="section-head reveal"><h2>What happens at each step</h2></div>
    <div class="detail-list">''' + detail_html + '''</div>
  </div>
</section>

<section class="section band">
  <div class="wrap-narrow">
    <div class="section-head reveal"><h2>Questions people ask first</h2></div>
    ''' + faq_html + '''
  </div>
</section>
''' + cta("Ready for step one?", "The audit call is free and takes 30 minutes.", "Book my audit call")

page("process.html", "How it works | SD Solutions",
     "The five-step process SD Solutions uses to take you from resume audit to signed offer.", process)

# ================================================================== INTERVIEW
video_svg = '''<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Mock interview recording with a scorecard">
  <rect width="400" height="300" fill="#3678D4"/>
  <circle cx="320" cy="58" r="70" fill="#A8D8F0" opacity=".95"/>
  <rect x="0" y="236" width="400" height="64" fill="#245CA8"/>
  <circle cx="150" cy="118" r="42" fill="#FFC9A3" stroke="#16324F" stroke-width="3"/>
  <path d="M108 112c2-30 22-46 46-46 26 0 42 16 40 40-14-6-30-10-46-24-12 14-24 24-40 30z" fill="#16324F"/>
  <circle cx="138" cy="122" r="3.4" fill="#16324F"/><circle cx="164" cy="122" r="3.4" fill="#16324F"/>
  <path d="M138 138c8 8 18 8 26 0" fill="none" stroke="#16324F" stroke-width="3" stroke-linecap="round"/>
  <path d="M70 262c4-52 34-80 80-80s76 28 80 80z" fill="#5BA7D1" stroke="#16324F" stroke-width="3"/>
  <g transform="translate(24 22)"><rect width="78" height="30" rx="15" fill="#fff" stroke="#16324F" stroke-width="2.5"/><circle class="rec-dot" cx="18" cy="15" r="6" fill="#5BA7D1"/><text x="32" y="20" font-family="Outfit,sans-serif" font-size="14" font-weight="700" fill="#16324F">REC</text></g>
  <g transform="translate(236 150)"><rect width="148" height="116" rx="16" fill="#fff" stroke="#16324F" stroke-width="3"/>
    <text x="14" y="26" font-family="Syne,sans-serif" font-size="14" font-weight="800" fill="#16324F">Scorecard</text>
    <rect x="14" y="40" width="120" height="9" rx="4.5" fill="#DCEBFA"/><rect x="14" y="40" width="102" height="9" rx="4.5" fill="#3678D4"/>
    <rect x="14" y="62" width="120" height="9" rx="4.5" fill="#DCEBFA"/><rect x="14" y="62" width="84" height="9" rx="4.5" fill="#5BA7D1"/>
    <rect x="14" y="84" width="120" height="9" rx="4.5" fill="#DCEBFA"/><rect x="14" y="84" width="112" height="9" rx="4.5" fill="#63C7B2"/>
  </g>
</svg>'''


def guide_svg(kind):
    person = ('<circle cx="160" cy="84" r="26" fill="#FFC9A3" stroke="#16324F" stroke-width="3"/>'
              '<path d="M118 160c3-34 21-50 42-50s39 16 42 50z" fill="#3678D4" stroke="#16324F" stroke-width="3"/>')
    if kind == 1:
        return ('<svg viewBox="0 0 320 180" role="img" aria-label="Person lit from the front"><rect width="320" height="180" fill="#DCEBFA"/>'
                '<circle cx="40" cy="60" r="26" fill="#A8D8F0" stroke="#16324F" stroke-width="3"/>'
                '<path d="M70 52l30 14M72 66l30 4M70 80l28-4" stroke="#A8D8F0" stroke-width="5" stroke-linecap="round"/>' + person + '</svg>')
    if kind == 2:
        return ('<svg viewBox="0 0 320 180" role="img" aria-label="Person in silhouette against a bright window"><rect width="320" height="180" fill="#A8D8F0"/>'
                '<rect x="70" y="14" width="180" height="110" rx="10" fill="#FFF6C9" stroke="#16324F" stroke-width="3"/>'
                '<circle cx="160" cy="92" r="26" fill="#16324F"/><path d="M118 160c3-34 21-50 42-50s39 16 42 50z" fill="#16324F"/></svg>')
    if kind == 3:
        return ('<svg viewBox="0 0 320 180" role="img" aria-label="Person centered in frame at eye level"><rect width="320" height="180" fill="#F3F8FC"/>'
                '<rect x="60" y="16" width="200" height="148" rx="12" fill="none" stroke="#16324F" stroke-width="3" stroke-dasharray="9 7"/>'
                '<path d="M20 84h280" stroke="#63C7B2" stroke-width="3" stroke-dasharray="4 6"/>' + person + '</svg>')
    return ('<svg viewBox="0 0 320 180" role="img" aria-label="Cluttered background and off-center framing"><rect width="320" height="180" fill="#FFD9D3"/>'
            '<rect x="22" y="30" width="60" height="44" rx="6" fill="#5BA7D1" stroke="#16324F" stroke-width="3" transform="rotate(-8 52 52)"/>'
            '<rect x="30" y="100" width="76" height="50" rx="6" fill="#A8D8F0" stroke="#16324F" stroke-width="3" transform="rotate(6 68 125)"/>'
            '<g transform="translate(70 40)"><circle cx="160" cy="104" r="26" fill="#FFC9A3" stroke="#16324F" stroke-width="3"/>'
            '<path d="M118 180c3-30 21-44 42-44s39 14 42 44z" fill="#3678D4" stroke="#16324F" stroke-width="3"/></g></svg>')


def gcard(kind, badge, title, text):
    cls = "do" if badge == "Do" else "dont"
    return ('<article class="gcard reveal"><div class="gv">%s</div><div class="gb"><span class="badge %s">%s</span><h3>%s</h3><p>%s</p></div></article>'
            % (guide_svg(kind), cls, badge, title, text))


qs = [
    ("Walk me through your resume.", "We coach a 60 to 90 second version that covers your last three roles without turning into a speech."),
    ("Tell me about a time you disagreed with a manager.", "You practise a clear structure so the story lands on the result, not just the conflict."),
    ("Why are you leaving your current role?", "We help you answer looking forward, without criticising a past employer."),
    ("What questions do you have for us?", "We build you a list that shows you have researched the team."),
]
qa_html = "".join('<div class="qa-item reveal"><div class="qm" aria-hidden="true">&ldquo;</div><div><b>%s</b><span>%s</span></div></div>' % q for q in qs)

interview = page_hero("Interview prep", "Practice on camera. Win in the room.",
    "Every mock interview is recorded and paired with questions for your role, plus a plain guide to how you look and sound on video.") + '''
<section class="section">
  <div class="wrap">
    <div class="video-split">
      <div class="video-frame reveal" data-reveal="left">''' + video_svg + '''</div>
      <div class="reveal" data-reveal="right">
        <h2>Two mock interviews, reviewed like game film.</h2>
        <p style="margin-top:18px;font-size:19px">We record every session and watch it back with you: your pace, your filler words, your posture, and what your answers actually say.</p>
        <div style="margin-top:26px">''' + checks([
            "Two full recorded mock interviews",
            "Questions and strong sample answers for your role",
            "A written scorecard on clarity, structure and confidence",
            "Recordings you keep and can rewatch before the real thing"]) + '''</div>
      </div>
    </div>
  </div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>How you look on camera matters before you speak</h2>
      <p>Small fixes to light, framing and background change how a recruiter reads you in the first ten seconds. Here is what we check.</p>
    </div>
    <div class="guide" data-stagger>
''' + gcard(1, "Do", "Face the light", "Sit facing a window, or put a soft lamp behind your laptop. Light on your face makes you look awake and approachable.") \
    + gcard(2, "Don't", "Sit with a window behind you", "Backlight turns you into a silhouette. Close the blinds or turn your desk around.") \
    + gcard(3, "Do", "Center yourself at eye level", "Prop the laptop on a stack of books so the lens is at eye height. Keep your head and shoulders in the middle of the frame.") \
    + gcard(4, "Don't", "Leave clutter or a low angle", "A messy background or a camera pointing up your chin looks unprepared. Check the frame before you join.") + '''
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap-narrow">
    <div class="section-head reveal"><h2>Questions we will drill you on</h2><p>Every question bank is built for your target role. Here is a sample.</p></div>
    <div class="qa" data-stagger>''' + qa_html + '''</div>
  </div>
</section>
''' + cta("Get your first mock interview on the calendar", "Sessions are recorded, reviewed and yours to keep.", "Book interview prep")

page("interview-coaching.html", "Interview prep | SD Solutions",
     "Recorded mock interviews, role-specific questions and a guide to looking good on video from SD Solutions.", interview)

# ================================================================== ABOUT
story_svg = '''<svg viewBox="0 0 400 400" role="img" aria-label="Rising steps toward a goal">
  <rect width="400" height="400" fill="#A8D8F0"/>
  <circle cx="300" cy="96" r="58" fill="#5BA7D1" stroke="#16324F" stroke-width="4"/>
  <path d="M0 340h400v60H0z" fill="#16324F"/>
  <rect x="30" y="278" width="76" height="62" fill="#fff" stroke="#16324F" stroke-width="4"/>
  <rect x="106" y="226" width="76" height="114" fill="#DCEBFA" stroke="#16324F" stroke-width="4"/>
  <rect x="182" y="174" width="76" height="166" fill="#3678D4" stroke="#16324F" stroke-width="4"/>
  <rect x="258" y="122" width="76" height="218" fill="#fff" stroke="#16324F" stroke-width="4"/>
  <path d="M48 262l62-46 74-56 88-44" fill="none" stroke="#16324F" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 12"/>
</svg>'''

about = page_hero("About", "We got tired of watching good people get ignored.",
    "SD Solutions is a career consultancy built on one idea: a better resume is wasted if nobody helps you use it. So we stay with you from the first edit to the last interview round.") + '''
<section class="section">
  <div class="wrap">
    <div class="story">
      <div class="reveal" data-reveal="left">
        <h2>Built from the recruiter's side of the table.</h2>
        <p>Strong candidates kept losing. Not because they lacked skills, but because their resume never got past the first screen, or they walked into an interview not knowing what to expect.</p>
        <p>So we built a service that closes that gap: people who have reviewed resumes and run interview loops, working through one clear process that anyone can follow.</p>
        <p>Today every client goes through the same steps, whether they need one service or all four.</p>
      </div>
      <div class="story-art reveal" data-reveal="right">''' + story_svg + '''</div>
    </div>
  </div>
</section>

''' + stats_band() + '''

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><h2>What we stand for</h2></div>
    <div class="beliefs" data-stagger>
      <div class="belief reveal"><h3>Specific beats generic</h3><p>A resume that is not written for your target role is not worth much. Everything we make is built around what you are actually chasing.</p></div>
      <div class="belief reveal"><h3>Show the work</h3><p>Recorded sessions, written scorecards, tracked applications. You can see what we did and why.</p></div>
      <div class="belief reveal"><h3>Honest about the odds</h3><p>We will not promise an offer. We will tell you where your resume is weak and where your answers need work.</p></div>
      <div class="belief reveal"><h3>Your pace, not ours</h3><p>Employed and searching on the side, or all-in and full time. The plan bends to the hours you have.</p></div>
    </div>
  </div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="facts" style="max-width:860px" data-stagger>
      <div class="fact reveal">''' + I["person"] + '''<div><h3>Recruiters on every review</h3><p>Every resume and interview session is checked by someone who has sat on a hiring panel.</p></div></div>
      <div class="fact reveal">''' + I["target"] + '''<div><h3>Fourteen platforms tracked</h3><p>From the big boards to niche communities, we keep a live view of where roles in your field get filled.</p></div></div>
      <div class="fact reveal">''' + I["check"] + '''<div><h3>Over a thousand searches run</h3><p>The process on our Process page has been refined across more than a thousand clients.</p></div></div>
    </div>
  </div>
</section>
''' + cta("Want to meet the team before you commit?", "The first call is free, and you owe us nothing after it.", "Book a free call")

page("about.html", "About | SD Solutions", "Why SD Solutions exists, how we work and what we stand for.", about)

# ================================================================== REVIEWS
reviews = page_hero("Reviews", "People who stopped getting ghosted.",
    "Resume rebuilds, guided applications and interview prep. Here is how it went for a few of them.") + '''
<section class="section">
  <div class="wrap">
    <div class="results" data-stagger>
      <div class="result reveal"><div class="big">8 days</div><p>From new resume to first interview call</p><small>Data analyst, after switching platforms</small></div>
      <div class="result reveal"><div class="big">2 mocks</div><p>Recorded before an offer from a product company</p><small>Product manager</small></div>
      <div class="result reveal"><div class="big">3 days</div><p>For a full resume rewrite that changed how recruiters replied</p><small>UX designer</small></div>
    </div>
    <div class="quotes" data-stagger>
''' + quote("q1", "The apply list alone was worth it. I was sending fifteen applications a week that were never going to land. Once they changed where I applied, I had three first-round calls in eight days.", "AR", "Ananya R.", "Data analyst", "#A8D8F0") \
    + quote("q2", "Watching my own mock interview was uncomfortable and exactly what I needed. The real one felt like a rerun.", "RK", "Rohit K.", "Product manager", "#fff") \
    + quote("q3", "I sent them a resume I was embarrassed by. Three days later I wanted to hand it to a recruiter.", "MS", "Meera S.", "UX designer", "#A8D8F0") \
    + quote("q4", "I never had hours for applications while working full time. They kept fifteen roles moving while I kept my day job.", "VP", "Vikram P.", "Backend engineer", "#fff") \
    + quote("q5", "Nobody told me my camera angle made me look bored until the video review. Tiny fix, huge difference.", "SN", "Sana N.", "Marketing lead", "#A8D8F0") \
    + quote("q6", "They were upfront about the odds instead of promising an offer. I trusted the platform advice more because of that.", "TK", "Tarun K.", "Business analyst", "#DCEBFA") + '''
    </div>
  </div>
</section>
''' + cta("Add your story to this page", "Start with a free resume audit. No commitment.", "Book my audit")

page("reviews.html", "Reviews | SD Solutions", "What clients say about working with SD Solutions.", reviews)

# ================================================================== CONTACT
map_svg = '''<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Map pin for Jaipur, Rajasthan">
  <rect width="400" height="300" fill="#DCEBFA"/>
  <path d="M-10 90c80-30 140 40 220 10s130-60 200-20" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round"/>
  <path d="M40 320c20-100 90-120 150-150s60-120 90-190" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round"/>
  <path d="M-10 230c110 20 200-30 420 30" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round"/>
  <ellipse cx="200" cy="196" rx="30" ry="9" fill="#16324F" opacity=".18"/>
  <g class="pin"><path d="M200 192c-34-40-44-58-44-78a44 44 0 0 1 88 0c0 20-10 38-44 78z" fill="#5BA7D1" stroke="#16324F" stroke-width="4" stroke-linejoin="round"/>
  <circle cx="200" cy="114" r="15" fill="#fff" stroke="#16324F" stroke-width="4"/></g>
</svg>'''

contact = page_hero("Contact", "Tell us where you are stuck.",
    "Share where you are applying and where you want to land. A real person replies within one business day.") + '''
<section class="section">
  <div class="wrap">
    <div class="methods" data-stagger>
      <div class="method reveal">''' + I["mail"] + '''<h3>Email</h3><p>For questions, or to send your resume straight over.</p><a class="link-u" href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a></div>
      <div class="method reveal">''' + I["phone"] + '''<h3>Phone</h3><p>Talk to the team directly, Monday to Saturday.</p><a class="link-u" href="tel:''' + PHONE_HREF + '''">''' + PHONE + '''</a></div>
      <div class="method reveal">''' + I["chat"] + '''<h3>WhatsApp</h3><p>The quickest way to reach us during office hours.</p><a class="link-u" href="https://wa.me/''' + WHATSAPP_HREF + '''" rel="noopener">Message us</a></div>
    </div>
  </div>
</section>

<section class="section band" id="audit">
  <div class="wrap">
    <div class="contact-split">
      <div class="reveal" data-reveal="left">
        <h2>Your free resume audit</h2>
        <p style="margin-top:18px;font-size:19px">Fill in the form and we will read what you send, then reply with a short, honest take on your resume and target roles, and which of our services would help most.</p>
        <div style="margin-top:26px">''' + checks(["You owe nothing after the audit", "A reply within one business day", "A straight recommendation, not a sales script"]) + '''</div>
        <div class="note-card">''' + I["lock"] + '''<p><b>Your resume stays private.</b> We only share it with an employer or recruiter after you say yes to that specific application.</p></div>
      </div>
      <div class="form reveal" data-reveal="right">
        <form id="contact-form" data-form="contact" novalidate>
          <div class="fields">
            <div class="row">
              <div class="field"><label for="name">Full name</label><input id="name" name="name" type="text" autocomplete="name" placeholder="Ananya Rao" required data-required-msg="Please tell us your name."><span class="err" role="alert"></span></div>
              <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" placeholder="you@email.com" required data-required-msg="We need an email to reply to."><span class="err" role="alert"></span></div>
            </div>
            <div class="row">
              <div class="field"><label for="phone">Phone <span class="opt">(optional)</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="+91 98765 43210"><span class="err" role="alert"></span></div>
              <div class="field"><label for="current-role">Current role <span class="opt">(optional)</span></label><input id="current-role" name="currentRole" type="text" placeholder="Senior analyst"></div>
            </div>
            <div class="row">
              <div class="field"><label for="target-role">Role you want</label><input id="target-role" name="targetRole" type="text" placeholder="Product manager" required data-required-msg="Tell us the role you are aiming for."><span class="err" role="alert"></span></div>
              <div class="field"><label for="service">What do you need help with?</label>
                <select id="service" name="service">
                  <option>Not sure. Start with the audit</option>
                  <option>Resume rebuild</option>
                  <option>Know where to apply</option>
                  <option>We hit submit</option>
                  <option>Camera-ready interviews</option>
                  <option>The full runway</option>
                </select>
              </div>
            </div>
            <div class="field"><label for="message">Anything else we should know? <span class="opt">(optional)</span></label><textarea id="message" name="message" placeholder="Your timeline, target companies, what has not worked so far"></textarea></div>
            <div class="field"><label for="resume">Attach your resume <span class="opt">(optional, PDF or Word, up to 5 MB)</span></label><input id="resume" name="resume" type="file" accept=".pdf,.doc,.docx,application/pdf"><span class="err" role="alert"></span></div>
            <div class="field"><label class="consent" for="consent"><input type="checkbox" id="consent" name="consent" required data-required-msg="Please tick this so we are allowed to reply."><span>I agree to the <a href="privacy.html">Privacy Policy</a> and to being contacted about my request.</span></label><span class="err" role="alert"></span></div>
            <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
            <button type="submit" class="btn btn-sun" style="width:100%"><span class="btn-label">Send my request</span></button>
            <p class="form-note">We only use your details to reply about your audit.</p>
            <div class="form-status" role="alert"></div>
          </div>
        </form>
        <div class="success" role="status" aria-live="polite">
          <svg viewBox="0 0 96 96" aria-hidden="true"><circle class="ring" cx="48" cy="48" r="38" fill="#63C7B2" stroke="#16324F" stroke-width="4"/><path class="tickmark" d="M30 50l12 12 24-26" fill="none" stroke="#16324F" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <h3>Got it. Thank you.</h3>
          <p>A real person will read your request and reply within one business day.</p>
          <p style="margin-top:20px"><a href="index.html" class="btn btn-white"><span class="btn-label">Back to home</span></a></p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="office reveal" data-reveal="zoom">
      <div class="office-info">
        <h3>Office hours</h3>
        <p>Monday to Saturday, 9:00 AM to 7:00 PM IST. Calls and mock interviews can run in the evening too.</p>
        <h3>Where we are</h3>
        <p>Jaipur, Rajasthan, working with clients across time zones.</p>
      </div>
      <div class="office-map">''' + map_svg + '''</div>
    </div>
  </div>
</section>
'''
page("contact.html", "Contact | SD Solutions", "Book a free resume audit or get in touch with SD Solutions.", contact)

# ================================================================== LEGAL
def legal_page(filename, title, crumb, lede, body):
    html = page_hero(crumb, title, lede) + '<section class="section"><div class="wrap-narrow prose">' + body + '</div></section>'
    page(filename, title + " | SD Solutions", lede, html)


legal_page("privacy.html", "Privacy policy", "Privacy policy",
    "What we collect, why we collect it, and what you can ask us to do with it.",
    '''<!-- Template text. Have a qualified professional review it for your business and region before publishing. -->
<span class="updated">Last updated: October 2026</span>
<h2>Who we are</h2>
<p>SD Solutions is a career consultancy based in Jaipur, Rajasthan, India. This policy explains how we handle the personal information you share with us through this website and our services.</p>
<h2>What we collect</h2>
<ul>
<li>Contact details you give us, such as your name, email address and phone number.</li>
<li>Career information you send, such as your resume, work history and the roles you are aiming for.</li>
<li>Recordings of mock interviews, which we make only with your agreement.</li>
<li>Basic technical information, such as your browser type, when you visit this site.</li>
</ul>
<h2>How we use it</h2>
<p>We use your information to reply to your requests, deliver the services you ask for, and keep our records. We do not sell your information.</p>
<h2>Who we share it with</h2>
<p>We share your resume with an employer or recruiter only after you have agreed to that specific application. We also use trusted providers for things like email and hosting, and they may only use your information to provide those services to us.</p>
<h2>How long we keep it</h2>
<p>We keep your information while we work together and for a reasonable period afterwards. Mock interview recordings are yours to keep, and we delete our copies on request.</p>
<h2>Your choices</h2>
<p>You can ask us to show you what we hold about you, correct it, or delete it. Write to <a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a> and we will respond within a reasonable time.</p>
<h2>Cookies</h2>
<p>This website does not use advertising cookies. If we add analytics later, we will update this page and tell you how to opt out.</p>
<h2>Changes</h2>
<p>If we change this policy we will update the date at the top of this page.</p>''')

legal_page("terms.html", "Terms of service", "Terms of service",
    "The ground rules for using this website and working with SD Solutions.",
    '''<!-- Template text. Have a qualified professional review it for your business and region before publishing. -->
<span class="updated">Last updated: October 2026</span>
<h2>Our services</h2>
<p>SD Solutions provides resume writing, job platform guidance, application support and interview coaching. The exact scope, timeline and fee for your engagement are confirmed with you in writing before work starts.</p>
<h2>No guarantee of employment</h2>
<p>We work hard to improve your chances, but we cannot guarantee interviews, offers or any particular hiring outcome. Those decisions belong to employers.</p>
<h2>Your responsibilities</h2>
<ul>
<li>Give us accurate, complete information. We will not add claims to your resume that are not true.</li>
<li>Review and approve every resume and application before it is sent.</li>
<li>Attend scheduled sessions, or let us know in good time if you need to move them.</li>
</ul>
<h2>Fees and changes</h2>
<p>Fees are quoted after your free audit. If your needs change we will agree any change in scope and price with you before doing extra work.</p>
<h2>Your content</h2>
<p>Your resume and the materials you send remain yours. You allow us to use them to deliver the services you asked for.</p>
<h2>Limits on liability</h2>
<p>To the extent the law allows, SD Solutions is not liable for indirect or consequential losses, and our total liability is limited to the fees you paid for the service in question.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of India, and disputes are handled in the courts of Jaipur, Rajasthan.</p>
<h2>Contact</h2>
<p>Questions about these terms? Write to <a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a>.</p>''')

# ================================================================== 404
nf = '''<section class="notfound">
  <div class="wrap">
    <div class="num" aria-hidden="true">404</div>
    <h1>This page got ghosted.</h1>
    <p>The page you are looking for has moved, or it never existed. Here is where most people head next.</p>
    <div class="links">
      <a href="index.html" class="btn btn-sun"><span class="btn-label">Back to home</span></a>
      <a href="services.html" class="btn btn-white"><span class="btn-label">See our services</span></a>
      <a href="contact.html" class="btn btn-white"><span class="btn-label">Contact us</span></a>
    </div>
  </div>
</section>'''
page("404.html", "Page not found | SD Solutions", "That page could not be found.", nf, active="none", noindex=True)

# ================================================================== sitemap + robots
pages = ["index.html", "services.html", "process.html", "interview-coaching.html", "about.html",
         "reviews.html", "contact.html", "privacy.html", "terms.html"]
urls = "".join("  <url><loc>%s/%s</loc></url>\n" % (SITE_URL, "" if p == "index.html" else p) for p in pages)
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)

print("Built %d pages + 404, sitemap.xml, robots.txt" % len(pages))
