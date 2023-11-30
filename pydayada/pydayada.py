import re
import math
import random
has_crypto = True
try:
    import simplecrypto
except:
    has_crypto = False
import logging
from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class lang:
    def __init__(self, name, consonants, matches, vowels, initials, finals, termination, syl_max_len, marker):
        # start with sanity checks
        if len(matches) != 0 and len(consonants) != len(matches):
            raise Exception("Number of consonants does not match number of consonantal matches")
        if math.gcd(len(consonants), len(vowels)) != 1:
            raise Exception("Consonants and vowels cannot have common multiples")
        if not lang.ispower2(len(initials)):
            raise Exception("Initials have to be a power of 2")
        if not lang.ispower2(len(finals)):
            raise Exception("Finals have to be a power of 2")
        self.name = name
        self.consonants = consonants
        self.matches = matches
        self.vowels = vowels
        self.initials = initials
        self.finals = finals
        self.termination = termination
        self.syl_max_len = syl_max_len
        self.marker = marker

    def ispower2(num):
        if num < 0:
            return False
        if num == 0:
            return True
        if num != math.pow(2, math.log2(num)):
            return False
        return True
        
class dayada:
    def __init__(self):
        self.langs = [ 
            lang( 
                "en", 
                ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "R", "S", "T", "V", "W", "X", "Z", "BL", "BR", "CH", "CR", "CL", "DR", "FL", "GL", "GN", "GR", "KN", "PH", "PL", "PR", "RH", "ST", "SP", "SH", "WH", "TH", "TR", "WR", "STR", "SHR"], 
                ["R", "N", "S", "L", "N", "M", "L", "P", "S", "R", "S", "L", "N", "M", "R", "N", "H", "N", "M", "N",  "S",  "M",  "L",  "S",  "N",  "S",  "D",  "S",  "N",  "S",  "L",  "N",  "N",  "S",  "N",  "N",  "M",  "T",  "N",  "M",  "S",   "N",   "L"], 
                ["A", "E", "I", "O", "U", "AE", "AI", "AY", "EE", "OO", "OU", "AU"], 
                ["A", "E", "I", "O", "U", "EU", "AI", "YO"], 
                ["R", "S", "T", "N", "RD", "ST", "NT", "NG"], 
                "SZ", 
                3, 
                "YA DAYADA" 
            ), 
            lang( 
                "jp", 
                ["",  "K", "S", "T", "H", "M", "Y", "R", "W"], 
                ["N",  "N", "N", "N", "N", "N", "N", "N", "N"], 
                ["A", "I", "U", "E", "O"], 
                [ ], 
                [ ], 
                "X", 
                3, 
                "YA TAYATA" 
            ), 
            lang( 
                "it", 
                ["B", "C", "D", "F", "G", "L", "M", "N", "P", "R", "S", "T", "V", "Z", "BR", "CR", "CL", "FL", "FR", "GR", "PL", "PR", "SC", "ST", "SP", "TR", "STR"], 
                ["R", "C", "D", "F", "N", "B", "L", "G", "P", "R", "S", "T", "N", "Z", "N",  "S",  "N",  "F",  "R",  "N",  "S",  "M",  "N",  "R",  "L",  "L",  "S"], 
                ["A", "E", "I", "O", "U", "AI", "AU"], 
                ["A", "E", "I", "O", "U", "EU", "AU", "AI"], 
                [ ], 
                "SZ", 
                2, 
                "ITA LIANO" 
            ), 
            lang( 
                "hi", 
                ["",  "H", "K", "L", "M", "N", "P", "W", "ʻ"], 
                [], 
                ["A", "E", "I", "O", "U", "Ā", "Ē", "Ī", "Ō", "Ū"], 
                [], 
                [], 
                "X", 
                5, 
                "KA MAʻAINA" 
            ) 
        ] 
        self.puncts = [
            [5, ", ", 8, ". ", 5, ', "', 6, '." '],
            [6, ", ", 5, ", ", 7, ". "]
        ];
        self.marker = True
        self.lang = None
        self.reset()
        
    def guess_lang(self, text):
        text = text.upper()
        text = re.sub("[-'`~!@#$%^&*()_|+=?;:'\",.<>\{\}\[\]\\\/]", '', text)
        for lang in self.langs:
            if lang.marker in text:
                return lang
            
    def find_language(self, name):
        for lang in self.langs:
            if lang.name == name:
                return lang
        return None
    
    def get_langs(self):
        return [lang.name for lang in self.langs]

    def set_default_lang(self):
        self.set_lang(self.get_langs()[0])
    
    def set_lang(self, lang):
        if isinstance(lang, str):
            lang = self.find_language(lang)
        if not lang:
            return
        self.lang = lang
        self.consonants_len = len(self.lang.consonants)
        self.vowels_len = len(self.lang.vowels)
        self.vowel_re = re.compile("[{}]+".format("".join(self.lang.vowels)), re.IGNORECASE)
        self.finals_len = self.get_power(self.lang.finals)
        self.initials_len = self.get_power(self.lang.initials)
        self.max_syl = self.consonants_len * self.vowels_len
        self.syl_max_len = self.lang.syl_max_len
        self.core_len = math.floor(math.log2(self.max_syl))
        self.exp2_syl = int(math.pow(2, self.core_len))
        self.allchars = "".join(set(self.lang.consonants + self.lang.matches + self.lang.vowels + self.lang.initials + self.lang.finals + list(self.lang.marker)))
        
    def get_power(self, l):
        if len(l) == 0:
            return -1
        return math.ceil(math.log2(len(l)))
    
    def reset(self):
        self.syl_len = 0
        self.bindata = ""
        self.bindata_cache = ""
        self.hexdata = ""
        self.yaddata = ""
        self.terminate = False
        self.first = True
        self.consonantal = False

    def set_marker(self, mark):
        self.marker = mark

    def encrypt(self, pwd, data, lang = None):
        if lang:
            self.set_lang(self.find_language(lang))
        x = simplecrypto.encrypt(data, pwd)
        enc = self.morph(x, "base64", "hex")
        dayada = self.encodehex(enc)
        return dayada

    def decrypt(self, pwd, data):
        adayad = self.decodehex(data)
        content = self.morph(adayad, "hex", "base64")
        recontent = simplecrypto.decrypt(content, pwd)
        if not recontent:
            recontent = data
        return recontent

    def encode(self, data):
        return self.encodehex(self.morph(data, None, "hex"))

    def encodehex(self, h):
        if self.lang is None:
            self.set_default_lang()
        self.reset()
        self.hexdata = h
        while True:
            self.yaddata += self.syl_encodehex()
            if self.terminate:
                break
        if self.marker:
            self.yaddata = self.add_dayada(self.yaddata)
        self.yaddata = self.add_punctuation(self.yaddata)
        self.yaddata = self.add_capitalization(self.yaddata)
        return self.yaddata 

    def decode(self, yada, format = "hex"):
        return self.morph(self.decodehex(yada), "hex", format)

    def decodehex(self, yada):
        if self.lang is None:
            self.set_default_lang()
        self.reset()
        self.yaddata = yada
        # turn all upper
        self.yaddata = self.yaddata.upper()
        # remove punctuation
        self.yaddata = re.sub("<[^>]*>", "", self.yaddata, )
        self.set_lang(self.guess_lang(self.yaddata))
        self.yaddata = re.sub("[^"+self.allchars+"]", "", self.yaddata, flags=re.IGNORECASE)
        # remove ya dayada
        if (self.yaddata.find(self.lang.marker + " ") != -1):
            self.yaddata = self.yaddata.replace(self.lang.marker + " ", "")
        syl_len = 0
        while True:
            self.syl_decodehex()
            if self.terminate:
                break
        self.backtrack()
        return self.hexdata

    def backtrack(self):
        lastBit = ""
        lastHex = ""
        if (self.bindata == ""):
            lastBit = self.bin2num_hex2bin(self.hexdata[-1])[-1]
        else:
            lastBit = self.bindata[-1]
        if (lastBit == "1"):
            lastHex = "f"
        else:
            lastHex = "0"
        while (self.hexdata[-1] == lastHex):
            self.hexdata = self.hexdata[:-1]
            
    def search_vowel(self):
        m = self.vowel_re.search(self.yaddata)
        if m:
            return m.start()
        else:
            return -1

    def syl_decodehex(self):
        self.syl_len += 1
        if self.first and self.initials_len > -1:
            initial = self.chomp_list(self.lang.initials)
            if (initial == -1):
                self.assemble("0", "noini")
            else:
                self.assemble("1", "ini")
                self.assemble(self.bin2num_num2bin(initial, self.initials_len), self.lang.initials[initial])
        frs = self.search_vowel()
        start = self.yaddata[:frs]
        mtc = self.find_list(start, self.lang.consonants)
        if (len(self.lang.matches) > 0):
            if mtc == -1:
                self.assemble("1", "cmatch")
                self.chomp_list(self.lang.matches)
            elif not self.first:
                self.assemble("0", "nofirstandnoc")
        con = self.chomp_list(self.lang.consonants)
        vow = self.chomp_list(self.lang.vowels)
        if con < 0 or vow < 0:
            self.terminate = True
            return
        num = con + self.consonants_len * vow
        add = ""
        if num >= self.exp2_syl:
            add = "1"
            num -= self.exp2_syl
        elif num + self.exp2_syl < self.max_syl:
            add = "0"
        self.assemble(self.bin2num_num2bin(num, self.core_len), "c("+self.lang.consonants[con]+")v("+self.lang.vowels[vow]+")")
        if add != "":
            self.assemble(add, "excess")
        frs = self.search_vowel()
        if (frs == -1):
            if self.finals_len > -1:
                # look for finals
                fin = self.chomp_list(self.lang.finals)
                if fin != -1:
                    if (self.syl_len < self.syl_max_len):
                        self.assemble("1", "notend")
                    self.assemble(self.bin2num_num2bin(fin, 3), "f("+self.lang.finals[fin]+")")            
                else:
                    self.assemble("0", "end")
                    if (self.chomp_list([self.lang.termination]) != -1):
                        self.assemble("1", "term")
                    else:
                        self.assemble("0", "noterm")
            self.terminate = True
            return
        
        spc = self.yaddata.find(" ")
        if spc == -1:
            spc = len(self.yaddata)

        if frs > spc:
            if self.syl_len < self.syl_max_len:
                self.assemble("1", "endword")
            self.syl_len = 0
            if self.finals_len > -1:
                fin = self.chomp_list(self.lang.finals)
                self.assemble(self.bin2num_num2bin(fin, 3), "f("+self.lang.finals[fin]+")")
            self.chomp_list([" "])
            self.first = True
        else:
            self.first = False
            self.assemble("0", "moresyl")

    def get_assembly(self):
        return self.bindata_cache
    
    def assemble(self, s, part):
        self.bindata += s
        self.bindata_cache += s + " " + part + " "
        while len(self.bindata) > 3:
            self.hexdata += self.bin2num_bin2hex(self.bindata[:4])
            self.bindata = self.bindata[4:]

    def chomp_list(self, l):
        if len(l) == 0:
            return -1
        for i in reversed(range(len(l))):
            if self.yaddata.startswith(l[i]):
                self.yaddata = self.yaddata[len(l[i]):]
                return i
        return -1

    def find_list(self, s, l):
        for i in reversed(range(len(l))):
            if (s == l[i]):
                return i
        return -1

    def syl_encodehex(self):
        self.syl_len += 1
        if self.terminate:
            return ""
        syl = ""
        consonantal = False
        if (self.first):
            if self.initials_len > -1:
                initial = self.chomp(1, "ini")
                if (initial):
                    index = self.chomp(self.initials_len, "idx")
                    syl += self.lang.initials[index]
        else:
            if len(self.lang.matches) > 0:
                consonantal = self.chomp(1, "cmatch")
        num = self.chomp(self.core_len, "syl")
        if num + self.exp2_syl < self.max_syl:
            num += self.chomp(1, "excess") * self.exp2_syl
        con = self.lang.consonants[num % self.consonants_len]
        vow = self.lang.vowels[int(num / self.consonants_len)]
        if consonantal:
            syl += self.lang.matches[num % self.consonants_len]
        syl += con + vow

        ter = 1
        if (self.syl_len >= self.syl_max_len):
            self.syl_len = 0
        else:
            ter = self.chomp(1, "end")
        cst = 0
        if ter:
            if self.finals_len > -1:
                syl += self.lang.finals[self.chomp(self.finals_len, "final")]
            syl += " "
            self.syl_len = 0
        self.first = ter
        return syl

    def add_dayada(self, s):
        pos = .2 + .6*random.random()
        spc = s.find(" ", int(pos * len(s)))
        s = s[:spc] + " " + self.lang.marker + s[spc:]
        return s

    def characteristic(self, punc):
        res = 0
        for p in punc:
            if isinstance(p, int):
                res += p
        return res

    def add_punctuation(self, s):
        s = s.strip()
        l = s.split(' ')
        res = ''
        while len(l) > 0:
            punctuation = random.choice(self.puncts)
            if self.characteristic(punctuation) > len(l):
                punctuation = [len(l), "."]
            for item in punctuation:
                if isinstance(item, int):
                    res += " ".join(l[:item])
                    l = l[item:]
                else:
                    res += item
        return res

    def add_capitalization(self, s):
        # make everything lowercase, except after .!?, or after ', "' and '."'
        if len(s) > 1:
            s = s[0].upper() + s[1:].lower()
        else:
            s = s.upper()
        uc = ['. ', '! ', '? ', ', "', '." ', ">"]
        for up in uc:
            pos = 0
            while True:
                pos = s.find(up, pos)
                if pos == -1:
                    break
                np = pos + len(up)
                if np < len(s):
                    s = s[:np] + s[np].upper() + s[np + 1:]
                pos += 1
        return s

    def chomp(self, b, part):
        if len(self.hexdata) == 0:
            if "1" not in self.bindata or "0" not in self.bindata:
                self.terminate = True
        else:
            while len(self.bindata) < b:
                h = self.hexdata[0]
                self.hexdata = self.hexdata[1:]
                self.bindata += self.bin2num_hex2bin(h)
                if len(self.hexdata) == 0:
                    if (self.bindata[-1] == "0"):
                        self.bindata = self.bindata + "1111111111111111111111"
                    else:
                        self.bindata = self.bindata + "0000000000000000000000"
        out = self.bindata[:b]
        self.bindata = self.bindata[b:]
        self.bindata_cache += out + " " + part + " "
        return self.bin2num_bin2num(out)
        
    def bin2num_bin2num(self, b):
        res = 0
        for c in b:
            res = 2 * res + (ord(c) - 48)
        return res

    def bin2num_num2bin(self, num, l):
        num = int(num)
        p = int(math.pow(2,l-1))
        res = ""
        for i in range(l):
            bit = int(num / p)
            res += str(bit)
            num -= p * bit
            p /= 2
        return res

    def bin2num_hex2bin(self, char):
        code = ord(char[0]) - 48
        if code > 9:
            code -= 39
        return self.bin2num_num2bin(code, 4)

    def bin2num_bin2hex(self, s):
        return "0123456789abcdef"[self.bin2num_bin2num(s)]
    
    def morph(self, data, from_format, to_format):
        if from_format == None:
            if isinstance(data, str):
                from_format = "str"
                # guess
                if re.match("^[0-9A-Fa-f]*$", data) and len(data) % 2 == 0:
                    from_format = "hex"
                elif re.match("^[0-9A-Za-z_=]*$", data):
                    from_format = "base64"
            else:
                from_format = "bytes"
                
        # uses bytes as intermediate format
        if from_format == "base64":
            data = b64decode(data)
        elif from_format == "hex":
            data = unhexlify(data)
        elif from_format == "str":
            if type(data) == str:
                data = bytes(data, "utf-8")
        
        if to_format == "base64":
            data = b64encode(data).decode()
        elif to_format == "hex":
            data = hexlify(data).decode()
        elif to_format == "str":
            if type(data) != str:
                data = str(data, "utf-8")
        elif to_format == "bytes":
            if type(data) != bytes:
                data = bytes(data, "utf-8")

        return data

