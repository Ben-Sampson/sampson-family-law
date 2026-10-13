"""Generates every page from one shared template (header, top line, nav, footer, disclaimers).
Run: python3 build.py   Content lives in content.py; credits come from img/credits.json."""
import html, re, json, pathlib
from content import *

PHONE="(918) 555-0142"; TEL="+19185550142"
ADDR1="1200 S. Fictional Avenue, Suite 555"; ADDR2="Tulsa, OK 74100"
HOURS=[("Monday – Thursday","8:30 am – 5:30 pm"),("Friday","8:30 am – 4:00 pm"),("Saturday","By appointment"),("Sunday","Closed")]

LOGO='''<svg viewBox="0 0 64 64" role="img" aria-label="Sampson Family Law monogram"><circle cx="32" cy="32" r="31" fill="#0a2540"/><circle cx="32" cy="32" r="26.5" fill="none" stroke="#cdbf9f" stroke-width="1.2"/><circle cx="32" cy="32" r="24" fill="none" stroke="#cdbf9f" stroke-width=".5" opacity=".7"/><text x="32" y="43" text-anchor="middle" font-family="Georgia,'Times New Roman',serif" font-size="32" font-style="italic" fill="#efe7d6">S</text><path d="M14 47h36" stroke="#cdbf9f" stroke-width=".8"/><text x="32" y="54" text-anchor="middle" font-family="Georgia,serif" font-size="5.2" letter-spacing="1.6" fill="#efe7d6">FAMILY LAW</text><circle cx="32" cy="13" r="1.4" fill="#cdbf9f"/></svg>'''

