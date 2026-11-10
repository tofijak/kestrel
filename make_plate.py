"""Lægger flere STL'er side om side på Prusa MINI-pladen (180x180) i én 3MF-fil med separate objekter.

Brug:  python make_plate.py ud.3mf del1.stl del2.stl ...
"""
import sys
import zipfile

import numpy as np
import trimesh

BED = 180.0
GAP = 10.0


def model_xml(meshes):
    objs, items = [], []
    widths = [m.bounds[1][0] - m.bounds[0][0] for m in meshes]
    x = (BED - (sum(widths) + GAP * (len(meshes) - 1))) / 2
    for i, (m, w) in enumerate(zip(meshes, widths), start=1):
        b = m.bounds
        tx = x - b[0][0]
        ty = BED / 2 - (b[0][1] + b[1][1]) / 2
        tz = -b[0][2]
        x += w + GAP
        v = "".join(f'<vertex x="{p[0]:.5f}" y="{p[1]:.5f}" z="{p[2]:.5f}"/>' for p in m.vertices)
        t = "".join(f'<triangle v1="{f[0]}" v2="{f[1]}" v3="{f[2]}"/>' for f in m.faces)
        objs.append(f'<object id="{i}" name="{m.metadata["name"]}" type="model"><mesh>'
                    f'<vertices>{v}</vertices><triangles>{t}</triangles></mesh></object>')
        items.append(f'<item objectid="{i}" transform="1 0 0 0 1 0 0 0 1 {tx:.4f} {ty:.4f} {tz:.4f}"/>')
    assert x - GAP <= BED, "delene kan ikke være på pladen"
    return ('<?xml version="1.0" encoding="UTF-8"?>'
            '<model unit="millimeter" xml:lang="en-US" '
            'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
            f'<resources>{"".join(objs)}</resources><build>{"".join(items)}</build></model>')


def main(out, paths):
    meshes = []
    for p in paths:
        m = trimesh.load(p)
        m.metadata["name"] = p.rsplit("/", 1)[-1].removesuffix(".stl") if hasattr(str, "removesuffix") \
            else p.rsplit("/", 1)[-1].replace(".stl", "")
        meshes.append(m)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/'
                   'package/2006/content-types"><Default Extension="rels" ContentType="application/'
                   'vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" '
                   'ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.'
                   'openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" '
                   'Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
                   '</Relationships>')
        z.writestr("3D/3dmodel.model", model_xml(meshes))
    print(f"{out}: {len(meshes)} objekter")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
