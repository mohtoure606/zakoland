"""ZAKO wordmark concepts. Pure geometry (no font), built with shapely.
Cap height 100 units, y grows downward. Outputs filled SVG paths."""
import math, os, sys
from shapely.geometry import LineString, Polygon, box, Point
from shapely.ops import unary_union
from shapely import affinity
sys.path.insert(0, os.path.dirname(__file__))

H = 100

def stroke(points, w, ext=40, ext_start=None):
    """Polyline stroked with width w, flat caps, mitre joins; ends extended so a later clip cuts them square."""
    pts = list(points)
    # extend first and last segments
    def extend(a, b, d):
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy)
        return (b[0] + dx / L * d, b[1] + dy / L * d)
    pts[0] = extend(pts[1], pts[0], ext if ext_start is None else ext_start) if (ext_start is None or ext_start > 0) else pts[0]
    pts[-1] = extend(pts[-2], pts[-1], ext)
    return LineString(pts).buffer(w / 2, cap_style='flat', join_style='mitre', mitre_limit=10)

def clip(g, x0, x1, y0=0, y1=H):
    return g.intersection(box(x0, y0, x1, y1))

# ---------- letters ----------
def Z(x, W, s, d=None):
    d = d or s * 1.32
    top = box(x, 0, x + W, s)
    bot = box(x, H - s, x + W, H)
    diag = Polygon([(x + W - d, s), (x + W, s), (x + d, H - s), (x, H - s)])
    return unary_union([top, bot, diag])

def A_pointed(x, W, s, bar_y=64):
    legs = stroke([(x + s * .62, H + 5), (x + W / 2, s * .55), (x + W - s * .62, H + 5)], s)
    legs = clip(legs, x, x + W)
    bar = box(x, bar_y, x + W, bar_y + s * .86).intersection(legs.convex_hull)
    return unary_union([legs, bar])

def A_flat(x, W, s, top_w=None, bar_y=62, bar_h=None):
    """A with a flat top (like a parcel line) and a low crossbar. Legs built tall then clipped at the baseline."""
    top_w = top_w if top_w is not None else s * 1.6
    bar_h = bar_h or s * .85
    cx = x + W / 2
    tl, tr = (cx - top_w / 2 - s * .5, 0), (cx + top_w / 2 + s * .5, 0)
    bl, br = (x, H), (x + W, H)
    k = 0.6  # extend legs below baseline by 60% of height, same slope
    blx, brx = bl[0] + (bl[0] - tl[0]) * k, br[0] + (br[0] - tr[0]) * k
    outer = Polygon([(blx, H * (1 + k)), tl, tr, (brx, H * (1 + k))])
    inner = outer.buffer(-s, join_style='mitre')
    counter = inner.difference(box(x - 50, bar_y, x + W + 50, bar_y + bar_h))
    return outer.difference(counter).intersection(box(x - 5, 0, x + W + 5, H))

def K(x, W, s, j=None):
    j = j if j is not None else 60
    stem = box(x, 0, x + s, H)
    a0, a1 = (x + s * .5, j), (x + W, 0)
    up = clip(stroke([a0, a1], s * 1.02), x, x + W)
    t = .40
    p0 = (a0[0] + (a1[0] - a0[0]) * t, a0[1] + (a1[1] - a0[1]) * t)
    dn = clip(stroke([p0, (x + W, H)], s * 1.06, ext_start=0), x, x + W)
    return unary_union([stem, up, dn])

def O_circle(x, W, s):
    r = H / 2
    c = Point(x + W / 2, H / 2)
    return c.buffer(r, 256).difference(c.buffer(r - s * 1.06, 256))

def O_square(x, W, s, n=3.4):
    def se(a, b, cx, cy):
        pts = []
        for i in range(720):
            t = 2 * math.pi * i / 720
            ct, st = math.cos(t), math.sin(t)
            pts.append((cx + a * abs(ct) ** (2 / n) * (1 if ct >= 0 else -1),
                        cy + b * abs(st) ** (2 / n) * (1 if st >= 0 else -1)))
        return Polygon(pts)
    cx, cy = x + W / 2, H / 2
    return se(W / 2, H / 2, cx, cy).difference(se(W / 2 - s * 1.06, H / 2 - s, cx, cy))

