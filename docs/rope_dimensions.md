# Rope Splicing & Cutting Dimensions Companion Guide

This document serves as the companion guide to the unified [Interactive Splicing & Sizing Calculator](rope_calculator.html). It explains the routing physics, splicing guidelines, and mathematical models for building a premium, custom kiteboarding control bar.

The system parameters are classified into three main groups to match the labeling on the interactive routing schematic:
- **Group A (Sheeting Rope & Throw)**: Main sheeting line specs, throw length, loop ends, and tail lengths.
- **Group B (Hardware & Trim Geometry)**: Control bar, cleat, block dimensions, and system adjustment travel distances.
- **Group C (Rigging & Splicing)**: Splicing shrinkage factors, leader line adjustments, and pigtail sizing targets.

---

## 1. System Components & Routing

### Desired Throw `(A1)`
The **Throw** is the single line running from the control bar center up to the cleat. It defines the physical range of depower available by sliding the bar.
* **Range**: 40 cm to 70 cm (default is 65 cm).
* **Formula Impact**: A longer throw increases the raw sheeting line length by twice the throw length (due to the 2:1 loop design above the cleat) and increases the length of the chafe sleeve.

### Sheeting Line Diam. `(A2)`
The diameter of the primary sheeting line (4.0mm Dyneema). Fixed at `0.4 cm`.

### Splice Loop Length `(A3)`
The finished splice loop length stitched at the bottom of the sheeting line to anchor it to the quick release. Fixed at `4 cm`.

### Depower Line Tail `(A4)`
The tail of the sheeting line exiting the left side of the cleat, ending with a cylindrical blue pull handle. Fixed at `9 cm` for grip and leverage.

---

### Bar Diameter `(B1)`
The outer diameter of the hollow carbon control bar (21 mm, 22 mm, 23 mm, or 24 mm). It guides the leader lines inside the bar ends.

### Cleat Dimensions `(B2, B3, B4)`
The **Cleat** secures the sheeting line at the top of the throw.
* **Cleat Length (B2)**: Fixed at `6 cm`.
* **Cleat Width (B3)**: Fixed at `1 cm`.
* **Cleat Holes (B4)**: Fixed at `4` routing holes.

### Upper Block Dimensions `(B5, B6)`
The **Upper Block** is the pulley redirection unit at the top of the trim system.
* **Upper Block Diam. (B5)**: Fixed at `1.0 cm`.
* **Upper Block Height (B6)**: Fixed at `2.5 cm`.

### Depower Move [Cleat to Block] `(B7)`
The **Depower Move** represents the physical distance between the Cleat (B2) and the Upper Block (B6) when fully extended. It determines the maximum adjustment travel of the trim system.
* **Range**: 10 cm to 50 cm (default is 25 cm).

### Depower Ratio `(B8)`
The **Depower Ratio** is the 2:1 block-and-tackle mechanical advantage of the trim adjustment loops. Fixed at `1/2`.

---

#### Splicing Specs & Adjustable Parameters `(Group C)`
These parameters are adjustable via left-right sliders in the main calculator:
* **Splicing Shrinkage**: General shrinkage rate applied to any splice. Range `10%` to `30%` (default `20%`).
* **Bury Ratio**: General bury length multiplier. Range `40x` to `60x` rope diameter (default `50x`).
* **Leader Adjustment (C2)**: Adjustment span for leader lines. Range `20` to `50` cm (default `30` cm).
* **Power Pigtail Adjustment**: Front line trim adjuster span. Range `10` to `30` cm (default `20` cm).
* **Pigtail Finished Length (C4)**: Raw base finished target length. Range `30` to `50` cm (default `40` cm).

---

## 2. Splicing Formulas Reference

These formulas are implemented dynamically in the [Interactive Calculator](rope_calculator.html):

### Sheeting Line Sizing
* **Raw Calculated Length**:
  $$\text{Raw Length} = (\text{Throw (A1)} \times 2) + \frac{\text{Depower Move (B7)}}{\text{Depower Ratio (B8)}} + \text{Line Tail (A4)} + \text{Splice Loop (A3, 4cm)} + \text{Block Height (B6)}$$
