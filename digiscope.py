"""Magnetisk digiscoping-adapter – flere scopes og telefoner.

Alle okular-ringe og alle telefon-adaptere har SAMME kobling (kugler/riller eller kant/rille),
så enhver telefon-adapter passer på enhver ring.

Kør:  python digiscope.py      -> skriver én okular_ring_<scope>.stl pr. scope
                                  og én telefon_adapter_<telefon>.stl pr. telefon
Alle mål i mm. Ret/tilføj profiler i SCOPES og PHONES herunder.
"""
import math
from pathlib import Path

import numpy as np
import trimesh
from manifold3d import CrossSection, Manifold

SEG = 160

# ---------- Scopes (okular-ringe) ----------
SCOPES = {
    # Swarovski ATX/STX: øjemusling Ø59 mm (Swarovskis AR-S-adapterring "for eyecups Ø 59 mm",
    # Outdoorsmans' Digidapter 59 mm-ring til ATX). PLA-huller printes ca. 0,2-0,3 mm for små -> 0,7 luft.
    "ATX": dict(eyepiece_d=59.0, fit=0.7),
    # Vortex Diamondback HD 20-60x85: officiel spec "Eyepiece Diameter 2.103 in" = 53,42 mm
    "DiamondbackHD85": dict(eyepiece_d=53.42),
}
fit_clear = 0.4        # ekstra diameter (0.2 = stramt, 0.8 = løst + filt/isoleringstape)
grip_depth = 11.0      # hvor langt ringen griber ned over øjestykket

# ---------- Telefoner (adaptere) ----------
# lens_to_magsafe: centrum af MagSafe-ring -> centrum af hovedkameraet
# bump_h:          fra bagside (ved MagSafe) til det, linse-delen hviler på (kamerakant/linsering)
PHONES = {
    # OnePlus 13 i magnetcover. Målt på officielt bagside-foto + Bizon CrystalO-cover:
    #   hovedkamera (nederst til venstre i øen) 21,4/43,9 fra hjørnet, MagSafe-centrum ca. 38/92,4
    # Koordinater set bagfra, origo i øverste venstre hjørne (y negativ nedad).
    # Kraven går ned rundt om den runde kamera-ø og låser vinklen, så hullet altid rammer hovedkameraet.
    # Hovedkamera = øverste venstre linse set bagfra (bekræftet på telefonen).
    # MagSafe-centrum: målt på Bizon-magnetcover; ringen sidder over opladerspolen i alle covers.
    "OP13": dict(bump_h=3.5, lens_hole_d=15.0,
                 lens=(21.4, -26.0), magsafe=(38.0, -92.4),
                 island=(30.6, -34.1), island_d=49.8),
    # iPhone 15 (uden cover). Apples målskitse (2023-10-10):
    #   MagSafe-centrum = produktcentrum 35,81/73,82, hovedkamera ("rear camera 2", 75,55° kegle)
    #   25,64/25,64 -> 49,24 mm. Kameraglas 3,48 over bagglas; linseringene står lidt højere.
    #   Med MagSafe-cover: sæt bump_h til højden af coverets kamerakant over coverets bagside.
    "iPhone15": dict(lens_to_magsafe=49.24, bump_h=3.6, lens_hole_d=13.0),
}

# ---------- Fælles grænseflade (må ikke ændres, hvis delene skal passe sammen) ----------
mag_d, mag_h = 6.0, 3.0  # 6x3 mm N52 rundmagneter
mag_n = 8
mag_clear_d = 0.25     # lommen er lidt større (lim)
mag_r = 32.3           # radius til magnetcirklen
ring_od = 74.0         # ydre diameter (ring og adapterens linse-del)
lip_outer_r = 28.0     # ydre radius af centreringskanten på ringen
lip_w = 2.0            # bredde af kanten (ens på alle ringe)
lip_h = 1.5
lip_clear = 0.5        # ekstra diameter i adapterens modsvarende fordybning
max_hole_d = 52.0      # største lysåbning i ringen

