# SPDX-License-Identifier: MS-PL
import random
import sys
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from analyse import parse, transform, metrics, FastControls
import numpy as np


class ScientificContracts(unittest.TestCase):
	def test_eva_compounds_and_minims(self):
		text='#=IVTFF Eva- 2.0 M 5\n<f1r>\n<f1r.1,@P0> chcthiin.{yk}@192;???\n'
		lines,audit=parse(text,eva=True)
		self.assertEqual(lines[0]['words'],[['ch','cth','i','i','n'],['{yk}','@192;','?']])
		self.assertEqual(audit['unknown_length_spans'],1)

	def test_fast_controls_against_scalar_metrics(self):
		lines=[dict(words=[['a','a','b','c','c'],['b'],['b','a','a','a']]),dict(words=[['c','a','b']])]
		words=[w for line in lines for w in line['words']]
		for scope in ('continuous','line','word'):
			for offset in (0,1):
				fast=FastControls(lines,scope,offset)
				for kind in ('word_matched','scope_matched'):
					mask=fast.random_mask(np.random.default_rng(8),kind)
					self.assertEqual(int(mask.sum()),sum(map(len,transform(lines,scope,offset))))
					filtered=[]; pos=0
					for w in words:
						filtered.append([g for j,g in enumerate(w) if mask[pos+j]])
						pos+=len(w)
					if kind=='word_matched':
						self.assertEqual(list(map(len,filtered)),list(map(len,transform(lines,scope,offset))))
					actual=fast.sample(np.random.default_rng(8),kind)
					for key,value in actual.items():
						self.assertAlmostEqual(value,metrics(filtered)[key])

	def test_glyphs_metadata_and_boundaries(self):
		text = '#=IVTFF STA1 2.0 M 5\n<f1r> <! $L=A>\n<f1r.1,@P0> <%>K1A1,[U2:A1Q2A1]C1<->Z1<$>\n'
		lines,audit = parse(text)
		self.assertEqual(lines[0]['words'],[['K1','A1'],['U2','C1'],['Z1']])
		self.assertEqual(audit['glyphs'],5)
		self.assertEqual(parse(text,False)[0][0]['words'][0],['K1','A1','U2','C1'])
		self.assertEqual(parse(text,True,1)[1]['glyphs'],7)

	def test_offsets_and_resets(self):
		lines = [dict(words=[list('abc'),list('de')]),dict(words=[list('fgh')])]
		self.assertEqual(transform(lines,'continuous',0),[list('ac'),['e'],['g']])
		self.assertEqual(transform(lines,'line',0),[list('ac'),['e'],list('fh')])
		self.assertEqual(transform(lines,'word',0),[list('ac'),['d'],list('fh')])
		self.assertEqual(transform(lines,'word',1),[['b'],['e'],['g']])
		for scope in ('continuous','line','word'):
			left,right = transform(lines,scope,0),transform(lines,scope,1)
			for original,a,b in zip([list('abc'),list('de'),list('fgh')],left,right):
				self.assertCountEqual(a+b,original)

	def test_random_matching_and_order(self):
		lines = [dict(words=[list('abcde'),list('f'),list('ghij')])]
		for scope in ('continuous','line','word'):
			for offset in (0,1):
				deterministic = transform(lines,scope,offset)
				for seed in range(20):
					random_words = transform(lines,scope,offset,random.Random(seed))
					self.assertEqual(list(map(len,random_words)),list(map(len,deterministic)))
					for original,word in zip(lines[0]['words'],random_words):
						self.assertEqual(word,sorted(word,key=original.index))

	def test_rejects_unparsed_not_silently_deleted(self):
		with self.assertRaises(ValueError):
			parse('#=IVTFF STA1 2.0 M 5\n<f1r>\n<f1r.1,@P0> K1?A1\n')

	def test_entropy_and_no_cross_word_pairs(self):
		self.assertEqual(metrics([['a','a'],['b','b']])['h2'],0)
		self.assertEqual(metrics([['a'],['b']])['adjacent_repeat'],0)
		self.assertEqual(metrics([['a','a','a']])['triple_repeat'],1)


if __name__ == '__main__':
	unittest.main()