def ico(name):
    P={"family":'<circle cx="9" cy="7" r="3"/><circle cx="17" cy="9" r="2.4"/><path d="M3 21v-2a5 5 0 0 1 5-5h2a5 5 0 0 1 5 5v2M15 21v-1.5a3.5 3.5 0 0 1 3.5-3.5h0a3.5 3.5 0 0 1 3.5 3.5V21"/>',
     "scale":'<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
     "rings":'<circle cx="9" cy="14" r="6"/><circle cx="15" cy="10" r="6"/>',
     "child":'<circle cx="12" cy="6" r="3"/><path d="M12 9v7M8 12h8M9 22l3-6 3 6"/>',
     "dollar":'<path d="M12 2v20M17 6.5C16 5 14.3 4.5 12 4.5c-3 0-5 1.3-5 3.5 0 5 10 2.5 10 7.5 0 2.2-2 3.5-5 3.5-2.4 0-4.3-.7-5.2-2.3"/>',
     "shield":'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
     "phone":'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
     "pin":'<path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
     "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
     "car":'<path d="M5 16h14M6 16l1.5-5h9L18 16M5 16v3h2v-2M19 16v3h-2v-2"/><circle cx="8" cy="14" r=".6"/><circle cx="16" cy="14" r=".6"/>',"heart":'<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',"doc":'<path d="M7 3h7l4 4v14H7zM14 3v4h4M10 12h5M10 16h5"/>',
     "mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'}
    return f'<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>'

AREA_ICON={"family-law":"family","mediation":"scale","divorce":"rings","child-custody":"child","child-support":"dollar","criminal-law":"shield","personal-injury":"car","wills-estate-planning":"doc"}

def shell(path,title,body,desc="",current=""):
    r="../"*path.count("/")
    pa="".join(f'<a href="{r}practice-areas/{a["slug"]}.html">{a["name"]}</a>' for a in AREAS)
    cur=lambda k:' aria-current="page"' if k==current else ''
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow"><title>{title} | Sampson Family Law (Student Demonstration)</title>
<meta name="description" content="{html.escape(desc or 'A fictional Tulsa family law firm website built as a law school course demonstration. Not a law firm.')}">
<meta name="theme-color" content="#0a2540"><link rel="icon" href="{r}img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&display=swap"><link rel="stylesheet" href="{r}css/styles.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="topline" role="note"><div class="container"><span>Demonstration project for a law school course; not a law firm. <a href="{r}about.html#disclaimer">Learn more</a></span><span class="tl-right"><span>{ADDR2} (fictional)</span><span>Mon–Thu 8:30–5:30 · Fri 8:30–4:00</span></span></div></div>
<header class="site-header"><div class="container nav">
<a class="brand" href="{r}index.html" aria-label="Sampson Family Law, home">{LOGO}<span class="brand-text"><span class="brand-name">Sampson</span><span class="brand-sub">Family Law · Tulsa</span></span></a>
<nav aria-label="Main"><button class="menu-toggle" aria-expanded="false" aria-controls="primary-menu" aria-label="Open menu"><span></span><span></span><span></span></button>
<ul class="menu" id="primary-menu">
<li><a href="{r}index.html"{cur("home")}>Home</a></li>
<li class="has-dd"><button aria-expanded="false" aria-haspopup="true">Practice Areas<span class="caret">▼</span></button><div class="dd"><a href="{r}practice-areas/index.html">All practice areas</a>{pa}</div></li>
<li class="has-dd"><button aria-expanded="false" aria-haspopup="true">Our Firm<span class="caret">▼</span></button><div class="dd"><a href="{r}about.html">About the firm</a><a href="{r}team.html">Our team</a><a href="{r}people/ben-sampson.html">Ben Sampson</a><a href="{r}people/libby-sampson.html">Libby Sampson</a><a href="{r}testimonials.html">Client stories</a></div></li>
<li><a href="{r}insights/index.html"{cur("insights")}>Insights</a></li>
<li class="has-dd"><button aria-expanded="false" aria-haspopup="true">Resources<span class="caret">▼</span></button><div class="dd"><a href="{r}evidence.html">Evidence &amp; data</a><a href="{r}build-log.html">Build log</a><a href="{r}credits.html">Image credits</a></div></li>
<li><a href="{r}contact.html"{cur("contact")}>Contact</a></li>
<li class="nav-cta-li nav-pay-li"><a class="btn nav-cta nav-pay" href="{r}payments.html"{cur("payments")}>Make a Payment</a></li>
<li class="nav-cta-li"><a class="btn nav-cta" href="{r}contact.html">Free Consultation</a></li>
</ul></nav></div></header><div class="scrim" aria-hidden="true"></div>
<main id="main">{body}</main>
<footer class="site-footer" style="background-image:linear-gradient(rgba(7,26,46,.93),rgba(7,26,46,.97)),url({r}img/bg/twilight.jpg)"><div class="container"><div class="f-grid">
<div><a class="brand" href="{r}index.html">{LOGO}<span class="brand-text"><span class="brand-name">Sampson</span><span class="brand-sub">Family Law · Tulsa</span></span></a>
<p>Steady counsel for Oklahoma families. A fictional firm, imagined and built for a law school course.</p></div>
<div><h4>Practice Areas</h4><ul>{"".join(f'<li><a href="{r}practice-areas/{a["slug"]}.html">{a["name"]}</a></li>' for a in AREAS)}</ul></div>
<div><h4>Explore</h4><ul><li><a href="{r}about.html">About the firm</a></li><li><a href="{r}people/ben-sampson.html">Ben Sampson</a></li><li><a href="{r}people/libby-sampson.html">Libby Sampson</a></li><li><a href="{r}team.html">Our team</a></li><li><a href="{r}testimonials.html">Client stories</a></li><li><a href="{r}insights/index.html">Insights</a></li><li><a href="{r}evidence.html">Evidence &amp; data</a></li><li><a href="{r}credits.html">Image credits</a></li><li><a href="{r}build-log.html">Build log</a></li><li><a href="{r}payments.html">Make a payment (demo)</a></li></ul></div>
<div><h4>Visit (fictional)</h4><ul><li>{ADDR1}<br>{ADDR2}</li><li><a href="tel:{TEL}">{PHONE}</a></li><li>Mon–Thu 8:30–5:30 · Fri 8:30–4:00</li></ul><p style="margin-top:18px"><a class="btn nav-cta" href="{r}contact.html">Schedule a consultation</a></p></div>
</div>
<div class="f-legal">
<p><strong>Demonstration project. Not a law firm.</strong> Sampson Family Law is a fictional firm created by a law student for a law school course on AI and the Law. It is not a real law firm and has no office, staff, or clients. Every person named on this site, including Ben Sampson, Libby Sampson, Jane, Tater, and every client, is a fictional character. The people in the photographs are the site owner's family and friends (and dog) playing those roles; their photos are used with permission of the owner and do not depict real attorneys, staff, or clients. No one on this site is a licensed attorney, and the creator is not licensed to practice law in Oklahoma or any other jurisdiction.</p>
<p><strong>No legal advice. No attorney-client relationship.</strong> Nothing on this site is legal advice, and using it does not create an attorney-client relationship. Statutes and procedures change; information here is general and may be incomplete or out of date. For help with a real legal matter in Oklahoma, contact <a href="https://www.legalaidok.org/">Legal Aid Services of Oklahoma</a> or a licensed attorney.</p>
<p><strong>Fictional details.</strong> The address, suite, phone number (555 numbers are reserved for fiction), hours, testimonials, client stories, characters, case outcomes, team members, credentials, and badges are invented for the demonstration. They are not real reviews, awards, bar memberships, or certifications. The consultation form on the contact page is a live class demonstration: submissions are emailed to the student presenter, so do not include sensitive or confidential information. The payments page takes no payments: its handles are fictional, and its QR codes open a demonstration page on this site, not any payment app or account. Statistics on the <a href="{r}evidence.html">evidence page</a> are real and cited to their public sources. Character photographs are personal photos used with permission of the owner; other photographs are free-licensed. See <a href="{r}credits.html">image credits</a>.</p>
<div class="f-bottom"><span>© <span id="yr">2026</span> Sampson Family Law (fictional). Student demonstration project.</span><span>Built with AI agents · <a href="{r}build-log.html">See how</a></span></div>
</div></div></footer>
<button class="to-top" aria-label="Back to top">↑</button>
<script src="{r}js/main.js"></script></body></html>
'''

def hero(title,sub,crumbs,img="philtower.jpg",r=""):
    c=" <span aria-hidden='true'>/</span> ".join(crumbs)
    return f'<section class="page-hero"><div class="bg" style="background-image:url({r}img/{img})"></div><div class="container"><nav class="crumbs" aria-label="Breadcrumb">{c}</nav><h1>{title}</h1><p>{sub}</p></div></section>'

def cta(r="",title="Ready for a fresh start?",text="Schedule a confidential consultation. We will listen first and explain your options in plain English."):
    return f'''<section class="cta"><div class="bg" style="background-image:url({r}img/bg/sunset.jpg)"></div><div class="container on-dark reveal"><div><span class="eyebrow">Free initial consultation</span><h2>{title}</h2><p>{text}</p><p class="fine" style="margin-top:10px">Demonstration only: consultations, fees, and the firm itself are fictional.</p></div>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="{r}contact.html">Request a consultation</a><a class="btn btn-ghost" href="tel:{TEL}">{PHONE}</a></div></div></section>'''

def carousel(r="",title="In their words"):
    s="".join(f'<div class="slide" role="group" aria-roledescription="slide"><blockquote>{p["quote"]}</blockquote><cite>{p["name"]}, {p["place"]}</cite><a class="more" href="{r}people/{p["slug"]}.html">Read {p["name"].replace("The ","the ")}\'s story</a></div>' for p in CLIENTS)
    return f'''<section class="s navy" aria-labelledby="t-h"><div class="container on-dark"><div class="s-head center"><span class="eyebrow">Client stories</span><h2 id="t-h">{title}</h2></div>
<div class="carousel" aria-roledescription="carousel" aria-label="Client testimonials (fictional)"><div class="slides" aria-live="polite">{s}</div>
<div class="c-ctrl"><button class="arrow prev" type="button" aria-label="Previous testimonial">←</button><div class="dots" role="tablist" aria-label="Choose testimonial"></div><button class="arrow next" type="button" aria-label="Next testimonial">→</button></div>
<p class="fine" style="margin-top:28px">Fictional testimonials from fictional characters, written for a class demonstration. Past results do not guarantee future outcomes.</p></div></div></section>'''

CLIENTS=[p for p in PEOPLE if p["kind"]=="client"]; STAFF=[p for p in PEOPLE if p["kind"]=="staff"]
AREA_NAME={a["slug"]:a["name"] for a in AREAS}

def gallery(p,r="../"):
    sl="".join(f'<figure class="g-slide{" active" if i==0 else ""}" role="group" aria-roledescription="slide" aria-label="{i+1} of {len(p["gallery"])}"><img src="{r}img/{src}" alt="{alt}" {"" if i==0 else "loading=lazy "}decoding="async">{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>' for i,(src,alt,cap) in enumerate(p["gallery"]))
    ctrl='' if len(p["gallery"])<2 else '<div class="g-ctrl"><button class="arrow prev" type="button" aria-label="Previous photo">←</button><div class="dots" role="tablist" aria-label="Choose photo"></div><button class="arrow next" type="button" aria-label="Next photo">→</button><button class="g-pause" type="button" aria-label="Pause slideshow">❚❚</button></div>'
    return f'<div class="gallery" aria-roledescription="carousel" aria-label="Photos of {p["name"]}"><div class="g-slides" aria-live="off">{sl}</div>{ctrl}</div>'

def person_card(p,r=""):
    src,alt,_=p["gallery"][0]; sub=p.get("role") or p.get("place")
    return f'<a class="person reveal" href="{r}people/{p["slug"]}.html"><img src="{r}img/{src}" alt="{alt}" loading="lazy"><span class="pc-body"><b>{p["name"]}</b><span>{sub}</span></span></a>'

def stories_for(slug,r="../"):
    cs=[p for p in CLIENTS if p["area"]==slug]
    if not cs: return ""
    return '<div class="side-box"><h3>Client stories</h3>'+"".join(f'<a class="mini" href="{r}people/{p["slug"]}.html"><img src="{r}img/{p["gallery"][0][0]}" alt="" loading="lazy"><span><b>{p["name"]}</b><br><small>{p["place"]}</small></span></a>' for p in cs)+'<p class="fine" style="margin:8px 0 0">Fictional characters.</p></div>'

def post_cards(r="",limit=3):
    return '<div class="posts">'+"".join(f'''<article class="post reveal d{i%3}"><a class="thumb" href="{r}insights/{p["slug"]}.html" tabindex="-1" aria-hidden="true"><img src="{r}img/{p["img"]}" alt="" loading="lazy" width="800" height="500"></a><div class="body"><div class="meta">{p["cat"]} · {p["read"]} min read</div><h3><a href="{r}insights/{p["slug"]}.html">{p["title"]}</a></h3><p>{p["dek"]}</p><a class="more" style="margin-top:auto;font-weight:700;text-decoration:none" href="{r}insights/{p["slug"]}.html">Read article →</a></div></article>''' for i,p in enumerate(POSTS[:limit]))+'</div>'

def area_cards(r="",img=False):
    return '<div class="cards">'+"".join(f'''<article class="card reveal d{i%3}"><div class="ico">{ico(AREA_ICON[a["slug"]])}</div><h3>{a["name"]}</h3><p>{a["card"]}</p><a class="more" href="{r}practice-areas/{a["slug"]}.html">Learn more<span class="sr"> about {a["name"]}</span></a></article>''' for i,a in enumerate(AREAS))+'</div>'

MAP='''<svg viewBox="0 0 600 380" role="img" aria-labelledby="mapt"><title id="mapt">Illustrative map of a fictional office location south of downtown Tulsa, near the Arkansas River. Not to scale.</title>
<rect width="600" height="380" fill="#f4f1ea"/><g fill="#e9e3d6"><rect x="30" y="30" width="110" height="70" rx="4"/><rect x="160" y="30" width="120" height="70" rx="4"/><rect x="300" y="30" width="110" height="70" rx="4"/><rect x="30" y="120" width="110" height="80" rx="4"/><rect x="160" y="120" width="120" height="80" rx="4"/><rect x="300" y="120" width="110" height="80" rx="4"/><rect x="30" y="220" width="110" height="70" rx="4"/><rect x="160" y="220" width="120" height="70" rx="4"/></g>
<rect x="430" y="30" width="150" height="110" rx="6" fill="#dbe8d6"/><text x="505" y="90" text-anchor="middle" font-size="12" fill="#5d7a56" font-family="sans-serif">Park</text>
<path d="M600 170 C 520 200, 470 260, 430 300 S 330 360, 250 380" fill="none" stroke="#b9d3e8" stroke-width="34"/><text x="470" y="300" font-size="12" fill="#5e86a8" font-family="sans-serif" transform="rotate(-38 470 300)">Arkansas River</text>
<g stroke="#fff" stroke-width="9" fill="none"><path d="M0 110H600M0 210H440M150 0V380M290 0V330M420 0V250"/></g><path d="M0 110H600" stroke="#cfe3df" stroke-width="4"/>
<g font-family="sans-serif" font-size="11" fill="#6b7785"><text x="40" y="106">W. Example St.</text><text x="295" y="20" transform="rotate(90 295 20)">S. Fictional Ave.</text><text x="70" y="70">Downtown</text></g>
<g transform="translate(290 210)"><circle r="30" fill="#cdbf9f" opacity=".18"><animate attributeName="r" values="14;34;14" dur="3s" repeatCount="indefinite"/></circle><path d="M0 0c-12-16-18-24-18-32a18 18 0 0 1 36 0c0 8-6 16-18 32z" fill="#0a2540" transform="translate(0 -4)"/><circle cy="-36" r="6.5" fill="#efe7d6"/></g>
<rect x="316" y="228" width="230" height="46" rx="6" fill="#fff" stroke="#e1e5ea"/><text x="330" y="248" font-family="Georgia,serif" font-size="14" fill="#0a2540">Sampson Family Law</text><text x="330" y="265" font-family="sans-serif" font-size="11" fill="#6b7785">Suite 555 · fictional location</text>
<text x="590" y="372" text-anchor="end" font-family="sans-serif" font-size="10" fill="#8a96a3">Illustration only, not to scale</text></svg>'''

def contact_block(r=""):
    hrs="".join(f"<tr><td>{d}</td><td>{h}</td></tr>" for d,h in HOURS)
    return f'''<div class="info-block"><div class="info-item"><div class="ico">{ico("pin")}</div><div><b>Office (fictional)</b><span>{ADDR1}<br>{ADDR2}</span></div></div>
<div class="info-item"><div class="ico">{ico("phone")}</div><div><b>Phone</b><a href="tel:{TEL}">{PHONE}</a> <span>(fictional 555 number)</span></div></div>
<div class="info-item"><div class="ico">{ico("mail")}</div><div><b>Email</b><span>hello@sampson-law.example (placeholder; the .example domain cannot receive mail)</span></div></div>
<div class="info-item"><div class="ico">{ico("clock")}</div><div style="flex:1"><b>Office hours</b><table class="hours">{hrs}</table></div></div></div>'''

pages={}
r=""
# ---------- HOME
pages["index.html"]=("Tulsa Law Firm",f'''
<section class="hero"><div class="hero-bg" style="background-image:url(img/bg/beach-hero.jpg)" role="img" aria-label="Palm trees above a calm blue ocean"></div><div class="container on-dark">
<span class="eyebrow">Sampson Family Law · Tulsa</span>
<h1>Steady counsel for the moments that matter.</h1>
<p class="lead">Family law, personal injury, estate planning, and defense, handled by a small team that knows your name and explains things plainly.</p>
<div class="hero-actions"><a class="btn" href="contact.html">Schedule a consultation</a><a class="btn btn-ghost" href="team.html">Meet the team</a></div>
<p class="fine" style="margin-top:28px">Fictional firm, created for a law school demonstration.</p></div></section>

<section class="s"><div class="container split"><div class="reveal"><span class="eyebrow">The firm</span><h2>A small practice, by design</h2>
<p>Sampson Family Law keeps its caseload small so clients reach their attorney directly, get a written plan after the first meeting, and are never surprised by a bill.</p>
<p>We favor agreement where it is realistic and prepare every case as though a judge will hear it.</p>
<a class="btn btn-navy" href="about.html">About the firm</a></div>
<figure class="photo-frame reveal d2"><img src="img/people/team-courtroom.jpg" alt="Ben Sampson and Libby Sampson with Tater the bulldog in a courtroom" width="675" height="900" loading="lazy"><figcaption>Ben, Libby, and Tater at the Oklahoma Court of Civil Appeals.</figcaption></figure></div></section>

<section class="s cream"><div class="container"><div class="s-head center reveal"><span class="eyebrow">Practice areas</span><h2>How we can help</h2></div>
{area_cards()}</div></section>

<section class="s"><div class="container"><div class="s-head center reveal"><span class="eyebrow">Our team</span><h2>The people you will work with</h2></div>
<div class="people">{"".join(person_card(p) for p in STAFF)}</div></div></section>

{carousel()}

<section class="s photo-band" style="background-image:url(img/bg/beach-palms.jpg)"><div class="container"><div class="band-card reveal"><span class="eyebrow">After the case</span><h2>Where our clients end up</h2><p>We cannot promise a beach. We can promise to handle the paperwork so you can get back to your life.</p><a class="more" href="testimonials.html">Read client stories</a></div></div></section>

<section class="band" aria-label="Public statistics"><div class="container"><div class="grid4">
<div><strong>2.4</strong><span>U.S. divorces per 1,000 people (2023, provisional)</span></div>
<div><strong>672,502</strong><span>Divorces reported by 45 states + D.C. (2023)</span></div>
<div><strong>41.0%</strong><span>Custodial parents with a support agreement (2022)</span></div>
<div><strong>$19.2B</strong><span>Child support received of $29.9B due (2022)</span></div></div>
<small>Real figures from CDC/NCHS FastStats and U.S. Census Bureau report P60-285. <a href="evidence.html">See sources →</a></small></div></section>

<section class="s cream"><div class="container info-grid"><div class="reveal"><span class="eyebrow">Visit the office</span><h2>Just south of downtown Tulsa</h2>{contact_block()}</div>
<div class="map reveal d2">{MAP}</div></div></section>
{cta()}''',"home")

# ---------- PRACTICE AREAS
for a in AREAS:
    r="../"
    paras="".join(f"<h2>{h}</h2>"+"".join(f"<p>{p}</p>" for p in ps) for h,ps in a["sections"])
    steps="".join(f'<div class="step reveal d{i%4}"><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(a["steps"]))
    faqs="".join(f"<details><summary>{q}</summary><p>{ans}</p></details>" for q,ans in a["faqs"])
    side="".join(f'<li><a href="{x["slug"]}.html"{" aria-current=page" if x is a else ""}>{x["name"]}<span>→</span></a></li>' for x in AREAS)
    body=hero(a["name"],a["tagline"],['<a href="../index.html">Home</a>','<a href="index.html">Practice Areas</a>',a["name"]],a["img"],r)+f'''
<section class="s"><div class="container layout"><article class="prose">{paras}
<blockquote>{a["pull"]}</blockquote>
<p class="fine">General educational information about Oklahoma law, written for a student demonstration. It is not legal advice and may not reflect current law. Verify statutes on <a href="https://www.oscn.net/">OSCN</a>.</p></article>
<aside class="side"><div class="side-box dark"><h3>Talk it through</h3><p>Every situation is different. A consultation is the fastest way to understand your options.</p><a class="btn" href="../contact.html" style="width:100%;justify-content:center">Request a consultation</a><p style="margin:14px 0 0;text-align:center"><a href="tel:{TEL}" style="color:var(--sand)">{PHONE}</a></p><p class="fine" style="margin:8px 0 0;text-align:center">Fictional firm; demo only.</p></div>
{stories_for(a["slug"])}<div class="side-box"><h3>Practice areas</h3><ul class="side-nav">{side}</ul></div>
<div class="side-box"><h3>Office hours</h3><table class="hours">{"".join(f"<tr><td>{d}</td><td>{h}</td></tr>" for d,h in HOURS)}</table></div></aside></div></section>
<section class="s cream"><div class="container"><div class="s-head reveal"><span class="eyebrow">The process</span><h2>What to expect, step by step</h2></div><div class="steps">{steps}</div></div></section>
<section class="s"><div class="narrow"><div class="s-head center reveal"><span class="eyebrow">FAQ</span><h2>{a["name"]} questions, answered</h2></div><div class="faq reveal">{faqs}</div></div></section>
{cta(r,f"Questions about {a['name'].lower()}?")}'''
    pages[f"practice-areas/{a['slug']}.html"]=(f"{a['name']} in Tulsa",body,"")
r="../"
pages["practice-areas/index.html"]=("Practice Areas",hero("Practice Areas","Focused family law services for Tulsa-area spouses and parents, from first questions to final orders.",['<a href="../index.html">Home</a>',"Practice Areas"],"gavel.jpg",r)+f'<section class="s cream"><div class="container">{area_cards(r)}</div></section>'+cta(r),"")

# ---------- PEOPLE (character pages)
r="../"
for p in PEOPLE:
    staff=p["kind"]=="staff"
    if staff:
        facts="".join(f"<dt>{k}</dt><dd>{v}</dd>" for k,v in p["facts"])
        rel="".join(f'<li><a href="../practice-areas/{x}.html">{AREA_NAME[x]}<span>→</span></a></li>' for x in p["areas"])
        body=f'''<section class="person-hero"><div class="container ph-grid"><div class="ph-text"><nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="../team.html">Our Team</a> / {p["name"]}</nav>
<h1>{p["name"]}</h1><p class="role-line">{p["role"]}</p><p class="lead">{p["summary"]}</p><dl class="facts">{facts}</dl>
<a class="btn" href="../contact.html">Schedule a consultation</a></div>{gallery(p)}</div></section>
<section class="s"><div class="container layout"><article class="prose">{"".join(f"<p>{x}</p>" for x in p["bio"])}
<p class="fine">{p["name"]} is a fictional character in a student demonstration, played by a member of the site owner's family or circle of friends. No license, bar admission, or bar number exists.</p></article>
<aside class="side">{f'<div class="side-box"><h3>Practice areas</h3><ul class="side-nav">{rel}</ul></div>' if rel else ""}<div class="side-box"><h3>The team</h3><ul class="side-nav">{"".join(f'<li><a href="{x["slug"]}.html">{x["name"]}<span>{x["role"]}</span></a></li>' for x in STAFF if x is not p)}</ul></div></aside></div></section>{cta(r)}'''
        title=f"{p['name']}, {p['role']}"
    else:
        body=f'''<section class="person-hero"><div class="container ph-grid"><div class="ph-text"><nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="../testimonials.html">Client Stories</a> / {p["name"]}</nav>
<span class="eyebrow">{AREA_NAME[p["area"]]}</span><h1>{p["name"]}</h1><p class="role-line">{p["place"]}</p>
<blockquote class="quote">{p["quote"]}</blockquote></div>{gallery(p)}</div></section>
<section class="s"><div class="container layout"><article class="prose"><h2>The story</h2>{"".join(f"<p>{x}</p>" for x in p["story"])}
<p class="fine">Fictional client and fictional story, played by a member of the site owner's family or circle of friends for a class demonstration. Not a real case or result. Past results do not guarantee future outcomes.</p></article>
<aside class="side"><div class="side-box"><h3>Practice area</h3><ul class="side-nav"><li><a href="../practice-areas/{p["area"]}.html">{AREA_NAME[p["area"]]}<span>→</span></a></li></ul></div><div class="side-box"><h3>More stories</h3><ul class="side-nav">{"".join(f'<li><a href="{x["slug"]}.html">{x["name"]}<span>→</span></a></li>' for x in CLIENTS if x is not p)}</ul></div></aside></div></section>{cta(r)}'''
        title=f"{p['name']}, Client Story"
    pages[f"people/{p['slug']}.html"]=(title,body,"")

r=""
pages["team.html"]=("Our Team",hero("Our Team","A small team that answers the phone, knows your file, and keeps your case moving.",['<a href="index.html">Home</a>','<a href="about.html">Our Firm</a>',"Our Team"],"bg/courtroom-wide.jpg")+f'''
<section class="s cream"><div class="container"><div class="people">{"".join(person_card(p) for p in STAFF)}</div>
<p class="fine" style="text-align:center;margin-top:30px">Fictional characters, played by the site owner's family and friends. Photos used with permission.</p></div></section>{cta()}''',"")

