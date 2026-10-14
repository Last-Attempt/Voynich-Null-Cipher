# Licence scope

The original software in this repository is licensed under the Microsoft Public License (MS-PL). The complete, unmodified licence text is in [LICENSE](LICENSE), obtained from the [SPDX licence list](https://spdx.org/licenses/MS-PL.html).

## Covered software

The licence covers the original Python source and tests: `analyse.py`, `archive.py`, `report.py`, `synthetic.py`, `verify.py`, and `tests/test_analyse.py`. It also covers the original software configuration in `.editorconfig`, `.gitattributes`, `.gitignore`, and `requirements.txt`. Source files use `SPDX-License-Identifier: MS-PL`; future original software should carry the same identifier unless an explicitly approved exception applies.

## Other material

This software licence does not relicense `data/`, `results/`, or research/governance documentation. In particular, original manuscript transliterations, tokenised corpora, retained transcription streams and result archives retain their existing rights and provenance. See [docs/sources.md](docs/sources.md) and [data/manifest.json](data/manifest.json). No new permission to redistribute those materials publicly is granted by this change.

External dependencies, including NumPy installed through `requirements.txt`, remain under their own licences. Their implementations are not vendored here, and this repository's MS-PL grant does not replace their licence terms or notices.

## Distribution and repository visibility

When distributing covered source code, include the complete [LICENSE](LICENSE) and preserve existing copyright, patent, trademark and attribution notices as required by its terms. Include this scope document so recipients can distinguish software from research data. A future code-only distribution should omit `data/` and `results/` unless their distribution rights have been separately established.

The repository remains private. Selecting MS-PL for the software does not authorise making the repository public, publishing a release, or distributing third-party datasets. Any such action requires its own explicit authorisation from the product owner.
