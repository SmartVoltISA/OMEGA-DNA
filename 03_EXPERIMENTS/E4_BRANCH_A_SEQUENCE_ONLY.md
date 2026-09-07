# E4 Branch A — Sequence-only

This branch is the control path.

- Input: the same rows and official train/valid/test assignment used by Branch B.
- Predictors: sequence-derived features only.
- No explicit relation/state channel is supplied.
- Target, groups, split, seeds, evaluation metric and stopping rule must remain identical to Branch B.

Purpose: establish the baseline before adding the relational branch.
