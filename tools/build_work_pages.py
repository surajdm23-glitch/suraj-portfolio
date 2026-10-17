"""Build the project pages in work/ from the original design documents in source/.

Each original keeps its own layout, colours and fonts. This script only:
  1. swaps embedded base64 images for the extracted files in images/work/<project>/
     (listed in document order below),
  2. removes the document's own top nav,
  3. wraps the content in the portfolio shell (assets/shell.css + assets/shell.js).

Run from the project root:  python3 tools/build_work_pages.py
If you add or reorder images in an original, update its `imgs` list to match.
"""
import re
I="../images/work/"
P=[dict(src="source/AI Assisted Workflow.html",out="work/ai-assisted-workflow.html",key="ai",n="01",
        title="An AI-Assisted Design Workflow — Suraj",
        imgs=[I+"ai-assisted-workflow/"+x for x in ["01-legacy-rate-card.jpg","02-vscode-claude-code.jpg","03-phase1-party-view.jpg","04-rate-ai.jpg"]],
        css="html[data-theme=\"dark\"]{--cp-bg:#1c1b19;--cp-bg-elevated:#151412;--cp-surface:#1f1d1a;--cp-surface-soft:#252320;--cp-border:#2f2c28;--cp-border-strong:#4a4640;--cp-panel:rgba(31,29,26,.72);--cp-panel-strong:rgba(31,29,26,.96);--cp-overlay:rgba(21,20,18,.88)}.cover{min-height:calc(100dvh - 84px)!important;padding-top:clamp(56px,7vw,96px)!important}"),
   dict(src="source/Rate Calculation Logic Builder Design.html",out="work/rate-calculation-logic-builder.html",key="rate",n="02",dark="rate-dark.css",
        title="Rate Calculation Logic Builder — Suraj",
        imgs=[I+"rate-calculation/00-pipeline.png"]+[I+"rate-calculation/"+x+".jpg" for x in ["01-party-view","02-empty-state","03-know-more","04-select-level","05-get-started","06-add-rule-panel","07-kanban","08-kebab-menu"]],
        css=".page{padding-top:0!important}.img-full img{max-width:100%;height:auto}@media (max-width:760px){.w [style*=\"grid-template-columns:1fr 1fr\"]{grid-template-columns:1fr!important}}"),
   dict(src="source/Mid Mile App Design.html",out="work/mid-mile-preload-app.html",key="mid",n="03",
        title="Mid-Mile Pre-Load App — Suraj",
        imgs=[I+"mid-mile/"+x for x in ["00-hero.png","nom-route.png","nom-consignment.png","nom-item.png","nom-units.png","s01-home-route-list.jpg","s02-route-details.jpg","s03-loading-scanning.jpg","s04a-scan-initiation.jpg","s04b-manual-entry.jpg","s05a-exception-shipment.jpg","s05b-exception-sku.jpg","s06-loading-complete.jpg","b1-loaded.png","b2-damaged-fit.png","b3-not-fit-missing.png"]],
        css="html[data-theme=\"dark\"]{--cp-bg:#1c1b19;--cp-bg-elevated:#151412;--cp-surface:#1f1d1a;--cp-surface-soft:#252320;--cp-border:#2f2c28;--cp-border-strong:#4a4640;--cp-panel:rgba(31,29,26,.72);--cp-panel-strong:rgba(31,29,26,.96);--cp-overlay:rgba(21,20,18,.88)}.cover{min-height:calc(100dvh - 84px)!important;padding-top:clamp(56px,7vw,96px)!important}@media (max-width:880px){.chapter-inner,#screens [style*=\"grid-template-columns:140px\"]{grid-template-columns:minmax(0,1fr)!important;gap:20px!important}.chapter-inner>*{min-width:0}}@media (max-width:760px){[style*=\"grid-template-columns:1fr 1fr\"]{grid-template-columns:1fr!important}}")]
WORK={"01":("ai-assisted-workflow.html","An AI-Assisted Design Workflow","Process, 2026","Using AI as a continuous critic, not a generator, in the design process.","ai-assisted-design-workflow.png"),
      "02":("rate-calculation-logic-builder.html","Rate Calculation Logic Builder","Enterprise web, 2026","A visual builder for configuring rate calculation logic across shipments.","rate-calculation-logic-builder.png"),
      "03":("mid-mile-preload-app.html","Mid-Mile Preload App","Mobile app, 2026","A warehouse loading flow for FarEye's Pilot app, from pending vehicles to item scanning.","mid-mile-preload-app.png")}