* **Measured Finished Length**:
  $$\text{Finished Length} = \text{Raw Length} - \text{Line Tail (A4)} - \text{Block Height (B6)} - \text{Cleat Length (B2)}$$

### Leader & Safety Sizing
* **Leader Line Raw Cut**: $(\text{Throw (A1)} + \text{Depower Move (B7)} + \text{Leader Adjustment (C2)}) \times (1 + \text{Splicing Shrinkage}) + \text{Leader Adjustment (C2)}$
* **Leader Line Finished**: $\text{Raw Cut} - \text{Bottom Loop (3.5 cm)} - \text{Top Loop (2.5 cm)} = \text{Raw Cut} - 6\text{ cm}$
* **Safety Line Raw Cut**: $\text{Sheeting Raw} - \text{Depower Move (B7)}$
* **Safety Line Finished**: $\text{Sheeting Finished} - \text{Depower Move (B7)}$

### Steering & Power Pigtails
The rope diameter and splicing bury dynamically adapt based on the selected Bar Outer Diameter (B1):
* **Splicing Bury**: $\text{Rope Diameter} \times \text{Bury Ratio}$
* **Steering Pigtail (Loop-to-Loop)**: $\text{Finished Length (C4)} + 2 \times \text{Bury} \times (1 + \text{Splicing Shrinkage}) + \text{Loop Knot Length (4 cm)} + \text{Pigtail Loop Length (3.5 cm)}$
  * *Default (22mm OD, 2.5mm rope)*: $40 + 2 \times 12.5 \times 1.2 + 4 + 3.5 = 77.5\text{ cm}$
  * *Default (24mm OD, 3.0mm rope)*: $40 + 2 \times 15.0 \times 1.2 + 4 + 3.5 = 83.5\text{ cm}$
* **Power Pigtail (Loop-to-Knot)**: $\text{Finished Length (C4)} + 2 \times \text{Bury} \times (1 + \text{Splicing Shrinkage}) + \text{Power Adjustment} + \text{Pigtail Loop Length (3.5 cm)}$
  * *Default (22mm OD, 2.5mm rope)*: $40 + 2 \times 12.5 \times 1.2 + 20 + 3.5 = 93.5\text{ cm}$
  * *Default (24mm OD, 3.0mm rope)*: $40 + 2 \times 15.0 \times 1.2 + 20 + 3.5 = 99.5\text{ cm}$

### Accessories & Chafe Sleeve
* **Chafe Sleeve Raw Length**: $\text{Throw (A1)} \times 1.28 + 5$
* **Chafe Sleeve Cut Target**: $\text{Throw (A1)} + \text{Depower Move (B7)} + \text{Splice Loop Length (A3)}$
* **Bungee for 65mm Bar End**: $30.0\text{ cm}$ ($25\text{cm base} + 5\text{cm tail}$)
* **Bungee for 100mm Bar End**: $24.0\text{ cm}$ ($19\text{cm base} + 5\text{cm tail}$)
* **PU Center Tube Length**: $100\text{ mm}$ (runs inside Bar center)
* **Safety Bungee for QR**: $35.0\text{ cm}$ (2.5mm elastic core)

---

## 3. Recommended Build Procedure

1. **Calculate & Cut**: Enter your desired throw and depower move in the [Interactive Calculator](rope_calculator.html) to obtain your custom target lengths.
2. **Sheeting Line Splice**:
   * Splice the 4 cm loop at one end of the 4.0mm sheeting line.
   * Lock-stitch the bury.
   * Feed the line through the bar center, cleat base, upper block, and trim cleat.
   * Cut the excess line once the finished length is reached, leaving a 9 cm tail.
3. **Bungee Threading**:
   * Cut a 32.5 cm piece of 2.5mm bungee elastic core.
   * Insert the bungee core inside the 2.5mm Dyneema bungee line. The line will bunch up and shrink by 33%.
   * Splice the leader line loops at the target finished dimensions.
4. **Pigtail Rigging**:
   * Splice loops at both ends of the steering pigtails (loop-to-loop connection).
   * Splice the power pigtails with adjustable loops on one end and stopper knots on the other.
