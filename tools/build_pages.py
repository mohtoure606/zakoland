"""Build the ZAKO site (v4). Edit content here, then run: python3 tools/build_pages.py

Settings to change at launch are the three constants below.
"""
import os, json
ROOT = os.path.join(os.path.dirname(__file__), '..', 'docs')

DOMAIN = 'https://zakoland.com'
EMAIL = 'team@zakoland.com'
# Formspree endpoint for the ZAKO-only account. Replace ZAKO_FORM_ID with the form's hashid
# (the part after /f/ in the form's endpoint URL), then set FORMS_LIVE = True and rebuild.
FORM_ACTION = 'https://formspree.io/f/ZAKO_FORM_ID'
FORMS_LIVE = False

PHOTOS = {  # name: (widths available, intrinsic w, h)
    'hero': ([800, 1280, 1920], 1920, 992),
    'valley': ([800, 1280, 1920], 1920, 992),
    'plan': ([800, 1360], 1360, 880),
    'dawn': ([800, 1360], 1360, 880),
    'founder': ([480, 839], 839, 1327),
}
ALT = {
    'hero': 'Dusk over Spanish Fork, Utah, with neighborhoods and open land below the mountains',
    'valley': 'View over Lehi and Saratoga Springs, Utah, toward Utah Lake',
    'plan': 'Aerial view of a residential cul-de-sac in Herriman, Utah',
    'dawn': 'Sunrise over a snow-covered neighborhood in Herriman, Utah',
    'founder': 'Mohamed Toure, founder of ZAKO Land Partners',
}

def pic(name, sizes='100vw', eager=False, alt=None):
    ws, w, h = PHOTOS[name]
    s = lambda ext: ', '.join(f'assets/photo/{name}-{x}.{ext} {x}w' for x in ws)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="{s("webp")}" sizes="{sizes}">'
            f'<img src="assets/photo/{name}-{ws[-1]}.jpg" srcset="{s("jpg")}" sizes="{sizes}" width="{w}" height="{h}" '
            f'alt="{ALT[name] if alt is None else alt}" {load} decoding="async"></picture>')

NAV = [('builders.html', 'Builders'), ('landowners.html', 'Landowners'), ('about.html', 'About'), ('contact.html', 'Contact')]

ORG = {
    '@context': 'https://schema.org', '@type': 'Organization', 'name': 'ZAKO Land Partners',
    'url': DOMAIN + '/', 'logo': DOMAIN + '/assets/img/zako-lockup.svg', 'email': EMAIL,
    'description': 'Residential land investment and acquisition in Utah.',
    'areaServed': {'@type': 'State', 'name': 'Utah'},
}

def head(title, desc, path, noindex=False, preload=None):
    canon = f'{DOMAIN}/{"" if path == "index.html" else path}'
    pre = (f'<link rel="preload" as="image" href="assets/photo/{preload}-1280.webp" type="image/webp" '
           f'imagesrcset="assets/photo/{preload}-800.webp 800w, assets/photo/{preload}-1280.webp 1280w'
           f'{", assets/photo/" + preload + "-1920.webp 1920w" if 1920 in PHOTOS[preload][0] else ""}" imagesizes="100vw">') if preload else ''
    ld = f'<script type="application/ld+json">{json.dumps(ORG)}</script>' if path == 'index.html' else ''
    return f'''<!DOCTYPE html>
<html lang="en" data-forms="{'live' if FORMS_LIVE else 'preview'}">
<head>
<meta charset="utf-8">
{'<base href="/">' if path == '404.html' else ''}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ZAKO Land Partners">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ZAKO Land Partners wordmark over a Utah valley at dusk">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
{pre}
<link rel="stylesheet" href="css/site.css">
<script>document.documentElement.classList.add('js')</script>
{ld}
</head>'''

def header(path, over=False):
    links = ''.join(f'<a href="{h}"{" aria-current=page" if h == path else ""}>{t}</a>' for h, t in NAV)
    notice = '' if FORMS_LIVE else '<div class="preview" role="note">Preview. Forms are not connected yet. <button type="button">Dismiss</button></div>'
    return f'''<body class="{'over' if over else ''}">
<a class="skip" href="#main">Skip to content</a>
{notice}
<header class="hdr"><div class="hdr__in">
<a class="logo" href="index.html" aria-label="ZAKO Land Partners, home">
<img class="on-light" src="assets/img/zako.svg" alt="ZAKO" width="104" height="21">
<img class="on-dark" src="assets/img/zako-white.svg" alt="" width="104" height="21"></a>
<button class="menu" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="Main">{links}</nav>
</div></header>'''

