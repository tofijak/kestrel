"""Renders the README images into docs/img/.

Run from the repo root:  python tools/render.py
Needs: manifold3d trimesh numpy pyvista
"""
import math
import sys
from pathlib import Path

import numpy as np
import pyvista as pv
from manifold3d import Manifold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import digiscope as d          # noqa: E402
import oneplus13_model as op   # noqa: E402

OUT = ROOT / "docs" / "img"
OUT.mkdir(parents=True, exist_ok=True)

# Kestrel palette: rufous back, slate-blue head, dark eye
RUFOUS = "#c8642b"
SLATE = "#5d7387"
GRAPHITE = "#34373c"
ISLAND = "#1c1d20"
GLASS = "#07080a"
NICKEL = "#c9ccd1"
RUBBER = "#26282c"
BG_TOP, FLOOR = "#f3f4f6", "#d5d9df"


# ---------- geometry helpers ----------
def cyl(h, r, seg=96):
    return Manifold.cylinder(h, r, r, seg)


def union(parts):
    out = None
    for p in parts:
        out = p if out is None else out + p
    return out


def magnets_ring_pattern(z, n=d.mag_n, r=d.mag_r, dia=d.mag_d, h=d.mag_h):
    return union(cyl(h, dia / 2, 40).translate(
        (r * math.cos(math.radians(i * 360 / n + 180 / n)),
         r * math.sin(math.radians(i * 360 / n + 180 / n)), z)) for i in range(n))


def at_angles(m, angles, r=d.mag_r):
    return union(m.translate((r * math.cos(math.radians(a)), r * math.sin(math.radians(a)), 0))
                 for a in angles)


def ring_with_magnets(scope):
    ring = d.okular_ring(**d.SCOPES[scope])
    H = d.ring_dims(**d.SCOPES[scope])[4]
    if d.coupling == "balls":  # stålkugler
        mags = at_angles(Manifold.sphere(d.ball_r, 64), d.ball_angles()).translate(
            (0, 0, H + d.ball_p - d.ball_r))
    elif d.steel_in == "ring":  # stålskiver i ringen
        mags = magnets_ring_pattern(H - d.disc_t - d.disc_recess, dia=d.disc_d, h=d.disc_t)
    else:
        mags = magnets_ring_pattern(H - d.mag_h - 0.05)
    return ring, mags, H


def adapter_with_magnets(phone):
    p = d.PHONES[phone]
    a = d.phone_adapter(**p)
    L = d.to_adapter_frame(p["lens"], p["magsafe"])[0] if "lens" in p else p["lens_to_magsafe"]
    top = d.lobe_t + p["bump_h"]
    if d.coupling == "balls":  # magneter lukket inde over rillerne
        mags = at_angles(cyl(d.mag_h, d.mag_d / 2, 40), d.groove_angles()).translate((0, 0, d.mag_z0))
    elif d.steel_in == "adapter":  # stålskiver på scope-siden
        mags = magnets_ring_pattern(d.disc_recess, dia=d.disc_d, h=d.disc_t)
    else:
        mags = magnets_ring_pattern(0.05)
    mags += magnets_ring_pattern(top - d.mag_h - 0.05, d.ms_mag_n, d.ms_mag_r).translate((0, L, 0))
    return a, mags


def atx_eyepiece(top_z, length=70.0):
    """Simplified ATX eyepiece: ribbed rubber eyecup Ø59 + wider body. Top (eye end) at top_z, extends -z."""
    cup_h = 22.0
    cup = cyl(cup_h, 59.0 / 2, 160) - cyl(cup_h + 2, 44.0 / 2, 160).translate((0, 0, -1))
    for k in range(3):
        cup += (cyl(1.2, 59.6 / 2, 160) - cyl(2, 58 / 2, 160).translate((0, 0, -0.4))).translate((0, 0, 3 + k * 2.4))
    body = cyl(length - cup_h, 66.0 / 2, 160) - cyl(length, 40.0 / 2, 160).translate((0, 0, -1))
    glass = cyl(0.6, 22.0, 120).translate((0, 0, cup_h - 9))
    ep = cup.translate((0, 0, -cup_h)) + body.translate((0, 0, -length))
    return ep.translate((0, 0, top_z)), glass.translate((0, 0, top_z - cup_h))


def phone_parts():
    body, island = op.phone()
    top = op.T + op.island_h + op.lens_ring_h
    glass = union(cyl(0.3, op.lens_glass_d / 2, 64).translate((x, y, top - 0.65))
                  for (x, y) in op.lenses.values())
    flash = cyl(0.2, 2.4, 48).translate((op.flash[0], op.flash[1], op.T + op.island_h - 0.25))
    return body, island, glass, flash


