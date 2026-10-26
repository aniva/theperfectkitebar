# ThePerfectKiteBar (TPKB)

An open-hardware **DIY kite control bar system** optimized for **kite-foiling**, built for riders who want lightweight performance, parametric customization, and full field serviceability.

Development began in **2023**, driven by the lack of suitable off-the-shelf bars—most commercial options were too expensive, overly complex, unnecessarily heavy, or built around identical generic designs across brands. The first functional version of TPKB was **tested in Spring 2024**, followed by continuous refinements driven by real-world water and snow sessions.

### Design Priorities & Scope
- **Minimal weight** without compromising structural strength
- **Full field-serviceability** and easy spare-part replacement using common hand tools
- **Low-cost, accessible manufacturing** via on-demand 3D printing services (SLS, MJF, SLM) and laser cutting
- **Parametric flexibility** in Shapr3D, allowing adaptation to different carbon tube diameters, rope sizes, bearings, and materials
- **All-climate ergonomics**, featuring glove-friendly operation in freezing conditions (5°C and below) alongside corrosion-resistant reliability in tropical saltwater

---

## License and Project Management

Design files and documentation are shared under [CC BY-NC 4.0](LICENSE.md), which requires attribution and restricts commercial use.

See [Contributing](CONTRIBUTING.md) for the change workflow and local checks, and [Validation Status](docs/validation.md) for recorded testing status and outstanding validation work.

---

## Project Structure & Navigation

Hardware components are organized under `/hardware/`, where the folder hierarchy encodes key design constraints (tube diameter, bearing type, rope diameter, and design variant). Each component directory contains its own `README.md` covering part function, bills of materials, 3D printing specifications, assembly notes, and previews:

- **[Bar](hardware/bar/README.md)** (`/hardware/bar/`) — Main carbon tube tracks (OD 22mm and OD 24mm), bar ends, and center pieces (off-center SLS nylon clamp and inline SLM titanium hub)
- **[Swivel](hardware/swivel/README.md)** (`/hardware/swivel/`) — Ceramic-bearing below-the-bar swivel for untwisting front lines
- **[Quick Release](hardware/quick_release/README.md)** (`/hardware/quick_release/`) — Compact, glove-friendly safety release mechanism
- **[Trim](hardware/trim/README.md)** (`/hardware/trim/`) — Depower trim cleat base, line stoppers, and V-splitters
- **[Tools](hardware/tools/README.md)** (`/hardware/tools/`) — Custom drilling jigs and sewing machine presser feet for assembly

