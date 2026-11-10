# Kestrel – magnetisk digiscoping-adapter

To dele: en **okular-ring** bliver siddende på scopet,
og en **telefon-adapter** sidder på telefonens MagSafe og klikker magnetisk på ringen.
Alle ringe og adaptere har samme magnetmønster og centreringskant, så **enhver adapter passer på enhver ring**.

| Fil | Til | Kilde til målene |
|---|---|---|
| `okular_ring_ATX.stl` | Swarovski ATX/STX | Swarovskis AR-S-adapterring er lavet til øjemusling Ø59 mm (ATX/STX). Ringen har indv. Ø59,7 |
| `okular_ring_DiamondbackHD85.stl` | Vortex Diamondback HD 20-60x85 | Vortex' spec: øjestykke 2,103" = 53,4 mm |
| `telefon_adapter_OP13.stl` | OnePlus 13 i magnetcover | Målt på officielt foto + magnetcover: 68,4 mm fra MagSafe til hovedkamera |
| `telefon_adapter_iPhone15.stl` | iPhone 15 (uden cover) | Apples målskitse: 49,24 mm fra MagSafe til hovedkamera |
| `digiscope.py` | Parametrisk kilde. Tilføj et scope/en telefon i `SCOPES`/`PHONES` og kør igen | |
| `preview.png` | Billede af delene | |
| `METODE.md` | **Læs før en ny telefon/et nyt scope:** regler for mål, kilder og validering | |

## Indkøb (6×3 mm N52 rundmagneter)
- 8 pr. okular-ring
- 20 pr. telefon-adapter (8 mod ringen + 12 i MagSafe-puden)
- Alle 4 dele: 56 stk. Køb 60.
- Sekundlim (CA) eller 2-komponent epoxy. Filt/flock-tape, hvis en ring sidder løst.

## Print
**Færdigt til Prusa MINI+ (Input Shaper) i PETG:** mappen `print/`
- `PETG_ATX_OnePlus13.3mf` / `PETG_Diamondback_iPhone15.3mf`: PrusaSlicer-projekter med begge dele på pladen og alle indstillinger.
- `.bgcode`: klar til at kopiere på USB-stikket (ca. 3 t 20 min og 60 g pr. plade).
- `digiscope_PETG_MINI.ini`: indstillingerne alene.
- Byg det hele igen efter ændringer: `./build_print.sh /sti/til/python`

Indstillinger: din MINI-IS-profil + `0.20mm STRUCTURAL @MINIIS`, din PETG-profil (245/90 °C),
4 perimetre, 6/5 top/bund, 30 % gyroid, søm bagved, ingen support.
- PETG eller ASA (PLA bliver blødt i en varm bil). Der skal ingen support til.
- **Ring:** åbningen nedad på pladen (magnetlommerne opad).
- **Adapter:** magnetsiden nedad på pladen (MagSafe-puden opad).

## Samling: få magneterne til at vende rigtigt
1. **Ringene:** Lim alle 8 magneter i med **samme side opad** (tag dem fra én stak). Gør det ens i alle ringe.
2. **Adapterens scope-side:** Sæt en ny magnet oven på hver ringmagnet (de klikker fast) og læg plastfolie over.
   Kom lim i adapterens 8 lommer og pres adapteren ned over dem. Så sidder polariteten automatisk rigtigt.
3. **MagSafe-puden (12 magneter):** Læg en løs magnet på telefonens/coverets MagSafe-ring, så den suger sig fast,
   og mærk siden *væk fra telefonen*. Tjek et par steder rundt på ringen. Lim de 12 i med den mærkede side
   **nedad i lommen**. Hurtigst: stil puden på telefonen med plastfolie imellem, så sætter magneterne sig selv.
   - iPhone 15: Apple anbefaler ingen metal direkte på telefonen. Sæt et stykke tape over magneterne.

## Brug
Sæt adapteren på MagSafe, og drej den, til linsehullet sidder over hovedkameraet:
- **iPhone 15:** det nederste af de to objektiver (diagonalt nederst til højre set bagfra). Det øverste er ultrawide.
- **OnePlus 13:** adapteren har en krave, der går ned omkring den runde kamera-ø. Den kan kun sidde én vej, og så sidder hullet over hovedkameraet (øverste venstre objektiv set bagfra). Brug et magnetcover, hvor øen stikker op over coveret, fx OnePlus 13 Sandstone Magnetic Case.

Klik så adapteren på ringen. Kanten centrerer, magneterne holder. Drej ringen på øjestykket, så telefonen står vandret.
Juster afstanden med øjenmuslingen (skru op/ned), til vignetteringen forsvinder.

## Mål der bør tjekkes (i `digiscope.py`)
| Parameter | Hvor | Standard | Hvad |
|---|---|---|---|
| `eyepiece_d` / `fit` | `SCOPES["ATX"]` | 59,0 / 0,7 | Øjemuslingens diameter og luft. Sidder den løst: filt/isoleringstape indeni |
| `bump_h` | `PHONES["OP13"]` | 3,5 | Hvor højt kamera-øen (inkl. linseringe) stikker op over coverets bagside |
| `island_d` | `PHONES["OP13"]` | 49,8 | Diameter på den runde kamera-ø. Adapterens krave går ned omkring den og låser vinklen |
| `bump_h` | `PHONES["iPhone15"]` | 3,6 | Uden cover: linseringenes højde over bagglasset. **Med MagSafe-cover:** højden af coverets kamerakant over coverets bagside (typisk 2,5–3) |
| `fit_clear` | fælles | 0,4 | Gør den større, hvis en ring er for stram |

Kør igen: `python digiscope.py` (kræver `pip install manifold3d trimesh numpy`).
