# Release Asset Intake — Full Relink Gate

This file records the final integration gate for the `Docs` / `backend docs` release intake.

## Human custody repair entering this gate

The incomplete/corrupt `raw/human/task3_human_native_parts/` custody has been reconstructed from the pinned release asset:

- asset: `ASI_Brain_Engine_Combined_Corpus_v1.xlsx`
- release asset id: `512182897`
- release SHA-256: `6d6bd608844b07728aaefb0d16e6c36bfcf7ba4ac3ec70af2610ea2bd7622a1b`
- source sheet: `03 Existing Parameters`
- selected canonical Brain Base range: `SB-ASI-P0001..SB-ASI-P2560`
- deterministic custody: 8 independently valid gzip/base64 parts, 320 parameter rows each
- reconstructed TSV SHA-256: `91ef0ecf425ab9d1a66c64a0134493941a98adc60bf88482bf096c66305732f8`

The existing `tools/materialize_human_native_2560_v1.py` gate passes the reconstruction with:

- 2,560 ordered parameter rows
- 80 containers
- 10 segments
- 13 columns per parameter row
- 2,560/2,560 `APPROVED BY USER`
- 2,560/2,560 `USER EVIDENT`
- 2,560/2,560 `Canonical Brain Base`

## Required final gate

This intake is mergeable only after `.github/workflows/relink-validate.yml` completes successfully on the intake branch, including registry generation, relinking, all Phase-2 R-F-R suites, and `tools/validate_repo.py`.

A release asset is still source evidence rather than automatic canonical truth. Passing this gate validates the provenance/intake machinery and the Human custody restoration; it does not bulk-promote every release document into canonical Sourceborn structures.