FOOTER = f'''<footer class="ftr"><div class="wrap">
<div class="ftr__top">
<a class="logo" href="index.html" aria-label="ZAKO Land Partners, home"><img src="assets/img/zako-lockup.svg" alt="ZAKO Land Partners" width="120" height="36"></a>
<p class="ftr__tag">Residential Land Investment &amp; Acquisition<br>Utah</p>
<nav aria-label="Footer"><a href="builders.html">Builders</a><a href="landowners.html">Landowners</a><a href="about.html">About</a><a href="contact.html">Contact</a></nav>
<p class="ftr__mail"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div>
<div class="ftr__fine">
<p>ZAKO Land Partners does not provide real estate brokerage, engineering, surveying, legal, title or financing services. When those services are needed, they are provided by independent professionals engaged separately.</p>
<p>&copy; <span data-year>2026</span> ZAKO Land Partners &middot; <a href="privacy.html">Privacy</a> &middot; <a href="terms.html">Terms</a> &middot; Photography by Zach Kessinger, Tyler Mower and Michael Tuszynski on Unsplash</p>
</div>
</div></footer>
<script src="js/site.js" defer></script>
</body>
</html>'''

def page(path, title, desc, body, over=False, noindex=False, preload=None):
    with open(os.path.join(ROOT, path), 'w') as fh:
        fh.write(head(title, desc, path, noindex, preload) + '\n' + header(path, over) + '\n<main id="main">\n' + body.strip() + '\n</main>\n' + FOOTER)

# ------------------------------------------------------------------ form helpers
def form(name, inner, submit):
    return f'''<form class="form" name="{name}" action="{FORM_ACTION}" method="POST" data-zako-form novalidate>
<input type="hidden" name="_subject" value="ZAKO website: {name}">
<input type="hidden" name="form" value="{name}">
<p class="hp" aria-hidden="true"><label>Leave this field blank <input name="_gotcha" tabindex="-1" autocomplete="off"></label></p>
{inner}
<div class="status" role="status" tabindex="-1"></div>
<div><button class="btn" type="submit">{submit}</button></div>
</form>'''

def consent(what):
    return f'<label class="check"><input type="checkbox" name="consent" value="yes" required> I agree that ZAKO may use this information to {what}, as described in the <a href="privacy.html">Privacy Policy</a>.</label>'

def field(id_, label, name, typ='text', req=True, auto='', ph=''):
    opt = '' if req else ' <span class="opt">(optional)</span>'
    a = f' autocomplete="{auto}"' if auto else ''
    p = f' placeholder="{ph}"' if ph else ''
    return f'<div class="field"><label for="{id_}">{label}{opt}</label><input id="{id_}" name="{name}" type="{typ}"{" required" if req else ""}{a}{p}></div>'

def select(id_, label, name, options):
    opts = ''.join(f'<option>{o}</option>' for o in options)
    return f'<div class="field"><label for="{id_}">{label}</label><select id="{id_}" name="{name}" required><option value="">Select</option>{opts}</select></div>'

def textarea(id_, label, name, req=False, ph=''):
    opt = '' if req else ' <span class="opt">(optional)</span>'
    p = f' placeholder="{ph}"' if ph else ''
    return f'<div class="field"><label for="{id_}">{label}{opt}</label><textarea id="{id_}" name="{name}"{" required" if req else ""}{p}></textarea></div>'

def chips(name, items):
    return ''.join(f'<label class="chip"><input type="checkbox" name="{name}" value="{v}"><span>{v}</span></label>' for v in items)

def r(d=0):  # reveal-on-scroll attribute with optional stagger (ms)
    return f' data-r style="--d:{d}ms"' if d else ' data-r'

# ------------------------------------------------------------------ shared sections
STEPS = [
    ('Understand the opportunity', 'We start with the property, its location and ownership, and the goals of the people involved.'),
    ('Research the land', 'We review available information on access, zoning, topography, utilities, water and surrounding development.'),
    ('Bring the right expertise', 'When a question needs a specialist, qualified independent professionals can help with surveying, engineering, land use, title and legal matters.'),
    ('Connect the opportunity', 'We look for builders and developers whose needs may align with the property.'),
    ('Move forward carefully', 'When there is mutual interest, the parties evaluate the opportunity and decide next steps with appropriate professional and transaction support.'),
]

