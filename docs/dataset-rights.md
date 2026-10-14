<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Dataset redistribution audit

Checked on 14 October 2026. **All four collected transcription files are covered by voynich.nu's explicit CC0 statement.** They are permissively reusable, including modification, redistribution and commercial use, under CC0 rather than BSD. The code's MS-PL licence is separate. This audit records licence evidence; it does not itself change repository visibility or create a release.

## Publisher evidence

René Zandbergen's [site map](https://www.voynich.nu/roadmap.html), under “Licences and copyright”, identifies the transcription tables as its CC0 scope. The observed page states:

> they are being made available at this web site in accordance with the Creative Commons CC0 licence

The page displayed a latest-update date of 6 October 2026. Its linked [transliteration table](https://www.voynich.nu/transcr.html) includes the ZL extended-EVA file, while the linked [STA table](https://www.voynich.nu/extra/sta.html) lists RF1b, ZL3b and IT2a. Thus the statement applies to these specific files, not merely to the medieval manuscript or an unrelated mirror. The page asks readers to acknowledge the source and link back; provenance and credits are retained here.

## File-by-file findings

| Preserved file | Upstream file | Attribution / provenance | Published terms |
| --- | --- | --- | --- |
| `data/raw/RF1b.txt.gz` | [RF1b.txt](https://www.voynich.nu/data/sta/RF1b.txt) | René Zandbergen's reference rendering, combining Zandbergen–Landini and Glen Claston material | CC0 |
| `data/raw/ZL3b.txt.gz` | [ZL3b.txt](https://www.voynich.nu/data/sta/ZL3b.txt) | René Zandbergen and Gabriel Landini, STA conversion | CC0 |
| `data/raw/IT2a.txt.gz` | [IT2a.txt](https://www.voynich.nu/data/sta/IT2a.txt) | Takeshi Takahashi's historical rendering via the Landini–Stolfi interlinear file, STA conversion | CC0 |
| `data/raw/ZL3b-n.txt.gz` | [ZL3b-n.txt](https://www.voynich.nu/data/ZL3b-n.txt) | René Zandbergen and Gabriel Landini, extended EVA | CC0 |

These attributions describe provenance; they do not assert that every listed contributor separately signed a newly obtained permission. The conclusion relies on the publisher's public CC0 declaration for its hosted transcription collection. Existing headers, source URLs and uncompressed SHA-256 hashes remain unchanged in [the manifest](../data/manifest.json).

## Meaning and boundaries

[Creative Commons' CC0 deed](https://creativecommons.org/publicdomain/zero/1.0/) expressly permits copying, modification and distribution, including commercial use, without asking permission. The operative [legal code](https://creativecommons.org/publicdomain/zero/1.0/legalcode.en) and a verbatim [CC0-1.0 text](../LICENSES/CC0-1.0.txt) are provided for reference. CC0 is a public-domain dedication with fallback provisions, not a BSD licence and not MS-PL.

Tokenisation, compression and alternate-glyph removal do not impose new restrictions on the underlying CC0 transcription data in `data/derived/` and the retained transcription streams in `results/`. Original research documentation, presentation, result compilations and synthetic examples now use CC BY 4.0 under [LICENSE-SCOPE.md](../LICENSE-SCOPE.md). Code remains MS-PL. Those grants cover only original project contributions and do not restrict the underlying CC0 transcription material or bare numerical facts.

The site's font conditions are distinct from its transcription terms; no font is part of these four datasets. Do not apply the CC0 statement to every website asset. No dataset replacement or permission email is needed for the four verified transcription sources. This finding supersedes the initial, unverified “private research preservation only” metadata and the earlier statement that permissive terms had not been established.
