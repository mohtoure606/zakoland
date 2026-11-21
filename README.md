# zakoland.com

Website for **ZAKO Land Partners**: Residential Land Investment & Acquisition, Utah.

Static HTML, CSS and a small amount of JavaScript. No framework, no third-party scripts, no trackers. Hosted on GitHub Pages from the `docs/` folder of `main`.

## Status

| Item | State |
|---|---|
| Website | v5 (simplified, premium redesign, 2026-11-20). Launch approved by the founder 2026-11-20. |
| Domain | zakoland.com registered at Namecheap. Website DNS still points to Namecheap parking. |
| Email | team@zakoland.com on Zoho Mail (free plan). MX, SPF, DKIM and DMARC set in Namecheap. |
| Forms | Connected to the ZAKO Formspree form `mdegdyea` (sends to team@zakoland.com). |
| Privacy / Terms | Drafts for attorney review. Marked `noindex` and labeled as drafts. |

## Layout

```
docs/                    the website (this is what GitHub Pages serves)
  index.html builders.html landowners.html about.html contact.html
  privacy.html terms.html 404.html
  css/site.css           all styles, including motion
  js/site.js             header, mobile menu, reveal-on-scroll, forms
  assets/img/            Meridian wordmark SVGs, favicon, social image (og-image.jpg)
  assets/photo/          photographs, JPG + WebP at several widths
  assets/fonts/          Instrument Serif, Inter (and Archivo, used only for the social image) — SIL Open Font License
  CNAME robots.txt sitemap.xml
tools/
  build_pages.py         generates every HTML page; edit content here
  wordmark.py            geometry for the Meridian wordmark (concept "a")
  test_site.py           Playwright: screenshots, overflow, console errors, links, forms
  axe.py                 axe-core WCAG 2 A/AA check on every page
```

## Updating content

1. Edit the text in `tools/build_pages.py`. Each page is a clearly labeled block.
2. Run `python3 tools/build_pages.py`. It rewrites the HTML in `docs/`.
3. Optional checks (needs `pip install playwright` and `npm install axe-core`):
   `python3 tools/test_site.py` and `python3 tools/axe.py`.
4. Commit and push. Once Pages is on, the live site updates within a minute or two.

Do not hand-edit the HTML in `docs/`: the next build will overwrite it.

## Connecting the forms

All three forms (builder criteria, landowner property, general contact) post to one Formspree form. Each submission includes a `form` field naming its source.

1. In the ZAKO Formspree account (team@zakoland.com), create a form. Its endpoint looks like `https://formspree.io/f/abcdwxyz`.
2. In `tools/build_pages.py`, replace `ZAKO_FORM_ID` in `FORM_ACTION` with the ID. Set `FORMS_LIVE = True`.
3. Rebuild, commit, push. The preview notice disappears and forms send.

The form ID is public by design (it appears in the page source). There are no secret keys in this repository; do not add any.

## Launch (founder approval required)

1. Repository **Settings → Pages**: Source = Deploy from a branch, Branch = `main`, Folder = `/docs`. Custom domain = `zakoland.com`.
2. Namecheap **Advanced DNS** for zakoland.com, Host Records only (leave Mail Settings and TXT records alone):
   - Delete the `URL Redirect @` record and the `CNAME www → parkingpage.namecheap.com` record.
   - Add `A @` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   - Add `CNAME www` → `mohtoure606.github.io.`
3. Back in Settings → Pages, wait for the DNS check to pass, then tick **Enforce HTTPS**.
4. Visit https://zakoland.com and https://www.zakoland.com, submit one test form, and confirm it arrives at team@zakoland.com.

## Brand

- Wordmark: **Meridian**. Header uses `zako.svg` / `zako-white.svg` (ZAKO only). Footer and documents use `zako-lockup.svg` (ZAKO over LAND PARTNERS). Favicon is ZA over KO in a charcoal square.
- Colors: ivory `#F5F1EA`, white `#FFFFFF`, sandstone `#B89470` (text use `#7D5F3E`), charcoal `#1C1B1A`, stone `#66615A`.
- Type: Archivo (wide, display) and Inter (text).

## Photography (Unsplash License)

- hero: Spanish Fork, Utah, by Zach Kessinger (unsplash.com/photos/bVTDky2Gfrc)
- valley: Lehi, Saratoga Springs and Eagle Mountain view, by Tyler Mower (unsplash.com/photos/KvPq29QhgjQ)
- plan: Herriman, Utah cul-de-sac, by Michael Tuszynski (unsplash.com/photos/4nuCGapo4Zs)
- dawn: Herriman, Utah at sunrise, by Michael Tuszynski (unsplash.com/photos/ylkHqlxx-gI)
- founder: Mohamed Toure, original photograph, resized only

## Separation from The 91st Foundation

This repository, its domain, email, form account and data belong to ZAKO only. Nothing here is shared with The 91st Foundation's site, email or forms.