pages["about.html"]=("About the Firm",hero("About Sampson Family Law","A small Tulsa practice, and a student experiment in building a responsible professional website.",['<a href="index.html">Home</a>',"About"],"bg/beach-hero.jpg")+f'''
<section class="s"><div class="container split"><div class="reveal"><span class="eyebrow">Our story (fictional)</span><h2>The family behind Sampson Family Law</h2>
<p>Ben Sampson founded the firm with a simple goal: clients should know their attorney, understand their options, and never be surprised by a bill. Libby Sampson leads the firm's trial work, Jane keeps every file in order, and Tater runs the front desk.</p>
<p>The practice values <strong>clarity</strong>, <strong>steadiness</strong>, and <strong>preparation</strong>.</p>
<a class="btn btn-navy" href="team.html">Meet the team</a></div><figure class="photo-frame reveal d2"><img src="img/people/family-behind-firm.jpg" alt="Ben and Libby Sampson outdoors with Tater the bulldog" width="619" height="900" loading="lazy"><figcaption>The family behind Sampson Family Law.</figcaption></figure></div></section>
<section class="s cream" id="disclaimer"><div class="narrow prose reveal"><span class="eyebrow">About this project</span><h2>A law school demonstration, not a practice</h2>
<p>Sampson Family Law was created by Ben Sampson, a law student, for a course on AI and the Law. The question behind it: can AI agents build a website as polished as a real firm's while staying honest about what it is?</p>
<p>No text, logos, reviews, or layout assets were copied from any real firm. The characters are played by the owner's family and friends using personal photos shared with permission; remaining stock photographs are free-licensed (see <a href="credits.html">credits</a>).</p>
<h2>What is real and what is not</h2><ul><li><strong>Real:</strong> the statistics on the <a href="evidence.html">evidence page</a> (each linked to CDC or Census sources), the official resource links, and the <a href="build-log.html">build log</a>.</li>
<li><strong>Fictional:</strong> the firm, every character and role (attorneys, staff, clients, and receptionist), the address and 555 phone number, testimonials, client stories, outcomes, and founding date.</li>
<li><strong>Not present:</strong> any bar number, license, real award, real review, or real intake system. (The contact form emails the student presenter for a live class demo; please don't send sensitive information.)</li></ul></div></section>{cta()}''',"")

