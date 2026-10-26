# Validation Status

This register distinguishes reported field experience from recorded test evidence. It does not certify a component or establish a safe operating load.

| Scope | Recorded status | Evidence and remaining work |
| --- | --- | --- |
| First functional bar | Field testing reported in spring 2024 | Root README; multi-season field use across water and snow conditions. |
| Printed materials | Multi-season use reported | Root README describes conditions (`3201PA-F` tested from -20°C to +30°C in freshwater, seawater, and snow); newer catalog materials (`3301PA`, `PA11-HP`, `PA12S-HP`) await component-specific field logs. |
| Quick release variants 1–4 | Did not proceed to field testing | Quick-release README; omitted from published variants. |
| Quick release variant 5 (M4 and M6) | Field-tested and validated | In active field use; see [Quick Release](../hardware/quick_release/README.md#variant-5-m4). |
| Quick release variant 6 (M4 and M6) | Field-tested and validated | In active field use across both M4 and M6 versions; no accidental pin release or pin-retention issues occurred during field testing. See [Quick Release](../hardware/quick_release/README.md#variant-6). |

## Outstanding work

- [ ] Record exact component variants and Git commits for previously reported field tests.
- [ ] Record formal load measurements for quick-release variants alongside existing field validation.
- [x] Validate Variant 6 (M4 and M6) quick-release pin retention in field testing (no accidental pin release observed).
- [ ] Associate any release with a component inventory and the validation records applicable to it.

## Recording a result

For each test, add a dated entry with the tester, component and variant, Git commit, CAD source hash, materials, manufacturing method, assembly configuration, test method, measured loads or conditions, outcome, and links to photos or measurements. Record failures and limitations. Change a status only when supporting evidence is available.