def process(heading_tag='h2', intro=True):
    items = ''.join(f'<li{r(i*110)}><span class="num" aria-hidden="true">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS))
    lead = '<p class="lead"' + r(80) + '>A clear sequence from first look to the right connection, with the right people involved at each step.</p>' if intro else ''
    return f'''<section class="process" id="how" aria-labelledby="how-h"><div class="wrap">
<div class="process__head"><p class="eyebrow"{r()}>How we work</p>
<{heading_tag} id="how-h" class="h-lines"{r(40)}><span>Five steps.</span> <span>No shortcuts.</span></{heading_tag}>{lead}</div>
<ol class="steps">{items}</ol>
</div></section>'''

AUDIENCE = [
    ('Builders and developers', 'Researched land opportunities and organized property information to help you evaluate a potential acquisition.'),
    ('Landowners', 'A professional, no-pressure starting point for a conversation about your land.'),
    ('Real estate professionals', 'A working relationship with a team that does its homework, built around appropriate, properly structured transactions.'),
    ('Engineers and surveyors', 'Specialized expertise matters. Qualified independent firms can be engaged when a site needs it.'),
    ('Title, legal, planning and financing', 'Organized opportunities where the right expertise can help a transaction come together properly.'),
]

def network():
    rows = ''.join(f'<li{r(i*70)}><h3>{a}</h3><p>{d}</p></li>' for i, (a, d) in enumerate(AUDIENCE))
    return f'''<section class="band band--ivory" aria-labelledby="net-h"><div class="wrap">
<div class="split split--head">
<div><p class="eyebrow"{r()}>Our network</p><h2 id="net-h" class="h-lines"{r(40)}><span>A strong network.</span> <span>A thoughtful process.</span></h2></div>
<p class="lead"{r(120)}>Residential land opportunities often need more than one perspective. We are building relationships with experienced real estate, surveying, engineering, land use, title, legal and financing professionals, so the right expertise can join the process when it is needed.</p>
</div>
<ul class="audience">{rows}</ul>
<p class="note"{r()}>ZAKO does not provide real estate brokerage, engineering, surveying, legal, title or financing services. Those services are provided by independent, qualified professionals when they are separately engaged.</p>
</div></section>'''

# ------------------------------------------------------------------ HOME
home = f'''
<section class="photo photo--hero" aria-labelledby="h">
{pic('hero', eager=True)}
<div class="photo__in">
<div class="hero__copy">
<p class="eyebrow eyebrow--light rise" style="--d:100ms">Residential Land Investment &amp; Acquisition</p>
<h1 id="h"><span class="rise" style="--d:250ms">Land.</span> <span class="rise" style="--d:420ms">Opportunity.</span> <span class="rise" style="--d:590ms">Vision.</span></h1>
<p class="sub rise" style="--d:820ms">We find residential land in Utah, research what it can become, and connect it with the builders and developers who need it.</p>
</div>
<div class="btns rise" style="--d:1000ms"><a class="btn btn--light" href="builders.html">For builders</a><a class="btn btn--ghost" href="landowners.html">For landowners</a></div>
</div>
<span class="cue" aria-hidden="true"></span>
</section>

<section class="band intro" aria-labelledby="what-h"><div class="wrap">
<p class="eyebrow center"{r()}>What we do</p>
<h2 id="what-h" class="statement"{r(80)}>We look closely at land, understand what it could support, and bring the right opportunities to the builders shaping Utah's communities.</h2>
<ul class="facts">
<li{r(0)}><span>Who</span>Homebuilders, developers and landowners</li>
<li{r(100)}><span>Where</span>Utah County, Salt Lake County and growing Utah markets</li>
<li{r(200)}><span>How</span>Research first, clear communication, the right professionals</li>
</ul>
</div></section>

<section class="pair" aria-label="Who we work with">
<a class="photo photo--half tile" href="builders.html">{pic('plan', '(min-width: 821px) 50vw, 100vw')}
<div class="photo__in"><div{r()}><p class="eyebrow eyebrow--light">For builders and developers</p><h2>Tell us what you build.</h2><p>Share your markets and criteria. We look for land that fits.</p>
<span class="more">Share your criteria</span></div></div></a>
<a class="photo photo--half tile" href="landowners.html">{pic('valley', '(min-width: 821px) 50vw, 100vw')}
<div class="photo__in"><div{r(120)}><p class="eyebrow eyebrow--light">For landowners</p><h2>Own land in Utah?</h2><p>Start a conversation. No cost, no pressure, and a straight answer.</p>
<span class="more">Tell us about it</span></div></div></a>
</section>

{process()}

{network()}

<section class="band" aria-labelledby="founder"><div class="wrap founder">
<div class="frame"{r()}>{pic('founder', '(min-width: 821px) 40vw, 90vw')}</div>
<div>
<p class="eyebrow"{r()}>Our founder</p>
<h2 id="founder"{r(60)}>Founded with a civil engineering perspective.</h2>
<p class="lead mt"{r(120)}>ZAKO was founded by Mohamed Toure. His background in land surveying and civil engineering shapes how we look at every site: what it is today, and what it could become.</p>
<p class="mt"{r(180)}><a class="link" href="about.html">Read his story</a></p>
</div>
</div></section>

<section class="photo photo--end" aria-labelledby="c">
{pic('dawn')}
<div class="photo__in"><div>
<h2 id="c"{r()}>Start the conversation.</h2>
<p class="sub"{r(100)}>Builders, landowners and land professionals across Utah.</p>
<div class="btns"{r(200)}><a class="btn btn--light" href="contact.html">Contact ZAKO</a></div>
</div></div>
</section>'''
page('index.html', 'ZAKO Land Partners | Utah Residential Land Investment & Acquisition',
     'ZAKO Land Partners finds residential land in Utah, researches what it can become, and connects it with the builders and developers who need it.',
     home, over=True, preload='hero')

# ------------------------------------------------------------------ BUILDERS
MARKETS = ['Alpine', 'Highland', 'Draper', 'Lehi', 'Saratoga Springs', 'Eagle Mountain', 'Utah County', 'Salt Lake County', 'Elsewhere in Utah']
TYPES = ['Infill lots', 'Older homes on large lots', 'Small subdivisions', 'Larger tracts', 'Assemblages', 'Townhome sites']
BENEFITS = [
    ('Researched opportunities', 'Land we have looked at before it reaches you, not a list sent to everyone.'),
    ('Property characteristics', 'Zoning, access, frontage, topography, utilities and water, summarized in plain terms.'),
    ('Constraints flagged early', 'Potential issues identified up front, so you can rule a site in or out sooner.'),
    ('Matched to your criteria', 'Opportunities filtered by your markets, lot sizes, product and price range.'),
    ('Organized information', 'Sources, open questions, and what is verified versus preliminary, in one package.'),
    ('A relationship, not a pitch', 'Direct communication, and an honest answer when a site does not fit.'),
]
ben = ''.join(f'<li{r((i % 2) * 90)}><span class="num" aria-hidden="true">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(BENEFITS))
builders = f'''
<section class="photo photo--page" aria-labelledby="h">
{pic('plan', eager=True)}
<div class="photo__in"><div>
<p class="eyebrow eyebrow--light rise" style="--d:100ms">For builders and developers</p>
<h1 id="h" class="rise" style="--d:250ms">Tell us what you build. We will look for the land.</h1>
</div></div>
</section>

<section class="band" aria-labelledby="what"><div class="wrap">
<div class="split split--head">
<div><p class="eyebrow"{r()}>What we bring</p><h2 id="what"{r(40)}>Land that fits, with the homework done.</h2></div>
<p class="lead"{r(120)}>We want to understand where you build, what you build and what you are looking for. Your criteria tell us where to look and what to rule out.</p>
</div>
<ul class="grid6">{ben}</ul>
</div></section>

<section class="band band--tight band--ivory" aria-labelledby="limits"><div class="wrap callout"{r()}>
<h2 id="limits">Research is where we start, not where you stop.</h2>
<p>Our property research is preliminary. ZAKO does not guarantee zoning approvals, utility availability, development feasibility or project outcomes. Every site should be confirmed through your own due diligence and qualified professionals.</p>
</div></section>

{process(intro=False)}

<section class="band band--ivory" id="criteria" aria-labelledby="f"><div class="wrap split">
<div><p class="eyebrow"{r()}>Share your criteria</p><h2 id="f"{r(40)}>Tell us what you are looking for.</h2>
<p class="lead mt"{r(100)}>It takes about two minutes and creates no obligation. We use it to bring you opportunities that fit.</p></div>
{form('builder-criteria', f"""
<div class="row2">{field('b-company','Company','company',auto='organization')}{field('b-name','Name','name',auto='name')}</div>
<div class="row2">{field('b-email','Business email','email','email',auto='email')}{field('b-phone','Phone','phone','tel',False,'tel')}</div>
<fieldset data-require-one><legend>Target markets</legend><div class="chips">{chips('markets', MARKETS)}</div></fieldset>
<fieldset><legend>Property types <span class="opt">(optional)</span></legend><div class="chips">{chips('property_types', TYPES)}</div></fieldset>
{field('b-size','Lot sizes or acreage','lot_sizes',req=False,ph='For example: 0.5 to 5 acres')}
{textarea('b-more','Anything else','criteria',ph='Price range, zoning, utilities, timing')}
{consent('contact me about land opportunities')}""", 'Send criteria')}
</div></section>'''
page('builders.html', 'Land Acquisition for Utah Builders | ZAKO Land Partners',
     'Researched residential development land for Utah homebuilders and developers, matched to your markets and acquisition criteria.',
     builders, over=True, preload=None)

# ------------------------------------------------------------------ LANDOWNERS
LSTEPS = [
    ('Start a conversation', 'Share the address or parcel number and a little about your plans. There is no cost and no obligation.'),
    ('We take a careful look', 'We review public information about the property and what builders in the area are looking for.'),
    ('We talk about options', 'If there may be a fit, we explain what we see and what a next step could look like. If not, we tell you.'),
]
lst = ''.join(f'<li{r(i*110)}><span class="num" aria-hidden="true">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(LSTEPS))
landowners = f'''
<section class="photo photo--page" aria-labelledby="h">
{pic('valley', eager=True)}
<div class="photo__in"><div>
<p class="eyebrow eyebrow--light rise" style="--d:100ms">For landowners</p>
<h1 id="h" class="rise" style="--d:250ms">Your land may be worth a closer look.</h1>
</div></div>
</section>

<section class="band" aria-labelledby="how-l"><div class="wrap">
<div class="split split--head">
<div><p class="eyebrow"{r()}>How it works</p><h2 id="how-l"{r(40)}>Simple, unhurried and clear.</h2></div>
<p class="lead"{r(120)}>You do not need to know anything about development to start. Tell us a little about your property and we will take it from there.</p>
</div>
<ol class="steps steps--3">{lst}</ol>
</div></section>

<section class="band band--tight band--ivory" aria-labelledby="know"><div class="wrap split">
<div><h2 id="know"{r()}>Good to know</h2></div>
<ul class="points">
<li{r()}><h3>We do not represent you</h3><p>ZAKO is not a real estate agent, and we do not list or market your property.</p></li>
<li{r(60)}><h3>Bring your own advisors</h3><p>You are welcome to involve your own agent, attorney or advisor at any point.</p></li>
<li{r(120)}><h3>Your information stays private</h3><p>We share property details with others only with your permission.</p></li>
<li{r(180)}><h3>Nothing is final until it is in writing</h3><p>A conversation creates no obligation. Any transaction would need a written agreement you have reviewed and signed.</p></li>
</ul>
</div></section>

<section class="band" id="property" aria-labelledby="f"><div class="wrap split">
<div><p class="eyebrow"{r()}>Tell us about your property</p><h2 id="f"{r(40)}>Start with the basics.</h2>
<p class="lead mt"{r(100)}>An address or parcel number is enough to begin.</p></div>
{form('property-owner', f"""
<div class="row2">{field('o-name','Name','name',auto='name')}{field('o-email','Email','email','email',auto='email')}</div>
<div class="row2">{field('o-phone','Phone','phone','tel',False,'tel')}
{select('o-rel','You are the','relationship',['Owner','Co-owner','Authorized representative'])}</div>
{field('o-addr','Property address or parcel number','property')}
<div class="row2">{select('o-county','County','county',['Utah County','Salt Lake County','Another Utah county'])}
{field('o-acres','Approximate acreage','acreage',req=False)}</div>
{textarea('o-msg','Anything we should know','message')}
{consent('review the property and contact me')}""", 'Submit property')}
</div></section>'''
page('landowners.html', 'Utah Land Opportunities for Landowners | ZAKO Land Partners',
     'Own residential land in Utah? Start a no-pressure conversation with ZAKO about what your property could support.',
     landowners, over=True)

# ------------------------------------------------------------------ ABOUT
STORY = [
    'I am originally from Mali, and Utah has become home. It is where I studied civil engineering.',
    'Before entering engineering, I worked on survey crews across Utah, gaining firsthand experience with property boundaries, land measurement and the early stages of residential development. Today, my work in civil engineering includes water and irrigation projects.',
    'These experiences shaped how I understand land. Its potential goes beyond acreage or location. Access, topography, drainage, water, utilities and surrounding development all play an important role in what a property may become.',
    'I founded ZAKO to bring that perspective to residential land investment and acquisition. Our focus is to identify promising land, understand the factors that shape its potential, and connect it with the builders and developers who may be the right fit.',
    'We believe good land decisions begin with careful research, clear communication and strong professional relationships.',
]
story = ''.join(f'<p{r(60 + i*40)}>{s}</p>' for i, s in enumerate(STORY))
about = f'''
<section class="phead"><div class="wrap">
<p class="eyebrow rise" style="--d:100ms">About ZAKO</p>
<h1 class="rise" style="--d:220ms">A Utah land company with an engineer's eye.</h1>
<p class="lead rise" style="--d:380ms">ZAKO identifies residential land opportunities and connects them with the builders shaping Utah's communities. We do the research first, so the right opportunities reach the right people.</p>
</div></section>

<section class="band band--ivory" aria-labelledby="f"><div class="wrap founder founder--story">
<div class="frame"{r()}>{pic('founder', '(min-width: 821px) 40vw, 90vw')}</div>
<div class="story">
<p class="eyebrow"{r()}>Founder</p>
<h2 id="f"{r(40)}>Why I started ZAKO</h2>
{story}
<p class="sign"{r(280)}>Mohamed Toure<span>Founder, ZAKO Land Partners</span></p>
</div>
</div></section>

<section class="band" aria-labelledby="b"><div class="wrap split">
<div><p class="eyebrow"{r()}>What we believe</p><h2 id="b"{r(40)}>Principles we work by</h2></div>
<ul class="points">
<li{r()}><h3>Demand comes first</h3><p>We learn what builders need before we look for land.</p></li>
<li{r(60)}><h3>Research before promises</h3><p>We separate what we know from what still needs checking, and we say so.</p></li>
<li{r(120)}><h3>The right expertise</h3><p>Specialized questions go to qualified, independent professionals.</p></li>
<li{r(180)}><h3>Utah first</h3><p>We are starting where we know the ground, and growing with the people we work with.</p></li>
</ul>
</div></section>

{process(intro=False)}'''
page('about.html', 'About | ZAKO Land Partners',
     'ZAKO Land Partners was founded in Utah by Mohamed Toure to bring a surveying and civil engineering perspective to residential land acquisition.', about)

# ------------------------------------------------------------------ CONTACT
ROLES = ['Builder or developer', 'Landowner', 'Real estate professional', 'Engineering or surveying professional', 'Investor or capital partner', 'Other']
contact = f'''
<section class="phead"><div class="wrap">
<p class="eyebrow rise" style="--d:100ms">Contact</p>
<h1 class="rise" style="--d:220ms">Start the conversation.</h1>
<p class="lead rise" style="--d:380ms">Tell us who you are and what you have in mind. We read every message and will get back to you.</p>
</div></section>
<section class="band band--ivory" id="general" aria-labelledby="f"><div class="wrap split">
<div class="aside">
<h2 id="f"{r()}>Send a message</h2>
<dl class="contacts"{r(80)}>
<dt>Email</dt><dd><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></dd>
<dt>Based in</dt><dd>Utah</dd>
<dt>Builders</dt><dd><a class="link" href="builders.html#criteria">Share your criteria</a></dd>
<dt>Landowners</dt><dd><a class="link" href="landowners.html#property">Tell us about your property</a></dd>
</dl></div>
{form('general', f"""
<div class="row2">{field('g-name','Name','name',auto='name')}{field('g-email','Email','email','email',auto='email')}</div>
<div class="row2">{field('g-co','Company','company',req=False,auto='organization')}{field('g-phone','Phone','phone','tel',False,'tel')}</div>
{select('g-role','I am a','role',ROLES)}
{textarea('g-msg','How can we help?','message',req=True)}
{consent('respond to me')}""", 'Send message')}
</div></section>'''
page('contact.html', 'Contact | ZAKO Land Partners',
     'Contact ZAKO Land Partners about Utah residential land opportunities. Builders, landowners and land professionals welcome.', contact)

# ------------------------------------------------------------------ LEGAL (drafts for attorney review; noindex)
DRAFT = '<p class="draft"><strong>Draft for attorney review.</strong> This policy is not in effect until it is finalized.</p>'
privacy = f'''<section class="phead phead--sm"><div class="wrap"><h1>Privacy Policy</h1></div></section>
<section class="band band--flush"><div class="wrap prose">{DRAFT}
<p>This policy explains what ZAKO Land Partners ("ZAKO", "we") collects through this website and how we use it.</p>
<h2>What we collect</h2><ul><li>What you send through our forms: name, company, email, phone, property details and messages.</li><li>Basic technical data our hosting provider records, such as IP address and pages requested.</li></ul><p>We do not use advertising or analytics trackers.</p>
<h2>How we use it</h2><ul><li>To respond to you and evaluate the property or criteria you shared.</li><li>To contact you about land opportunities related to your inquiry.</li><li>To keep business records and run the website securely.</li></ul>
<h2>Sharing</h2><p>We do not sell personal information. We share it only with service providers that run this site and its forms (website hosting through GitHub Pages, and Formspree, which delivers form submissions to our email), with your permission, or when the law requires. We share property details with builders only with the owner's permission.</p>
<h2>Email</h2><p>Every marketing email we send will include a way to opt out, and we will honor your request promptly.</p>
<h2>Your choices</h2><p>To see, correct or delete your information, contact {EMAIL}.</p>
<h2>Security</h2><p>We use reasonable safeguards, but no system is completely secure.</p>
<h2>Children</h2><p>This site is for adults and businesses. We do not knowingly collect information from children under 13.</p>
<p class="mt"><strong>Effective date:</strong> set when finalized.</p></div></section>'''
page('privacy.html', 'Privacy Policy | ZAKO Land Partners', 'How ZAKO Land Partners handles information submitted through this website.', privacy, noindex=True)

terms = f'''<section class="phead phead--sm"><div class="wrap"><h1>Terms of Use</h1></div></section>
<section class="band band--flush"><div class="wrap prose">{DRAFT.replace('policy', 'page')}
<h2>About this site</h2><p>This site gives general information about ZAKO Land Partners. Using it means you accept these terms.</p>
<h2>No offer or advice</h2><p>Nothing here is an offer to buy, sell or lease property, or real estate brokerage, engineering, surveying, appraisal, legal, tax or financial advice.</p>
<h2>Independent professionals</h2><p>ZAKO does not provide licensed professional services. Where such services are needed, they are provided by independent professionals under their own separate engagements.</p>
<h2>Submissions</h2><p>Sending us information does not create an agreement or obligation. Any transaction requires a separate written agreement signed by the parties.</p>
<h2>Accuracy</h2><p>We work to keep information accurate, but the site is provided as is. Property information may be preliminary and should be verified independently.</p>
<h2>Content</h2><p>The ZAKO name and wordmark belong to ZAKO. Photographs are used under the Unsplash License and belong to their photographers.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Utah.</p>
<p class="mt"><strong>Effective date:</strong> set when finalized.</p></div></section>'''
page('terms.html', 'Terms of Use | ZAKO Land Partners', 'Terms of use for the ZAKO Land Partners website.', terms, noindex=True)

page('404.html', 'Page Not Found | ZAKO Land Partners', 'Page not found.',
     '<section class="phead phead--404"><div class="wrap"><p class="eyebrow">404</p><h1>This page could not be found.</h1>'
     '<p class="lead">The link may be out of date. Everything else is a click away.</p>'
     '<div class="btns"><a class="btn" href="index.html">Go to the homepage</a><a class="btn btn--line" href="contact.html">Contact us</a></div></div></section>',
     noindex=True)
print('built')
