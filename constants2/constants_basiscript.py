"""
This is version 2.0

Version control
1.0   
Created by Wieke Harmsen (see Harmsen et al. (2021) Computational Linguistics in the Netherlands Journal)

2.0
Adaptation of version 1.0 by Sasja Westgeest. Released September 2023

2.1
Replaced "U": ["eu", "ü"] with "U": ["eu", "u"],
Removed "t" from /s/ -> "s": ["sch", "ss", "zz", "z", "c", "ç", "s", "ti"],
Removed "wa" from /wA/ -> "wA": ["oi", "o"],

"""

zero_char = "*"
place_holder_char = "#" #%

strong_verbs = ["bederven","bedriegen","beginnen","bergen","bevelen","bezwijken","bidden","bieden","bijten","binden","blazen","blijken","blijven","blinken","breken","brengen","buigen","denken","doen","dragen","drijven","dringen","drinken","druipen","duiken","dwingen","eten","fluiten","gaan","gelden","genezen","genieten","geven","gieten","glijden","glimmen","graven","grijpen","hangen","hebben","heffen","helpen","hijsen","houden","kiezen","kijken","klimmen","klinken","kluiven","knijpen","komen","kopen","krijgen","krimpen","kruipen","kunnen","laten","lezen","liegen","liggen","lijden","lijken","lopen","mijden","moeten","mogen","nemen","prijzen","rijden","rijzen","roepen","ruiken","schelden","schenden","schenken","scheppen","schieten","schijnen","schijten","schrijden","schrijven","schrikken","schuiven","slaan","slapen","slijten","sluipen","sluiten","smelten","smijten","snijden","snuiven","spijten","spreken","springen","spuiten","staan","steken","stelen","sterven","stijgen","stinken","strijden","strijken","stuiven","treden","treffen","trekken","vallen","vangen","varen","vechten","verbieden","verdwijnen","vergelijken","vergeten","verlaten","verliezen","verslinden","verzinnen","verzwelgen","vinden","vliegen","vragen","vreten","vriezen","wegen","werpen","weten","wijken","wijten","wijzen","winden","worden","wrijven","wringen","zenden","zien","zijn","zingen","zinken","zitten","zoeken","zuigen","zuipen","zullen","zwellen","zwemmen","zwerven","zwijgen"]

adapt_consonants = "qwrtpsdfghjklzxcvbnmQWRTPSDFGHJKLZXCVBNMñç"

single_cons = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z"]
double_cons = ["bb", "cc", "dd", "ff", "gg", "hh", "jj", "kk", "ll", "mm", "nn", "pp", "qq", "rr", "ss", "tt", "vv", "ww", "xx", "zz"]

all_vowels = ["aa", "ee", "oo", "uu", "ie", "a", "e", "o", "u", "i"]
short_vowels = ["a", "e", "o", "u", "i"]
long_vowels = ["aa", "ee", "oo", "uu", "ie"]

short_vowels_phon = ["A", "E", "O", "I", "U"]
long_vowels_phon = ["a", "e", "i", "o", "y", "u", "EU", "UI", "AU"]


#Phonetic dictionary
#Dictionary in which each phoneme is mapped with its graphemic equivalents
phon_dict = {
    "a": ["aa", "a", "ä", "á", "ah"],
    "A": ["a", "e", "ä", "ah"],
    "b": ["bb", "b"],
    "d": ["dd", "d", "t"],
    "dZ": ["j"],
    "e": ["eeu", "ae", "ai", "ee", "é", "e", "ë", "ay"],
    "@": ["ij", "e", "i", "u", "ë"],
    "E": ["a", "e", "i", "ë", "aï", "è"],
    "E2": ["ae", "ai", "è", "e", "aï", "fin"],
    "EI": ["ei", "ij", "eï"],
    "f": ["ff", "ph", "f", "v"],
    "g": ["g", "k"],
    "G": ["gg", "g"],
    "h": ["h"],
    "i": ["ieu", "ea", "ee", "ie",  "i", "ij", "y", "ï", "í"],
    "I": ["i", "y", "ï"],
    "Iks": ["x"],
    "j": ["ill", "i", "j", "y", "ï", "oi"],
    "ja": ["a"],
    "jAU": ["auw"],
    "k": ["ch", "kk", "qu", "k",  "c", "cc", "q"],
    "ks": ["cc", "x", "ks"],
    "kw": ["qu", "kw"],
    "l": ["ll", "l"],
    "m": ["mm", "m"],
    "n": ["nn", "n", "ñ"],
    "nj": ["gn", "nh", "nj"],
    "N": ["ng", "n"],
    "o": ["eau", "au", "oo", "oi", "o", "ö","ó", "oa"],
    "EU": ["eu"],
    "U": ["eu", "u"],
    "UI": ["eui", "ui", "uï"],
    "O": ["o", "ö", "oh"],
    "p": ["pp", "p", "b"],
    "r": ["rr", "r"],
    "s": ["sch", "ss", "zz", "z", "c", "ç", "s", "ti"],
    "S": ["ch", "sh", "si", "sj", "ci", "stj"],
    "t": ["th", "tt", "t", "d", "dt"],
    "ts": ['t', 'z'],
    "u": ["oe", "oo", "ou", "ü", "u"],
    "v": ["v", "f"],
    "w": ["ww", "u", "w", "uw"],
    "wA": ["oi", "o"],
    "wa": ["a"],
    "wI": ["uï", "wi"],
    "AU": ["auw", "ouw", "au", "ou", "ow"],
    "x": ["ch", "g"],
    "y": ["u", "uu", "ü", "ú"],
    "U": ["u"],
    "z": ["z", "s"],
    "Z": ["ti", "g", "j"]
}  

# toegevoegd: 
# p: b
# k: cc, q
# ts: t
# E2: fin (Enfin --> A f E2)
# @: en (gegeten)
# wA: o (foyer --> f w A j e)
# TOCH WEGGEHAALD! e: er (zie hierboven), ay 
# a: ah (beha)
# O: oh (goh)
# o: oa (downloaden)
# j: oi (nooit)
# t: dt
# s: ti (vakantie --> v a k A n s i)
# w: uw (eeuw)
# Iks: i (x-as)
# dZ: j
# A: ah
# ts: z (pizza)
# ja: a (musea)
# wa: a
# jAU: auw (miauw)

# yoghurt	j O G U r t (waar zit de h?)

multi_phon_dict = {
    "k": ["s", "w"],
    "n": ["j"],
    "w": ["A", "I"]
}

multi_graph_dict = {
    "N": ["g", 2, "G"],
    "AU": ["w", 3, "w"],
    "s": ["x", 3, "x"],
    "t": ["h", 2, "h"]
}

punctuation = [x for x in ".!?,;\:#(){}[]'`/…\"’°‘=+±€%$´|"]
numbers = [x for x in "1234567890"]

cons_dict = {
    "voiced_chars":["b", "d", "g", "v", "z", "g", "g"],
    "unvoiced_chars": ["p", "t", "k", "f", "s", "sj", "ch"],
    "voiced_phons": ["b", "d", "g", "v", "z", "Z", "G"],
    "unvoiced_phons": ["p", "t", "k", "f", "s", "S", "x"]
}


pcus_letters = set()
for value in phon_dict.values():
    pcus_letters.update(value)
pcus = list(pcus_letters) + punctuation + numbers