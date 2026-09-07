# E4 Branch B — OMEGA relational/state

This branch is the treatment path.

- Input: exactly the same rows and official train/valid/test assignment as Branch A.
- Predictors: the identical sequence representation plus explicitly measured/annotated relation/state channels.
- Relation families remain typed and separate.
- Target, groups, split, seeds, evaluation metric and stopping rule must remain identical to Branch A.

Required comparison: Branch B − Branch A, followed by a relation-shuffle null and relation-family ablations.