# ---------- concepts ----------
def layout(parts, gap):
    shapes, x = [], 0
    for fn, w in parts:
        shapes.append(fn(x, w)); x += w + gap
    return unary_union(shapes), x - gap

def concept_a():  # Meridian: light monoline, very wide, pointed A, true circle
    s = 9.5
    return layout([(lambda x, w: Z(x, w, s), 96), (lambda x, w: A_pointed(x, w, s, 66), 112),
                   (lambda x, w: K(x, w, s, 60), 88), (lambda x, w: O_circle(x, w, s), 100)], 34)

def concept_b():  # Parcel: medium weight, flat-top A, squared O, measured spacing
    s = 13
    return layout([(lambda x, w: Z(x, w, s), 90), (lambda x, w: A_flat(x, w, s, s * 1.4, 62), 106),
                   (lambda x, w: K(x, w, s, 60), 86), (lambda x, w: O_square(x, w, s, 3.0), 106)], 25)

def concept_c():  # Horizon: B-weight letters, round O, one hairline cut through the word
    s = 13
    g, W = layout([(lambda x, w: Z(x, w, s), 90), (lambda x, w: A_flat(x, w, s, s * 1.4, 62), 106),
                   (lambda x, w: K(x, w, s, 60), 86), (lambda x, w: O_circle(x, w, s), 100)], 25)
    return g.difference(box(-10, 58.5, W + 10, 61.5)), W

# ---------- SVG ----------
def to_path(g, dx=0, dy=0, sc=1.0):
    polys = [g] if g.geom_type == 'Polygon' else list(g.geoms)
    out = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            cs = list(ring.coords)
            out.append('M' + ' L'.join(f'{(x*sc+dx):.2f},{(y*sc+dy):.2f}' for x, y in cs[:-1]) + 'Z')
    return ' '.join(out)

def svg(g, W, fill='#1C1B1A', pad=2, title='ZAKO'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {W+2*pad:.2f} {H+2*pad}" role="img" aria-label="{title}">'
            f'<title>{title}</title><path fill="{fill}" fill-rule="evenodd" d="{to_path(g)}"/></svg>')

def lockup(g, W, desc_d, desc_w, desc_h, fill, sub_fill, gap=30):
    total_h = H + gap + desc_h
    dx = (W - desc_w) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 {W+4:.2f} {total_h+6:.2f}" role="img" aria-label="ZAKO Land Partners">'
            f'<title>ZAKO Land Partners</title><path fill="{fill}" fill-rule="evenodd" d="{to_path(g)}"/>'
            f'<path fill="{sub_fill}" transform="translate({dx:.2f},{H+gap+desc_h:.2f})" d="{desc_d}"/></svg>')

def stacked(parts_fn, s, fill, bg, size=64):
    """ZA / KO stacked in a square: the full word, for favicon and avatars."""
    return None

if __name__ == "__main__" and len(sys.argv) < 3:
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    for name, fn in [('a', concept_a), ('b', concept_b), ('c', concept_c)]:
        g, W = fn()
        open(os.path.join(out, f'concept-{name}.svg'), 'w').write(svg(g, W))
        print(name, round(W, 1))

# ---------- descriptor + stacked + build ----------
def outline_text(text, size, tracking_em, wdth=125, wght=520):
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    FONT = os.path.join(os.path.dirname(__file__), '..', 'node_modules/@fontsource-variable/archivo/files/archivo-latin-wdth-normal.woff2')
    f = instantiateVariableFont(TTFont(FONT), {'wdth': wdth, 'wght': wght})
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    sc = size / upm; x = 0; paths = []
    for ch in text:
        g = gs[cmap[ord(ch)]]
        if ch != ' ':
            pen = SVGPathPen(gs); g.draw(TransformPen(pen, (sc, 0, 0, -sc, x, 0))); paths.append(pen.getCommands())
        x += g.width * sc + tracking_em * size
    return ' '.join(paths), x - tracking_em * size, size * 0.72

