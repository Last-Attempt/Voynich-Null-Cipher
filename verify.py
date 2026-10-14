#!/usr/bin/env python3
"""Read-only verification of hashes, derived data and seeded scientific results."""
import gzip
import hashlib
import json
from pathlib import Path
import numpy as np
from analyse import ROOT, FastControls, metrics, parse, read_source, transform
from report import read_json


def verify():
	manifest=read_json(ROOT/'data/manifest.json')
	for item in manifest['sources']:
		p=ROOT/item['path']
		data=gzip.decompress(p.read_bytes())
		assert hashlib.sha256(data).hexdigest()==item['sha256'],item['path']
		assert len(data)==item['uncompressed_bytes']
	r=read_json(ROOT/'results/results.json')
	assert r['replicates']==199 and r['seed']==20261014
	configs={'RF1b':('RF1b.txt',True,0), 'ZL3b':('ZL3b.txt',True,0),
		'ZL3b_join':('ZL3b.txt',False,0), 'ZL3b_alt':('ZL3b.txt',True,1),
		'IT2a':('IT2a.txt',True,0), 'ZL3b_EVA':('ZL3b-n.txt',True,0)}
	assert set(r['datasets'])==set(configs)
	for name,(filename,comma,alt) in configs.items():
		data=read_source(ROOT/'data/raw'/filename)
		lines,audit=parse(data.decode(),comma,alt,name.endswith('_EVA'))
		entry=r['datasets'][name]
		assert entry['source_sha256']==hashlib.sha256(data).hexdigest()
		assert audit==entry['audit']
		assert lines==read_json(ROOT/'data/derived'/f'{name}.json')
		assert metrics([w for line in lines for w in line['words']])==entry['baseline']
		assert len(entry['variants'])==6
		for variant,item in entry['variants'].items():
			scope,offset=variant.rsplit('_',1);offset=int(offset)
			words=transform(lines,scope,offset)
			assert metrics(words)==item['observed']
			stream=read_source(ROOT/'results'/f'{name}_{variant}.txt').decode()
			assert stream=='\n'.join(' '.join(w) for w in words)+'\n'
			fast=FastControls(lines,scope,offset)
			for kind,c in item['controls'].items():
				seed=int.from_bytes(hashlib.sha256(f"{r['seed']}:{name}:{variant}:{kind}".encode()).digest()[:8],'big')
				assert seed==c['seed']
				assert len(c['replicates'])==199
				rng=np.random.default_rng(seed)
				# Bounded exact replay; all other replicates are preserved, not rerun here.
				for expected in c['replicates'][:3]:
					assert fast.sample(rng,kind)==expected
	for p in ROOT.rglob('*'):
		if p.is_file() and p.suffix in ('.py','.md','.json','.txt') and '__pycache__' not in p.parts:
			data=p.read_bytes()
			assert b'\r' not in data,str(p)
			assert data.endswith(b'\n'),str(p)
	print('Verified 4 source hashes, 6 parsed corpora, 36 retained streams, all observed metrics and 216 seeded control replicates; LF checks passed.')


if __name__=='__main__':
	verify()