def place_on_phone(m, phone="OP13"):
    """Same transform as oneplus13_model.placed_adapter, for any solid in the adapter frame."""
    p = d.PHONES[phone]
    m = m.rotate((0, 180, 0)).translate((0, 0, d.lobe_t + p["bump_h"] + op.T))
    mx, my = op.magsafe_c
    lx, ly = op.lenses["main"]
    ang = math.degrees(math.atan2(ly - my, lx - mx)) + 90
    return m.rotate((0, 0, ang)).translate((lx, ly, 0))


# ---------- rendering ----------
def to_pv(m):
    mesh = m.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3]
    f = np.asarray(mesh.tri_verts)
    return pv.PolyData(v, np.hstack([np.full((len(f), 1), 3), f]).ravel())


MAT = {
    RUFOUS: dict(ambient=0.22, diffuse=0.85, specular=0.22, specular_power=16),
    SLATE: dict(ambient=0.22, diffuse=0.85, specular=0.28, specular_power=20),
    GRAPHITE: dict(ambient=0.18, diffuse=0.75, specular=0.55, specular_power=45),
    ISLAND: dict(ambient=0.15, diffuse=0.6, specular=0.7, specular_power=70),
    GLASS: dict(ambient=0.05, diffuse=0.3, specular=1.0, specular_power=100),
    NICKEL: dict(ambient=0.3, diffuse=0.6, specular=1.0, specular_power=70),
    RUBBER: dict(ambient=0.15, diffuse=0.75, specular=0.12, specular_power=8),
}


KEY = np.array([-0.9, -0.35, 1.6])   # key light direction (towards the light)


def shadow_floor(meshes, z0, c, S, res=2400):
    """Soft shadows baked into the floor: a cast shadow along the key light + a tight contact shadow."""
    from PIL import Image, ImageDraw, ImageFilter
    ppm = res / S
    acc = np.zeros((res, res))
    k = KEY / KEY[2]

    def layer(pm, shift, blur, strength):
        img = Image.new("L", (res, res), 0)
        dr = ImageDraw.Draw(img)
        h = np.clip(pm.points[:, 2] - z0, 0, None)
        xy = pm.points[:, :2] - (h[:, None] * k[:2] if shift else 0)
        px = (xy - (c[:2] - S / 2)) * ppm
        px[:, 1] = res - px[:, 1]
        for tri in pm.faces.reshape(-1, 4)[:, 1:]:
            dr.polygon([tuple(px[i]) for i in tri], fill=255)
        return np.asarray(img.filter(ImageFilter.GaussianBlur(blur * ppm))) / 255 * strength

    for pm, _ in meshes:
        h = max(pm.bounds[4] - z0, 0.0)
        hm = (pm.bounds[4] + pm.bounds[5]) / 2 - z0
        for sh in (layer(pm, True, 2.0 + 0.18 * hm, 0.55 * math.exp(-h / 120)),
                   layer(pm, False, 1.0 + 0.3 * h, 0.55 * math.exp(-h / 6))):
            acc = 1 - (1 - acc) * (1 - sh)
    base = np.array(pv.Color(FLOOR).float_rgb)
    shade = np.array([0.80, 0.83, 0.88])               # cool shadow tint
    rgb = base * (1 - acc[..., None] * (1 - shade * 0.55))
    return pv.numpy_to_texture((np.clip(rgb, 0, 1) * 255).astype(np.uint8))