# Kobling mellem ring og adapter.
#   "balls" (v2): 3 stålkugler i ringen (120°) falder i 3 af 12 radiale V-riller i adapteren
#                 (hver 30°, så stående og liggende virker). Magneten sidder lige over rillen og
#                 trækker i kuglen. Kuglerne centrerer og låser rotationen; ingen centreringskant.
#   "lip"   (v1): stålstifter i ringen + centreringskant på ringen og rille i adapteren.
coupling = "balls"
ball_d = 6.0           # lejekugler Ø6 mm, kromstål (GCr15/52100, magnetisk)
ball_n = 3
ball_p = 2.0           # hvor meget kuglen stikker op over ringens flade
ball_fit = 0.0         # ekstra diameter på kuglelommen (PLA-huller printes ~0,2 for små -> let presning + lim)
face_gap = 0.3         # luft mellem ringens og adapterens flader, når kuglerne sidder i rillerne
groove_n = 12          # riller i adapteren, jævnt fordelt (12 = hver 30°)
groove_len = 7.0       # rillens længde radialt
mag_gap = 0.3          # luft fra kuglens top til magneten
cap_t = 0.6            # plast over magneterne, printes efter pausen hvor magneterne lægges i
layer_h = 0.2          # lagtykkelse; magnetlommens top lægges på et laggrænse

# ---------- Adapter ----------
lobe_t = 5.0           # tykkelse af linse-delen
magsafe_od = 58.0      # MagSafe-pude
plate_r_ms = 29.0      # pladens radius omkring MagSafe-centrum
# Ringen på okularet har stålskiver, adapteren har magneterne.
# Ingen magneter på scopet; ca. 2 mT ved kameraet mens adapteren sidder på telefonen
# (mod 3,6 mT med magneter i begge dele).
steel_in = "ring"      # "ring" = stål i ringen, "adapter" = stål i adapteren, "none" = magneter i begge
# Stålskiver = GB119-cylinderstifter M6 x 6 mm, lejestål HRC62 (magnetisk). Ø6-skiver af jern
# findes næsten ikke, og Ø6-stifter starter ved 6 mm (AliExpress 1005010026576161, M6x6, 50 stk.).
# Kilde: sælgers spec, mål med skydelære ved modtagelse og ret her før print.
disc_d, disc_t = 6.0, 6.0
disc_clear_d = 0.25    # lommen er lidt større (lim)
disc_recess = 0.1      # skiven ligger lidt under fladen
magsafe_mode = "magnets"  # "magnets" = rundmagneter i puden, "steel" = fordybning til stål-ring sticker
ms_mag_n = 12          # antal magneter i MagSafe-puden
ms_mag_r = 24.5        # radius = midt i MagSafe-ringen (Ø44-54)
steel_od, steel_id, steel_t = 56.0, 44.0, 0.8  # kun ved magsafe_mode = "steel"
island_fit = 0.8       # ekstra diameter i kraven omkring kamera-øen
collar_wall = 2.0      # vægtykkelse på kraven
collar_gap = 1.0       # kraven stopper så langt over coverets bagside (plads til coverkant)

# ======================================================================
E = 0.01
ring_r = ring_od / 2
pocket_d = mag_d + mag_clear_d
pocket_h = mag_h + 0.15

# Kugle-kobling, adapterens koordinater (z = 0 er fladen mod scopet, +z ind i adapteren).
# Rillen er en 90° V: kuglen rører begge sider i 45°, R/√2 fra centrum.
ball_r = ball_d / 2
ball_zc = -face_gap + ball_p - ball_r              # kuglens centrum
groove_apex = ball_zc + ball_r * math.sqrt(2)      # V'ens (tænkte) top
mag_z0 = math.ceil((ball_zc + ball_r + mag_gap) / layer_h - 1e-6) * layer_h  # magnetens underside
mag_z1 = math.ceil((mag_z0 + mag_h + 0.05) / layer_h - 1e-6) * layer_h      # lommens top
pause_z = mag_z1 + layer_h                         # print-pause: læg magneterne i før dette lag
if coupling == "balls":
    lobe_t = max(lobe_t, mag_z1 + cap_t)


def cyl(h, r1, r2=None, seg=SEG):
    return Manifold.cylinder(h, r1, r1 if r2 is None else r2, seg)


def magnet_pockets(z_bottom, n=mag_n, r=mag_r, d=None, h=None):
    d = pocket_d if d is None else d
    h = pocket_h if h is None else h
    out = None
    for i in range(n):
        a = math.radians(i * 360 / n + 180 / n)
        p = cyl(h + E, d / 2, seg=48).translate(
            (r * math.cos(a), r * math.sin(a), z_bottom))
        out = p if out is None else out + p
    return out


def ring_pockets():
    """(diameter, dybde) for lommerne i ringens top."""
    if coupling == "balls":
        return ball_d + ball_fit, ball_d - ball_p
    if steel_in == "ring":
        return disc_d + disc_clear_d, disc_t + disc_recess
    return pocket_d, pocket_h


