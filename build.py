"""Generates the static pages with a shared header/banner/footer. Run: python3 build.py"""
import html, re, pathlib
AREAS=[("family-law","Family Law"),("mediation","Mediation"),("divorce","Divorce"),("child-custody","Child Custody"),("child-support","Child Support"),("criminal-law","Criminal Law")]
FICTION='<span class="tag">Fictional example</span>'
def shell(path,title,body):
    r="../"*path.count("/")
    pa="".join(f'<a href="{r}practice-areas/{s}.html">{n}</a>' for s,n in AREAS)
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex"><title>{title} | Sampson Family Law (Student Project)</title>
<link rel="stylesheet" href="{r}css/styles.css"></head><body>
<div class="student-banner" role="note">Student project for a law school class. Not a law firm. No legal advice.</div>
<header><div class="container"><nav aria-label="Main">
<a class="logo" href="{r}index.html">Sampson <span>Family Law</span></a>
<button class="menu-toggle" aria-expanded="false" aria-label="Open menu">Menu</button>
<ul>
<li><a href="{r}index.html">Home</a></li>
<li class="dropdown"><button aria-expanded="false">Practice Areas ▾</button><div class="dropdown-content"><a href="{r}practice-areas/index.html">All practice areas</a>{pa}</div></li>
<li class="dropdown"><button aria-expanded="false">About ▾</button><div class="dropdown-content"><a href="{r}about.html">About the project</a><a href="{r}stories.html">Client stories (fictional)</a><a href="{r}build-log.html">Build log</a></div></li>
<li><a href="{r}evidence.html">Evidence &amp; Resources</a></li>
<li><a href="{r}contact.html">Contact (demo)</a></li>
</ul></nav></div></header>
<main>{body}</main>
<footer><div class="container"><p>© 2026 Sampson Family Law, a fictional firm created as a student project for a law school AI and the Law class.</p>
<p>Not a law firm. Not a licensed attorney. Nothing here is legal advice. No attorney-client relationship is created by using this site.
If you need legal help in Oklahoma, see <a href="https://www.legalaidok.org/">Legal Aid Services of Oklahoma</a>.</p></div></footer>
<script src="{r}js/main.js"></script></body></html>
'''
def head(t,s): return f'<section class="page-head"><div class="container"><h1>{t}</h1><p>{s}</p></div></section>'
DISC='<div class="disclaimer"><strong>Student class project only.</strong> Sampson Family Law is not a real law firm. The creator is a law student and is not licensed to practice law in Oklahoma or any other jurisdiction. Nothing on this site is legal advice. Do not rely on it for a real legal matter.</div>'
pages={}
pages["index.html"]=("Home",f'''<section class="hero"><div class="container">
<h1>Compassionate Guidance Through Life's Most Important Moments</h1>
<p>A student-built model of a Tulsa family law website: divorce, custody, mediation, and more, presented evidence first.</p>
<a href="contact.html" class="btn">Try the demo contact form</a></div></section>
<div class="container">{DISC}</div>
<section><div class="container"><h2>Practice areas (as a real firm might describe them)</h2><div class="grid">
''' + "".join(f'<div class="card"><h3>{n}</h3><p><a href="practice-areas/{s}.html">Read the overview →</a></p></div>' for s,n in AREAS) + '''
</div></div></section>
<section class="alt"><div class="container"><h2>Evidence first</h2>
<p>Instead of marketing claims, this project shows published public data with a link to every source. Two examples:</p>
<div class="grid" style="margin-top:20px">
<div class="card"><div class="stat">2.4 per 1,000</div><p>U.S. divorce rate, provisional 2023 (45 reporting states and D.C.).</p><p class="src">Source: <a href="https://www.cdc.gov/nchs/fastats/marriage-divorce.htm">CDC / NCHS FastStats</a></p></div>
<div class="card"><div class="stat">$19.2B of $29.9B</div><p>Child support received vs. owed to U.S. custodial parents in 2022.</p><p class="src">Source: <a href="https://www2.census.gov/library/publications/2025/demo/p60-285.pdf">U.S. Census Bureau, P60-285</a></p></div>
</div><p style="margin-top:20px"><a href="evidence.html">See all data and sources →</a></p></div></section>
<section><div class="container"><h2>How this site was built</h2><p>AI agents turned a one-page draft into this multi-page site, and every step is logged. <a href="build-log.html">Read the build log →</a></p></div></section>''')

AREA_BODY={
"family-law":("Family Law","<p>Family law covers the legal relationships within a family: marriage and divorce, parentage, custody and visitation, child support, adoption, and protective orders. In Oklahoma, most of these rules are in Title 43 of the Oklahoma Statutes and are handled in district court.</p><p>A real firm page here would explain who the firm helps and how a first meeting works. This page stays general on purpose.</p>"),
"mediation":("Mediation","<p>Mediation is a process where a neutral third party helps people reach their own agreement, often on a parenting plan or property division, without a judge deciding. It can reduce conflict and cost, but it is not right for every case, for example where there is a history of domestic violence.</p>"),
"divorce":("Divorce","<p>Divorce ends a marriage and usually decides property, debts, support, and (if there are children) custody and child support. Cases range from uncontested agreements to fully contested trials.</p><p>For national context on how common divorce is, see the <a href=\"../evidence.html\">evidence page</a>.</p>"),
"child-custody":("Child Custody","<p>Custody decisions focus on the best interests of the child. Courts look at factors such as each parent's relationship with the child, stability, and the child's needs. Parenting plans set out where a child lives and how time is shared.</p>"),
"child-support":("Child Support","<p>Child support is money one parent pays toward a child's living costs. Oklahoma uses statewide guidelines, and Oklahoma Human Services runs the state's child support services program (<a href=\"https://oklahoma.gov/okdhs/services/child-support-services.html\">official site</a>).</p><p>National data on how much support is actually paid is on the <a href=\"../evidence.html\">evidence page</a>.</p>"),
"criminal-law":("Criminal Law","<p>The original draft listed criminal defense, since family and criminal matters sometimes overlap (for example, protective orders alongside a custody case). It is kept here only as an overview; this project focuses on family law.</p>"),
}
for s,(n,b) in AREA_BODY.items():
    pages[f"practice-areas/{s}.html"]=(n,head(n,"General educational overview, not legal advice.")+f'<section><div class="container">{DISC}{b}<p style="margin-top:20px"><a href="index.html">← All practice areas</a></p></div></section>')
pages["practice-areas/index.html"]=("Practice Areas",head("Practice Areas","How a family law firm might organize its services.")+'<section><div class="container">'+DISC+'<div class="grid">'+"".join(f'<div class="card"><h3><a href="{s}.html">{n}</a></h3><p>{re.sub("<[^>]+>","",AREA_BODY[s][1])[:150]}…</p></div>' for s,n in AREAS)+'</div></div></section>')

pages["about.html"]=("About",head("About the Project","Why Sampson Family Law exists.")+f'''<section><div class="container">{DISC}
<h2>A class project, not a practice</h2>
<p>Sampson Family Law was created for a law school course on AI and the Law. It looks at how firms present themselves online and asks whether AI agents can build a site like that responsibly: with honest disclaimers, cited data, and nothing that could be mistaken for a real attorney.</p>
<p>The design follows the look of many Tulsa-area firm websites (navy and gold, dropdown navigation, practice-area pages, client stories). The difference is that every claim of fact here links to a public source, and every story is labeled fictional.</p>
<h2 style="margin-top:36px">What you will not find here</h2>
<ul><li>No bar number, license number, or credentials. The creator is a student and is not licensed.</li><li>No outcome promises or success rates.</li><li>No way to send information to anyone. The contact form is a demo.</li></ul>
<p style="margin-top:20px">Built by Hunter Briben with AI agents. See the <a href="build-log.html">build log</a>.</p></div></section>''')

stories=[("Resolving Custody Through Mediation","A parent seeking a stable parenting plan worked through mediation to create a schedule built around the child's school and activities, reducing courtroom conflict."),
("Navigating Divorce and Property","Clear documentation and steady guidance helped a client understand their options during a divorce involving shared property and financial accounts."),
("Catching Up on Child Support Paperwork","A parent unsure how support was calculated was pointed to the state's official child support services program and organized their income records before a hearing.")]
pages["stories.html"]=("Client Stories",head("Client Stories","All stories are fictional. No real clients, cases, or outcomes.")+'<section><div class="container">'+DISC+'<div class="grid">'+"".join(f'<div class="card">{FICTION}<h3>{t}</h3><p>{d}</p><p class="src"><em>Fictional story written for a class project. Any resemblance to real people or cases is coincidental.</em></p></div>' for t,d in stories)+'</div></div></section>')

pages["evidence.html"]=("Evidence & Resources",head("Evidence &amp; Resources","Public data with links. If a number could not be verified, it was left out.")+f'''<section><div class="container">{DISC}
<h2>Marriage and divorce (U.S.)</h2>
<table><tr><th>Measure</th><th>Value</th><th>Source</th></tr>
<tr><td>Divorces (45 reporting states + D.C.)</td><td>672,502</td><td rowspan="4"><a href="https://www.cdc.gov/nchs/fastats/marriage-divorce.htm">CDC / NCHS FastStats</a>, provisional 2023</td></tr>
<tr><td>Divorce rate</td><td>2.4 per 1,000 population</td></tr>
<tr><td>Marriages</td><td>2,041,926</td></tr>
<tr><td>Marriage rate</td><td>6.1 per 1,000 population</td></tr></table>
<p class="src">Note: not every state reports divorces to NCHS, so the national divorce count is incomplete. Oklahoma-specific rates are omitted here because they were not verified for this build.</p>
<h2 style="margin-top:36px">Child support (U.S.)</h2>
<table><tr><th>Measure</th><th>Value</th><th>Source</th></tr>
<tr><td>Custodial parents with agreements supposed to receive support (2022)</td><td>about 4.7 million</td><td rowspan="4"><a href="https://www2.census.gov/library/publications/2025/demo/p60-285.pdf">U.S. Census Bureau, P60-285</a> (2025)</td></tr>
<tr><td>Average annual support due (2022)</td><td>$6,390 (about $533/month); median $4,816</td></tr>
<tr><td>Total due vs. received (2022)</td><td>$29.9 billion due; $19.2 billion received</td></tr>
<tr><td>Share of custodial parents with an agreement (2022)</td><td>41.0%</td></tr>
<tr><td>Parents receiving cash child support (2021)</td><td>4.1 million; $20.2 billion total; $441 average monthly</td><td><a href="https://www.census.gov/library/fact-sheets/2022/demo/p70fs-185.html">U.S. Census Bureau, Child Support Received: 2021</a></td></tr></table>
<p class="src">The 2021 and 2022 figures come from different Census surveys and measure different things, so they should not be compared directly.</p>
<h2 style="margin-top:36px">Official resources</h2>
<ul><li><a href="https://oklahoma.gov/okdhs/services/child-support-services.html">Oklahoma Human Services, Child Support Services</a></li>
<li><a href="https://www.oscn.net/">Oklahoma State Courts Network (OSCN)</a> for statutes and court records</li>
<li><a href="https://www.acf.hhs.gov/css">U.S. Office of Child Support Services (HHS)</a></li>
<li><a href="https://www.legalaidok.org/">Legal Aid Services of Oklahoma</a> for people who need real legal help</li></ul>
</div></section>''')

pages["contact.html"]=("Contact (Demo)",head("Contact (Demo Only)","This form does not send anything anywhere.")+f'''<section><div class="container">{DISC}
<form id="demo-form" class="contact-form" action="#" novalidate>
<label for="n">Name</label><input id="n" type="text" autocomplete="off">
<label for="e">Email</label><input id="e" type="email" autocomplete="off">
<label for="m">How can we help? (demo only; please do not enter real details)</label><textarea id="m" rows="5"></textarea>
<p style="margin-top:16px"><button type="submit" class="btn">Send (demo)</button></p></form>
<div id="demo-notice" class="demo-notice" role="status"><strong>Demo only.</strong> Nothing was sent or saved. This is a student project, not a law firm. For real legal help in Oklahoma, contact <a href="https://www.legalaidok.org/">Legal Aid Services of Oklahoma</a> or a licensed attorney.</div>
<p style="margin-top:24px">Location in the story: Tulsa, Oklahoma (fictional firm, no real office).</p></div></section>''')

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
pages["build-log.html"]=("Build Log",head("Build Log","How AI agents built this site. Rendered from BUILD_LOG.md.")+'<section><div class="container">'+md2html(pathlib.Path("BUILD_LOG.md").read_text())+'</div></section>')

for p,(t,b) in pages.items(): pathlib.Path(p).write_text(shell(p,t,b))
print(len(pages),"pages")