pages["testimonials.html"]=("Client Stories",hero("Client Stories","Fictional stories from fictional clients, written for a class demonstration.",['<a href="index.html">Home</a>','<a href="about.html">Our Firm</a>',"Client Stories"],"bg/beach-palms.jpg")+f'''
<section class="s cream"><div class="container"><div class="stories">{"".join(f'<article class="story reveal"><a href="people/{p["slug"]}.html" tabindex="-1" aria-hidden="true"><img src="img/{p["gallery"][0][0]}" alt="" loading="lazy"></a><div><span class="eyebrow">{AREA_NAME[p["area"]]}</span><blockquote>{p["quote"]}</blockquote><cite>{p["name"]}, {p["place"]}</cite><a class="more" href="people/{p["slug"]}.html">Read the story<span class="sr"> of {p["name"]}</span></a></div></article>' for p in CLIENTS)}</div>
<p class="fine" style="text-align:center;margin-top:30px">All clients, stories, and testimonials are fictional and do not describe real cases or results.</p></div></section>{cta()}''',"")

# ---------- INSIGHTS
r="../"
pages["insights/index.html"]=("Insights",hero("Insights","Plain-English guides on Oklahoma family law topics, written for a student demonstration.",['<a href="../index.html">Home</a>',"Insights"],"law-books.jpg",r)+f'<section class="s cream"><div class="container">{post_cards(r)}</div></section>'+cta(r),"insights")
for p in POSTS:
    pages[f"insights/{p['slug']}.html"]=(p["title"],hero(p["title"],p["dek"],['<a href="../index.html">Home</a>','<a href="index.html">Insights</a>',p["cat"]],p["img"],r)+f'''
<section class="s"><div class="container layout"><article class="prose"><p class="fine">By the Sampson Family Law editorial team (fictional) · {p["read"]} min read · General information, not legal advice.</p>{p["body"]}</article>
<aside class="side"><div class="side-box dark"><h3>Have a question?</h3><p>Talk to an attorney about your specific situation.</p><a class="btn" href="../contact.html" style="width:100%;justify-content:center">Request a consultation</a><p class="fine" style="margin:10px 0 0">Demo only; fictional firm.</p></div>
<div class="side-box"><h3>More insights</h3><ul class="side-nav">{"".join(f'<li><a href="{q["slug"]}.html">{q["title"]}<span>→</span></a></li>' for q in POSTS if q is not p)}</ul></div></aside></div></section>{cta(r)}''',"insights")