def ring_dims(eyepiece_d, fit=fit_clear):
    """(ep_r, hole_r, chamf, top_t, H) – H er højden af ringens topflade."""
    ep_r = (eyepiece_d + fit) / 2
    hole_r = min(max_hole_d, eyepiece_d + fit - 6) / 2  # mindst 3 mm anlæg til øjestykkets kant
    if coupling == "lip":
        assert hole_r <= lip_outer_r - lip_w, "lysåbningen er større end kantens inderside"
    chamf = ep_r - hole_r
    # væg mellem lommens nederste inderhjørne og 45°-fasen (vinkelret afstand) >= 1,2 mm
    r_pd, r_ph = ring_pockets()
    p_in = mag_r - r_pd / 2
    top_t = max(4.15, chamf + 1.2)
    while (p_in - (ep_r - (top_t - r_ph))) / math.sqrt(2) < 1.2:
        top_t += 0.05
    return ep_r, hole_r, chamf, top_t, grip_depth + top_t


def ball_angles():
    return [90 + i * 360 / ball_n for i in range(ball_n)]


def groove_angles():
    return [90 + i * 360 / groove_n for i in range(groove_n)]


def ball_pockets(z_bottom, d, h):
    out = None
    for a in map(math.radians, ball_angles()):
        p = cyl(h + E, d / 2, seg=64).translate((mag_r * math.cos(a), mag_r * math.sin(a), z_bottom))
        out = p if out is None else out + p
    return out


def groove_cutter():
    """12 radiale V-riller (45°-tag, printes uden support) + lukkede magnetlommer lige over dem."""
    half = groove_apex + 1  # V'ens halve bredde ved z = -1
    v = CrossSection([[(-half, -1), (half, -1), (0, groove_apex)]])
    prism = v.extrude(groove_len).rotate((90, 0, 0))   # profil i x-z, længde langs y
    prism = prism.translate((0, groove_len / 2, 0))  # centreret om y = 0
    pocket = cyl(mag_z1 - mag_z0, pocket_d / 2, seg=48).translate((0, 0, mag_z0))
    one = (prism + pocket).rotate((0, 0, -90)).translate((mag_r, 0, 0))  # længde langs x (radialt)
    out = None
    for a in groove_angles():
        g = one.rotate((0, 0, a))
        out = g if out is None else out + g
    return out


def okular_ring(eyepiece_d, fit=fit_clear):
    """Print med åbningen NED på pladen (magnet-/kuglesiden opad)."""
    ep_r, hole_r, chamf, top_t, H = ring_dims(eyepiece_d, fit)
    profile = [
        (ep_r + 0.6, 0), (ring_r - 0.8, 0), (ring_r, 0.8),
        (ring_r, H - 0.5), (ring_r - 0.5, H), (hole_r, H),
        (hole_r, H - (top_t - chamf)),  # flange ved lysåbningen
        (ep_r, H - top_t),              # 45° fase ned til øjestykke-væggen
        (ep_r, 0.6),
    ]
    body = CrossSection([profile]).revolve(SEG)
    lip_ri = lip_outer_r - lip_w
    lip_profile = [(lip_ri, H - E), (lip_outer_r, H - E),
                   (lip_outer_r, H + lip_h - 0.5), (lip_outer_r - 0.5, H + lip_h),
                   (lip_ri + 0.5, H + lip_h), (lip_ri, H + lip_h - 0.5)]
    r_pd, r_ph = ring_pockets()
    if coupling == "balls":
        return body - ball_pockets(H - r_ph, r_pd, r_ph)
    body = body + CrossSection([lip_profile]).revolve(SEG)
    return body - magnet_pockets(H - r_ph, d=r_pd, h=r_ph)


def to_adapter_frame(lens, magsafe):
    """Returnerer (L, f) hvor f mapper et punkt set bagfra på telefonen til adapterens koordinater
    (origo = linsen, MagSafe på +Y). Adapteren vendes 180° om sin Y-akse for at ligge på telefonen,
    så x skal spejles: set fra telefon-siden er alt spejlvendt i forhold til bagsiden set udefra."""
    vx, vy = magsafe[0] - lens[0], magsafe[1] - lens[1]
    L = math.hypot(vx, vy)
    rot = math.pi / 2 - math.atan2(vy, vx)
    c, s = math.cos(rot), math.sin(rot)

    def f(p):
        x, y = p[0] - lens[0], p[1] - lens[1]
        return (-(c * x - s * y), s * x + c * y)
    return L, f


