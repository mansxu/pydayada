#! /usr/bin/env python
import sys
from os import path
project_root = path.join(path.abspath(__file__), '..', '..', '..')
sys.path.append(path.normpath(project_root))

import random
import unittest
from pydayada import dayada

text = "The quick brown fox jumped over the lazy dog's head"
rand = random.randbytes(256)

class TestLang(unittest.TestCase):
    def test_langs(self):
        d = dayada()
        for lang in d.get_langs():
          d.set_lang(lang)

class TestMorph(unittest.TestCase):
    def test_morph_str_str(self):
        d = dayada()
        o = d.morph(text, "str", "str")
        self.assertEqual(text, o)

    def test_morph_str_hex(self):
        d = dayada()
        o = d.morph(text, "str", "hex")
        self.assertEqual("54686520717569636b2062726f776e20666f78206a756d706564206f76657220746865206c617a7920646f6727732068656164", o)

    def test_morph_str_base64(self):
        d = dayada()
        o = d.morph(text, "str", "base64")
        self.assertEqual("VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cncyBoZWFk", o)

    def test_morph_str_bytes(self):
        d = dayada()
        o = d.morph(text, "str", "bytes")
        self.assertEqual(str.encode(text), o)

    def test_morph_hex_str(self):
        d = dayada()
        o = d.morph("54686520717569636b2062726f776e20666f78206a756d706564206f76657220746865206c617a7920646f6727732068656164", "hex", "str")
        self.assertEqual(text, o)

    def test_morph_base64_str(self):
        d = dayada()
        o = d.morph("VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wZWQgb3ZlciB0aGUgbGF6eSBkb2cncyBoZWFk", "base64", "str")
        self.assertEqual(text, o)

    def test_morph_bytes_str(self):
        d = dayada()
        o = d.morph(str.encode(text), "bytes", "str")
        self.assertEqual(text, o)

class TestEncoding(unittest.TestCase):
    def test_encode_decode_default(self):
        d = dayada()
        o = d.encode(text)
        i = d.decode(o, 'str')
        self.assertEqual(text, i)

    def test_encode_decode_languages(self):
        d = dayada()
        for lang in d.get_langs():
          d.set_lang(lang)
          o = d.encode(text)
          i = d.decode(o, 'str')
          self.assertEqual(text, i)

    def test_encode_decode_difflang(self):
        d = dayada()
        langs = random.choices(d.get_langs(), k=2)
        o, i = langs
        try:
          d.set_lang(langs[0])
          o = d.encode(text)
          d.set_lang(langs[1])
          i = d.decode(text)
        except:
          pass
        finally:
          self.assertTrue(o != i)

    def test_rand_encode_decode_languages(self):
        d = dayada()
        for lang in d.get_langs():
          d.set_lang(lang)
          o = d.encode(rand)
          i = d.decode(o, 'bytes')
          self.assertEqual(rand, i)

class TestEncrypting(unittest.TestCase):

    def test_encrypt_decode_default(self):
        d = dayada()
        pwd = random.randbytes(8)
        o = d.encrypt(pwd, text)
        i = d.decrypt(pwd, o).decode()
        self.assertEqual(text, i)

    def test_rand_encrypt_decode_default(self):
        d = dayada()
        pwd = random.randbytes(8)
        o = d.encrypt(pwd, rand)
        i = d.decrypt(pwd, o)
        self.assertEqual(rand, i)

if __name__ == '__main__':
    unittest.main()