# ---------- EVIDENCE (real cited data, unchanged numbers)
r=""
pages["evidence.html"]=("Evidence & Data",hero("Evidence &amp; Data","Real public data with a link to every source. If a number could not be verified, it was left out.",['<a href="index.html">Home</a>',"Evidence &amp; Data"],"law-books.jpg")+f'''
<section class="s"><div class="container">
<div class="stat-cards" style="margin-bottom:60px"><div class="stat-card reveal"><div class="num">2.4 per 1,000</div><p>U.S. divorce rate, provisional 2023 (45 reporting states and D.C.).</p><p class="src">Source: <a href="https://www.cdc.gov/nchs/fastats/marriage-divorce.htm">CDC / NCHS FastStats</a></p></div>
<div class="stat-card reveal d1"><div class="num">$19.2B of $29.9B</div><p>Child support received vs. owed to U.S. custodial parents in 2022.</p><p class="src">Source: <a href="https://www2.census.gov/library/publications/2025/demo/p60-285.pdf">U.S. Census Bureau, P60-285</a></p></div></div>
<h2>Marriage and divorce (U.S.)</h2>
<table class="data"><tr><th>Measure</th><th>Value</th><th>Source</th></tr>
<tr><td>Divorces (45 reporting states + D.C.)</td><td>672,502</td><td rowspan="4"><a href="https://www.cdc.gov/nchs/fastats/marriage-divorce.htm">CDC / NCHS FastStats</a>, provisional 2023</td></tr>
<tr><td>Divorce rate</td><td>2.4 per 1,000 population</td></tr>
<tr><td>Marriages</td><td>2,041,926</td></tr>
<tr><td>Marriage rate</td><td>6.1 per 1,000 population</td></tr></table>
<p class="src">Note: not every state reports divorces to NCHS, so the national divorce count is incomplete. Oklahoma-specific rates are omitted here because they were not verified for this build.</p>
<h2 style="margin-top:50px">Child support (U.S.)</h2>
<table class="data"><tr><th>Measure</th><th>Value</th><th>Source</th></tr>
<tr><td>Custodial parents with agreements supposed to receive support (2022)</td><td>about 4.7 million</td><td rowspan="4"><a href="https://www2.census.gov/library/publications/2025/demo/p60-285.pdf">U.S. Census Bureau, P60-285</a> (2025)</td></tr>
<tr><td>Average annual support due (2022)</td><td>$6,390 (about $533/month); median $4,816</td></tr>
<tr><td>Total due vs. received (2022)</td><td>$29.9 billion due; $19.2 billion received</td></tr>
<tr><td>Share of custodial parents with an agreement (2022)</td><td>41.0%</td></tr>
<tr><td>Parents receiving cash child support (2021)</td><td>4.1 million; $20.2 billion total; $441 average monthly</td><td><a href="https://www.census.gov/library/fact-sheets/2022/demo/p70fs-185.html">U.S. Census Bureau, Child Support Received: 2021</a></td></tr></table>
<p class="src">The 2021 and 2022 figures come from different Census surveys and measure different things, so they should not be compared directly.</p>
<h2 style="margin-top:50px">Official resources</h2>
<ul class="checks"><li><a href="https://oklahoma.gov/okdhs/services/child-support-services.html">Oklahoma Human Services, Child Support Services</a></li>
<li><a href="https://www.oscn.net/">Oklahoma State Courts Network (OSCN)</a> for statutes and court records</li>
<li><a href="https://www.acf.hhs.gov/css">U.S. Office of Child Support Services (HHS)</a></li>
<li><a href="https://www.legalaidok.org/">Legal Aid Services of Oklahoma</a> for people who need real legal help</li></ul></div></section>''',"")

