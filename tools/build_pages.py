"""Build the ZAKO site (v6). Edit content here, then run: python3 tools/build_pages.py

Settings to change at launch are the three constants below.
"""
import os, json
ROOT = os.path.join(os.path.dirname(__file__), '..', 'docs')

DOMAIN = 'https://zakoland.com'
EMAIL = 'team@zakoland.com'
# Online forms are OFF (CEO decision 2026-11-23, APQ-2026-0036 option A): email-only contact until
# counsel finalizes the Privacy Policy and Terms. No form endpoint is included in the public build.
FORMS_LIVE = True   # True = no 'preview' banner. Forms themselves are replaced by email_block().
PUBLISH_LEGAL = False  # Privacy/Terms are attorney-review drafts; written to legal_drafts/, not docs/.

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
<html lang="en">
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
<link rel="preload" href="assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
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
<p class="ftr__fine">&copy; <span data-year>2026</span> ZAKO Land Partners. ZAKO is not a real estate brokerage and does not provide engineering, surveying, legal, title or financing services. Photography: Zach Kessinger, Tyler Mower, Michael Tuszynski (Unsplash)</p>
</div>
</div></footer>
<script src="js/site.js" defer></script>
</body>
</html>'''

def page(path, title, desc, body, over=False, noindex=False, preload=None):
    with open(os.path.join(ROOT, path), 'w') as fh:
        fh.write(head(title, desc, path, noindex, preload) + '\n' + header(path, over) + '\n<main id="main">\n' + body.strip() + '\n</main>\n' + FOOTER)

# ------------------------------------------------------------------ form helpers
SUBJECTS = {'builder-criteria': 'Builder introduction', 'property-owner': 'Land inquiry', 'general': 'Website inquiry'}
def form(name, inner, submit):
    """Email-only contact (forms disabled). `inner` is ignored; nothing is submitted from the site."""
    subj = SUBJECTS[name].replace(' ', '%20')
    what = 'property submissions' if name == 'property-owner' else 'submissions'
    return f'''<div class="mailbox">
<p class="mailbox__note">This website is not currently accepting {what} through online forms. Please contact us by email.</p>
<p><a class="mailbox__addr" href="mailto:{EMAIL}?subject={subj}">{EMAIL}</a></p>
<div><a class="btn" href="mailto:{EMAIL}?subject={subj}">{submit}</a></div>
</div>'''

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
    lis = ''.join(f'<li{r(i*110)}><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(items))
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

# ------------------------------------------------------------------ HOME (v6 local draft)
FOCUS = [
 ('Land Intelligence', 'Research the property. Understand its potential.'),
 ('Acquisition', 'Identify opportunities worth pursuing.'),
 ('Land Holdings', 'Build lasting value through ownership.'),
 ('Development', 'Understand what it takes to move land forward.'),
]
focus = ''.join(f'<li{r(i*90)}><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(FOCUS))
home = f'''
<section class="photo photo--hero" aria-labelledby="h">
{pic('hero', eager=True)}
<div class="photo__in">
<div class="hero__copy">
<p class="label label--light rise" style="--d:100ms">Residential Land Investment &amp; Acquisition</p>
<h1 id="h"><span class="rise" style="--d:250ms">Land.</span> <span class="rise" style="--d:400ms">Opportunity.</span> <span class="rise v" style="--d:550ms">Vision.</span></h1>
<p class="sub rise" style="--d:760ms">A Utah company focused on residential land investment and acquisition.</p>
</div>
<div class="btns rise" style="--d:920ms"><a class="btn btn--light" href="#approach">Our approach</a><a class="btn btn--ghost" href="contact.html">Contact</a></div>
</div>
<span class="cue" aria-hidden="true"></span>
</section>

<section class="band" id="approach" aria-labelledby="what-h"><div class="wrap intro">
<p class="label"{r()}>Our approach</p>
<div>
<h2 id="what-h" class="statement"{r(80)}>We study the land before we pursue it.</h2>
<p class="lead"{r(140)}>Every property has its own possibilities and constraints. We evaluate location, access, zoning, utilities, terrain and surrounding growth before deciding whether an opportunity fits our investment strategy.</p>
<div class="intro__foot"{r(200)}>
<p><span>Focus</span>Residential land</p>
<p><span>Markets</span>Utah County and the Wasatch Front</p>
<p><span>Approach</span>Research first, then disciplined decisions</p>
</div>
</div>
</div></section>

<section class="band band--alt" aria-labelledby="focus-h"><div class="wrap">
<div class="head2"><p class="label"{r()}>Our focus</p><h2 id="focus-h"{r(60)}>Four areas that guide how ZAKO is being built.</h2></div>
<ul class="focus">{focus}</ul>
<p class="focus-note"{r(200)}>Land intelligence and acquisition research are where ZAKO is working today. Holdings and development are long-term goals.</p>
</div></section>