ORDER={"01":["02","03"],"02":["03","01"],"03":["01","02"]}
NEXT={"01":("rate-calculation-logic-builder.html","Rate Calculation Logic Builder","A visual builder for configuring rate calculation logic across shipments.","rate-calculation-logic-builder.png"),
      "02":("mid-mile-preload-app.html","Mid-Mile Pre-Load App","A warehouse loading flow for FarEye's Pilot app, from pending vehicles to item scanning.","mid-mile-preload-app.png"),
      "03":("ai-assisted-workflow.html","An AI-Assisted Design Workflow","Using AI as a continuous critic, not a generator, in the design process.","ai-assisted-design-workflow.png")}
X='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 5l14 14M19 5L5 19"/></svg>'
MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>'
def top(p):
    nx=NEXT[p["n"]]
    return f'''
<!-- ===== Portfolio shell (assets/shell.css) ===== -->
<button class="pf pf-rail pf-rail-l" id="pfRailL" data-pf-contact aria-label="Get in touch"><span id="pfRailLabel">Get in touch</span></button>
<div class="pf pf-rail pf-rail-r">
  <button class="pf-icon pf-plus" data-pf-menu aria-label="Open menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3v18M3 12h18"/></svg></button>
  <button class="pf-icon" data-theme-toggle aria-label="Switch light or dark theme">{MOON}</button>
</div>
<div class="pf pf-header" role="banner">
  <div class="pf-nav">
    <div class="pf-left"><a class="pf-icon pf-back" href="../index.html#work" aria-label="Back to work" title="Back to work"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg></a><a href="../index.html" class="pf-brand">Suraj</a></div>
    <div class="pf-links" role="navigation" aria-label="Main">
      <a href="../about.html">About</a><a href="../index.html#work" aria-current="page">Work</a><a href="../index.html#experience">Experience</a><a href="../index.html#articles">Articles</a><a href="#" data-pf-contact>Contact</a>
    </div>
    <div class="pf-end">
      <span class="pf-clock" id="pfClock">Kodagu, Karnataka<b>✳</b>--:--</span>
      <button class="pf-icon pf-mobile" data-theme-toggle aria-label="Switch light or dark theme">{MOON}</button>
      <button class="pf-icon pf-plus pf-mobile" data-pf-menu aria-label="Open menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4v16M4 12h16"/></svg></button>
    </div>
  </div>
</div>
<!-- ===== Original project document ===== -->
'''
def card(k):
    w=WORK[k]
    return f'<a class="pf-card" href="{w[0]}"><div class="pf-thumb"><img src="../images/projects/{w[4]}" alt="" loading="lazy"></div><h3>{w[1]}<span>{w[2]}</span></h3><p>{w[3]}</p></a>'
