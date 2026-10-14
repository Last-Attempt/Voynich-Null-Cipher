<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Licence scope

The original software is licensed under [Microsoft Public License (MS-PL)](LICENSE). Original non-software material produced by the VOY project is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSES/CC-BY-4.0.txt). The upstream CC0 transcription material remains CC0.

## File and material mapping

| Material | Licence | Scope |
| --- | --- | --- |
| Original Python source/tests and software configuration | MS-PL | `analyse.py`, `archive.py`, `report.py`, `synthetic.py`, `verify.py`, `tests/test_analyse.py`, `.editorconfig`, `.gitattributes`, `.gitignore`, `requirements.txt` |
| Original documentation and research presentation | CC BY 4.0 | `README.md`, `AGENTS.md`, `START-HERE.md`, this scope document, and original prose/tables/charts in `docs/`, `data/README.md` and `results/README.md` |
| Original research-result compilations and synthetic examples | CC BY 4.0 | Original project contributions in `results/results.json.gz` and `results/synthetic.json.gz`, and future original non-software research output |
| Original provenance/licensing metadata | CC BY 4.0 | Original project contributions in `data/manifest.json`; underlying source facts and CC0 material remain outside this grant |
| Upstream transcription files | CC0-1.0 | All four archives in `data/raw/`; see [the verified audit](docs/dataset-rights.md) |
| Mechanical transformations of upstream transcriptions | CC0-1.0 remains applicable to the underlying transcription material | `data/derived/*.json.gz` and retained transcription streams `results/*_0.txt.gz` / `results/*_1.txt.gz`; no new attribution restriction is imposed |
| External dependencies, quoted third-party material and licence texts | Their existing terms | These are not relicensed as project-owned contributions |

CC BY applies only to copyright and similar rights the project is entitled to license in its original contributions. It does not create restrictions on bare facts or numerical values, underlying CC0 transcriptions, public-domain material, or third-party contributions. A mixed file's project presentation or compilation must not be confused with ownership of its individual CC0/factual contents. Keep existing source credits and provenance.

## Attribution for original non-software material

Credit **Voynich Null Cipher (VOY), a Last Attempt project**, link to [the repository](https://github.com/Last-Attempt/Voynich-Null-Cipher) and [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), and indicate modifications. Retain any additional named creator/source credits already supplied with the reused material. Attribution can be provided in a reasonable manner for the medium under the licence; no implication of endorsement is permitted.

## Distribution and repository visibility

Software distributions must include the complete MS-PL text and retain existing notices under its terms. Research/documentation distributions must retain the CC BY notice and attribution information for covered original contributions; retain the separate CC0 provenance for transcription material. The canonical CC BY legal text is preserved verbatim from the SPDX licence list in `LICENSES/CC-BY-4.0.txt`.

Repository visibility changes and release publication require separate product-owner authorisation; these licence grants do not themselves provide it. External dependencies remain under their own licences and are not vendored here.