def phone_adapter(bump_h, lens_hole_d, lens_to_magsafe=None,
                  lens=None, magsafe=None, island=None, island_d=None):
    """Print med scope-siden (magneterne) NED på pladen. Origo = linsecentrum, MagSafe på +Y."""
    if lens is not None:
        L, f = to_adapter_frame(lens, magsafe)
    else:
        L, f = lens_to_magsafe, None
    outline = [cyl(lobe_t, ring_r), cyl(lobe_t, plate_r_ms).translate((0, L, 0))]
    collar = None
    if island is not None:
        ix, iy = f(island)
        ci = (island_d + island_fit) / 2
        co = ci + collar_wall
        outline.append(cyl(lobe_t, co).translate((ix, iy, 0)))
        collar_h = bump_h - collar_gap
        collar = (cyl(collar_h + E, co) - cyl(collar_h + 1, ci).translate((0, 0, -0.5))
                  ).translate((ix, iy, lobe_t - E))
        assert math.hypot(ix, iy - L) - co > magsafe_od / 2, "kraven rammer MagSafe-puden"
    plate = Manifold.batch_hull(outline)
    pad = cyl(bump_h + E, magsafe_od / 2).translate((0, L, lobe_t - E))
    body = plate + pad
    if collar is not None:
        body = body + collar
    top = lobe_t + bump_h
    if magsafe_mode == "steel":
        steel = (cyl(steel_t + 1, steel_od / 2) - cyl(steel_t + 3, steel_id / 2).translate((0, 0, -1)))
        body -= steel.translate((0, L, top - steel_t))
    else:  # magnetlommer åbne mod telefonen, så magneterne rører telefonen/coveret
        body -= magnet_pockets(top - pocket_h, ms_mag_n, ms_mag_r).translate((0, L, E))
    if coupling == "balls":
        body -= groove_cutter()
    else:
        body = _lip_groove_and_pockets(body)
    # linsehul: 45° kegle der åbner sig mod scopet (printbar uden support)
    cone_d = lens_hole_d + 2 * lobe_t
    body -= cyl(lobe_t + 2 * E, cone_d / 2, lens_hole_d / 2).translate((0, 0, -E))
    # pil på MagSafe-puden der peger mod linsen
    arrow = CrossSection([[(-3, 3), (0, -2), (3, 3)]]).extrude(1)
    body -= arrow.translate((0, L - 12, top - 0.6))
    return body


def _lip_groove_and_pockets(body):
    # Rille til ringens centreringskant med spidst 45°-tag: ingen flade lofter/broer,
    # så adapteren kan printes med denne side på pladen uden support.
    g_ro = lip_outer_r + lip_clear / 2
    g_ri = lip_outer_r - lip_w - lip_clear / 2
    g_h = lip_h + 0.3
    half = (g_ro - g_ri) / 2
    groove = CrossSection([[(g_ri, -1), (g_ro, -1), (g_ro, g_h), (g_ri + half, g_h + half),
                            (g_ri, g_h)]]).revolve(SEG)
    body -= groove
    if steel_in == "adapter":
        body -= magnet_pockets(-E, d=disc_d + disc_clear_d, h=disc_t + disc_recess)
    else:
        body -= magnet_pockets(-E)
    return body


def test_ring():
    """Testprint: kun ringens top (Ø74, med kuglelommer) til at mærke og måle holdekraften."""
    d_, h_ = ring_pockets()
    t = h_ + 1.0
    body = cyl(t, ring_r) - cyl(t + 2, 24.0).translate((0, 0, -1))
    return body - ball_pockets(t - h_, d_, h_)


def test_adapter():
    """Testprint: kun adapterens linse-del (Ø74, riller + magnetlommer, pause til magneterne)."""
    body = cyl(lobe_t, ring_r) - cyl(lobe_t + 2, 24.0).translate((0, 0, -1))
    return body - groove_cutter()


def save(m, path):
    assert m.volume() > 0, f"{path.name}: tom geometri ({m.status()})"
    mesh = m.to_mesh()
    tm = trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts))
    tm.export(path)
    b = tm.bounds
    print(f"{path.name}: watertight={tm.is_watertight} vol={tm.volume / 1000:.1f} cm3 "
          f"size={b[1][0] - b[0][0]:.1f} x {b[1][1] - b[0][1]:.1f} x {b[1][2] - b[0][2]:.1f} mm")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    for name, p in SCOPES.items():
        save(okular_ring(**p), here / f"okular_ring_{name}.stl")
    for name, p in PHONES.items():
        save(phone_adapter(**p), here / f"telefon_adapter_{name}.stl")
    if coupling == "balls":
        save(test_ring(), here / "test_ring.stl")
        save(test_adapter(), here / "test_adapter.stl")
        print(f"pause til magneter: før laget ved z = {pause_z:.2f} mm (adapteren, {lobe_t:.1f} mm tyk)")
