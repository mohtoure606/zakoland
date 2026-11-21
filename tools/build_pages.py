"""Build the ZAKO site (v5). Edit content here, then run: python3 tools/build_pages.py

Settings to change at launch are the three constants below.
"""
import os, json
ROOT = os.path.join(os.path.dirname(__file__), '..', 'docs')

DOMAIN = 'https://zakoland.com'
EMAIL = 'team@zakoland.com'
# Formspree endpoint for the ZAKO-only account. Replace ZAKO_FORM_ID with the form's hashid
# (the part after /f/ in the form's endpoint URL), then set FORMS_LIVE = True and rebuild.
FORM_ACTION = 'https://formspree.io/f/mdegdyea'
FORMS_LIVE = True

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

NAV = [('index.html', 'Home'), ('builders.html', 'Builders'), ('landowners.html', 'Landowners'), ('about.html', 'About'), ('contact.html', 'Contact')]

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
<meta name="theme-color" content="#F5F3EE">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/instrument-serif.woff2" as="font" type="font/woff2" crossorigin>
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
<p class="ftr__say">Land. Opportunity. <em>Vision.</em></p>
<div><h2>Explore</h2><nav aria-label="Footer"><a href="builders.html">Builders</a><a href="landowners.html">Landowners</a><a href="about.html">About</a><a href="contact.html">Contact</a></nav></div>
<div class="ftr__contact"><h2>Contact</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><p>Utah</p></div>
</div>
<div class="ftr__bar">
<a class="logo" href="index.html" aria-label="ZAKO Land Partners, home"><img src="assets/img/zako-white.svg" alt="ZAKO" width="104" height="21"></a>
<p class="ftr__fine">&copy; <span data-year>2026</span> ZAKO Land Partners. ZAKO does not provide real estate brokerage, engineering, surveying, legal, title or financing services. <a href="privacy.html">Privacy</a> &middot; <a href="terms.html">Terms</a> &middot; Photography: Zach Kessinger, Tyler Mower, Michael Tuszynski (Unsplash)</p>
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
    return f'<label class="check"><input type="checkbox" name="consent" value="yes" required><span>I agree that ZAKO may use this information to {what}, as described in the <a href="privacy.html">Privacy Policy</a>.</span></label>'

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