def render(name, items, size, view, zoom=1.0, up=(0, 0, 1), floor=True, ssao=True, frames=0,
           focus=None, front=0.0):
    """items: [(Manifold, color)]. view: direction from target to camera. zoom > 1 = closer."""
    meshes = [(to_pv(m), c) for m, c in items]
    b = np.array([pm.bounds for pm, _ in meshes])
    lo = np.array([b[:, 0].min(), b[:, 2].min(), b[:, 4].min()])
    hi = np.array([b[:, 1].max(), b[:, 3].max(), b[:, 5].max()])
    c = (lo + hi) / 2
    R = np.linalg.norm(hi - lo) / 2

    if focus is not None:      # orbit/aim around this point instead of the bounding-box centre
        R = max(np.linalg.norm(hi[:2] - np.array(focus[:2])), np.linalg.norm(lo[:2] - np.array(focus[:2])),
                (hi[2] - lo[2]) / 2) * 0.95
    target = np.array(focus if focus is not None else c, float)
    pl = pv.Plotter(off_screen=True, window_size=size, lighting="none")
    pl.set_background(FLOOR)
    for pos, inten in [(tuple(KEY), 0.72),           # key
                       ((1.2, -0.5, 0.6), 0.24),     # fill
                       ((0.3, 1.4, 0.8), 0.34)]:     # rim
        pl.add_light(pv.Light(position=tuple(c + np.array(pos) * R * 6), focal_point=tuple(c),
                              intensity=inten, light_type="scene light"))
    for pm, col in meshes:
        pl.add_mesh(pm, color=col, smooth_shading=True, split_sharp_edges=True, feature_angle=35, **MAT[col])
    if floor:
        S = R * 14
        z0 = lo[2] - 0.05
        fl = pv.Plane(center=(c[0], c[1], z0), direction=(0, 0, 1), i_size=S, j_size=S)
        fl.texture_map_to_plane(origin=(c[0] - S / 2, c[1] - S / 2, z0), point_u=(c[0] + S / 2, c[1] - S / 2, z0),
                                point_v=(c[0] - S / 2, c[1] + S / 2, z0), inplace=True)
        pl.add_mesh(fl, texture=shadow_floor(meshes, z0, c, S), ambient=1.0, diffuse=0.0, specular=0.0)
    v = np.array(view, float); v /= np.linalg.norm(v)
    if front:
        pl.add_light(pv.Light(position=tuple(target + v * R * 6 + np.array([0, 0, R * 2])),
                              focal_point=tuple(target), intensity=front, light_type="scene light"))
    dist = R / math.sin(math.radians(30 / 2)) / zoom
    pl.camera.view_angle = 30
    pl.camera.focal_point = tuple(target)
    pl.camera.position = tuple(target + v * dist)
    pl.camera.up = up
    pl.reset_camera_clipping_range()
    if ssao and not floor:
        pl.enable_ssao(radius=3.0, bias=0.15, kernel_size=128, blur=True)
    pl.enable_anti_aliasing("ssaa")
    if frames:   # turntable GIF: orbit the camera around the vertical axis
        from PIL import Image
        imgs = []
        for _ in range(frames):
            imgs.append(Image.fromarray(pl.screenshot(None, return_img=True)))
            pl.camera.Azimuth(360 / frames)
            pl.reset_camera_clipping_range()
            pl.render()
        pal = imgs[0].quantize(colors=255, method=Image.Quantize.MEDIANCUT)
        frames_q = [im.quantize(palette=pal, dither=Image.Dither.NONE) for im in imgs]
        frames_q[0].save(OUT / name, save_all=True, append_images=frames_q[1:], duration=70, loop=0,
                         optimize=True, disposal=1)
    else:
        pl.screenshot(OUT / name)
    pl.close()
    print("wrote", OUT / name)


def flip_ring(m, z):
    """Ring turned magnet face down (towards the adapter), its magnet face at height z."""
    return m.rotate((0, 180, 0)).translate((0, 0, z))


def hero():
    """Phone with adapter on the table; ring and ATX eyepiece hovering above in an exploded stack."""
    body, island, glass, flash = phone_parts()
    a, am = adapter_with_magnets("OP13")
    ring, rm, H = ring_with_magnets("ATX")
    p = d.PHONES["OP13"]
    lx, ly = op.lenses["main"]
    face = op.T + d.lobe_t + p["bump_h"]
    g_ring, g_ep = 26.0, 24.0
    top_t = H - d.grip_depth
    ep, epg = atx_eyepiece(0, 36)
    up = lambda m: m.rotate((0, 180, 0))
    items = [(body, GRAPHITE), (island, ISLAND), (glass, GLASS), (flash, NICKEL),
             (place_on_phone(a), RUFOUS), (place_on_phone(am), NICKEL),
             (flip_ring(ring, face + H + g_ring).translate((lx, ly, 0)), SLATE),
             (flip_ring(rm, face + H + g_ring).translate((lx, ly, 0)), NICKEL),
             (up(ep).translate((lx, ly, face + g_ring + top_t + g_ep)), RUBBER),
             (up(epg).translate((lx, ly, face + g_ring + top_t + g_ep)), GLASS)]
    items = [(m.rotate((0, 0, -62)), col) for m, col in items]
    render("hero.png", items, (2000, 1150), view=(0.1, -1.0, 0.58), zoom=1.3)


