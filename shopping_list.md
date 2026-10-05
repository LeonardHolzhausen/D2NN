# D²NN shopping list

Everything needed to go from an empty room to a working bench, sized for the current plan: 16×16 regions at 100–150 µm pitch, two-level photoresist layers, up to three layers, camera readout. Prices are approximate.

**Status:** change `open` to `bought`, `at home` or `DIY`.
**(special)** means the wrong product quietly breaks the experiment.

---

## 1. Room and furniture

| Status | Item | Why / requirement | Rough cost |
|---|---|---|---|
| open | Sturdy table, at least 150 × 75 cm | Light path with 3 layers at 100 µm pitch is about 1.2–1.3 m. Must not wobble. A heavy used wooden table is fine. | €80–200 |
| open | Bench board, ~150 × 40 cm, 3–4 cm thick (plywood or film-faced) | Rigid base for the optics, separate from the table surface | €30–60 |
| open | 4–6 squash balls or partly inflated bicycle inner tubes | Under the board to damp vibration from footsteps | €10–20 |
| open | Chair | — | €0–50 |
| open | Blackout curtain or blinds | Room light swamps the camera signal | €20–40 |
| open | **(special)** Yellow safelight bulb or amber filter | Photoresist is UV/blue sensitive. Ordinary white LED light slowly exposes it. | €10–20 |
| open | Normal desk lamp | Working light when no resist is open | €15 |
| open | 2 switchable power strips | One only for the laser, so it can be cut instantly | €15 |
| open | Shelf or storage boxes | Keep optics dust-free and chemicals apart | €20 |

## 2. Safety

| Status | Item | Why / requirement | Suggested product | Rough cost |
|---|---|---|---|---|
| open | **(special)** Laser goggles, EN 207, covering 532 nm **and** 1064 nm | Cheap green DPSS lasers are pumped by an 808 nm diode; weak modules can leak invisible infrared | Picotronic, rated 316–532 nm DIR LB5+M LB5 and 900–1080 nm DIR LB5 (also sold via Laserfuchs). Alternative: GMT DBY 532/1064. | ~€80–150 |
| open | Chemical splash goggles | Separate from the laser goggles. For developer and solvents. | any | €10 |
| open | Nitrile gloves, lab coat or apron | Resist, acetone, NaOH | any | €25 |
| open | Small fire extinguisher (foam or CO₂) | Acetone and IPA are flammable | any | €25–40 |
| open | Laser warning sign for the door | Keeps others from walking into a live beam | any | €5 |
| open | First aid kit, eye wash bottle | Chemical splash to the eyes | any | €15–20 |

> Don't buy goggles rated only up to 532 nm. Example: Picotronic PICO-LPG-405-532 covers only 315–532 nm (DIRM LB6), with no infrared protection.

## 3. Laser and power

Buy two lasers if the budget allows: coherence varies between individual cheap modules, and the Michelson test (section 6) decides which one you keep.

