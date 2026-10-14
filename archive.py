#!/usr/bin/env python3
# SPDX-License-Identifier: MS-PL
"""Lossless deterministic gzip preservation of data/results; no network calls."""
import gzip
from pathlib import Path

ROOT=Path(__file__).resolve().parent

if __name__=='__main__':
	for folder in ('data/raw','data/derived','results'):
		for p in (ROOT/folder).iterdir():
			if p.suffix in ('.txt','.json'):
				data=p.read_bytes()
				archive=Path(str(p)+'.gz')
				archive.write_bytes(gzip.compress(data,mtime=0))
				assert gzip.decompress(archive.read_bytes())==data
				p.unlink()
