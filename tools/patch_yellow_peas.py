"""Adds Finnish/Swedish letters (ä ö å Ä Ö Å) and a few punctuation glyphs to the
Yellow Peas DEMO fonts so the site preview renders Finnish text in one typeface.
Preview-only stopgap: buy the full licence from MyFonts before publishing."""
import math, sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.cu2quPen import Cu2QuPen

def contours(font, gname):
    glyf = font['glyf'][gname]
    coords, ends, flags = glyf.getCoordinates(font['glyf'])
    out, start = [], 0
    for e in ends:
        out.append((list(coords[start:e+1]), list(flags[start:e+1])))
        start = e + 1
    return out

def draw_contour(pen, pts, flags, dx=0, dy=0):
    # Reconstruct a TrueType contour (on/off curve points) into pen calls.
    pts = [(x+dx, y+dy) for x, y in pts]
    on = [bool(f & 1) for f in flags]
    n = len(pts)
    # rotate so we start on an on-curve point
    if not any(on):
        mid = ((pts[0][0]+pts[-1][0])/2, (pts[0][1]+pts[-1][1])/2)
        pts.insert(0, mid); on.insert(0, True); n += 1
    k = on.index(True)
    pts = pts[k:]+pts[:k]; on = on[k:]+on[:k]
    pen.moveTo(pts[0])
    i = 1; offs = []
    while i <= n:
        p = pts[i % n]; o = on[i % n]
        if o:
            if offs:
                pen.qCurveTo(*offs, p); offs = []
            else:
                if i < n: pen.lineTo(p)
        else:
            offs.append(p)
        i += 1
    if offs:
        pen.qCurveTo(*offs, pts[0])
    pen.closePath()

def circle(pen, cx, cy, r, clockwise=True):
    k = 0.5523 * r
    if clockwise:  # TrueType outer contours are clockwise
        pen.moveTo((cx, cy+r))
        pen.curveTo((cx+k, cy+r), (cx+r, cy+k), (cx+r, cy))
        pen.curveTo((cx+r, cy-k), (cx+k, cy-r), (cx, cy-r))
        pen.curveTo((cx-k, cy-r), (cx-r, cy-k), (cx-r, cy))
        pen.curveTo((cx-r, cy+k), (cx-k, cy+r), (cx, cy+r))
    else:
        pen.moveTo((cx, cy+r))
        pen.curveTo((cx-k, cy+r), (cx-r, cy+k), (cx-r, cy))
        pen.curveTo((cx-r, cy-k), (cx-k, cy-r), (cx, cy-r))
        pen.curveTo((cx+k, cy-r), (cx+r, cy-k), (cx+r, cy))
        pen.curveTo((cx+r, cy+k), (cx+k, cy+r), (cx, cy+r))
    pen.closePath()

def rect(pen, x0, y0, x1, y1):
    pen.moveTo((x0, y0)); pen.lineTo((x0, y1)); pen.lineTo((x1, y1)); pen.lineTo((x1, y0)); pen.closePath()