| Status | Item | Why / requirement | Suggested product | Rough cost |
|---|---|---|---|---|
| open | **(special)** Laser A: 532 nm, ≤ 1 mW, Class 2 | Safest option, plenty of light for a camera | **Recommended:** [Picotronic DD532-1-3(12x45), 1 mW, Class 2, TEM00, 3 V](https://shop.picotronic.de/en/p/70154023) (German shop, in stock, 1–2 days). IR filter not stated in the datasheet, so run the IR test anyway. | €122.90 |
| open | **(special)** Laser B: 532 nm, ≤ 1 mW, with IR filter | Second candidate for the coherence test | [Roithner CW532-001](http://www.roithner-laser.com/laser_modules_dot_532.html): < 1 mW, TEM00, APC, **IR filter confirmed** in the [datasheet](http://www.roithner-laser.com/datasheets/laser/laser_modules/cw532-001.pdf). Vienna, ships to Germany, MOQ 1. No public price: request a quote via their [order form](https://roithner-laser.com/orders.php) or sales@roithner-laser.com. | ask |
| open | **(special)** Linear bench power supply, 0–30 V / 0–5 A, **with output on/off** | Runs the lasers at 3 V (set 3.0 V and 0.35 A current limit *before* connecting) and the spin coater motor. Output switch avoids power-on spikes; memory slots M1–M5 for laser / spin coater settings; OVP/OCP. | [Korad KA3005D – fixshop-online.de](https://www.fixshop-online.de/werkzeuge-stromversorgungen-und-ladestationen/korad-ka3005d-geregeltes-dc-netzteil-0-30v-0-5a/). Cheaper without output switch: [Korad KD3005D – eleshop.de](https://eleshop.de/korad-kd3005d-netzgerat.html) (€73.76). | €96.73 |
| open | Test leads, 4 mm banana plug to crocodile clip, red + black | Supply binding posts → laser. Clip onto the tinned laser wire ends (26 AWG, too thin to clamp reliably in the binding posts). | [McPower 80 cm red/black – BerryBase](https://www.berrybase.de/messleitungen-4mm-stecker-krokodilklemme-80cm-rot-schwarz) | €1.90 |
| open | DC coupler 5.5 × 2.1 mm female → 2-pin screw terminal | Only for the Roithner laser (it has a barrel plug, not bare wires). Plug in, clip the test leads onto the screws. | [goobay DC coupler – BerryBase](https://www.berrybase.de/dc-kupplung-fuer-hohlstecker-5-5x2-1mm-schraubmontage-terminal-block-2-pin) | €0.50 |
| open | Battery holder 2 × AA with cable | Quick alignment sessions without the bench supply (fresh alkaline ≈ 3.1–3.2 V, safe). **Never NiMH or lithium.** | [2 × AA, 150 mm cable – BerryBase](https://www.berrybase.de/batteriehalter-fuer-2x-mignon-aa-1-1-mit-150mm-anschlusskabel) | €0.27 |
| open | Cable tie / tape as strain relief | Fixes the thin laser cable to the holder so a tug doesn't break the solder joints | at home | €0 |
| open | **(special)** Digital multimeter | Check 3.0 V before the laser is connected, find + and − on the laser wires, spin coater motor. The temperature probe also cross-checks the hotplate (IR thermometers read wrong on shiny aluminium). | [UNI-T UT131C – BerryBase](https://www.berrybase.de/uni-t-ut131c-digitales-multimeter-palm-size-mit-temperaturmessung) | €13.90 |
| open | Laser holder with a small heatsink | DPSS output drifts with temperature (modules are specified for 15–30 °C) | Roithner holder, or an aluminium V-clamp | €15–30 |

> First connection: output off → set 3.0 V / 0.35 A → check with multimeter → connect + to +, − to − → goggles on → output on.

> Note: in Roithner part numbers, **F means focusable, not filter**. The CW532-005 (< 5 mW) is Class 3R; the CW532-001 stays in Class 2.

## 4. Bench mechanics

| Status | Item | Why / requirement | Suggested product | Rough cost |
|---|---|---|---|---|
| open | Rail, about 1.5 m | Keeps every component on one straight line | Cheap: 2040 aluminium V-slot profile plus M6 T-nuts. Proper: OptoSigma rail, 1 m at €133.20, plus carriers. | €25–30 (cheap) / €200+ (proper) |
| open | 8–10 post holders and posts, metric | Hold every component at the same beam height | Generic metric posts (AliExpress/eBay) | €80–120 |
| open | **(special)** 4 XY-adjustable slide holders | Input mask plus up to 3 layers. Must allow sideways adjustment of a fraction of a millimetre. | "XY translating lens/plate mount, 1 inch" | €30–60 each |
| open | 3–4 kinematic mounts, 1 inch | Mirrors for the Michelson test, laser pointing | Generic kinematic mirror mounts | €15–30 each |
| open | 3 fixed 1-inch lens holders | Beam expander lenses | generic | €10 each |
| open | Screw assortment (M4/M6), metric Allen keys | — | any | €15 |

## 5. Beam preparation

| Status | Item | Why / requirement | Suggested product | Rough cost |
|---|---|---|---|---|
| open | Short focal lens, f ≈ 10–20 mm, or 10×/20× microscope objective | First lens of the beam expander. The raw beam (~1–2.5 mm) is smaller than the pattern (1.6–2.4 mm) and uneven. | Cheap objectives from eBay | €15–30 |
| open | Plano-convex lens, Ø25 mm, f ≈ 100–150 mm | Second lens: wide, parallel beam, so the pattern sits in its even centre | any | €20–40 |
| open | **(special)** Pinhole, 15–25 µm, at the focus between the lenses | Cleans the beam profile. Can be added later. | Edmund 15 µm mounted pinhole ($95.50) in a cheap XY mount. A full Thorlabs spatial filter costs €598.70, hence DIY. | €90–130 |
| open | 2 iris diaphragms | Standard tool for aligning a beam along the rail | generic | €15 each |
| open | Linear polarizer in a rotating mount | Dims the beam smoothly before the camera (DPSS light is polarized) | polarizer film or glass polarizer | €15–30 |
| open | Black card, black aluminium foil | Beam blocks, stray-light shields | any | €10 |

## 6. Coherence test (Michelson)

| Status | Item | Why | Rough cost |
|---|---|---|---|
| open | 50/50 non-polarizing beamsplitter cube, 25 mm | Splits and recombines the beam | €25–60 |
| open | 2 flat mirrors, Ø25 mm | The two arms | €10–20 each |
| open | Linear stage with micrometer | Lengthens one arm while you watch the fringes fade | €30–60 |
| open | White card screen | Watch the fringes | €0 |

## 7. Camera and inspection

| Status | Item | Why / requirement | Suggested product | Rough cost |
|---|---|---|---|---|
| open | **(special)** Monochrome USB camera, removable lens, small pixels | Colour cameras put filters over the pixels. A ~3.8 × 2.4 mm sensor matches the output pattern size. | Arducam B0332 (OV9281, 1 MP mono, global shutter, 3 µm pixels, UVC driver). RobotShop: $63.12. | ~€60–75 |
| open | USB extension cable, active, 5 m | Keeps the laptop off the bench (the B0332 is USB 2.0) | [Active USB 2.0 repeater 5 m – BerryBase](https://www.berrybase.de/aktive-usb-2.0-verlaengerung-repeater-5m) | €8.40 |
| open | USB microscope | Inspecting 100–150 µm features on masks and layers. Focus distance < 1 cm, so it needs a simple stand or block. | [Elecrow handheld 500×, 2 MP, USB-C – BerryBase](https://www.berrybase.de/elecrow-portable-handheld-mini-digital-microscope-2-mp-500x-vergroesserung-2-0-zoll-ips-led-licht) | €26.90 |
| open | Stage micrometer slide (0.01 mm scale) | Calibrates what "100 µm" looks like in the microscope | any | €10–15 |
| open | Digital caliper, 1 m steel ruler or tape measure | Measuring layer gaps (z) and parts | Caliper: [goobay 150 mm – BerryBase](https://www.berrybase.de/digitale-schieblehre-messschieber-150mm) (€17.90). Ruler/tape: any. | €25 |

> The B0332 is IR-sensitive, one more reason for an IR-filtered laser. Record uncompressed, not MJPG: compression distorts brightness values.

## 8. Fabrication: glass and chemistry

| Status | Item | Why / requirement | Suggested product | Rough cost |
|---|---|---|---|---|
| open | Glass microscope slides, pack of 50 | One per layer, plus many practice slides | any | €5–10 |
| open | Practice resist: Positiv 20 spray | Cheap resist for learning the process | Kontakt Chemie Positiv 20, 200 ml (~€17.95). Most sensitive in near-UV. **Check the expiry date.** | €18–21 |
| open | **(special)** Real resist: thin positive resist, e.g. AZ 1505 | Spins to the ~400–500 nm needed for π phase; well characterized | MicroChemicals (Ulm). Email for the smallest bottle and whether they sell to private buyers. | ask |
| open | Developer | Positiv 20: dilute NaOH (~7 g/L). AZ resists: matching MicroChemicals developer. **Never drain cleaner.** | — | €5–30 |
| open | Isopropanol 99.9% (1 L), acetone (1 L), distilled water (5 L) | Cleaning slides, removing failed coatings | IPA: [teslanol IP 99.5 %, 1 L – BerryBase](https://www.berrybase.de/teslanol-ip-isopropanol-1000ml) (€14.90). Acetone: toom 8500235. Water: supermarket. | €20–25 |
| open | 3 glass beakers, 100 ml measuring cylinder, 0.01 g scale | Mixing developer accurately | any | €30 |
| open | Flat tweezers, wash bottles, droppers, lint-free wipes, air blower | Handling slides without touching the coated side | Tweezers: [4-piece plastic set – BerryBase](https://www.berrybase.de/4-teiliges-kunststoff-pinzetten-set) (€3.55, won't scratch glass). Rest: any. | €25 |
| open | Developing trays, labelled waste bottle | — | any | €10 |

> Some chemical sellers require you to be 18 and show ID.

## 9. Fabrication: equipment

| Status | Item | Why / requirement | Rough cost |
|---|---|---|---|
| open | **(special)** Spin coater, 4,000–5,000 rpm | PC fans are too slow. Common DIY build: brushless RC motor, ESC, servo tester as speed knob, flat chuck with double-sided tape, inside a plastic splash container with lid. | €30–50 |
| open | Optical tachometer | rpm sets resist thickness, so measure it | €15 |
| open | Small hotplate plus IR thermometer | Soft-bake at 110–115 °C. An aluminium plate on top gives even heat. IR thermometer: toom 10469907, or [UNI-T UT300A+ – BerryBase](https://www.berrybase.de/uni-t-ut300a-infrarot-thermometer-20-4000-c) (€14.90). Both read low on shiny aluminium: cross-check with the multimeter's probe or put black tape on the spot. | €30–50 |
| open | UV LED lamp, 365 or 395–405 nm | Exposure through the mask | €15–30 |
| open | Glass plate (e.g. from a picture frame) | Presses the mask flat against the resist | €5 |
| open | Laser-printer transparency film, A4 | For masks. Must say laser-compatible: inkjet film melts in a laser printer. | €10–15 |
| open | Access to a 1200 dpi laser printer | Copy shop if you don't own one | €1–5 per print |

---

## Order batches

### BerryBase (one order, 1–3 days, free shipping from €150)

| Item | Section | Price |
|---|---|---|
| [Test leads, banana → crocodile, red/black](https://www.berrybase.de/messleitungen-4mm-stecker-krokodilklemme-80cm-rot-schwarz) | 3 | €1.90 |
| [DC coupler 5.5 × 2.1 → screw terminal](https://www.berrybase.de/dc-kupplung-fuer-hohlstecker-5-5x2-1mm-schraubmontage-terminal-block-2-pin) (only for Roithner) | 3 | €0.50 |
| [Battery holder 2 × AA](https://www.berrybase.de/batteriehalter-fuer-2x-mignon-aa-1-1-mit-150mm-anschlusskabel) | 3 | €0.27 |
| [Multimeter UNI-T UT131C](https://www.berrybase.de/uni-t-ut131c-digitales-multimeter-palm-size-mit-temperaturmessung) | 3 | €13.90 |
| [Active USB extension 5 m](https://www.berrybase.de/aktive-usb-2.0-verlaengerung-repeater-5m) | 7 | €8.40 |
| [USB microscope Elecrow 500×](https://www.berrybase.de/elecrow-portable-handheld-mini-digital-microscope-2-mp-500x-vergroesserung-2-0-zoll-ips-led-licht) | 7 | €26.90 |
| [Digital caliper goobay 150 mm](https://www.berrybase.de/digitale-schieblehre-messschieber-150mm) | 7 | €17.90 |
| [Isopropanol 99.5 %, 1 L](https://www.berrybase.de/teslanol-ip-isopropanol-1000ml) | 8 | €14.90 |
| [Plastic tweezers, 4 pcs](https://www.berrybase.de/4-teiliges-kunststoff-pinzetten-set) | 8 | €3.55 |
| *Optional:* [IR thermometer UNI-T UT300A+](https://www.berrybase.de/uni-t-ut300a-infrarot-thermometer-20-4000-c) (instead of toom) | 9 | €14.90 |
| **Total** (without / with IR thermometer) | | **≈ €88 / €103** |

**Not available at BerryBase** (checked): Arducam B0332, Korad bench supply, UV LED lamp, brushless motor/ESC/servo tester, optical tachometer, nitrile gloves, air blower, 2040 aluminium profile.

### Other shops
- **Picotronic:** laser (section 3)
- **Roithner:** laser B quote (section 3)
- **fixshop-online.de:** Korad KA3005D (section 3)
- **toom:** aluminium tube, splash goggles, acetone, IR thermometer, Hama supply (see project_state.md)