def bottom(p):
    nx=NEXT[p["n"]]
    return f'''
<!-- ===== Portfolio shell ===== -->
<div class="pf pf-more"><div class="pf-mhead"><h2>More work</h2><span></span><a href="../index.html#work">All work</a></div><div class="pf-mgrid">{"".join(card(k) for k in ORDER[p["n"]])}</div></div>
<div class="pf pf-footer" id="pfContact" role="contentinfo">
  <p class="pf-tag">Digital Product Designer &nbsp;|&nbsp; Enterprise B2B SaaS</p>
  <a class="pf-mail" href="mailto:surajdm23@gmail.com">surajdm23@gmail.com</a><br>
  <button class="pf-ghost" data-pf-copy>Copy email</button>
  <div class="pf-foot">
    <div class="pf-cols">
      <ul><li><a href="../index.html">Home</a></li><li><a href="../index.html#work">Work</a></li><li><a href="../index.html#experience">Resume</a></li><li><a href="../index.html#testimonials">Testimonials</a></li><li><a href="../index.html#articles">Articles</a></li></ul>
      <ul><li><a href="https://www.linkedin.com/in/surajdm23/" target="_blank" rel="noopener noreferrer">LinkedIn</a></li><li><a href="https://medium.com/@surajdm23" target="_blank" rel="noopener noreferrer">Medium</a></li><li><a href="https://www.behance.net/surajdsuraj" target="_blank" rel="noopener noreferrer">Behance</a></li></ul>
    </div>
    <small>© <span id="pfYear"></span> Suraj</small>
  </div>
</div>
<div class="pf pf-scrim" id="pfScrim"></div>
<div class="pf pf-menu" id="pfMenu" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="pf-mtop"><strong>Suraj</strong><button class="pf-close" data-pf-close aria-label="Close menu">{X}</button></div>
  <div class="pf-mlinks" role="navigation"><a href="../index.html">Home</a><a href="../about.html">About</a><a href="../index.html#services">Services</a><a href="../index.html#work">Work</a><a href="../index.html#experience">Experience</a><a href="../index.html#articles">Articles</a><a href="#" data-pf-contact>Contact</a></div>
  <p class="pf-mfoot">Digital Product Designer &nbsp;|&nbsp; Enterprise B2B SaaS</p>
</div>
<div class="pf pf-drawer" id="pfDrawer" role="dialog" aria-modal="true" aria-label="Contact">
  <div class="pf-dtop">
    <div class="pf-socials"><a href="https://www.linkedin.com/in/surajdm23/" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="https://medium.com/@surajdm23" target="_blank" rel="noopener noreferrer">Medium</a><a href="https://www.behance.net/surajdsuraj" target="_blank" rel="noopener noreferrer">Behance</a></div>
    <button class="pf-close" data-pf-close aria-label="Close contact">{X}</button>
  </div>
  <div>
    <a class="pf-mail" href="mailto:surajdm23@gmail.com">surajdm23@gmail.com</a>
    <p>Tell me a little about what you're building, your timeline and where you need help. I usually reply within two working days.</p>
    <div class="pf-drow"><button class="pf-ghost" data-pf-copy>Copy email</button><a class="pf-ghost pf-drow-dl" href="../pdf/Daddera%20Suraj%20S%20-%20Resume.pdf" download="Daddera-Suraj-S-Resume.pdf"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>Download CV</a></div>
  </div>
</div>
<div class="pf pf-cursor" id="pfCursor" aria-hidden="true"></div>
<script src="../assets/shell.js?v=3"></script>
'''
HEAD_SHELL='''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/shell.css?v=3">
<link rel="stylesheet" href="../assets/harmonize.css?v=3">
'''
for p in P:
    s=open(p["src"]).read()
    # 1. embedded images -> extracted files (same order as in the document)
    it=iter(p["imgs"]);n=[0]
    def rep(m):
        n[0]+=1; return next(it)
    s=re.sub(r'data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+',rep,s)
    assert n[0]==len(p["imgs"]),(p["src"],n[0])
    # 2. drop the document's own top nav (first <nav> after <body>)
    b=s.index("<body>");m=re.compile(r'<nav\b.*?</nav>',re.S).search(s,b)
    assert m and m.start()-b<200,p["src"]
    s=s[:m.start()]+s[m.end():]
    # 3. title, theme handling, shell styles
    s=re.sub(r"<title>.*?</title>",f"<title>{p['title']}</title>",s,count=1)
    # follow the portfolio's stored theme (shared with index.html through localStorage)
    THEME="<script>try{document.documentElement.dataset.theme=localStorage.getItem('theme')||'light'}catch(e){document.documentElement.dataset.theme='light'}</script>"
    s,k=re.subn(r'<script>\s*\(\(\) => \{.*?data-theme.*?</script>',THEME,s,count=1,flags=re.S)
    if not k: s=s.replace("</head>",THEME+"\n</head>",1)
    extra=f'<link rel="stylesheet" href="../assets/{p["dark"]}?v=3">\n' if p.get("dark") else ""
    s=s.replace("</head>",HEAD_SHELL+extra+f"<style>/* portfolio header replaces the original fixed nav */html{{scroll-padding-top:100px}}{p['css']}</style>\n</head>",1)
    # 4. shell around the content
    s=s.replace("<body>",f'<body class="pf-body pf-{p["key"]}">'+top(p),1)
    i=s.rindex("</body>"); s=s[:i]+bottom(p)+s[i:]
    open(p["out"],"w").write(s)
    print(p["out"],len(s))