def patch(src, dst, cfg):
    f = TTFont(src)
    for tag in ('hdmx', 'LTSH', 'VDMX'):
        if tag in f: del f[tag]
    cmap = f.getBestCmap(); order = f.getGlyphOrder()
    glyf = f['glyf']; hmtx = f['hmtx']
    # tittle = highest contour of 'i'
    ic = contours(f, cmap[ord('i')])
    tit = max(ic, key=lambda c: min(p[1] for p in c[0]))
    tx0 = min(p[0] for p in tit[0]); tx1 = max(p[0] for p in tit[0])
    ty0 = min(p[1] for p in tit[0])
    tcx = (tx0+tx1)/2; tw = tx1-tx0
    new = {}
    def base_bounds(g):
        cs = contours(f, g); xs=[p[0] for c in cs for p in c[0]]; ys=[p[1] for c in cs for p in c[0]]
        return min(xs), min(ys), max(xs), max(ys)
    def build(name, base, kind, upper):
        bg = cmap[ord(base)]
        x0, y0, x1, y1 = base_bounds(bg)
        cx = (x0+x1)/2
        pen = TTGlyphPen(None)
        for pts, fl in contours(f, bg):
            draw_contour(pen, pts, fl)
        top = y1 if upper else cfg['xh']
        gap = ty0 - cfg['xh']
        if kind == 'dier':
            spread = cfg['spread_u'] if upper else cfg['spread_l']
            dy = (top + gap) - ty0
            for sx in (-spread, spread):
                draw_contour(pen, tit[0], tit[1], dx=cx+sx-tcx, dy=dy)
        else:  # ring
            r = cfg['ring_r']; s = cfg['ring_s']
            cy = top + gap + r
            qp = Cu2QuPen(pen, 1.0, reverse_direction=False)
            circle(qp, cx, cy, r, clockwise=True)
            circle(qp, cx, cy, r - s, clockwise=False)
        new[name] = (pen.glyph(), hmtx[bg][0])
    for name, base, kind, up in [('adieresis','a','dier',False),('odieresis','o','dier',False),('aring','a','ring',False),
                                 ('Adieresis','A','dier',True),('Odieresis','O','dier',True),('Aring','A','ring',True)]:
        build(name, base, kind, up)
    # hyphen / endash
    s = cfg['stem']; hy = cfg['xh']*0.5
    for name, w, adv in [('hyphen', cfg['hyw'], cfg['hyw']+2*cfg['side']), ('endash', cfg['hyw']*1.8, cfg['hyw']*1.8+2*cfg['side'])]:
        pen = TTGlyphPen(None); rect(pen, cfg['side'], hy - s/2, cfg['side']+w, hy + s/2)
        new[name] = (pen.glyph(), int(adv))
    # period / comma / apostrophe from tittle if missing
    for name, uni, ydst in [('period', 0x2E, 0), ('comma', 0x2C, 0), ('quoteright', 0x2019, cfg['cap']-(tit and (max(p[1] for p in tit[0])-ty0)))]:
        if uni in cmap and name != 'quoteright':
            continue
        if name == 'quoteright' and 0x2C in cmap and cfg.get('use_comma_for_apos'):
            cg = cmap[0x2C]; pen = TTGlyphPen(None)
            cs = contours(f, cg); cy1 = max(p[1] for c in cs for p in c[0])
            for pts, fl in cs: draw_contour(pen, pts, fl, dy=cfg['cap']-cy1)
            new[name] = (pen.glyph(), hmtx[cg][0]); continue
        pen = TTGlyphPen(None); side = cfg['side']
        draw_contour(pen, tit[0], tit[1], dx=side - tx0, dy=ydst - ty0)
        new[name] = (pen.glyph(), int(tw + 2*side))
    unis = {'adieresis':0xE4,'odieresis':0xF6,'aring':0xE5,'Adieresis':0xC4,'Odieresis':0xD6,'Aring':0xC5,
            'hyphen':0x2D,'endash':0x2013,'period':0x2E,'comma':0x2C,'quoteright':0x2019}
    for name, (g, adv) in new.items():
        gname = name if name not in order else name + '.bcr'
        glyf.glyphs[gname] = g; g.recalcBounds(glyf)
        order.append(gname)
        hmtx.metrics[gname] = (adv, g.xMin if hasattr(g, 'xMin') else 0)
        for t in f['cmap'].tables:
            if t.isUnicode(): t.cmap[unis[name]] = gname
        if name == 'quoteright':
            for t in f['cmap'].tables:
                if t.isUnicode(): t.cmap[0x27] = gname
    if cfg.get('drop_comma'):
        # the synthetic comma looked like a period -> let the browser fall back to Switzer's comma
        for t in f['cmap'].tables:
            if t.isUnicode(): t.cmap.pop(0x2C, None)
    f.setGlyphOrder(order)
    if 'post' in f and hasattr(f['post'], 'extraNames'):
        f['post'].formatType = 2.0
    f['OS/2'].usWinAscent = max(f['OS/2'].usWinAscent, 950)
    f.flavor = 'woff2'
    f.save(dst)
    print('saved', dst, len(order), 'glyphs')

if __name__ == '__main__':
    srcdir, outdir = sys.argv[1], sys.argv[2]
    patch(f'{srcdir}/yellow peas demo.ttf', f'{outdir}/yellow-peas-regular.woff2',
          dict(xh=437, cap=699, stem=18, spread_l=95, spread_u=120, ring_r=62, ring_s=18, hyw=200, side=60, use_comma_for_apos=True))
    patch(f'{srcdir}/Yellow Peas Bold demo.ttf', f'{outdir}/yellow-peas-bold.woff2',
          dict(xh=387, cap=594, stem=78, spread_l=92, spread_u=110, ring_r=78, ring_s=42, hyw=170, side=40, drop_comma=True))
