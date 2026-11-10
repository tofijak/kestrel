# Metode: sådan måler og validerer vi en ny telefon eller et nyt scope

Skrevet efter tre fejl i første version. Følg listen, før der printes noget.

## Fejl vi har lavet (og hvorfor)
| Fejl | Årsag | Regel der forhindrer den |
|---|---|---|
| ATX-ringen kunne ikke komme ned over okularet (57,9 mm hul, øjemusling 59 mm) | Diameteren blev **gættet** ud fra "Outdoorsmans' 59 mm-ring passer med filt" | Regel 1 og 6 |
| Hullet ramte blitzen på OnePlus 13 | (a) Hovedkameraet blev antaget at være nederst til venstre. Det er **øverst til venstre** set bagfra. (b) Adapteren blev tjekket med en **spejling** i stedet for en vending | Regel 2 og 4 |
| Det var ikke sagt, hvilket cover designet byggede på | Coveret bestemmer MagSafe-ringens placering og hvor meget kamera-øen stikker op | Regel 3 |

## Regler

### 1. Mål på scopet: brug producentens eget tilbehør først
Rækkefølge for kilder til øjestykkets/øjenmuslingens diameter:
1. Producentens spec eller **producentens eget tilbehør** til netop det okular. Eksempel: Swarovski AR-S-ringen er lavet til "eyecups Ø 59 mm" (ATX/STX).
2. Dedikerede adapterproducenters størrelsesskemaer (Phone Skope, Outdoorsmans Digidapter, Vortex-spec "Eyepiece Diameter").
3. Brugerens skydelære.

**Aldrig** udled en diameter ved at trække "filt" eller "løs pasform" fra en tredjeparts ring. Find ingen kilde 1–2, så **spørg om en skydelæremåling, før der printes**.

### 2. Hovedkameraet: bekræft hvilken linse det er
- Find den på et mærket foto eller teardown fra producenten, ikke ud fra "det plejer at sidde der".
- Er der tvivl, så bed brugeren om denne test: kameraet på 1×, dæk én linse ad gangen med en finger. Den linse, der gør billedet sort, er hovedkameraet.
- Skriv i `PHONES`-kommentaren, hvilken linse det er, set **bagfra**, og hvordan det er bekræftet.

### 3. Coveret er en del af målet
- Skriv altid, hvilket cover designet er lavet til (navn og model), i `PHONES` og i svaret til brugeren.
- MagSafe-ringen i et cover sidder centreret over opladerspolen. Tjek den med en MagSafe-puck: læg den på coveret, så den suger sig fast, og mål fra coverets topkant til puckens centrum.
- Mål, hvor meget kamera-øen stikker op over coverets bagside (`bump_h`). Det bestemmer kraven.

### 4. Koordinater og vending (chiralitet)
- Telefonmål noteres **set bagfra**, origo i øverste venstre hjørne, y negativ nedad.
- Adapteren printes med scope-siden nedad og **vendes 180° om Y**, når den sættes på telefonen. Derfor spejles x i `to_adapter_frame`.
- I samlingstjek: brug `rotate((0, 180, 0))`, **aldrig** `mirror`. En spejling skjuler netop den fejl, vi skal fange. En printet del kan ikke spejles.

### 5. Marker hver værdi med kilde og sikkerhed
- Hver dimension i `SCOPES`/`PHONES` får en kommentar: kilde (link/dokument) eller `SKØN`.
- Alle `SKØN`-værdier, der påvirker pasform, nævnes for brugeren **før** print.

### 6. Validering før print (skal køre og bestå)
1. **Ring på okular:** overlap = 0 for øjenmuslingens diameter, både nominelt og med hullet printet 0,3 mm for småt (PLA/PETG printer huller ca. 0,2–0,3 mm for små). Luft: 0,6–0,8 mm på diameteren.
2. **Adapter på ring:** overlap = 0 for alle kombinationer af ring og adapter, og en forskydning på 0,5 mm skal kollidere (negativ kontrol, beviser at kanten centrerer).
   Stålskiverne i adapteren passer i lommerne med mindst 0,8 mm væg til rille, kegle og kant. Skivens mål (`disc_d`, `disc_t`) er SKØN, indtil skiverne er købt og målt med skydelære.
3. **Adapter på telefon** (fysisk vending, regel 4): hullets centrum ligger på hovedkameraet (afstand < 0,5 mm), MagSafe-puden er centreret over MagSafe-ringen, og kraven går fri af øen (overlap = 0 ved +0,3 mm, kollision ved +0,6 mm).
4. **Slicer:** PrusaSlicer uden support og uden advarsler om bridging/floating. Ingen flade lofter på den side, der vender mod pladen: brug 45°-kegler og spidse riller.
   Overflade (lært af første print: lodret søm, tråde over magnetlommerne, knopper på puden):
   skrå søm (`scarf_seam_placement = everywhere`), `avoid_crossing_perimeters`, retraktion 3,2 mm + wipe på MINI'ens bowden,
   ironing kun `topmost` (hele toppen koster +1 t 45, øverste lag kun +25 min). Ligger i `build_print.sh`.
   Tråde der ligner hår: tør filamentet (PLA 45–50 °C i 4–6 t).
5. **Usikker diameter?** Print først en tynd testring (3–5 mm høj, ca. 10 min), før hele delen.

### 7. Svaret til brugeren
- Sig, hvad der er verificeret i CAD, og hvad der ikke er afprøvet fysisk.
- Angiv kilder med links.