# ---------- CONTACT
pages["contact.html"]=("Contact",hero("Contact Us","Tell us a little about your situation and we will explain your options. (Class demonstration: submissions go to the student presenter.)",['<a href="index.html">Home</a>',"Contact"],"bg/twilight.jpg")+f'''
<section class="s cream"><div class="container info-grid"><div class="reveal"><span class="eyebrow">Get in touch</span><h2>Schedule a confidential consultation</h2><p>Most consultations are held within the same week, in person or by video. Bring any court papers, a rough list of assets and debts, and your questions.</p>{contact_block()}<div class="map" style="margin-top:28px">{MAP}</div></div>
<div class="form-card reveal d1"><h3>Request a consultation</h3><div class="demo-flag" role="note"><strong>Live class demo.</strong> This form really sends your request to the student presenter. Please do not enter sensitive or confidential details.</div>
<form id="consult-form" action="https://formsubmit.co/lus3896@utulsa.edu" method="post" novalidate>
<input type="hidden" name="_subject" value="Sampson Family Law demo consultation request"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">
<div style="position:absolute;left:-9999px" aria-hidden="true"><label for="f-honey">Leave blank</label><input id="f-honey" type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
<div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
<div class="form-row"><div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div><div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div></div>
<div class="field"><label for="f-area">Matter type</label><select id="f-area" name="matter_type"><option value="">Choose one…</option>{"".join(f'<option>{a["name"]}</option>' for a in AREAS)}<option>Something else</option></select></div>
<div class="field"><label for="f-time">Preferred contact time</label><select id="f-time" name="preferred_contact_time"><option>Morning (8–11)</option><option>Midday (11–2)</option><option>Afternoon (2–5)</option><option>Evening (after 5)</option><option>Any time</option></select></div>
<div class="field"><label for="f-msg">How can we help?</label><textarea id="f-msg" name="message" rows="5"></textarea></div>
<p id="form-err" class="form-err" role="alert" hidden></p>
<button type="submit" class="btn" style="width:100%;justify-content:center">Send request</button>
<p class="fine" style="margin-top:12px">Demonstration form for a law school course. Your submission is sent to the student presenter. Don't include sensitive or confidential information.</p></form>
<div id="demo-notice" class="demo-notice success" role="status" tabindex="-1"><div class="ok-check" aria-hidden="true">✓</div><h3 id="ok-title">Thanks.</h3><p>Your request was received; this is a class demonstration, so no attorney-client relationship is formed and no legal services will be provided.</p><p class="fine">For real legal help in Oklahoma, contact <a href="https://www.legalaidok.org/">Legal Aid Services of Oklahoma</a> or a licensed attorney.</p></div></div></div></section>''',"contact")

