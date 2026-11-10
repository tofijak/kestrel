"""3D-model af OnePlus 13 + samling med telefon-adapteren (til visuelt tjek af pasform).

Kilder til målene (der findes ingen officiel CAD-model af OnePlus 13):
  - Krop 162,9 x 76,5 x 8,5 mm: OnePlus' officielle specifikationer
  - Kamera-ø og linser: målt på OnePlus' officielle bagside-foto (skala 0,197 mm/px)
  - MagSafe-centrum: målt på Bizon CrystalO-magnetcover
  - Hjørneradius, kamera-øens højde og linseringe: skøn (markeret SKØN herunder)

Koordinater: telefonen ligger med skærmen nedad, bagsiden opad (z = 0 .. 8,5).
x mod højre og y opad set bagfra. Origo = øverste venstre hjørne af bagsiden.

Kør:  python oneplus13_model.py
"""
import math
from pathlib import Path

import numpy as np
import trimesh
from manifold3d import Manifold

import digiscope as d

W, H, T = 76.5, 162.9, 8.5
corner_r = 9.0            # SKØN: hjørneradius set bagfra
edge = 1.0                # SKØN: afrunding/fase på kanterne

island_c = (30.6, -34.1)  # kamera-øens centrum
island_d = 49.8
island_h = 3.0            # SKØN: hvor meget kamera-øen står ud fra bagsiden
lenses = {                # linsecentre (fra officielt foto)
    "main": (21.4, -26.0),     # øverst til venstre set bagfra (bekræftet på telefonen)
    "lens_TR": (39.7, -26.0),
    "lens_BL": (21.4, -43.9),
}
flash = (39.7, -43.9)
lens_ring_d, lens_ring_h = 13.0, 0.5   # SKØN: linseringe står lidt op over øen
lens_glass_d = 9.0

magsafe_c = (38.0, -92.4)  # MagSafe-centrum i magnetcover

SEG = 120


def cyl(h, r, seg=SEG):
    return Manifold.cylinder(h, r, r, seg)


def phone():
    corners = [(corner_r, -corner_r), (W - corner_r, -corner_r),
               (corner_r, -H + corner_r), (W - corner_r, -H + corner_r)]
    parts = []
    for (x, y) in corners:
        parts.append(cyl(T - 2 * edge, corner_r).translate((x, y, edge)))
        parts.append(cyl(T, corner_r - edge).translate((x, y, 0)))
    body = Manifold.batch_hull(parts)

    ix, iy = island_c
    island = cyl(island_h + 0.01, island_d / 2).translate((ix, iy, T - 0.01))
    top = T + island_h
    for (x, y) in lenses.values():
        ring = cyl(lens_ring_h + 0.01, lens_ring_d / 2).translate((x, y, top - 0.01))
        island = island + ring
        island = island - cyl(1.0, lens_glass_d / 2).translate((x, y, top + lens_ring_h - 0.6))
    island = island - cyl(0.4, 2.5).translate((flash[0], flash[1], top - 0.3))
    return body, island


def placed_adapter():
    """Adapteren vendt med telefon-siden nedad, MagSafe-puden på bagsiden, hul over hovedkameraet."""
    p = d.PHONES["OP13"]
    a = d.phone_adapter(**p)
    # Fysisk vending: 180° om Y-aksen (IKKE spejling — en printet del kan ikke spejles)
    a = a.rotate((0, 180, 0))                    # telefon-siden nedad
    pad_face = d.lobe_t + p["bump_h"]
    a = a.translate((0, 0, pad_face + T))        # puden hviler på bagsiden
    mx, my = magsafe_c
    lx, ly = lenses["main"]
    # i adapteren peger (linse - MagSafe) langs -Y; drej så den peger mod hovedkameraet
    ang = math.degrees(math.atan2(ly - my, lx - mx)) - (-90)
    a = a.rotate((0, 0, ang)).translate((lx, ly, 0))
    return a


def to_trimesh(m, color):
    mesh = m.to_mesh()
    tm = trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts))
    mat = trimesh.visual.material.PBRMaterial(baseColorFactor=color, metallicFactor=0.1,
                                              roughnessFactor=0.6)
    tm.visual = trimesh.visual.TextureVisuals(material=mat)
    return tm


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    body, island = phone()
    ph = body + island
    ad = placed_adapter()

    lx, ly = lenses["main"]
    mx, my = magsafe_c
    print(f"Afstand MagSafe -> hovedkamera: {math.dist((lx, ly), (mx, my)):.2f} mm")
    ci = (island_d + d.island_fit) / 2
    print(f"Krave omkring kamera-ø: indv. Ø{2 * ci:.1f} mm, luft {ci - island_d / 2:.2f} mm pr. side, "
          f"høj {d.PHONES['OP13']['bump_h'] - d.collar_gap:.1f} mm")
    overlap = (ph ^ ad).volume()
    print(f"Overlap telefon/adapter: {overlap:.3f} mm3")
    gap = (d.lobe_t + d.PHONES['OP13']['bump_h']) - (d.lobe_t + island_h + lens_ring_h)
    print(f"Luft mellem linse-del og linseringe: {gap:.2f} mm (uden cover)")

    phone_tm = trimesh.util.concatenate([to_trimesh(body, [40, 40, 45, 255]),
                                         to_trimesh(island, [20, 20, 22, 255])])
    adapter_tm = to_trimesh(ad, [230, 120, 30, 255])
    to_trimesh(ph, [40, 40, 45, 255]).export(here / "oneplus13_model.stl")
    to_trimesh(ph + ad, [200, 200, 200, 255]).export(here / "samling_OP13_adapter.stl")
    trimesh.Scene({"OnePlus 13": phone_tm, "Adapter": adapter_tm}).export(here / "samling_OP13_adapter.glb")
    print("Skrev oneplus13_model.stl, samling_OP13_adapter.stl, samling_OP13_adapter.glb")
