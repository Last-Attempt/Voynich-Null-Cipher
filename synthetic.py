#!/usr/bin/env python3
"""Calibration: an inserted-noise toy and a structured stream with no nulls."""
import json
import numpy as np
from analyse import ROOT, FastControls, compare, metrics, transform


def run():
	rng=np.random.default_rng(314159)
	plain=[['A1','B1']*20 for _ in range(200)]
	padded=[sum(([g,f'C{int(rng.integers(1,10))}'] for g in word),[]) for word in plain]
	no_padding=[['A1','B1','C1']*24 for _ in range(200)]
	result={}
	for name,words in [('inserted_noise',padded),('no_padding_periodic',no_padding)]:
		lines=[dict(words=words)]
		entry={'baseline':metrics(words),'variants':{}}
		for offset in (0,1):
			observed=metrics(transform(lines,'word',offset))
			fast=FastControls(lines,'word',offset)
			rng=np.random.default_rng(314159+offset)
			controls=[fast.sample(rng,'word_matched') for _ in range(199)]
			entry['variants'][str(offset)]={'observed':observed,'comparison':compare(observed,controls),'replicates':controls}
		result[name]=entry
	(ROOT/'results/synthetic.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
	return result


if __name__=='__main__':
	run()