**Rigging & Assembly Guides:**
- **[Rope Splicing & Cutting Dimensions Guide](docs/rope_dimensions.md)** — Line routing physics, splicing formulas, and build procedure
- **[Interactive Splicing & Sizing Calculator](https://raw.githack.com/aniva/theperfectkitebar/main/docs/rope_calculator.html)** — Unified web calculator for sheeting lines, leaders, pigtails, and bungees

---

## Design Philosophy: Variant vs Version

| Term    | Meaning                                                             | How it's handled                       |
| ------- | ------------------------------------------------------------------- | -------------------------------------- |
| Variant | Different design direction or conceptual approach                   | Separate folder or filename indication |
| Version | Evolution of the same variant (small changes, tweaks, improvements) | Managed via Git version control        |

**Example Filename Breakdown:**

```text
bar/carbon_tube_od24_id22mm/bar_end/leader_line_3mm/variant_7/bar-end_24-22_sls.*
```

- `bar` folder = part of the bar (vs QR etc.)
- `carbon_tube_od24_id22mm` = must use carbon tube with these OD/ID dimensions
- `leader_line_3mm` = must use 3mm leader (steering) lines
- `variant` = 7
- `version` = _git commit id_


---

## General 3D Print Material Selection Guide

Material selection must consider ductility, impact resistance, print orientation, and cyclic loading as well as tensile strength. The recommendations below incorporate the expanded JLC3DP SLS and MJF catalog; supplier specifications were checked on **2026-09-05**.

**3301PA is the recommended SLS choice for new bar ends and center inserts**, including white parts previously specified in 1172 Pro. **PA11-HP is preferred for new V-splitters carrying direct line tension, with PA12-HP retained as the existing alternative.** PA12-HP remains the baseline for cleat bases. Consider PA12S-HP for lightly loaded MJF accessories when the actual quote offers a saving.

The project previously reported multi-season field use of 3201PA-F from -20°C to +30°C in freshwater, seawater, and snow. That experience does not transfer automatically to another material. The newer recommendations are material-selection decisions, not recorded TPKB field validation; see [Validation Status](docs/validation.md). Component-specific geometry, metal hardware, and assembly requirements still apply.

### Material Recommendations by Use Case

| Part / Component | Recommended Material | Manufacturing Technology | Notes |
|------------------|----------------------|-------------------------|-------|
| Bar ends and center inserts, including white parts | [3301PA Nylon](https://jlc3dp.com/help/article/3301pa-nylon) | SLS | Recommended for new builds; 48 MPa tensile strength and 30% elongation. Higher listed elongation than 1172 Pro, but not than the current 3201PA-F specification. Verify fit, line wear, and impact behavior on the finished part. |
| Existing black SLS parts / established material option | [3201PA-F Nylon](https://jlc3dp.com/help/article/3201pa-f-nylon) | SLS | Retain as an alternative backed by the project's reported field experience. Current supplier figures are 44 MPa and 35% elongation. |
| Existing white SLS parts | [Precimid 1172 Pro](https://jlc3dp.com/help/article/precimid-1172-pro) | SLS | Legacy white option; 46 MPa and 8–15% elongation. Prefer evaluating 3301PA for new bar ends and center inserts. |
| V-splitters carrying direct kite-line tension | [PA11-HP Nylon](https://jlc3dp.com/help/article/pa11-hp-nylon) preferred; [PA12-HP](https://jlc3dp.com/help/article/pa12-hp-nylon) existing alternative | MJF | Prefer PA11-HP for new builds based on its higher listed tensile strength, elongation, and notched impact strength. Validate the finished part under representative line loads, including sustained-load creep and line-hole wear. Do not substitute PA12S solely to reduce cost. |
| Cleat bases | [PA12-HP Nylon](https://jlc3dp.com/help/article/pa12-hp-nylon) | MJF | Retain the existing baseline; evaluate PA11-HP separately for fit and loaded operation. |
| Lightly loaded housings, covers, and slider blocks without significant shock loading | [PA12S-HP Nylon](https://jlc3dp.com/help/article/pa12s-hp-nylon) | MJF | Potential cost-saving choice with a finer surface texture. Account for orientation: elongation is 12% in XY but only 5% in Z. Compare actual part quotes. |
| Polymer components requiring greater ductility | [PA11-HP Nylon](https://jlc3dp.com/help/article/pa11-hp-nylon) | MJF | Candidate for testing: 52 MPa and 50% elongation. A QR housing substitution requires assembly and release-function testing. This is not a recommendation to replace metal pins or load-bearing metal mechanisms with nylon. |
| Inline bar center hub (Variant 8) and Swivel metal parts (housing and shaft) | [Titanium TC4](https://jlc3dp.com/help/article/titanium-tc4) or [316L Stainless Steel](https://jlc3dp.com/help/article/316L-Stainless-Steel) | SLM | Titanium preferred for lower weight and high strength-to-weight ratio; otherwise 316L stainless steel, following component specifications. |
| Quick Release (QR) mechanism flat parts | Titanium sheet | Laser or waterjet cutting | Use the exact thickness specified in the component instructions. |
| Assembly tools | Refer to [Tools](hardware/tools/README.md) | SLM and SLA | Follow each tool's requirements; CBY resin remains an economical option for suitable jig adapters and presser feet. |

### Supplier Property Comparison

These are supplier coupon-test values, not allowable loads for the printed components. XY and Z identify print orientation; test methods and specimen conditioning differ between materials. Higher elongation alone does not establish better fatigue life or impact performance.

| Technology | Material / Supplier Source | Tensile Strength | Elongation at Break | Selection Notes |
|------------|----------------------------|------------------|---------------------|-----------------|
| MJF | [PA12-HP](https://jlc3dp.com/help/article/pa12-hp-nylon) | 48 MPa | 20% | Existing structural baseline. |
| MJF | [PA12S-HP](https://jlc3dp.com/help/article/pa12s-hp-nylon) | 45 MPa XY; 43 MPa Z | 12% XY; 5% Z | Finer texture; lower ductility. Its listed 1700 MPa tensile modulus is lower than PA12-HP's 1800 MPa. |
| MJF | [PA11-HP](https://jlc3dp.com/help/article/pa11-hp-nylon) | 52 MPa XY/Z | 50% XYZ | Preferred for new V-splitters; validate the finished component. |
| MJF | [PAC-HP](https://jlc3dp.com/help/article/pac-hp-nylon) | Not listed on linked page | Not listed on linked page | JLC3DP describes full-color nylon for models and prototypes, not carbon-fiber-filled nylon. Excluded from structural recommendations. |
| SLS | [3201PA-F](https://jlc3dp.com/help/article/3201pa-f-nylon) | 44 MPa | 35% | Current figures differ from the supplied research's 45–48 MPa and 10–15%. |
| SLS | [1172 Pro](https://jlc3dp.com/help/article/precimid-1172-pro) | 46 MPa | 8–15% | Existing white material. |
| SLS | [3301PA](https://jlc3dp.com/help/article/3301pa-nylon) | 48 MPa | 30% | White; selected for new bar ends and center inserts. |
| SLS | [3401GB](https://jlc3dp.com/help/article/3401gb-nylon) | 42 MPa | 8% | 2500 MPa tensile modulus. Not selected for impact-prone kite-bar parts because this project prioritizes ductility over increased stiffness. |

### Cost, Exposure, and Manufacturing Notes

- **Cost:** JLC3DP lists starting prices of $1 for the linked PA12-HP, PA12S-HP, PA11-HP, 3201PA-F, 1172 Pro, and 3301PA materials. These minimum prices do not establish equal finished-part costs or a guaranteed PA12S saving; compare quotes for the same geometry and quantity.
- **Marine exposure:** The linked specifications do not establish comparative long-term UV, saltwater, cold-water, or fatigue performance for these TPKB parts. Record representative exposure and loading results before describing a replacement material as field-proven. PA11's ductility is not a guarantee against fracture.
- **Print review:** Evaluate supplier dimensional or wall-thickness warnings against the affected part's fit and loading requirements. Do not dismiss a warning solely because a previous print worked. See the [example supplier warning](images/jlc3dp_warning.jpeg).