# ---------- CREDITS
_used=" ".join(v[1] for v in pages.values())
cr=[c for c in json.loads(pathlib.Path("img/credits.json").read_text()) if f'img/{c["key"]}.jpg' in _used]
rows="".join(f'<tr><td><img src="img/{c["key"]}.jpg" alt="" width="120" height="80" style="width:120px;height:80px;object-fit:cover;border-radius:4px" loading="lazy"></td><td><a href="{html.escape(c["page"])}">{html.escape(c["title"])}</a></td><td>{html.escape(c["artist"])}</td><td>{f"<a href=\"{c['licurl']}\">{c['license']}</a>" if c["licurl"] else c["license"]}</td></tr>' for c in cr)
pages["credits.html"]=("Image Credits",hero("Image Credits","Stock photographs are free-licensed and credited here; character photos are personal photos used with permission.",['<a href="index.html">Home</a>',"Credits"],"gavel.jpg")+f'''
<section class="s"><div class="container"><table class="data credits"><tr><th>Preview</th><th>Image (Wikimedia Commons)</th><th>Author</th><th>License</th></tr>{rows}</table>
<p class="src">Changes: images were downscaled, recompressed, and displayed under navy color overlays or cropped. CC BY and CC BY 4.0 images are used with attribution as required; CC0 images require none but are credited anyway.</p>
<h2 style="margin-top:40px">Personal photographs</h2><p>All photographs of people (and Tater), and the Hawaii beach and golf backgrounds, are personal photos used with permission of the owner. They were resized, cropped, and stripped of all EXIF and GPS metadata before publishing. The people shown are family and friends playing fictional characters.</p><h2 style="margin-top:40px">Original artwork</h2><p>The Sampson monogram logo, icons, and the office map illustration are original SVG artwork created for this project.</p></div></section>''',"")

# ---------- PAYMENTS (demo only)
PAY=[("cashapp","Cash App","$SampsonFamilyLaw","Open Cash App, tap the scan icon, and point your camera at the code."),
     ("venmo","Venmo","@Sampson-Family-Law","In Venmo, tap Scan and hold your phone over the code."),
     ("strike","Strike","sampsonlaw","In Strike, tap Send, then scan the code.")]
