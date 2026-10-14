#!/usr/bin/env python3
"""Render the initial report from preserved calculated results."""
import gzip
import json
from analyse import ROOT


def read_json(path):
	return json.loads(path.read_text() if path.exists() else gzip.decompress(type(path)(str(path)+'.gz').read_bytes()))


def render():
	r=read_json(ROOT/'results/results.json')
	s=read_json(ROOT/'results/synthetic.json')
	parts=['# Initial alternating-glyph investigation — 14 October 2026','',
		'**Conclusion: alternating deletion preserves more serial structure than matched random deletion, but this does not identify a meaningless-padding stream. Both offsets retain structure, and a synthetic stream containing no inserted padding produces the same direction of effect. No decipherment or language identification was attempted or obtained.**','',
		'All six masks were evaluated under two deletion controls, with 199 replicates per control, on six dataset/configuration choices (14,328 random deletions in total). The experiment is exploratory; the endpoint was fixed after a parser smoke run. See [the protocol](protocol.md) for assumptions and [sources](sources.md) for provenance and the bounded literature search.','',
		'## Corpus audit','',
		'| Configuration | Loci | Words | Tokens | Unknown slots | Alternative readings | Uncertain spaces |','| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
	for name,d in r['datasets'].items():
		a=d['audit'];parts.append(f"| {name} | {a['loci']} | {a['words']} | {a['glyphs']} | {a.get('unknown_tokens',0)} | {a.get('alternatives',0)} | {a['uncertain_spaces']} |")
	parts += ['', 'STA treats many composite signs/minim groups as units; ZL3b_EVA keeps individual repeated `i` minims separate while retaining standard compound benches and explicitly marked ligatures. These are materially different segmentation hypotheses. RF is combined from related sources; the configurations are sensitivity checks, not six independent replications. All loci are included in file order. Unknown-length spans and ambiguous original reading order limit physical-manuscript continuous-parity conclusions.','',
		'## Primary RF1b comparison','',
		'H2 is within-word conditional entropy in bits per retained token. Lower means more predictable. Offset 0 keeps the first glyph; offset 1 keeps the second. Monte Carlo probabilities below are lower-tail comparisons, not probabilities that the cipher hypothesis is true.','',
		'| Mask | H2 | Word-matched mean [95% interval] | Scope-matched mean | Lower-tail p | Bonferroni ×6 |',
		'| --- | ---: | --- | ---: | ---: | ---: |']
	for name,v in r['datasets']['RF1b']['variants'].items():
		w=v['controls']['word_matched']['comparison']['h2'];c=v['controls']['scope_matched']['comparison']['h2']
		parts.append(f"| {name} | {w['observed']:.4f} | {w['mean']:.4f} [{w['q025']:.4f}, {w['q975']:.4f}] | {c['mean']:.4f} | {w['p_lower']:.3f} | {min(1,w['p_lower']*6):.3f} |")
	base=r['datasets']['RF1b']['baseline']
	parts += ['',f"The original RF1b H2 is {base['h2']:.4f}, below every alternating-deletion result. Thus deletion loses original predictability even though alternation preserves more than random deletion. The two streams have similar H2; a low H2 here does not select content over padding.",'',
		'## Segmentation and transcription sensitivity','',
		'| Configuration | Original H2 | Retained H2 range (six masks) | Word-matched control mean range | Lower-tail p range |',
		'| --- | ---: | --- | --- | --- |']
	for name,d in r['datasets'].items():
		rows=[v['controls']['word_matched']['comparison']['h2'] for v in d['variants'].values()]
		parts.append(f"| {name} | {d['baseline']['h2']:.4f} | {min(x['observed'] for x in rows):.4f}–{max(x['observed'] for x in rows):.4f} | {min(x['mean'] for x in rows):.4f}–{max(x['mean'] for x in rows):.4f} | {min(x['p_lower'] for x in rows):.3f}–{max(x['p_lower'] for x in rows):.3f} |")
	parts += ['', 'The full result archive also records H1, pair/triple repetitions, all control replicates, both tails, standard deviations and empirical intervals. Word repetition and compression are descriptive measurements only. Sensitivity endpoints are not a separately corrected confirmatory family.','',
		'## Repeated triples','',
		'| Configuration | Original triple fraction | Retained triple fraction range | Word-matched mean range |',
		'| --- | ---: | --- | --- |']
	for name in ('RF1b','ZL3b_EVA'):
		d=r['datasets'][name];rows=[v['controls']['word_matched']['comparison']['triple_repeat'] for v in d['variants'].values()]
		parts.append(f"| {name} | {d['baseline']['triple_repeat']:.6f} | {min(x['observed'] for x in rows):.6f}–{max(x['observed'] for x in rows):.6f} | {min(x['mean'] for x in rows):.6f}–{max(x['mean'] for x in rows):.6f} |")
	parts += ['', 'Removing alternating positions necessarily breaks a run of three original identical glyphs. New triples can still form after deletion. That mechanism applies to ordinary repeated glyphs as well as hypothetical padding; the table is not evidence that the removed signs were meaningless. STA and EVA count repeated minims differently, so their raw triple rates are not directly comparable.','',
		'## Calibration and negative findings','',
		'| Toy corpus | Offset 0 H2 / random mean | Offset 1 H2 / random mean |','| --- | --- | --- |']
	for name,d in s.items():
		a,b=(d['variants'][str(i)]['comparison']['h2'] for i in (0,1))
		parts.append(f"| {name} | {a['observed']:.4f} / {a['mean']:.4f} | {b['observed']:.4f} / {b['mean']:.4f} |")
	parts += ['', 'The inserted-noise toy interleaves deterministic content with random padding and confirms that the test can detect that simple mechanism. The no-padding toy is an ordinary repeating three-symbol sequence: both decimated offsets are predictable while random deletion is less predictable. It demonstrates directly that our main statistic is not specific to alternating null insertion. Neither toy is a natural-language benchmark.','',
		'Negative findings: this analysis identifies no consistently distinguished plaintext/padding offset, obtains no reading, and provides no evidence that surviving words are linguistic units. Lower entropy than random deletion is a serial-structure result, not a decipherment. The hypothesis is neither established nor comprehensively ruled out. Unknown-length glyph gaps, synthetic STA composites, arbitrary file ordering, boundary uncertainty and finite-sample entropy bias constrain interpretation. We did not carry out image audits, quire-level resampling, a trained language model or an exhaustive historical search.','',
		'## Preserved evidence and review','',
		'Original datasets are stored losslessly as gzip archives with uncompressed SHA-256 hashes in the manifest. Derived locus/word/glyph JSON, all 36 retained streams, seeded control metrics and calibration results are archived alongside reproducible code. Validation checks the parser/reset contracts, accelerated metrics against scalar examples, source hashes, derived/transformed output agreement and seeded replicate replay. No hosted workflow or unattended job was enabled.','',
		'For the next investigation, prioritise an image-grounded audit of the motivating triple runs and a calibrated comparison that preserves ordinary lag-two/word-position structure, before trying plaintext guesses. True gap-length and original ordering sensitivity, followed by Currier/quire stratification, would tighten the continuous model. These are recommendations, not completed work or permission to select more tasks.','']
	(ROOT/'docs/initial-results.md').write_text('\n'.join(parts))


if __name__=='__main__':
	render()