<section class="band" aria-label="Builders and landowners"><div class="wrap cards">
<a class="card" href="builders.html"{r()}><div class="frame">{pic('plan', '(min-width: 901px) 46vw, 92vw')}</div>
<h3>Homebuilders and developers</h3><p>We are building relationships with the companies that shape Utah&rsquo;s neighborhoods.</p><span class="arrow">For builders</span></a>
<a class="card" href="landowners.html"{r(120)}><div class="frame">{pic('valley', '(min-width: 901px) 46vw, 92vw')}</div>
<h3>Landowners</h3><p>We are interested in residential land that may fit our own investment strategy.</p><span class="arrow">For landowners</span></a>
</div></section>

<section class="band band--alt" aria-labelledby="founder"><div class="wrap founder">
<div class="frame"{r()}>{pic('founder', '(min-width: 901px) 40vw, 90vw')}</div>
<div>
<p class="label"{r()}>Founder</p>
<h2 id="founder"{r(60)}>Founded with a civil engineering perspective.</h2>
<p class="lead"{r(120)}>ZAKO was founded by Mohamed Toure. His background in land surveying and civil engineering shapes how we look at every site: what it is today, and what it could become.</p>
<a class="arrow"{r(180)} href="about.html">Read his story</a>
</div>
</div></section>

<section class="photo photo--end" aria-labelledby="c">
{pic('dawn')}
<div class="photo__in"><div>
<h2 id="c"{r(60)}>Start the conversation.</h2>
<div class="btns"{r(160)}><a class="btn btn--light" href="contact.html">Contact ZAKO</a></div>
</div></div>
</section>'''
page('index.html', 'ZAKO Land Partners | Utah Residential Land Investment & Acquisition',
     'ZAKO Land Partners is a Utah company focused on residential land investment and acquisition. We study the land before we pursue it.',
     home, over=True, preload='hero')

# ------------------------------------------------------------------ BUILDERS (v6 local draft)
MARKETS = ['Lehi', 'Saratoga Springs', 'Eagle Mountain', 'American Fork', 'Spanish Fork', 'South Utah County', 'Salt Lake County', 'Elsewhere in Utah']
builders = f'''
{opening('Builders and developers', 'Building relationships with Utah&rsquo;s homebuilders.',
 'ZAKO is a residential land investment company. As we build our acquisition strategy, we want to understand how Utah homebuilders and developers think about land: where they build, what they need and what makes a site work.',
 '<a class="btn" href="#introduce">Introduce your company</a>', 'plan')}

<section class="band band--alt" aria-labelledby="how"><div class="wrap">
<div class="head2"><p class="label"{r()}>Why it matters to us</p><h2 id="how"{r(60)}>Land decisions start with demand.</h2></div>
{steps([
 ('Understand the market', 'Knowing what homebuilders look for helps us judge which land is worth our time and capital.'),
 ('Research with discipline', 'We evaluate zoning, access, utilities, terrain and surrounding growth before pursuing any property.'),
 ('Build for the long term', 'We value relationships that grow over years, not single transactions.'),
])}
</div></section>

<section class="band" id="introduce" aria-labelledby="f"><div class="wrap split">
<div><p class="label"{r()}>Introduce your company</p><h2 id="f"{r(60)}>Tell us about what you build.</h2>
<p class="lead"{r(120)}>A short email introduction is enough: your company, where you build and what you build. It creates no obligation on either side.</p>
<p class="fine"{r(180)}>ZAKO acts for its own account. It does not act as a broker or agent for any builder, seller or buyer.</p></div>
{form('builder-criteria', f"""
<div class="row2">{field('b-company','Company','company',auto='organization')}{field('b-name','Name','name',auto='name')}</div>
<div class="row2">{field('b-email','Business email','email','email',auto='email')}{field('b-phone','Phone','phone','tel',False,'tel')}</div>
<fieldset data-require-one><legend>Where you build</legend><div class="chips">{chips('markets', MARKETS)}</div></fieldset>
{textarea('b-more','What you build','criteria',ph='Product types, typical lot sizes, community size')}
{consent('contact me about ZAKO')}""", 'Email ZAKO')}
</div></section>'''
page('builders.html', 'Builders and Developers | ZAKO Land Partners',
     'ZAKO Land Partners is building relationships with Utah homebuilders and developers as part of its residential land investment strategy.', builders)

# ------------------------------------------------------------------ LANDOWNERS (v6 local draft)
landowners = f'''
{opening('Landowners', 'Residential land in Utah.',
 'ZAKO is interested in learning about residential land that may fit its own investment and acquisition strategy. If you own land in Utah County or along the Wasatch Front, we would be glad to hear from you.',
 '<a class="btn" href="#property">Tell us about your land</a>', 'valley')}

<section class="band band--alt" aria-labelledby="how"><div class="wrap">
<div class="head2"><p class="label"{r()}>What to expect</p><h2 id="how"{r(60)}>Careful, unhurried and clear.</h2></div>
{steps([
 ('Share the basics', 'Email us the address or parcel number and a little about your plans. There is no cost.'),
 ('We study the property', 'We review public information such as zoning, access, utilities and terrain.'),
 ('We follow up', 'If the property may fit our strategy, we will tell you and ask whether you would like to talk further. If not, we will say so.'),
])}
</div></section>