def steps(items):
    lis = ''.join(f'<li{r(i*110)}><span class="num">{i+1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(items))
    return f'<ol class="steps">{lis}</ol>'

def opening(label, h1, lead, cta, photo, extra_cls=''):
    return f'''<section class="open {extra_cls}" aria-labelledby="h"><div class="wrap open__grid">
<div>
<p class="label rise" style="--d:80ms">{label}</p>
<h1 id="h" class="rise" style="--d:200ms">{h1}</h1>
<p class="lead rise" style="--d:360ms">{lead}</p>
{('<div class="btns rise" style="--d:480ms">' + cta + '</div>') if cta else ''}
</div>
<div class="frame frame--land rise" style="--d:300ms">{pic(photo, '(min-width: 901px) 40vw, 90vw', eager=True)}</div>
</div></section>'''

# ------------------------------------------------------------------ HOME (hero preserved)
home = f'''
<section class="photo photo--hero" aria-labelledby="h">
{pic('hero', eager=True)}
<div class="photo__in">
<div class="hero__copy">
<p class="label label--light rise" style="--d:100ms">Residential Land Investment &amp; Acquisition</p>
<h1 id="h"><span class="rise" style="--d:250ms">Land.</span> <span class="rise" style="--d:420ms">Opportunity.</span> <span class="rise" style="--d:590ms"><em>Vision.</em></span></h1>
<p class="sub rise" style="--d:820ms">We find residential land in Utah, research what it can become, and connect it with the builders and developers who need it.</p>
</div>
<div class="btns rise" style="--d:1000ms"><a class="btn btn--light" href="builders.html">For builders</a><a class="btn btn--ghost" href="landowners.html">For landowners</a></div>
</div>
<span class="cue" aria-hidden="true"></span>
</section>

<section class="band" aria-labelledby="what-h"><div class="wrap intro">
<p class="label"{r()}><b>01</b> What we do</p>
<div>
<h2 id="what-h" class="statement"{r(80)}>We look closely at land, understand what it could support, and bring the right opportunities to <em>the builders shaping Utah&rsquo;s communities.</em></h2>
<div class="intro__foot"{r(160)}>
<p><span>Focus</span>Residential land</p>
<p><span>Markets</span>Utah County, Salt Lake County and growing Utah markets</p>
<p><span>Approach</span>Research first, clear communication</p>
</div>
</div>
</div></section>

<section class="pair" aria-label="Who we work with">
<a class="photo photo--half tile" href="builders.html">{pic('plan', '(min-width: 901px) 50vw, 100vw')}
<div class="photo__in"><div{r()}><p class="label label--light"><b style="color:inherit">02</b> Builders</p><h2>Tell us what you build.</h2><p>Share your markets and criteria. We look for land that may fit your requirements.</p>
<span class="arrow">For builders</span></div></div></a>
<a class="photo photo--half tile" href="landowners.html">{pic('valley', '(min-width: 901px) 50vw, 100vw')}
<div class="photo__in"><div{r(120)}><p class="label label--light"><b style="color:inherit">03</b> Landowners</p><h2>Own land in Utah?</h2><p>Start a conversation. No cost, no pressure, and a straight answer.</p>
<span class="arrow">For landowners</span></div></div></a>
</section>

<section class="band" aria-labelledby="founder"><div class="wrap founder">
<div class="frame"{r()}>{pic('founder', '(min-width: 901px) 40vw, 90vw')}</div>
<div>
<p class="label"{r()}><b>04</b> Founder</p>
<h2 id="founder"{r(60)}>Founded with a civil engineering <em>perspective.</em></h2>
<p class="lead"{r(120)}>ZAKO was founded by Mohamed Toure. His background in land surveying and civil engineering shapes how we look at every site: what it is today, and what it could become.</p>
<a class="arrow"{r(180)} href="about.html">Read his story</a>
</div>
</div></section>

<section class="photo photo--end" aria-labelledby="c">
{pic('dawn')}
<div class="photo__in"><div>
<p class="label label--light"{r()}>Contact</p>
<h2 id="c"{r(60)}>Start the conversation.</h2>
<p class="sub"{r(100)} style="margin-top:18px;opacity:.95">Builders, landowners and land professionals across Utah.</p>
<div class="btns"{r(160)}><a class="btn btn--light" href="contact.html">Contact ZAKO</a></div>
</div></div>
</section>'''
page('index.html', 'ZAKO Land Partners | Utah Residential Land Investment & Acquisition',
     'ZAKO Land Partners finds residential land in Utah, researches what it can become, and connects it with the builders and developers who need it.',
     home, over=True, preload='hero')

# ------------------------------------------------------------------ BUILDERS
MARKETS = ['Lehi', 'Saratoga Springs', 'Eagle Mountain', 'American Fork', 'Spanish Fork', 'South Utah County', 'Salt Lake County', 'Elsewhere in Utah']
builders = f'''
{opening('For builders', 'Tell us what you build. <em>We will look for the land.</em>',
 'ZAKO identifies and researches residential land opportunities in Utah. Share your acquisition criteria and target markets, and we will look for opportunities that may fit your requirements.',
 '<a class="btn" href="#criteria">Share your criteria</a>', 'plan')}

<section class="band band--alt" aria-labelledby="how"><div class="wrap">
<div class="head2"><p class="label"{r()}>How it works</p><h2 id="how"{r(60)}>A clear, focused process.</h2></div>
{steps([
 ('Share your criteria', 'Your target markets, product types, lot sizes and any requirements that would rule a site out.'),
 ('We identify and research', 'We look for residential land that may match your criteria and review the available information on each property.'),
 ('We share what may fit', 'When an opportunity may align with your requirements, we present our findings and discuss next steps. If nothing fits, we will tell you.'),
])}
</div></section>

<section class="band" id="criteria" aria-labelledby="f"><div class="wrap split">
<div><p class="label"{r()}>Share your criteria</p><h2 id="f"{r(60)}>Tell us what you are looking for.</h2>
<p class="lead"{r(120)}>It takes about two minutes and creates no obligation.</p>
<p class="fine"{r(180)}>Property information we share is preliminary and should be confirmed through your own due diligence.</p></div>
{form('builder-criteria', f"""
<div class="row2">{field('b-company','Company','company',auto='organization')}{field('b-name','Name','name',auto='name')}</div>
<div class="row2">{field('b-email','Business email','email','email',auto='email')}{field('b-phone','Phone','phone','tel',False,'tel')}</div>
<fieldset data-require-one><legend>Target markets</legend><div class="chips">{chips('markets', MARKETS)}</div></fieldset>
{textarea('b-more','Criteria','criteria',ph='Lot sizes or acreage, product type, price range, timing')}
{consent('contact me about land opportunities')}""", 'Send criteria')}
</div></section>'''
page('builders.html', 'For Builders | ZAKO Land Partners',
     'Share your acquisition criteria and target markets. ZAKO researches residential land in Utah that may fit what you build.', builders)

# ------------------------------------------------------------------ LANDOWNERS
landowners = f'''
{opening('For landowners', 'Your land may be worth <em>a closer look.</em>',
 'ZAKO is interested in learning about residential land opportunities in Utah. Share basic information about your property, and we will review whether there may be a fit.',
 '<a class="btn" href="#property">Tell us about your property</a>', 'valley')}

<section class="band band--alt" aria-labelledby="how"><div class="wrap">
<div class="head2"><p class="label"{r()}>How it works</p><h2 id="how"{r(60)}>Simple, unhurried and clear.</h2></div>
{steps([
 ('Start a conversation', 'Share the address or parcel number and a little about your plans. There is no cost.'),
 ('We take a careful look', 'We review public information about the property and what builders in the area are looking for.'),
 ('We discuss options', 'If there may be a fit, we explain what we see and what a next step could look like. If not, we tell you.'),
])}
</div></section>

<section class="band" id="property" aria-labelledby="f"><div class="wrap split">
<div><p class="label"{r()}>Your property</p><h2 id="f"{r(60)}>Start with the basics.</h2>
<ul class="assure"{r(120)}>
<li>Starting a conversation creates no obligation to sell.</li>
<li>You are welcome to involve your own agent, attorney or advisor at any point.</li>
<li>We share property details with others only with your permission.</li>
</ul>
<p class="fine"{r(180)}>ZAKO is not a real estate agent and does not list or market property. Any transaction would require a written agreement reviewed and signed by you.</p></div>
{form('property-owner', f"""
<div class="row2">{field('o-name','Name','name',auto='name')}{field('o-email','Email','email','email',auto='email')}</div>
<div class="row2">{field('o-phone','Phone','phone','tel',False,'tel')}{select('o-rel','You are the','relationship',['Owner','Co-owner','Authorized representative'])}</div>
<div class="row2">{field('o-addr','Address or parcel number','property')}{select('o-county','County','county',['Utah County','Salt Lake County','Another Utah county'])}</div>
{textarea('o-msg','Anything we should know','message')}
{consent('review the property and contact me')}""", 'Submit property')}
</div></section>'''
page('landowners.html', 'For Landowners | ZAKO Land Partners',
     'Own residential land in Utah? Share a few details and ZAKO will take a careful look. No obligation.', landowners)

# ------------------------------------------------------------------ ABOUT
STORY = [
    'I am originally from Mali, and Utah has become home. It is where I studied civil engineering.',
    'Before entering engineering, I worked on survey crews across Utah, gaining firsthand experience with property boundaries, land measurement and the early stages of residential development. Today, my work in civil engineering includes water and irrigation projects.',
    'These experiences shaped how I understand land. Its potential goes beyond acreage or location. Access, topography, drainage, water, utilities and surrounding development all play an important role in what a property may become.',
    'I founded ZAKO to bring that perspective to residential land investment and acquisition, with the goal of building a respected land company grounded in careful research and clear communication.',
]
story = ''.join(f'<p{r(60 + i*40)}>{x}</p>' for i, x in enumerate(STORY))
about = f'''
{opening('About ZAKO', 'A Utah land company with <em>an engineer&rsquo;s eye.</em>',
 'ZAKO Land Partners identifies residential land opportunities in Utah and evaluates them with a careful, research-first perspective. The company was founded by Mohamed Toure.', '', 'founder', 'about-open')}

<section class="band band--alt" aria-labelledby="f"><div class="wrap split">
<div><p class="label"{r()}>Founder</p><h2 id="f"{r(60)}>Why I started ZAKO</h2></div>
<div class="story">
{story}
<p class="sign"{r(240)}>Mohamed Toure<span>Founder, ZAKO Land Partners</span></p>
</div>
</div></section>'''
page('about.html', 'About | ZAKO Land Partners',
     'ZAKO Land Partners was founded in Utah by Mohamed Toure, bringing a surveying and civil engineering perspective to land investment and acquisition.', about)

# ------------------------------------------------------------------ CONTACT
contact = f'''
<section class="phead"><div class="wrap">
<p class="label rise" style="--d:80ms">Contact</p>
<h1 class="rise" style="--d:200ms">Start the <em>conversation.</em></h1>
</div></section>
<section class="band band--flush" aria-label="Contact form"><div class="wrap split">
<div><p class="lead"{r()}>Tell us who you are and what you have in mind. We read every message and will respond promptly.</p>
<dl class="contacts"{r(80)}>
<div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
<div><dt>Based in</dt><dd>Utah</dd></div>
</dl></div>
{form('general', f"""
<div class="row2">{field('g-name','Name','name',auto='name')}{field('g-email','Email','email','email',auto='email')}</div>
{select('g-role','I am a','role',['Builder or developer','Landowner','Other'])}
{textarea('g-msg','Message','message',req=True)}
{consent('respond to me')}""", 'Send message')}
</div></section>'''
page('contact.html', 'Contact | ZAKO Land Partners',
     'Contact ZAKO Land Partners about residential land in Utah. team@zakoland.com', contact)

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
     '<section class="phead phead--404"><div class="wrap"><p class="label">404</p><h1>This page could not be found.</h1>'
     '<p class="lead">The link may be out of date. Everything else is a click away.</p>'
     '<div class="btns"><a class="btn" href="index.html">Go to the homepage</a><a class="btn btn--line" href="contact.html">Contact us</a></div></div></section>',
     noindex=True)
print('built')