def turntable():
    """Same exploded stack as hero(), spinning."""
    body, island, glass, flash = phone_parts()
    a, am = adapter_with_magnets("OP13")
    ring, rm, H = ring_with_magnets("ATX")
    p = d.PHONES["OP13"]
    lx, ly = op.lenses["main"]
    face = op.T + d.lobe_t + p["bump_h"]
    g_ring, g_ep = 26.0, 24.0
    top_t = H - d.grip_depth
    ep, epg = atx_eyepiece(0, 36)
    up = lambda m: m.rotate((0, 180, 0))
    items = [(body, GRAPHITE), (island, ISLAND), (glass, GLASS), (flash, NICKEL),
             (place_on_phone(a), RUFOUS), (place_on_phone(am), NICKEL),
             (flip_ring(ring, face + H + g_ring).translate((lx, ly, 0)), SLATE),
             (flip_ring(rm, face + H + g_ring).translate((lx, ly, 0)), NICKEL),
             (up(ep).translate((lx, ly, face + g_ring + top_t + g_ep)), RUBBER),
             (up(epg).translate((lx, ly, face + g_ring + top_t + g_ep)), GLASS)]
    # spin around the optical axis of the stack
    items = [(m.translate((-lx, -ly, 0)), col) for m, col in items]
    render("turntable.gif", items, (900, 620), view=(0.0, -1.0, 0.72), zoom=0.92, frames=48,
           focus=(0, 0, 45))


def kit():
    """Flat-lay of every part, magnet faces up."""
    rings = [ring_with_magnets(s) for s in d.SCOPES]
    adps = [adapter_with_magnets(ph) for ph in d.PHONES]
    items, x = [], 0.0
    for ring, rm, H in rings:
        items += [(ring.translate((x, 0, 0)), SLATE), (rm.translate((x, 0, 0)), NICKEL)]
        x += 84
    for (a, am), dx in zip(adps, (0, 84)):
        f = lambda m: m.rotate((180, 0, 0)).translate((dx, -95, d.lobe_t + 8.6))
        items += [(f(a), RUFOUS), (f(am), NICKEL)]
    render("kit.png", items, (1800, 1300), view=(0.15, -0.55, 1.0), zoom=1.15)


def parts():
    for scope in d.SCOPES:
        ring, rm, H = ring_with_magnets(scope)
        render(f"ring_{scope}.png", [(ring, SLATE), (rm, NICKEL)], (1000, 760), (0.55, -0.95, 0.95), 1.25)
    for phone in d.PHONES:
        a, am = adapter_with_magnets(phone)
        flip = lambda m: m.rotate((180, 0, 0)).translate((0, 0, 9))
        render(f"adapter_{phone}_scope_side.png", [(flip(a), RUFOUS), (flip(am), NICKEL)],
               (1000, 760), (0.6, -0.8, 1.0), 1.3)
        render(f"adapter_{phone}_phone_side.png", [(a, RUFOUS), (am, NICKEL)],
               (1000, 760), (0.6, -0.8, 1.0), 1.3)


def on_phone():
    body, island, glass, flash = phone_parts()
    a, am = adapter_with_magnets("OP13")
    items = [(body, GRAPHITE), (island, ISLAND), (glass, GLASS), (flash, NICKEL),
             (place_on_phone(a), RUFOUS), (place_on_phone(am), NICKEL)]
    render("on_phone_OP13.png", [(m.rotate((0, 0, 24)), c) for m, c in items], (1600, 1000),
           (-0.35, -0.9, 0.85), 1.35)
    # phone alone, so the camera island the collar locks onto is visible
    render("oneplus13.png", [(m.rotate((0, 0, 24)), c) for m, c in items[:4]], (1600, 1000),
           (-0.35, -0.9, 0.85), 1.35)


def cutaway():
    """Half-section through ATX eyepiece + ring + adapter, clicked together."""
    ring, rm, H = ring_with_magnets("ATX")
    a, am = adapter_with_magnets("OP13")
    ep, epg = atx_eyepiece(d.grip_depth, 26)
    zA = H + (d.face_gap if d.coupling == "balls" else 0)
    items = [(ring, SLATE), (rm, NICKEL), (a.translate((0, 0, zA)), RUFOUS),
             (am.translate((0, 0, zA)), NICKEL), (ep, RUBBER), (epg, GLASS)]
    rot = -d.ball_angles()[0] if d.coupling == "balls" else 22.5  # snit gennem en kugle/magnet
    cut = [(m.rotate((0, 0, rot)).trim_by_plane((0, 1, 0), 0.0), col) for m, col in items]
    render("cutaway.png", cut, (1600, 1000), (0.22, -1.0, 0.25), 1.4, floor=False, front=0.45)


if __name__ == "__main__":
    which = sys.argv[1:] or ["hero", "turntable", "kit", "parts", "on_phone", "cutaway"]
    for w in which:
        globals()[w]()
