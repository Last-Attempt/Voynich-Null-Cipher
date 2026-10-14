#!/usr/bin/env python3
"""VOY alternating-null experiment. Python 3.10+ and NumPy."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
import math
from pathlib import Path
import random
import re
import statistics
import numpy as np

ROOT = Path(__file__).resolve().parent
TOKEN = re.compile(r'[A-Z][1-9a-z]')
EVA_TOKEN = re.compile(r'\{[^{}]+\}|@[0-9]{3};|c[tfpk]h|ch|sh|[a-zI?\']')


def parse(text, comma_space=True, alternative=0, eva=False):
	"""Strict STA1 parser: metadata never enters the symbol stream."""
	expected = '#=IVTFF Eva- 2.0' if eva else '#=IVTFF STA1 2.0'
	if not text.startswith(expected):
		raise ValueError(f'Expected {expected}')
	lines, audit = [], Counter()
	page, language = None, None
	for number, raw in enumerate(text.splitlines(), 1):
		if not raw.strip() or raw.startswith('#'):
			continue
		m = re.match(r'^<([^>]+)>\s*(.*)$', raw)
		if not m:
			raise ValueError(f'Invalid record at {number}')
		locus, body = m.groups()
		if ',' not in locus:
			page = locus
			lang = re.search(r'\$L=([A-Z])', body)
			language = lang.group(1) if lang else None
			continue
		if page is None:
			raise ValueError('Locus without page')
		def choose(match):
			audit['alternatives'] += 1
			options = match.group(1).split(':')
			return options[min(alternative, len(options)-1)]
		body = re.sub(r'\[([^\[\]]+)\]', choose, body)
		audit['uncertain_spaces'] += body.count(',')
		body = body.replace('<->', '.').replace('<~>', '.')
		body = re.sub(r'<[^>]*>', '', body)
		body = ''.join(body.split())
		body = body.replace(',', '.' if comma_space else '')
		words = []
		for word in body.split('.'):
			if not word:
				continue
			if eva:
				audit['unknown_length_spans'] += word.count('???')
				word = word.replace('???','?')
			tokens = (EVA_TOKEN if eva else TOKEN).findall(word)
			if ''.join(tokens) != word:
				raise ValueError(f'Unparsed glyph data at {locus}: {word!r}')
			audit['unknown_tokens'] += tokens.count('?' if eva else 'Z1')
			words.append(tokens)
		lines.append(dict(locus=locus, page=page, language=language, words=words))
		audit['loci'] += 1
		audit['words'] += len(words)
		audit['glyphs'] += sum(map(len, words))
	return lines, dict(audit)


def transform(lines, scope, offset, rng=None, control='word_matched'):
	"""Keep zero-indexed offset 0/1; preserve positions, spaces and empty words."""
	words = [w for line in lines for w in line['words']]
	lengths = [len(w) for w in words]
	groups, pos, index = [], 0, 0
	for line in lines:
		line_start = index
		for word in line['words']:
			if scope == 'word':
				groups.append(list(range(index, index+len(word))))
			index += len(word)
		if scope == 'line':
			groups.append(list(range(line_start, index)))
	if scope == 'continuous':
		groups = [list(range(index))]
	if scope not in ('continuous', 'line', 'word'):
		raise ValueError(scope)
	mask = set()
	for group in groups:
		mask.update(group[offset::2])
	if rng is not None:
		if control == 'scope_matched':
			mask = {i for group in groups for i in rng.sample(group, len(group[offset::2]))}
		elif control == 'word_matched':
			random_mask = set()
			for n in lengths:
				group = list(range(pos, pos+n))
				k = sum(i in mask for i in group)
				random_mask.update(rng.sample(group, k))
				pos += n
			mask = random_mask
		else:
			raise ValueError(control)
	result, pos = [], 0
	for word in words:
		result.append([g for j,g in enumerate(word) if pos+j in mask])
		pos += len(word)
	return result


def entropy(counts):
	n = sum(counts.values())
	return -sum((c/n)*math.log2(c/n) for c in counts.values()) if n else 0.0


def metrics(words):
	flat = [g for w in words for g in w]
	unigrams = Counter(flat)
	pairs = Counter((a,b) for w in words for a,b in zip(w,w[1:]))
	starts = Counter()
	for (a,b), n in pairs.items():
		starts[a] += n
	conditional = entropy(pairs)-entropy(starts)
	repeats = sum(n for (a,b),n in pairs.items() if a == b)
	triples = sum(a == b == c for w in words for a,b,c in zip(w,w[1:],w[2:]))
	triple_slots = sum(max(0,len(w)-2) for w in words)
	vocab = Counter(tuple(w) for w in words if w)
	nwords = sum(vocab.values())
	# Stable byte encoding; boundaries included. Compression is descriptive only.
	encoded = '.'.join(''.join(w) for w in words).encode('ascii')
	return dict(glyphs=len(flat), nonempty_words=nwords, empty_words=sum(not w for w in words),
		h1=entropy(unigrams), h2=conditional, adjacent_repeat=repeats/sum(pairs.values()) if pairs else 0,
		triple_repeat=triples/triple_slots if triple_slots else 0,
		repeated_word_mass=sum(n for n in vocab.values() if n>1)/nwords if nwords else 0,
		gzip_bits_per_glyph=8*len(gzip.compress(encoded, mtime=0))/len(flat) if flat else 0)


def compare(observed, controls):
	result = {}
	for key in ('h1','h2','adjacent_repeat','triple_repeat'):
		values = sorted(c[key] for c in controls)
		mean, sd = statistics.mean(values), statistics.stdev(values) if len(values)>1 else 0
		result[key] = dict(observed=observed[key], mean=mean, sd=sd,
			q025=values[int(.025*(len(values)-1))], q975=values[int(.975*(len(values)-1))],
			z=(observed[key]-mean)/sd if sd else None,
			p_lower=(1+sum(v<=observed[key] for v in values))/(1+len(values)),
			p_upper=(1+sum(v>=observed[key] for v in values))/(1+len(values)))
	return result


class FastControls:
	"""Array implementation of uniform subset deletion, preserving original order."""
	def __init__(self, lines, scope, offset):
		words = [w for line in lines for w in line['words']]
		vocab = sorted({g for w in words for g in w})
		lookup = {g:i for i,g in enumerate(vocab)}
		self.size = len(vocab)
		self.glyph = np.array([lookup[g] for w in words for g in w])
		self.word = np.repeat(np.arange(len(words)),[len(w) for w in words])
		line_ids = np.repeat(np.arange(len(lines)),[sum(map(len,l['words'])) for l in lines])
		self.scope = {'continuous':np.zeros(len(self.glyph),dtype=int),'line':line_ids,'word':self.word}[scope]
		starts = np.r_[0,np.flatnonzero(np.diff(self.scope))+1]
		local = np.arange(len(self.glyph))-np.repeat(starts,np.diff(np.r_[starts,len(self.glyph)]))
		self.mask = local % 2 == offset
		self.counts = {kind:np.bincount(group[self.mask],minlength=int(group[-1])+1) for kind,group in [('word_matched',self.word),('scope_matched',self.scope)]}

	def random_mask(self,rng,kind):
		group = self.word if kind == 'word_matched' else self.scope
		order = np.lexsort((rng.random(len(group)),group))
		starts = np.r_[0,np.flatnonzero(np.diff(group[order]))+1]
		ranks = np.arange(len(group))-np.repeat(starts,np.diff(np.r_[starts,len(group)]))
		mask = np.zeros(len(group),dtype=bool)
		mask[order] = ranks < self.counts[kind][group[order]]
		return mask

	def sample(self,rng,kind):
		mask = self.random_mask(rng,kind)
		g,w = self.glyph[mask],self.word[mask]
		def h(counts):
			counts=counts[counts>0]
			if not len(counts): return 0.0
			p=counts/counts.sum()
			return float(-(p*np.log2(p)).sum())
		valid = w[:-1] == w[1:]
		a,b=g[:-1][valid],g[1:][valid]
		pairs=np.bincount(a*self.size+b,minlength=self.size**2)
		starts=np.bincount(a,minlength=self.size)
		triples=(w[:-2]==w[2:])
		return dict(h1=h(np.bincount(g,minlength=self.size)),h2=h(pairs)-h(starts),
			adjacent_repeat=float(np.mean(a==b)) if len(a) else 0.0,
			triple_repeat=float(np.mean((g[:-2]==g[1:-1])[triples] & (g[1:-1]==g[2:])[triples])) if triples.any() else 0.0)


def read_source(path):
	return path.read_bytes() if path.exists() else gzip.decompress(Path(str(path)+'.gz').read_bytes())


def run(replicates, seed, output, only=None):
	if replicates < 2:
		raise ValueError('At least two controls required')
	output.mkdir(parents=True, exist_ok=True)
	configs = [('RF1b','RF1b.txt',True,0), ('ZL3b','ZL3b.txt',True,0),
		('ZL3b_join','ZL3b.txt',False,0), ('ZL3b_alt','ZL3b.txt',True,1), ('IT2a','IT2a.txt',True,0),
		('ZL3b_EVA','ZL3b-n.txt',True,0)]
	all_results = dict(seed=seed, replicates=replicates, primary='RF1b h2 lower tail word_matched; six variants, Bonferroni 6', datasets={})
	for name, filename, comma, alt in configs:
		if only and name not in only:
			continue
		source = ROOT/'data/raw'/filename
		source_bytes = read_source(source)
		lines, audit = parse(source_bytes.decode(), comma, alt, name.endswith('_EVA'))
		(ROOT/'data/derived'/f'{name}.json').write_text(json.dumps(lines, separators=(',',':'))+'\n')
		entry = dict(source_sha256=hashlib.sha256(source_bytes).hexdigest(),audit=audit,
			baseline=metrics([w for line in lines for w in line['words']]), variants={})
		for scope in ('continuous','line','word'):
			for offset in (0,1):
				variant = f'{scope}_{offset}'
				words = transform(lines,scope,offset)
				observed = metrics(words)
				(output/f'{name}_{variant}.txt').write_text('\n'.join(' '.join(w) for w in words)+'\n')
				item = dict(observed=observed, controls={})
				fast = FastControls(lines,scope,offset)
				for control in ('word_matched','scope_matched'):
					control_seed = int.from_bytes(hashlib.sha256(f'{seed}:{name}:{variant}:{control}'.encode()).digest()[:8],'big')
					rng = np.random.default_rng(control_seed)
					rows = [fast.sample(rng,control) for _ in range(replicates)]
					item['controls'][control] = dict(seed=control_seed,comparison=compare(observed,rows),replicates=rows)
				entry['variants'][variant] = item
				print(name,variant,'h2',round(observed['h2'],4),flush=True)
		all_results['datasets'][name] = entry
	(output/'results.json').write_text(json.dumps(all_results,indent=2,sort_keys=True)+'\n')
	return all_results


if __name__ == '__main__':
	p = argparse.ArgumentParser(description=__doc__)
	p.add_argument('--replicates',type=int,default=199)
	p.add_argument('--seed',type=int,default=20261014)
	p.add_argument('--output',type=Path,default=ROOT/'results')
	p.add_argument('--only',nargs='+',help='Optional subset of named dataset configurations')
	a = p.parse_args()
	run(a.replicates,a.seed,a.output,a.only)