def pay_card(k,name,handle,how):
    return f'''<article class="pay-card pay-{k} reveal"><div class="pay-top"><span class="wordmark">{name}</span><span class="pay-tag">Demo</span></div>
<div class="qr-wrap"><img src="img/qr/{k}.svg" width="200" height="200" alt="Demo QR code. Opens a demonstration page on this site, not {name}."></div>
<p class="qr-fine">Demo QR, opens a demonstration page</p>
<p class="pay-handle"><span>Pay to (fictional)</span><strong>{html.escape(handle)}</strong></p><p class="pay-how">{how}</p>
<p class="fine">Fictional handle, not a real {name} account. Do not send money.</p></article>'''
pages["payments.html"]=("Make a Payment",hero("Make a Payment","Pay an invoice or replenish a retainer. (Demonstration: no payment can be made on this site.)",['<a href="index.html">Home</a>',"Make a Payment"],"bg/twilight.jpg")+f"""
<div class="pay-banner" role="note"><div class="container"><strong>Demonstration only.</strong> Sampson Family Law is a fictional firm. Nothing on this page can request, process, or receive a payment. Please do not send money to any handle shown here.</div></div>
<section class="s cream"><div class="container"><div class="s-head center reveal"><span class="eyebrow">Pay your invoice</span><h2>Pay with the app you already use</h2><p>Have your invoice number handy. Scan a code with your phone's camera, or enter your invoice details below to see how a real payment portal would work.</p></div>
<div class="trust-row reveal"><span>{ico("shield")} Encrypted connection (HTTPS)</span><span>{ico("doc")} Itemized receipts</span><span>{ico("scale")} Retainers held in trust</span></div>
<p class="fine" style="text-align:center;margin:0 0 34px">Illustrative badges only; they are not certifications, audits, or compliance claims.</p>
<div class="pay-grid">{"".join(pay_card(*x) for x in PAY)}</div></div></section>
<section class="s"><div class="container info-grid"><div class="reveal"><span class="eyebrow">Invoice or retainer</span><h2>Pay by invoice number</h2><p>Enter the invoice number from your statement and the amount you want to pay. Retainer replenishments use the matter number in place of an invoice number.</p>
<ul class="checks"><li>Partial payments are welcome; your balance updates on the next statement.</li><li>Retainer deposits go to the firm's client trust account until earned.</li><li>A receipt is emailed the same business day.</li></ul><p class="fine">Describes how a real firm might work. This fictional firm has no clients, invoices, or trust account.</p></div>
<div class="form-card reveal d1"><h3>Invoice payment</h3><div class="demo-flag" role="note"><strong>Demo form.</strong> Nothing is charged, sent, or stored. Do not enter real card or account details.</div>
<form id="pay-form" action="#" method="post" novalidate>
<div class="form-row"><div class="field"><label for="p-inv">Invoice or matter number</label><input id="p-inv" name="invoice" type="text" placeholder="e.g. SFL-2026-0142" autocomplete="off"></div><div class="field"><label for="p-amt">Amount (USD)</label><input id="p-amt" name="amount" type="text" inputmode="decimal" placeholder="250.00" autocomplete="off"></div></div>
<div class="field"><label for="p-type">Payment for</label><select id="p-type" name="type"><option>Invoice balance</option><option>Retainer replenishment</option><option>Consultation fee</option></select></div>
<div class="field"><label for="p-name">Name on matter</label><input id="p-name" name="name" type="text" autocomplete="off"></div>
<button type="submit" class="btn btn-navy" style="width:100%;justify-content:center">Continue to payment (demo)</button>
<p class="fine" style="margin-top:12px">This demo performs no network request and collects no payment information.</p></form>
<div id="pay-notice" class="demo-notice" role="status" tabindex="-1"><strong>Demo only.</strong> No payment was requested or taken, and nothing was sent or saved. Sampson Family Law is a fictional firm created for a law school course.</div></div></div></section>
<section class="s cream"><div class="narrow reveal"><div class="s-head center"><span class="eyebrow">Payment FAQ</span><h2>Questions about paying</h2></div><div class="faq">
<details><summary>What is a trust account, and why does my retainer go there?</summary><p>Lawyers must keep money that belongs to clients, such as an unearned retainer, separate from the firm's own money, usually in a client trust (IOLTA) account. Funds move to the firm only as work is performed and billed.</p></details>
<details><summary>Will I get a receipt?</summary><p>A real firm would email an itemized receipt showing the invoice, amount, method, and remaining balance. Your monthly statement would also list every payment.</p></details>
<details><summary>Can I pay part of an invoice?</summary><p>Most firms accept partial payments or a payment plan. Ask your attorney before paying.</p></details>
<details><summary>Is it safe to pay with a payment app?</summary><p>Only pay handles listed on your firm's official invoice, and confirm by phone if anything looks different. Payment-app transfers are often hard to reverse. On this demonstration site, every handle is fictional; do not send money.</p></details>
<details><summary>Who do I call with billing questions?</summary><p>A real firm's billing office would help. This firm and its number ({PHONE}) are fictional.</p></details></div></div></section>
<section class="s"><div class="narrow"><p class="fine"><strong>Fine print.</strong> This page is part of a fictional law firm website built for a law school course. No payment can be made here. The Cash App, Venmo, and Strike handles are invented and are not connected to any real account; the QR codes open a demonstration page on this site and never open a payment app. Cash App, Venmo, and Strike are trademarks of their respective owners, are named only to illustrate a typical payments page, and are not affiliated with or endorsing this project. Badges are illustrative and are not certifications.</p></div></section>""","payments")
DEMO_NAMES={"cashapp":"Cash App","venmo":"Venmo","strike":"Strike"}
pages["payment-demo.html"]=("Payment Demo",f"""<section class="demo-screen"><div class="receipt" id="receipt">
<div class="r-check" aria-hidden="true"><svg viewBox="0 0 52 52"><circle cx="26" cy="26" r="24"/><path d="M15 27l7 7 15-16"/></svg></div>
<p class="r-method" id="r-method">Payment</p><h1 class="r-title">Thanks for scanning!</h1><p class="r-to">Sampson Family Law <span>(fictional)</span></p>
<div class="r-big" role="alert"><strong>Demonstration only.</strong> No payment was requested or taken. Sampson Family Law is a fictional firm created for a law school course.</div>
<figure class="tater"><img src="img/people/tater-receptionist.jpg" alt="Tater the bulldog at the front desk"><figcaption>Tater, Receptionist, says thanks for scanning.</figcaption></figure>
<dl class="r-rows"><div><dt>Amount</dt><dd>$0.00</dd></div><div><dt>Status</dt><dd>Nothing charged</dd></div><div><dt>Method</dt><dd id="r-m2">Demo QR</dd></div></dl>
<a class="btn btn-navy" href="payments.html" style="width:100%;justify-content:center">Back to payments page</a>
<p class="fine" style="margin-top:14px">This page never opens a payment app and collects no data. Payment app names are trademarks of their owners, who are not affiliated with this project.</p></div></section>
<script>(function(){{var n={json.dumps(DEMO_NAMES)};var m=new URLSearchParams(location.search).get("method");var t=n[m]||"Demo QR";document.getElementById("r-method").textContent=t+" · demo";document.getElementById("r-m2").textContent=t+" (demo)";if(n[m])document.getElementById("receipt").classList.add("m-"+m)}})();</script>""","")

# ---------- BUILD LOG
def md2html(md):
    out=[];inlist=False
    for line in md.splitlines():
        l=html.escape(line); l=re.sub(r"`([^`]+)`",r"<code>\1</code>",l); l=re.sub(r"\*\*([^*]+)\*\*",r"<strong>\1</strong>",l)
        if line.startswith("- "):
            if not inlist: out.append('<ul class="log">');inlist=True
            out.append(f"<li>{l[2:]}</li>");continue
        if inlist: out.append("</ul>");inlist=False
        if line.startswith("## "): out.append(f'<h2 style="margin-top:30px">{l[3:]}</h2>')
        elif line.startswith("# "): continue
        elif line.strip(): out.append(f"<p>{l}</p>")
    if inlist: out.append("</ul>")
    return "\n".join(out)
pages["build-log.html"]=("Build Log",hero("Build Log","How AI agents built this site, including wrong turns. Rendered from BUILD_LOG.md.",['<a href="index.html">Home</a>',"Build Log"],"signing.jpg")+'<section class="s"><div class="narrow prose">'+md2html(pathlib.Path("BUILD_LOG.md").read_text())+'</div></section>',"")

for p,v in pages.items():
    t,b=v[0],v[1]; cur=v[2] if len(v)>2 else ""
    pathlib.Path(p).parent.mkdir(parents=True,exist_ok=True)
    pathlib.Path(p).write_text(shell(p,t,b,current=cur))
pathlib.Path("img/favicon.svg").write_text(LOGO.replace('role="img"','xmlns="http://www.w3.org/2000/svg" role="img"'))
print(len(pages),"pages")
