# Voynich Null Cipher — VOY

A reproducible investigation of the hypothesis that every second Voynich manuscript glyph is meaningless padding. Research is **Incubating** within Last Attempt; no supported product or deployment is implied.

Start with [the results](docs/initial-results.md), [the protocol](docs/protocol.md) and [source provenance](docs/sources.md). The initial experiment tests continuous, per-line and per-word alternation at both offsets against 199 seeded controls under each of two random-deletion models. It preserves negative and inconclusive findings. Removing letters from an EVA string is not generally equivalent to removing manuscript glyphs.

## Reproduce

Use Python 3.11+ and the pinned NumPy dependency. Run in the foreground from this repository:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python analyse.py --replicates 199 --seed 20261014
.venv/bin/python synthetic.py
.venv/bin/python report.py
.venv/bin/python archive.py
.venv/bin/python verify.py
```

On Windows use `.venv/Scripts/python.exe` instead. Analysis takes several minutes, depending on hardware. No background daemon, network retrieval during analysis or hosted CI is needed. `--only RF1b` limits analysis to a named configuration and `--output /tmp/voy-test` selects another results directory; derived files remain under `data/derived`. A subset run is not the complete investigation and must not replace the full result archive for handoff. Exact floating-point/gzip reproduction assumes the recorded dependency/runtime versions.

`data/raw/*.txt.gz` preserves original file bytes. Read one with Python's `gzip.open(path, 'rt')`, or extract it with `gzip -dc data/raw/RF1b.txt.gz`. `data/manifest.json` records uncompressed hashes and retrieval provenance. `data/derived/*.json.gz` preserves loci, page, language and tokenised words. `results/*_0.txt.gz` and `*_1.txt.gz` contain retained streams: one original word per row, tokens separated by spaces, with empty words retained as blank rows. The derived corpus supplies the original line grouping. `results/results.json.gz` contains every measurement and control replicate. `results/synthetic.json.gz` contains positive calibration and a no-padding counterexample.

Governance entry points are [AGENTS.md](AGENTS.md) and [START-HERE.md](START-HERE.md). Research changes target `main` through review; repository creation and registry acceptance are separate from accepting scientific conclusions. Source rights are retained; dataset rights are separate from the software licence.

## Licence

Original code and software configuration are licensed under the [Microsoft Public License (MS-PL)](LICENSE), with the covered files and exclusions explained in [LICENSE-SCOPE.md](LICENSE-SCOPE.md). Manuscript datasets, derived transcription files, result archives and research documentation are outside this software licence. External dependencies retain their own licences. The repository remains private until the product owner explicitly authorises otherwise.
