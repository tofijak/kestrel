<div align="center">

<img src="docs/img/hero.png" alt="Kestrel: OnePlus 13 adapter, ATX ring and eyepiece in an exploded view" width="100%">

# Kestrel

**Snap-on magnetic digiscoping. Any scope, any phone, one click.**

A ring lives on your spotting scope's eyepiece. An adapter lives on your phone's MagSafe.<br>
Bring them together and 8 neodymium magnets in the adapter pull on steel discs in the ring, and the camera lands dead-centre on the eyepiece.

![3D printed](https://img.shields.io/badge/3D%20printed-PLA%20%7C%20PETG-c8642b?style=flat-square) ![Supports](https://img.shields.io/badge/supports-none-5d7387?style=flat-square) ![Printer](https://img.shields.io/badge/tested%20on-Prusa%20MINI%2B-5d7387?style=flat-square) ![Magnets](https://img.shields.io/badge/magnets-6%C3%973%20mm%20N52-c8642b?style=flat-square) ![Status](https://img.shields.io/badge/status-prototype-34373c?style=flat-square)

</div>

---

<table>
<tr>
<td width="55%"><img src="docs/img/turntable.gif" alt="Exploded stack spinning"></td>
<td>

### Why

Clamp adapters take a minute to line up, and you lose the bird while you do it. Kestrel splits the job in two:

- 🔭 **Ring** stays on the scope all day
- 📱 **Adapter** stays on the phone
- 🧲 **Click.** A centring lip drops into a groove and the magnets do the rest

Every ring fits every adapter, so one phone works on all your scopes, and one scope takes everyone's phone.

</td>
</tr>
</table>

## How it works

```mermaid
flowchart LR
    E[Eyepiece] -- slides over --> R[Ring<br/>8 × steel discs + centring lip]
    R <-- "🧲 magnets on steel + lip in groove" --> A[Phone adapter<br/>8 + 12 magnets]
    A -- MagSafe --> P[Phone / magnetic case]
```

<img src="docs/img/cutaway.png" alt="Cutaway through eyepiece, ring and adapter" width="100%">

<sub>Section through the ATX eyepiece, the ring and the adapter, clicked together. The adapter's magnets pull on thin steel discs in the ring; the lip on the ring sits in the peaked groove of the adapter, which takes out any sideways play. The 45° cone over the camera keeps the light path open and prints without supports.</sub>

| | |
|---|---|
| **Self-centring** | 2 mm lip on the ring, peaked groove in the adapter. A 0.5 mm offset is enough to collide, so it can only sit centred. |
| **Rotation lock** | On the OnePlus 13 a collar drops around the round camera island, so the hole can only land on the main camera. |
| **Universal interface** | Magnet circle Ø64.6 mm, ring OD 74 mm, lip Ø52–56 mm. Same on every part. |
| **Steel in the ring** | The ring holds plain steel discs and the magnets live in the adapter. No magnets on your optics, and about 2 mT at the phone camera instead of 3.6 mT with magnets on both sides. |
| **Support-free** | No flat ceilings on any bed face: peaked grooves and 45° cones only. |

## The parts

<table>
<tr>
<td align="center" width="50%"><img src="docs/img/ring_ATX.png" alt="ATX ring"><br><b>Ring: Swarovski ATX / STX</b><br><sub>Bore Ø59.7 for the Ø59 eyecup</sub></td>
<td align="center" width="50%"><img src="docs/img/ring_DiamondbackHD85.png" alt="Diamondback ring"><br><b>Ring: Vortex Diamondback HD 85</b><br><sub>Bore for the Ø53.4 eyepiece</sub></td>
</tr>
<tr>
<td align="center"><img src="docs/img/adapter_OP13_scope_side.png" alt="Adapter scope side"><br><b>Adapter, scope side</b><br><sub>8 magnets, centring groove, 45° light cone</sub></td>
<td align="center"><img src="docs/img/adapter_OP13_phone_side.png" alt="Adapter phone side"><br><b>Adapter, phone side</b><br><sub>12-magnet MagSafe pad + collar for the camera island</sub></td>
</tr>
<tr>
<td align="center"><img src="docs/img/oneplus13.png" alt="OnePlus 13 model"><br><b>OnePlus 13 reference model</b><br><sub>Built from official dimensions + photo measurements</sub></td>
<td align="center"><img src="docs/img/on_phone_OP13.png" alt="Adapter on the OnePlus 13"><br><b>Adapter on the phone</b><br><sub>Hole on the main (top-left) camera, pad on MagSafe</sub></td>
</tr>
</table>

<img src="docs/img/kit.png" alt="All parts" width="100%">

## Supported gear

| | Model | Key dimension | Source | STL |
|---|---|---|---|---|
| 🔭 | Swarovski ATX / STX | Eyecup Ø59 mm | Swarovski AR-S ring spec, Outdoorsmans 59 mm ring | [`okular_ring_ATX.stl`](okular_ring_ATX.stl) |
| 🔭 | Vortex Diamondback HD 20-60×85 | Eyepiece Ø53.42 mm | Vortex spec (2.103 in) | [`okular_ring_DiamondbackHD85.stl`](okular_ring_DiamondbackHD85.stl) |
| 📱 | OnePlus 13 + Sandstone Magnetic Case | MagSafe → main camera 68.4 mm | Official specs + photo; MagSafe centre measured on a Bizon magnetic case (Sandstone not yet confirmed) | [`telefon_adapter_OP13.stl`](telefon_adapter_OP13.stl) |
| 📱 | iPhone 15 | MagSafe → main camera 49.24 mm | Apple dimensional drawing | [`telefon_adapter_iPhone15.stl`](telefon_adapter_iPhone15.stl) |

> [!TIP]
> Click an STL above. GitHub shows it in an interactive 3D viewer.

## Build one

### 1. Buy

| Item | Qty |
|---|---|
| 6 × 3 mm N52 round magnets, axially magnetised | 20 per adapter (8 scope side + 12 MagSafe) |
| Ø6 × 3 mm steel dowel pins (GB119 M6×3, bearing steel), e.g. [AliExpress 1005005710466043](https://www.aliexpress.com/item/1005005710466043.html) | 8 per ring (50 pcs ≈ 21 kr). Any magnetic steel works, **not stainless 304**. Measure yours and set `disc_d` / `disc_t` in `digiscope.py` before printing |
| Superglue (CA) or 2-part epoxy | a few drops |
| Felt / flock tape | optional, if a ring sits loose |

### 2. Print

Ready-to-print files for a **Prusa MINI+ (Input Shaper)** are in [`print/`](print/):

| File | Contents | Time | Filament |
|---|---|---|---|
| `PLA_ATX_OnePlus13.bgcode` | ATX ring + OnePlus 13 adapter | 4 h 01 min | 63 g |
| `PLA_Diamondback_iPhone15.bgcode` | Diamondback ring + iPhone 15 adapter | 3 h 51 min | 59 g |
| `PLA_kun_ring_ATX.bgcode` | ATX ring only | 1 h 30 min | 24 g |
| `PETG_*.bgcode` | Same plates in PETG | ~ +6 min | ~ +1 g |

The `.3mf` next to each is the PrusaSlicer project with every setting embedded.

<details>
<summary><b>Print settings</b></summary>

| Setting | Value | Why |
|---|---|---|
| Profile | `0.20mm STRUCTURAL @MINIIS` | |
| Walls / top / bottom | 4 / 6 / 5 | stiff, magnets never print through |
| Infill | 30 % gyroid | |
| Supports | none | geometry is designed for it |
| Seam | rear + **scarf seam** | no vertical zipper line on the round walls |
| Avoid crossing perimeters | on | no strings or blobs over the magnet pockets |
| Retraction | 3.2 mm @ 35 mm/s + wipe | Prusa's MINI bowden default |
| Ironing | topmost layer | smooth MagSafe pad, +25 min (all top surfaces: +1 h 45) |
| PLA / PETG | 195 °C / 245 °C | |

**Orientation:** rings opening-down, adapters scope-side down (MagSafe pad up). The plates are already laid out this way.

PLA softens in a hot car. Use PETG or ASA if it lives in the glovebox.

If you see hair-thin strings, dry the filament (PLA 45–50 °C for 4–6 h).

</details>

### 3. Glue magnets and steel discs

1. **Rings:** glue a steel pin into each of the 8 pockets, flush or just below the surface. Steel has no polarity, so either end up. Check with a magnet first that the pins are magnetic.
2. **Adapter, scope side:** glue the 8 magnets in, flush or just below the surface. They pull on steel, so polarity doesn't matter here.
3. **MagSafe pad (12 magnets):** let a loose magnet snap onto the phone's MagSafe ring and mark the side facing *away* from the phone. Glue all 12 with the marked side **down in the pocket**. Quickest: stand the pad on the phone with cling film between and the magnets set themselves.

> [!NOTE]
> iPhone 15 without a case: Apple advises against bare metal on the back glass. Put a strip of tape over the magnets.

### 4. Use

1. Put the adapter on the phone. It snaps to MagSafe; on the OnePlus 13 the collar locks it around the camera island.
2. Slide the ring onto the eyepiece and turn it so the phone hangs level.
3. Click the phone on. Twist the eyecup up or down until the vignetting disappears.

## Add your own scope or phone

Everything is generated by [`digiscope.py`](digiscope.py). Add one line and run it:

```python
SCOPES = {
    "ATX": dict(eyepiece_d=59.0, fit=0.7),
    "MyScope": dict(eyepiece_d=56.0),               # eyecup diameter in mm
}
PHONES = {
    "MyPhone": dict(lens_to_magsafe=52.0,           # MagSafe centre -> main camera
                    bump_h=3.0, lens_hole_d=14.0),  # camera bump height, hole size
}
```

```bash
pip install manifold3d trimesh numpy
python digiscope.py                                # STLs
./build_print.sh "$(which python)" PLA             # PrusaSlicer projects + G-code
python tools/render.py                             # README images (needs pyvista)
```

> [!IMPORTANT]
> Read [`METODE.md`](METODE.md) (Danish) first. It's the checklist we wrote after the first prints: where dimensions must come from, how to confirm which lens is the main camera, and the fit checks every part has to pass before it gets printed.

## What gets checked before printing

- **Ring on eyepiece:** zero overlap at nominal size *and* with the hole printed 0.3 mm undersize
- **Adapter on ring:** every ring × every adapter has zero overlap; a 0.5 mm offset must collide
- **Steel discs:** the discs fit the ring's pockets, with at least 0.8 mm wall to the lip, chamfer and edge
- **Adapter on phone:** physical 180° flip (never a mirror), hole within 0.5 mm of the main camera, collar clears the island
- **Slicer:** no support, no bridging or floating warnings

## Repository

```
digiscope.py        parametric generator: rings + adapters
oneplus13_model.py  OnePlus 13 reference model + fit check
build_print.sh      PrusaSlicer projects and G-code for the Prusa MINI
make_plate.py       lays parts out on the bed
tools/render.py     renders everything in docs/img
METODE.md           measurement and validation rules
print/              ready-to-print .3mf / .bgcode
```

## Roadmap

- [ ] Physical fit test of the new Ø59.7 ATX ring
- [ ] Measure holding force, magnet on steel pin (not measured yet; magnet-on-steel is weaker than magnet-on-magnet)
- [ ] Confirm the MagSafe centre on the Sandstone case with a MagSafe puck
- [ ] Quick test-ring print (5 min) for unverified eyepiece sizes
- [ ] More phones and scopes
- [ ] English version of `METODE.md`

---

<div align="center"><sub>Named after the kestrel: hovers dead still, spots everything.</sub></div>
