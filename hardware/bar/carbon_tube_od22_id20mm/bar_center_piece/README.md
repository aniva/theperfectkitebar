# Central Piece for 22mm Carbon Tube (OD 22mm / ID 20mm)

This directory contains the design files and specifications for the **Central Piece** of ThePerfectKiteBar system, specifically designed to fit a **22mm outer diameter** carbon tube.

---

## Design Overview

The central piece guides the sheeting and safety lines through the center of the control bar. Two distinct design architectures are available depending on your build preference:

1. **Variant 7 (Off-Center Plastic Clamp — Ultralight & Easy Assembly)**: An off-center, snap-on guide 3D printed in **SLS PA12 Nylon**. It clamps directly over a single continuous carbon tube without requiring a central cutout, delivering an ultra-lightweight build and fast, straightforward assembly.
2. **Variant 8 (Inline Titanium Center-Hole Hub — Mainstream Split-Tube Design)**: A classic inline center-hole architecture where the central core is 3D printed in **Titanium via SLM** (available through the same JLC3DP service). Two separate carbon tube segments slide over each end of the titanium hub and bolt into place to form the required bar length.

---

## Variant 7 (Off-Center SLS Nylon Clamp)

**Variant 7** focuses on ultralight minimalism, smooth control line travel, and quick installation over a one-piece carbon bar. It is available in two versions based on the securing bolt size:

| Version | Securing Bolt | Description | Image Preview |
|---------|---------------|-------------|---------------|
| **2.5mm Bolt** | M2.5 x 12mm | Most compact, lightweight profile. Recommended for short or joystick-style bars. | <img src="variant_7/bar-center-piece_22_m2.5x12_sls.png" width="30%"> |
| **3mm Bolt** | M3 x 12mm | Slightly bulkier but highly robust version for maximum durability under heavy load. | <img src="variant_7/bar-center-piece_22_m3x12_sls.png" width="30%"> |

Choose the version that fits your priority: **lightweight minimalism (2.5mm)** or **maximum durability (3mm)**.

---

## Variant 8 (Inline SLM Titanium Center-Hole Hub)

Unlike the off-center plastic clamp of Variant 7, [`Variant 8`](variant_8) follows a mainstream inline center-hole kite bar layout. The central structural joiner is 3D printed in **Titanium (SLM)** (orderable from the same JLC3DP print shop) with a smooth, low-friction center aperture for the sheeting and safety lines.

To build the bar to your target length, two **OD 22mm / ID 20mm** carbon fiber tubes slide onto the opposing sleeve ends of the titanium centerpiece and are bolted securely through the integrated recessed hex-nut pockets.

> **Hardware & Drilling Note:** Variant 8 uses the exact same bolt pattern as the [Bar Ends](../bar_end/README.md), meaning it is assembled using the same **2mm countersunk bolts and nuts** and the same **[2mm Bolt Drilling Jig](../../../tools/README.md)**. Because the two carbon tubes must be drilled at both their inner ends (for the center piece) and outer ends (for the bar ends), assembling a bar with Variant 8 requires **twice as much drilling** as a Variant 7 bar (see the [Assembly Guide](../../../../docs/assembly.md)).

<img src="variant_8/bar-center-piece_22-20_slm.png" width="55%">

---

## Specifications

| Parameter | Variant 7 (Off-Center Clamp) | Variant 8 (Inline Center-Hole Hub) |
|-----------|------------------------------|------------------------------------|
| **Carbon Tube Compatibility** | Single continuous tube (OD 22mm / ID 20mm) | Two split tube halves (OD 22mm / ID 20mm) |
| **Manufacturing Technology** | **SLS** (Selective Laser Sintering) | **SLM** (Selective Laser Melting) |
| **Material** | **PA12 Nylon** | **Titanium (TC4 / Ti-6Al-4V)** (via JLC3DP) |
| **Mounting Style** | Snap-on clamp with single M2.5 or M3 bolt | Dual internal sleeves bolted to each carbon tube |
| **Model Files** | [`variant_7`](variant_7) (`.step`, `.stl`, `.shapr`) | [`variant_8`](variant_8) (`.step`, `.stl`, `.3mf`, `.shapr`) |

---

## Assembly & Installation

Thanks to the elasticity and strength of the SLS PA12 Nylon material, this central piece can be snapped over the carbon tube directly without fully disassembling the bar ends.

### Tools Required
- Hex Allen key (size matching your bolt choice)
- Awl or small hook (to undo knots in the trim line)
- Long-nose pliers

### Installation Steps
1. Neatly wind your control lines up to the V-splitter.
2. Remove the trim system.
3. Remove the sheeting and safety lines.
4. Remove the old/broken central piece.
5. Gently expand the new central piece and snap it directly over the middle of the carbon tube.
6. Align it, insert and tighten the securing bolt (do not overtighten).
7. Re-thread the sheeting/safety lines and reinstall the trim system.
