<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Alternating null-glyph hypothesis

The product owner proposed that every second manuscript glyph is meaningless padding, with repeated triples as one motivation. The authorised experiment tests continuous, per-line and per-word alternation at both offsets against random deletion. This protocol documents exploratory choices made during the initial run; it is not a prospectively preregistered study. A parser smoke run preceded the choice of the primary endpoint.

## Symbol units and data

The primary representation is RF1b in STA1. Each STA glyph code is a two-byte token; deleting alternate ASCII bytes would merely remove family/member identifiers. STA is synthetic: a token can include ligatures or several minims, and its designer explicitly cautions that it does not establish the manuscript's true character inventory. ZL3b and IT2a provide transcription sensitivity checks; RF and ZL are not independent witnesses. IT2a is the historical 1999 Takahashi rendering, not the latest Takahashi text.

ZL3b_EVA additionally uses the original extended EVA file with `ch`, `sh`, `cth`, `ckh`, `cph`, `cfh`, explicit brace ligatures and rare `@nnn;` codes kept atomic. Other minims, including successive `i`, remain separate. Isolated uppercase `I` on f57v is retained as recorded. This model tests the motivating repeated-minim idea, but neither this nor STA defines an undisputed physical glyph inventory.

Parse IVTFF loci in file order, including paragraphs, labels, circular and radial text. Ignore headers and comments as content; retain locus/page/Currier-language metadata in derived JSON. A 'line' is an IVTFF locus, which can be a label or circular text rather than a physical prose line. File order is an operational ordering, not established original manuscript reading order. No page, paragraph, space or comment advances parity. Primary word boundaries include periods, uncertain commas and drawing intrusions; ZL3b_join joins uncertain comma boundaries. ZL3b_alt selects the second supplied reading, capped at the last available option; other configurations select the first, most likely reading.

STA `Z1` occupies one unknown token, but can represent an unknown-length run. In EVA, `???` is collapsed to one unknown placeholder while single `?` remains one slot. This assumption prevents silently deleting uncertainty, but cannot recover actual parity downstream of missing-length text. Corpus-wide continuous results are conditional on it, and cannot falsify every physical-manuscript continuous variant. Alternative readings can also change token counts. Original bytes and uncertainty remain preserved.

## Six masks

Offsets are zero based: 0 keeps positions 1,3,5,…; 1 keeps positions 2,4,6,…. Continuous counts through all selected loci in file order. Line resets at each locus. Word resets at each transcribed word. Preserve empty words and original word boundaries. Every retained sequence is a subsequence, never reordered. Both offsets partition the original token inventory within every word.

## Controls and measurements

For each dataset and variant, draw 199 seeded random-deletion controls under each of two null models. `scope_matched` retains exactly the deterministic total in each alternation scope. `word_matched` instead retains exactly the deterministic number within every original word, keeping word shortening and empty-word patterns fixed. All subsets of the required size are equiprobable; selection uses independent continuous random scores and ranks within each group, then restores original order. NumPy PCG64 seeds are derived via SHA-256 from the top-level seed, dataset, variant and control name. Record every replicate metric, not just summaries.

Primary descriptive test: RF1b within-word conditional entropy H(next glyph | current glyph), lower tail, compared with word-matched deletion across six masks. Report add-one Monte Carlo probabilities and Bonferroni ×6 for that family only. Minimum attainable probability is 1/200. This endpoint is a test of special serial structure, not a necessary property of every null cipher. All other configurations and endpoints are exploratory; no isolated small probability is presented as a discovery. Random-deletion exchangeability is a reference model, not a proof about an unknown language.

Also measure unigram entropy, adjacent identical-pair fraction and identical-triple fraction within words, with control distributions. Report full-text word repetition and gzip bits per glyph descriptively only; gzip includes delimiters and is sensitive to representation. Compute no pairs/triples across word boundaries. Unknown placeholders participate as tokens, so they can bias estimates. No language classifier, dictionary match, plaintext recovery or cross-language benchmark is claimed.

A disappearance of triples alone has little evidential value: alternating positions mechanically prevents three equal consecutive original glyphs from surviving together, while deletion can create new adjacencies. A padding stream may itself be structured, chosen to resemble text, or use the same distribution as the content stream. Both retained offsets must be examined; neither a lower entropy nor a more random stream establishes which is meaningful.

## Validation and next questions

Behavioural tests protect compound-token parsing, metadata exclusion, unknown/alternative handling, reset boundaries, complementary masks, random retention counts/order and agreement of accelerated metrics with scalar calculations. Validate result reproducibility against stored hashes and seeded replicates. Run no hosted CI by default; local foreground execution has no unattended cost.

Further decisions should depend on the report: manuscript-image auditing of repeat triples and glyph boundaries, independent transcription confirmation, Currier/quire/page stratification, true gap-length parity sensitivity and calibrated known-language null-insertion positive controls are not completed in this initial investigation. Preserve negative findings; never tune glyph segmentation or offsets until a desired reading appears.
