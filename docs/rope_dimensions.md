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

### Splicing Specs `(C1, C2, C3, C4)`
* **Leader Splicing Shrink (C1)**: Splicing shrinkage rate for leader lines, fixed at `20%`.
* **Leader Adjustment (C2)**: Leader line adjustment span, fixed at `30 cm`.
* **Pigtail Bury Ratio (C3)**: Dyneema splicing bury ratio, fixed at `50x` rope diameter.
* **Pigtail Finished Len. (C4)**: Target pigtail connection length, fixed at `40 cm`.

---

## 2. Splicing Formulas Reference

These formulas are implemented dynamically in the [Interactive Calculator](rope_calculator.html):

### Sheeting Line Sizing
* **Raw Calculated Length**:
  $$\text{Raw Length} = (\text{Throw (A1)} \times 2) + \frac{\text{Depower Move (B7)}}{\text{Depower Ratio (B8)}} + \text{Line Tail (A4)} + \text{Splice Loop (A3)} + \text{Block Height (B6)}$$
* **Measured Finished Length**:
  $$\text{Finished Length} = \text{Raw Length} - \text{Line Tail (A4)} - \text{Block Height (B6)} - \text{Cleat Length (B2)}$$

### Leader & Safety Sizing
* **Leader Line Raw Cut**: $(\text{Throw (A1)} + \text{Depower Move (B7)} + \text{Leader Adjustment (C2)}) \times (1 + \text{Leader Splicing Shrink (C1)}) + \text{Leader Adjustment (C2)}$
* **Leader Line Finished**: $\text{Raw Cut} - (2 \times 2.5\text{ Splice Loop}) = 169.0\text{ cm}$ [runs inside Bar (B1)]
* **Safety Line Raw Cut**: $\text{Sheeting Raw} - \text{Depower Move (B7)}$
* **Safety Line Finished**: $\text{Sheeting Finished} - \text{Depower Move (B7)}$

### Steering & Power Pigtails
The rope diameter and splicing bury dynamically adapt based on the selected Bar Outer Diameter (B1):
* **22mm Bar OD**: Utilizes 2.5mm Dyneema. Splicing Bury = $\text{Rope Diameter (0.25 cm)} \times \text{Bury Ratio (C3)} = 12.5\text{ cm}$
  * **Steering Pigtail (Loop-to-Loop)**: $\text{Finished Length (C4)} + 2 \times \text{Bury} \times (1 + \text{Splicing Shrinkage (20\%)}) + \text{Loop Knot Length (4 cm)} + \text{Steering Loop Length (3 cm)} = 77.0\text{ cm}$
  * **Power Pigtail (Loop-to-Knot)**: $\text{Finished Length (C4)} + 2 \times \text{Bury} \times (1 + \text{Splicing Shrinkage (20\%)}) + \text{Power Adjustment (20 cm)} + \text{Power Loop Length (4 cm)} = 94.0\text{ cm}$
* **24mm Bar OD**: Utilizes 3.0mm Dyneema. Splicing Bury = $\text{Rope Diameter (0.30 cm)} \times \text{Bury Ratio (C3)} = 15.0\text{ cm}$
  * **Steering Pigtail (Loop-to-Loop)**: $\text{Finished (40)} + 2 \times \text{Bury} \times (1.2) + \text{Loop Knot (4)} + \text{Steering Loop (3)} = 83.0\text{ cm}$
  * **Power Pigtail (Loop-to-Knot)**: $\text{Finished (40)} + 2 \times \text{Bury} \times (1.2) + \text{Adjustment (20)} + \text{Power Loop (4)} = 100.0\text{ cm}$

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
