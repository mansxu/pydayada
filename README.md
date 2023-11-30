<h1 align="center">
pydayada
</h1>
<p align="center">
A variable length text encoding that takes binary data and turns it into semi-readable text in a bunch of different "languages." 
</p>

# Rationale

I often need a way to encode (usually encrypted) binary data as plain text to send as SMS or email. With Dayada encoding, you can specify a "language" to use and you receive something resembling normal text you can copy/paste/send. This text can be hidden in other text or shared simply as is. Once desired, the text can be decoded as binary data.

This library came about because my hosting and my email provider both complained about spam messages I received on contact forms on sites I own. They saw the obvious spam I both sent and received and decided I was abusing their service. So, instead of sending the messages in cleartext, I needed to somehow hide the offensive content.

All available forms of encoding seemed to suffer from the problem that they were easily detected and raised suspicion, be it ZIP files, base64 encoded data, or the similar. We live in a world full of abuse, sadly.

But the Dayada encoding allowed me to send data as what looked like human readable text in something resembling language, avoiding pretty much all detection and surviving even major mangling and wrangling.

## Use Cases

- You want to send an image over a messenger client that doesn't allow transfer of binary files
- You want to include an encoded message to someone without making it obvious (obfuscation)
- You want to store a message for the short term in relative safety (encryption)
- You want to generate natural-looking text that is legible for use as filler text
- You want to generate natural-looking words that can be used as randomized names

## Examples

- Yohiya su a yu mi, si kohi sina wike so e mi muwaru. Kunse yuriwu ku yo hinyuru, "Sinkata te erunmi hoye ho wa." U hahi taro mo una ue ya tayata hunruse ru hahiya tu ka urenhe.
- Fosstri ucobra vorfrau froblo si aspisplai, ovo luma ufungu si ispi, soddi plorfri si odu epli ubride trespli. Si ovagni strausi ita liano ucli auscospi austestra claunvi usi bro.
- Liʻimōuwa lōwuhu wī mi hī, nī u kānē o mamō nō kākawīluwu ʻi. Lānā wiʻao hā kuwu ōkī, "Ūpo he hī wū lī wā." Lēwenāo ka maʻaina ʻu nānē mōkīpo kō lī ʻamū.

All three "sentences" above are encoded forms of "The quick brown fox jumped over the lazy dog's head". They were obtained by running the code:

echo "The quick brown fox jumped over the lazy dog's head" | pydayada --encode --language {language chosen} -

Note that decoding can be done without specifying the "language." The correct "language" is inferred from content. Conversely, the "language" marker can be removed if the "language" is specified explicitly.

## History

The Dayada encoding was originally created as a Joomla Javascript extension. Users would highlight text in blog posts, click a button, and find the text encrypted and encoded in their original text.

When the text was presented to users, clicking on encrypted text would prompt entry of a password and the encrypted and encoded text would be replaced by the cleartext version.

Storing text, even encrypted and encoded, in a public place is a terrible idea and was hence abandoned, but the idea for Dayada encoding was born.

## Name

The **Dayada Encoding** gets its name from the phrase, "yada yada," meaning "and so on." It is a phrase commonly used in the show, *Seinfeld* and the author (of the encoding, not of the show) may have been watching an episode as the naming was introduced.

To facilitate decoding of Dayada-encoded passages, a marker phrase is inserted that is removed on detection. The `en` "language" in Dayada is marked by the phrase `ya dayada`.

# Installation

## Install using `pip`
*Note: Installation using `pip` is not available yet.*
```console
$ python3 -m pip install --user pydayada
```

## Install using `git`
```
$ git clone https://github.com/mansxu/pydayada
$ cd pydayada
$ python3 setup.py install
```

Please not that pydayada depends on pycryptodome and simplecrypto for its encryption/decryption components. If you just want to use the encoding/decoding functionality, you can remove the dependency in setup.py.

# Usage

## Console
```console
usage: pydayada [-h] [-c] [-x] [-y] [-d] [-p PASSWORD] [-l LANGUAGE] [-o OUTPUT] [-f {bytes,str,base64,hex}] [-F {bytes,str,base64,hex}] sinfile

positional arguments:
  infile

options:
  -h, --help            show this help message and exit
  -c, --encode
  -x, --encrypt
  -y, --decrypt
  -d, --decode
  -p PASSWORD, --password PASSWORD
  -l LANGUAGE, --language LANGUAGE
  -o OUTPUT, --output OUTPUT
  -f {bytes,str,base64,hex}, --output_format {bytes,str,base64,hex}
  -F {bytes,str,base64,hex}, --input_format {bytes,str,base64,hex}
```

## Library
```
import pydayada

engine = pydayada.dayada()
engine.set_lang('en')
out = engine.encode('The quick brown fox')
print(out)
in = engine.decode(out)
assert('The quick brown fox' == in)
```

# Reference

## "Languages"

Dayada "languages" are constituted of a series of phonological and phonotactical roles that are generally taken from existing languages, whose alphabet the "languages" also take on.