def stacked_svg(row1, row2, fill, bg, rgap=26, pad=34, radius=0.18):
    (g1, w1), (g2, w2) = row1, row2
    W = max(w1, w2); Hs = 2 * H + rgap
    side = max(W, Hs) + 2 * pad
    ox1 = (side - w1) / 2; ox2 = (side - w2) / 2; oy = (side - Hs) / 2
    d = to_path(g1, ox1, oy) + ' ' + to_path(g2, ox2, oy + H + rgap)
    r = side * radius
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {side:.1f} {side:.1f}">'
            f'<rect width="{side:.1f}" height="{side:.1f}" rx="{r:.1f}" fill="{bg}"/>'
            f'<path fill="{fill}" fill-rule="evenodd" d="{d}"/></svg>')

CONCEPTS = {
    'a': dict(name='Meridian', s=9.5, fav_s=14, gap=34, parts=lambda s: [('Z', 96, lambda x, w: Z(x, w, s)), ('A', 112, lambda x, w: A_pointed(x, w, s, 66)), ('K', 88, lambda x, w: K(x, w, s, 60)), ('O', 100, lambda x, w: O_circle(x, w, s))]),
    'b': dict(name='Parcel', s=13, gap=30, parts=lambda s: [('Z', 90, lambda x, w: Z(x, w, s)), ('A', 106, lambda x, w: A_flat(x, w, s, s * 1.4, 62)), ('K', 86, lambda x, w: K(x, w, s, 60)), ('O', 106, lambda x, w: O_square(x, w, s, 3.0))]),
    'c': dict(name='Horizon', s=13, gap=25, parts=lambda s: [('Z', 90, lambda x, w: Z(x, w, s)), ('A', 106, lambda x, w: A_flat(x, w, s, s * 1.4, 62)), ('K', 86, lambda x, w: K(x, w, s, 60)), ('O', 100, lambda x, w: O_circle(x, w, s))], cut=True),
}

def build(key):
    c = CONCEPTS[key]; parts = c['parts'](c['s'])
    g, W = layout([(fn, w) for _, w, fn in parts], c['gap'])
    fparts = c['parts'](c.get('fav_s', c['s']))
    def row(sub):
        gg, ww = layout([(fn, w) for _, w, fn in sub], c['gap'] * 0.7)
        return gg, ww
    r1, r2 = row(fparts[:2]), row(fparts[2:])
    if c.get('cut'):
        g = g.difference(box(-10, 58.5, W + 10, 61.5))
        r1 = (r1[0].difference(box(-10, 58.5, 999, 61.5)), r1[1]); r2 = (r2[0].difference(box(-10, 58.5, 999, 61.5)), r2[1])
    return g, W, r1, r2

def write_all(out, key, primary=False):
    os.makedirs(out, exist_ok=True)
    g, W, r1, r2 = build(key)
    size = 26
    _, w0, _ = outline_text('LAND PARTNERS', size, 0.0)
    n = len('LAND PARTNERS')
    t = (W - w0) / (size * (n - 1))  # tracking so the descriptor spans the full wordmark width
    desc_d, desc_w, desc_h = outline_text('LAND PARTNERS', size, t)
    pre = '' if primary else f'concept-{key}-'
    files = {
        f'{pre}zako.svg': svg(g, W, '#1C1B1A'),
        f'{pre}zako-white.svg': svg(g, W, '#FFFFFF'),
        f'{pre}zako-lockup.svg': lockup(g, W, desc_d, desc_w, desc_h, '#1C1B1A', '#1C1B1A'),
        f'{pre}zako-lockup-white.svg': lockup(g, W, desc_d, desc_w, desc_h, '#FFFFFF', '#FFFFFF'),
        f'{pre}favicon.svg': stacked_svg(r1, r2, '#FFFFFF', '#1C1B1A'),
    }
    for n, t in files.items():
        open(os.path.join(out, n), 'w').write(t)
    return W

if __name__ == '__main__' and len(sys.argv) > 2 and sys.argv[2] == 'sheet':
    for k in CONCEPTS: write_all(sys.argv[1], k)