<section class="band" id="property" aria-labelledby="f"><div class="wrap split">
<div><p class="label"{r()}>Your land</p><h2 id="f"{r(60)}>Start with the basics.</h2>
<ul class="assure"{r(120)}>
<li>Contacting us creates no obligation to sell.</li>
<li>You are welcome to involve your own agent, attorney or advisor at any point.</li>
<li>We do not share your property information without your permission.</li>
</ul>
<p class="fine"{r(180)}>ZAKO is not a real estate brokerage. We do not represent landowners, list or market property, or find buyers for others. Any transaction would depend on due diligence, legal review and a separate written agreement signed by both parties.</p></div>
{form('property-owner', f"""
<div class="row2">{field('o-name','Name','name',auto='name')}{field('o-email','Email','email','email',auto='email')}</div>
<div class="row2">{field('o-phone','Phone','phone','tel',False,'tel')}{select('o-rel','You are the','relationship',['Owner','Co-owner','Authorized representative'])}</div>
<div class="row2">{field('o-addr','Address or parcel number','property')}{select('o-county','County','county',['Utah County','Salt Lake County','Another Utah county'])}</div>
{textarea('o-msg','Anything we should know','message')}
{consent('review the property and contact me')}""", 'Email ZAKO')}
</div></section>'''
page('landowners.html', 'Landowners | ZAKO Land Partners',
     'ZAKO Land Partners is interested in residential land in Utah that may fit its own investment and acquisition strategy. No obligation.', landowners)

# ------------------------------------------------------------------ ABOUT
STORY = [
    'I am originally from Mali. Utah has become home, and it is where I studied civil engineering.',
    'Before engineering, I worked on survey crews across Utah. That work taught me about property boundaries, land measurement and the early stages of residential development. Today my engineering work includes water and irrigation projects.',
    'These experiences shaped how I see land. Its potential goes beyond acreage or location. Access, topography, drainage, water, utilities and surrounding development all shape what a property can become.',
    'I founded ZAKO to bring that perspective to residential land investment and acquisition. The goal is a respected, long-term land company built on careful research and clear communication.',
]
story = ''.join(f'<p{r(60 + i*40)}>{x}</p>' for i, x in enumerate(STORY))
about = f'''
{opening('About ZAKO', 'A Utah land company with an engineer&rsquo;s eye.',
 'ZAKO Land Partners is a Utah residential land investment and acquisition company, founded by Mohamed Toure.', '', 'founder', 'about-open')}

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
<h1 class="rise" style="--d:200ms">Start the conversation.</h1>
</div></section>
<section class="band band--flush" aria-label="Contact by email"><div class="wrap split">
<div><p class="lead"{r()}>Tell us who you are and what you have in mind. Email is the best way to reach us.</p>
<dl class="contacts"{r(80)}>
<div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
<div><dt>Based in</dt><dd>Utah</dd></div>
</dl></div>
{form('general', f"""
<div class="row2">{field('g-name','Name','name',auto='name')}{field('g-email','Email','email','email',auto='email')}</div>
{select('g-role','I am a','role',['Builder or developer','Landowner','Other'])}
{textarea('g-msg','Message','message',req=True)}
{consent('respond to me')}""", 'Email ZAKO')}
</div></section>'''
page('contact.html', 'Contact | ZAKO Land Partners',
     'Contact ZAKO Land Partners about residential land in Utah. team@zakoland.com', contact)

# ------------------------------------------------------------------ LEGAL (drafts for attorney review; NOT published)
DRAFTS = os.path.join(os.path.dirname(__file__), '..', 'legal_drafts')
def draft_page(path, title, desc, body, noindex=True):
    if PUBLISH_LEGAL:
        return page(path, title, desc, body, noindex=noindex)
    os.makedirs(DRAFTS, exist_ok=True)
    with open(os.path.join(DRAFTS, path), 'w') as fh:
        fh.write(head(title, desc, path, True) + '\n' + header(path) + '\n<main id="main">\n' + body.strip() + '\n</main>\n' + FOOTER)
    stale = os.path.join(ROOT, path)
    if os.path.exists(stale): os.remove(stale)
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
draft_page('privacy.html', 'Privacy Policy | ZAKO Land Partners', 'How ZAKO Land Partners handles information submitted through this website.', privacy, noindex=True)

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
draft_page('terms.html', 'Terms of Use | ZAKO Land Partners', 'Terms of use for the ZAKO Land Partners website.', terms, noindex=True)

page('404.html', 'Page Not Found | ZAKO Land Partners', 'Page not found.',
     '<section class="phead phead--404"><div class="wrap"><p class="label">404</p><h1>This page could not be found.</h1>'
     '<p class="lead">The link may be out of date. Everything else is a click away.</p>'
     '<div class="btns"><a class="btn" href="index.html">Go to the homepage</a><a class="btn btn--line" href="contact.html">Contact us</a></div></div></section>',
     noindex=True)
print('built')
