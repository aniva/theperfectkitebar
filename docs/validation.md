# Validation Status

This register distinguishes reported field experience from recorded test evidence. It does not certify a component or establish a safe operating load.

| Scope | Recorded status | Evidence and remaining work |
| --- | --- | --- |
| First functional bar | Field testing reported in spring 2024 | Root README; exact tested commit, configuration, loads, and results are not recorded here. |
| Printed materials | Multi-season use reported | Root README describes conditions; component-specific test records remain to be added. |
| Quick release variants 1–4 | Did not proceed to field testing | Quick-release README; omitted from published variants. |
| Quick release variant 5 | Formal validation record absent | Manufacturing instructions are available; document the tested configuration and results before assigning a validated status. |
| Quick release variant 6 (M4 and M6) | Experimental; not field-tested according to component documentation | The documented risk of accidental pin release remains unresolved. See the [component warning](../hardware/quick_release/README.md#variant-6). |

## Outstanding work

- [ ] Record exact component variants and Git commits for previously reported field tests.
- [ ] Record test methods, conditions, measurements, and outcomes for the quick-release variants.
- [ ] Resolve and document variant 6 pin-retention behavior before changing its experimental status.
- [ ] Associate any release with a component inventory and the validation records applicable to it.

## Recording a result

For each test, add a dated entry with the tester, component and variant, Git commit, CAD source hash, materials, manufacturing method, assembly configuration, test method, measured loads or conditions, outcome, and links to photos or measurements. Record failures and limitations. Change a status only when supporting evidence is available.