def main():
    import argparse
    import sys
    loglmap = {"NOTSET": logging.NOTSET, "DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL}
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--encode', action='store_true')
    parser.add_argument('-x', '--encrypt', action='store_true')
    parser.add_argument('-y', '--decrypt', action='store_true')
    parser.add_argument('-d', '--decode', action='store_true')
    parser.add_argument('-p', '--password')
    parser.add_argument('-l', '--language', default="en")
    parser.add_argument('-o', '--output') # the default output is stdout, which doesn't need to be specified
    parser.add_argument('-f', '--output_format', choices=['bytes', 'str', 'base64', 'hex'])
    parser.add_argument('-F', '--input_format', choices=['bytes', 'str', 'base64', 'hex'], default="str")
    parser.add_argument('--loglevel', choices=loglmap.keys(), default="INFO")
    parser.add_argument('infile', default='-')
    o = parser.parse_args()

    def abort(*msg):
        print(*msg)
        exit(1)
    modes = 'encode, encrypt, decrypt, decode'
    op_modes = [o.__dict__[x] for x in modes.split(', ')]
    true_modes = [x for x in op_modes if x]
    if len(true_modes) == 0:
        abort("Must specify mode, one of", modes)
    elif len(true_modes) > 1:
        abort("Only one operating mode can be specified")
    if (o.encrypt or o.decrypt) and o.password is None:
        abort("Encryption and decryption require a password (-p or --password option)")

    if (o.encrypt or o.decrypt) and not has_crypto:
        abort("Encryption/decryption selected by simplecrypto library not found. Install simplecrypto first using 'pip3 install simplecrypto'")

    d = dayada()
    langs = [l.name for l in d.langs]
    if o.language not in langs:
        abort("Unknown language", o.language)

    if o.infile == '-':
        data = sys.stdin.read()
    else:
        with open(o.infile, 'rb') as f:
            data = f.read()
    d.set_lang(o.language)
    if o.encode:
        out = d.encode(d.morph(data, o.input_format, "hex"))
    elif o.decode:
        out = d.decode(data, o.output_format)
    elif o.encrypt:
        out = d.encrypt(o.password, d.morph(data, o.input_format, "bytes"))
    elif o.decrypt:
        out = d.morph(d.decrypt(o.password, data), None, o.output_format)
    if o.output == '-' or o.output is None:
        print(out)
    else:
        with open(o.output, 'wb') as f:
            f.write(out)

if __name__ == "__main__":
    main()
