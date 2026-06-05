# Reference Alignment Report

This report compares family rule drafts against the current stable family references. It does not auto-edit the references.

## Alignment Rows

| Family | Reference | Covered | Recommended Action | Draft Item |
|---|---|---|---|---|
| software/system | `software-system-thesis.md` | no | hold | Consider adding or strengthening these chapter-role hints in the family reference: `background_significance` (1), `cause_analysis` (1), `current_state_diagnosis` (1), `experiment_evaluation` (1) |
| software/system | `software-system-thesis.md` | no | hold | Consider adding these family-specific anchor signals in the family reference: `role:background_significance` (1), `role:cause_analysis` (1), `role:current_state_diagnosis` (1), `role:experiment_evaluation` (1) |
| control/optimization | `control-optimization-thesis.md` | no | hold | Consider adding or strengthening these chapter-role hints in the family reference: `current_state_diagnosis` (3), `scheme_design` (3), `background_significance` (2), `experiment_evaluation` (2) |
| control/optimization | `control-optimization-thesis.md` | no | hold | Consider adding these family-specific anchor signals in the family reference: `role:current_state_diagnosis` (3), `role:scheme_design` (3), `topic:algorithm_modeling` (3), `role:background_significance` (2) |
| mechanical/manufacturing | `mechanical-manufacturing-thesis.md` | no | review_merge | Consider adding or strengthening these chapter-role hints in the family reference: `current_state_diagnosis` (22), `background_significance` (19), `literature_review` (16), `scheme_design` (16) |
| mechanical/manufacturing | `mechanical-manufacturing-thesis.md` | no | review_merge | Consider adding these family-specific anchor signals in the family reference: `topic:equipment_maintenance` (24), `role:current_state_diagnosis` (22), `topic:algorithm_modeling` (20), `role:background_significance` (19) |

## Next Step

- `hold` means the family still lacks enough evidence and the reference should stay unchanged.
- `already_covered` means the existing family reference already contains a close hint and does not need a new edit yet.
- `review_merge` means the family evidence is no longer fully blocked and the draft item is not obviously covered in the current reference.