Words in the "languages" are constituted of a possibile list of initials, of regular syllables, and of finals. Regular syllables are constituted either of a list of allowed syllables or of combinations of vowels and consonants, where both vowels and consonants can be made up of more than one letter (diphtongs for vowels and clusters for consonants). Words also have a maximum length.

To encode an original message, the engine takes as many bits from its beginning as required for the next section. If the language provides 8 initials (which means word-beginning syllables), then 3 bits are taken from the message. The next segment of the word is determined by considering following bits.

When it comes to syllables, the constituent parts (vowels and consonants) must be relatively prime, such that the the number of bit fitting into the product can be uniquely considered. In a "language" with 5 vowels and 9 consonants, there are 45 possible combinations, meaning each at most 5 bits fit into the syllable. To make it possible to have all syllables present, the remaining syllables are considered modulo 32. Which of the modulo pairs is used is determined by random chance.

After each syllable, a bit is used to determine if the word is terminated, except if the word already reached the maximum allowed length for the language. In this case, the word is terminated without reading the next bit.

Capitalization, punctuation, and other non-alphabetical markers can be placed into the text as preferred. In general, it is a good idea to take some existing text and copy sentence structure and punctuation, then apply this to the Dayada text. Everything that is not part of the language alphabet is stripped before decoding.

## Creating "Languages"

The four "languages" provided with the engine are just examples and can be extended with the same mechanism. Just copy any of the language arrays into a new element and edit as desired/required. As long as identical copies of the array elements are used to encode and decode, the same message is going to be present at both ends.

The inspiration for the example languages gave them their short names:

- "en" is inspired by English. Only the English alphabet is used and the word rules prefer relatively short words with consistent endings
- "jp" is inspired by Latinized Japanese. Again, only English alphabet letters are used, but the syllable structure is much more consistent between mid-word and final syllables
- "it" is inspired by Italian. It doesn't use any of the accented letters but uses Italian inspired phonology (which includes an alphabet without K, J, W, X, Y)
- "hi" is inspired by Hawaiian. It has special characters that only exist in Hawaiian (mainly vowels with a macron). Because of this, sentences in the hi "language" are generally shorter than in the other three languages in characters but may potentially be lost in transmission where only ASCII characters are allowed

Please note that the short names of the default "languages" indicate inspiration by phonology. None of the "languages" would be recognized by native speakers as anything other than gibberish, and the goal of the Dayada encoding is not natural language generation.

## Efficiency

As you can see in the example above, the Dayada encoding is very inefficient in terms of lenght of encoded messages. Its goal is not to encode large amounts of data, but to provide an Internet messaging-safe way to transmit small chunks of information.

For that reason, the Dayada engine is not programmed for high performance or throughput. Instead, it is programmed for legibility and consistency of the source code.

## Encryption

Strictly speaking, Dayada is simply an *encoding*: it is just a different representation of source data that hides it from view only if the encoding is unknown. If an attacker knows that Dayada has been used to hide information, it can be decoded painlessly.

Because one of the more obvious uses of Dayada is to transmit small pieces of information that have been encrypted, password-protected, and then made "legible" to messaging systems, a simple encryption engine is built in. To use it, specify the options --encrypt or --decrypt instead of the corresponding --encode or --decode, and provide a password. While using the library, use the encrypt() or decrypt() methods similarly.

The en/de-cryption routines are provided by `simplecrypto` and are optional. You can use pydayada without those, but then en/de-cryption will not be available. You can of course use any tool you'd like, to encrypt source data and encode the resulting blog using pydayada. This includes asymmetic encryption.

# Risks

## Malware Abuse

As any technology, the dayada encoding can be abused. Of particular concern are uses to hide malware, which could be embedded in a regular text stream, decoded using Dayada, and run on the target machine.

This would initially work, because malware detectors function by pattern recognition, and since modifying a "language" in Dayada encoding is trivial, all such patterns would be quickly moot.

In the long term, this could lead to the Dayada decoder being detected as malware, as it is absolutely required to decode the malware and hence constitutes a less trivial commonality between malware vectors.

## Character Stripping

It is generally presumed that text processing never modifies or filters the ASCII alphabet letters, which are the only letters present in the "en", "jp", and "it" "languages". Of these three, the "jp" language has the fewest letters (5 vowels and 9 consonants) and is hence the least likely to be filtered (and accordingly also the most inefficient).

Notice that English alphabet letters are identical in their ASCII encoding and UTF-8 encoding, such that the "languages" that only use those do not usually require an explicit encoding marker.

Other languages, like "hi," may see some software strip characters or mangle them. Please notice that there is no general way to reverse the encoding in this case.

## Detection

### Repetitive Source

Because of its nature as variable encoding, it is hard to detect Dayada encoded streams. Source material that is very repetitive, on the other hand, will generally be encoded in a repetitive manner. In this case, it is advantageous to encrypt or compress the source material, as the resulting blobs are not as repetitive.

### Language Detection

Should a Dayada-encoded message be processed by a natural language processor, no existing language would be detected and the message may be flagged. This can only be avoided by using a natural language generator, in which case the encoding would be much more wasteful.
