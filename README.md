# ThePerfectKiteBar (TPKB)

An **open-source kite control bar** designed for all **chill kite-foil enthusiasts** that means max kitefoil session enjoyment with added benefits of flexibility, customization, and full DIY freedom.

---

## Project Purpose

ThePerfectKiteBar is an open hardware project focused on designing and sharing components of a kite control bar system optimized for kite-foiling.

This project is intended for:

- DIY enthusiasts
- Riders seeking lightweight or custom solutions
- Experimental design exploration
- Field replacement and customization of bar components

All parts are designed with parametric flexibility in mind — allowing for adaptation to different materials, manufacturing methods, and rope/tube sizes.

---

## Project Organization and Directory Structure

Main components of the project are organized like this:

- `/bar/` → The main bar body
- `/bar_center_piece/` → Center insert parts
- `/bar_end/` → End pieces for the bar
- `/swivel/` → Swivel component to untwist lines
- `/trim/` → Depower trim and V-splitter
- `/quick_release/` → Quick release system (Coming soon)

Each component has its own folder, containing:

- Its own `README.md` file with details
- Subfolders indicating key design constraints (tube diameter, bearing type, rope diameter, etc.)
- Variants reflecting different design ideas

---

## Design Philosophy: Variant vs Version

| Term    | Meaning                                                             | How it's handled                       |
| ------- | ------------------------------------------------------------------- | -------------------------------------- |
| Variant | Different design direction or conceptual approach                   | Separate folder or filename indication |
| Version | Evolution of the same variant (small changes, tweaks, improvements) | Managed via Git version control        |

Example filename (STL version to print)

```
bar/carbon_tube_od24_id22mm/bar_end/leader_line_3mm/variant_7/bar-end_24_22_sls.*
```

- `bar` folder = part of the bar (vs QR etc.)
- `carbon_tube_od24_id22mm` = must use carbon tube with these OD/ID
- `leader_line_3mm` = must use 3mm leadr (steering) lines 
- `variant` = 7 
- `version` = _git commit id_

---

## Navigation Guide

To explore any component:

1. Navigate to: `hardware/3D_models/<component_name>/`
2. Open: `README.md`
3. Inside you will find:
   - Part purpose
   - Design constraints
   - 3D printing instructions
   - Relevant assembly notes
   - Images and previews
   - Available variants

Example links:

- [Bar Center Piece](hardware/3D_models/bar_center_piece/README.md)
- [Swivel](hardware/3D_models/swivel/README.md)
- Quick Release → Coming Soon

---

## File Types and Their Purpose

Each component folder may contain the following file types:

| Extension | Purpose |
|-----------|---------|
| `.shapr`  | Native design file created in Shapr3D. Editable source model including sketches, constraints, and parametric features. |
| `.step`   | Industry-standard neutral 3D file format (ISO 10303). Used for CAD interoperability, CNC machining, or modification in other CAD software. |
| `.stl`    | 3D mesh file optimized for 3D printing. Triangulated surface model ready to slice for FDM, SLS, or SLA printing. |
| `.png`    | Preview or reference image of the part. Used in documentation to visualize the shape, assembled view, or specific details. |

---

## Contribution & Collaboration

Pull requests, design discussions, and new variants are welcome.

- Fork the repository
- Open Issues to suggest improvements or report problems
- Contribute new components or variants

Documentation and structure are continuously evolving.

---

## License

This project is licensed under

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](LICENSE)  

See above for details.

## Issues

[![GitHub Issues](https://img.shields.io/github/issues/aniva/theperfectkitebar.svg)](https://github.com/aniva/theperfectkitebar/issues)  


---

## Maintainer

Maintained by: 
* [aniva](https://github.com/aniva)
* [Deboitemendumenix](https://github.com/Deboitemendumenix)---

