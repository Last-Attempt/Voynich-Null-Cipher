<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Initial alternating-glyph investigation — 14 October 2026

**Conclusion: alternating deletion preserves more serial structure than matched random deletion, but this does not identify a meaningless-padding stream. Both offsets retain structure, and a synthetic stream containing no inserted padding produces the same direction of effect. No decipherment or language identification was attempted or obtained.**

All six masks were evaluated under two deletion controls, with 199 replicates per control, on six dataset/configuration choices (14,328 random deletions in total). The experiment is exploratory; the endpoint was fixed after a parser smoke run. See [the protocol](protocol.md) for assumptions and [sources](sources.md) for provenance and the bounded literature search.

## Corpus audit

| Configuration | Loci | Words | Tokens | Unknown slots | Alternative readings | Uncertain spaces |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| IT2a | 5215 | 37919 | 155352 | 257 | 0 | 0 |
| RF1b | 5385 | 38525 | 157254 | 114 | 0 | 677 |
| ZL3b | 5385 | 39026 | 157304 | 209 | 817 | 2748 |
| ZL3b_EVA | 5385 | 39026 | 174190 | 159 | 817 | 2749 |
| ZL3b_alt | 5385 | 39026 | 157317 | 249 | 817 | 2748 |
| ZL3b_join | 5385 | 36278 | 157304 | 209 | 817 | 2748 |

STA treats many composite signs/minim groups as units; ZL3b_EVA keeps individual repeated `i` minims separate while retaining standard compound benches and explicitly marked ligatures. These are materially different segmentation hypotheses. RF is combined from related sources; the configurations are sensitivity checks, not six independent replications. All loci are included in file order. Unknown-length spans and ambiguous original reading order limit physical-manuscript continuous-parity conclusions.

## Primary RF1b comparison

H2 is within-word conditional entropy in bits per retained token. Lower means more predictable. Offset 0 keeps the first glyph; offset 1 keeps the second. Monte Carlo probabilities below are lower-tail comparisons, not probabilities that the cipher hypothesis is true.

| Mask | H2 | Word-matched mean [95% interval] | Scope-matched mean | Lower-tail p | Bonferroni ×6 |
| --- | ---: | --- | ---: | ---: | ---: |
| continuous_0 | 3.2898 | 3.5399 [3.5246, 3.5534] | 3.3551 | 0.005 | 0.030 |
| continuous_1 | 3.2971 | 3.5399 [3.5265, 3.5534] | 3.3549 | 0.005 | 0.030 |
| line_0 | 3.2865 | 3.5380 [3.5265, 3.5505] | 3.3758 | 0.005 | 0.030 |
| line_1 | 3.2985 | 3.5421 [3.5281, 3.5548] | 3.3853 | 0.005 | 0.030 |
| word_0 | 3.2779 | 3.4866 [3.4740, 3.4966] | 3.4870 | 0.005 | 0.030 |
| word_1 | 3.2891 | 3.6047 [3.5894, 3.6205] | 3.6040 | 0.005 | 0.030 |

The original RF1b H2 is 2.6252, below every alternating-deletion result. Thus deletion loses original predictability even though alternation preserves more than random deletion. The two streams have similar H2; a low H2 here does not select content over padding.

## Segmentation and transcription sensitivity

| Configuration | Original H2 | Retained H2 range (six masks) | Word-matched control mean range | Lower-tail p range |
| --- | ---: | --- | --- | --- |
| IT2a | 2.5151 | 3.1309–3.1599 | 3.3615–3.4645 | 0.005–0.005 |
| RF1b | 2.6252 | 3.2779–3.2985 | 3.4866–3.6047 | 0.005–0.005 |
| ZL3b | 2.5101 | 3.1297–3.1534 | 3.3584–3.4603 | 0.005–0.005 |
| ZL3b_EVA | 2.2620 | 2.7568–2.7894 | 3.0189–3.1043 | 0.005–0.005 |
| ZL3b_alt | 2.5115 | 3.1326–3.1518 | 3.3597–3.4610 | 0.005–0.005 |
| ZL3b_join | 2.5290 | 3.1689–3.1941 | 3.3904–3.4966 | 0.005–0.005 |

The full result archive also records H1, pair/triple repetitions, all control replicates, both tails, standard deviations and empirical intervals. Word repetition and compression are descriptive measurements only. Sensitivity endpoints are not a separately corrected confirmatory family.

## Repeated triples

| Configuration | Original triple fraction | Retained triple fraction range | Word-matched mean range |
| --- | ---: | --- | --- |
| RF1b | 0.000369 | 0.002444–0.004569 | 0.000732–0.001328 |
| ZL3b_EVA | 0.006351 | 0.001732–0.002973 | 0.003378–0.003683 |

Removing alternating positions necessarily breaks a run of three original identical glyphs. New triples can still form after deletion. That mechanism applies to ordinary repeated glyphs as well as hypothetical padding; the table is not evidence that the removed signs were meaningless. STA and EVA count repeated minims differently, so their raw triple rates are not directly comparable.

## Calibration and negative findings

| Toy corpus | Offset 0 H2 / random mean | Offset 1 H2 / random mean |
| --- | --- | --- |
| inserted_noise | 0.0000 / 2.9550 | 3.1646 / 2.9565 |
| no_padding_periodic | 0.0000 / 1.3793 | 0.0000 / 1.3789 |

The inserted-noise toy interleaves deterministic content with random padding and confirms that the test can detect that simple mechanism. The no-padding toy is an ordinary repeating three-symbol sequence: both decimated offsets are predictable while random deletion is less predictable. It demonstrates directly that our main statistic is not specific to alternating null insertion. Neither toy is a natural-language benchmark.

Negative findings: this analysis identifies no consistently distinguished plaintext/padding offset, obtains no reading, and provides no evidence that surviving words are linguistic units. Lower entropy than random deletion is a serial-structure result, not a decipherment. The hypothesis is neither established nor comprehensively ruled out. Unknown-length glyph gaps, synthetic STA composites, arbitrary file ordering, boundary uncertainty and finite-sample entropy bias constrain interpretation. We did not carry out image audits, quire-level resampling, a trained language model or an exhaustive historical search.

## Preserved evidence and review

Original datasets are stored losslessly as gzip archives with uncompressed SHA-256 hashes in the manifest. Derived locus/word/glyph JSON, all 36 retained streams, seeded control metrics and calibration results are archived alongside reproducible code. Validation checks the parser/reset contracts, accelerated metrics against scalar examples, source hashes, derived/transformed output agreement and seeded replicate replay. No hosted workflow or unattended job was enabled.

For the next investigation, prioritise an image-grounded audit of the motivating triple runs and a calibrated comparison that preserves ordinary lag-two/word-position structure, before trying plaintext guesses. True gap-length and original ordering sensitivity, followed by Currier/quire stratification, would tighten the continuous model. These are recommendations, not completed work or permission to select more tasks.

## Licence and attribution

This report's original prose, tables and presentation are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit Voynich Null Cipher (VOY), a Last Attempt project, link to [the repository](https://github.com/Last-Attempt/Voynich-Null-Cipher), and indicate modifications. Underlying CC0 transcriptions and bare numerical facts remain unrestricted by this grant. See [LICENSE-SCOPE.md](../LICENSE-SCOPE.md) for the complete material mapping.
