# Multiple sequence alignment on Dutch phoneme and grapheme strings
This repository contains scripts to perform phoneme-grapheme, grapheme-grapheme, phoneme-phoneme and multiple sequence alignment for the Dutch language.


## ADAPT: Algorithm for Dynamic Alignment of Phoneme Transcriptions
An algorithm to align two phoneme strings, written in the ADAPT Computer Phonetic Alphabet. For a description of how this CPA links to IPA, see the attached pdf. For a description of the implementation of the algorithm, see [this paper by Elffers et al. (2013)]({https://lands.let.ru.nl/literature/elffers.2005.1.pdf). The phonetic feature definitions are obtained from [Cucchiarini (1993)](https://lib.ugent.be/catalog/rug01:000310899) and [Cucchiarini (1996)](https://doi.org/10.3109/02699209608985167).

'''
python3 run.py --type 'adapt' --target_phonemes 'k EI k @' --realised_phonemes 'k i s'
'''


## ADAGT: Algorithm for Dynamic Alignment of Grapheme Transcriptions
An adaptation of the ADAPT algorithm, so that grapheme-grapheme alignment can be performed.
This adaptation is made by Wieke Harmsen, see [this paper by Harmsen et al. (2021), section 2.2.1 'Clean and align original and target texts' (p. 288)]({https://www.clinjournal.org/clinj/article/view/140).

'''
python3 run.py --type 'adagt' --target_graphemes 'kijken' --realised_graphemes 'keiken'
'''


## APGA: Algorithm for Phoneme-Grapheme alignment
This algorithm is made by Wieke Harmsen, see [this paper by Harmsen et al. (2021), section 2.3.2 'Phoneme-grapheme alignment' (p. 289)]({https://www.clinjournal.org/clinj/article/view/140).
'''
python3 run.py --type 'apga' --target_graphemes 'kijken' --target_phonemes 'k EI k @'
'''

## Multiple sequence alignment: AGPA & ADAGT 
Used for spelling error detection, see [this paper by Harmsen et al. (2021), section 2.3.3 'Deduce PCU segmentation' (p. 289)]({https://www.clinjournal.org/clinj/article/view/140).

'''
python3 run.py --type 'multi_graph' --target_graphemes 'kijken' --target_phonemes 'k EI k @' --realised_graphemes 'keiken' 
'''

## Multiple sequence alignment: AGPA & ADAPT
Used for pronunciation error detection.

'''
python3 run.py --type 'multi_phon' --target_graphemes 'kijken' --target_phonemes 'k EI k @' --realised_phonemes 'k i s'
'''

@LanguageResource{ADAPT,
    author = "{Elffers et al.}",
    title = {{ADAPT: Algorithm for Dynamic Alignment of Phonetic Transcriptions}},
    publisher = {Radboud University, \url{https://lands.let.ru.nl/literature/elffers.2005.1.pdf}},
    year = {2013},
}

@book{Cucchiarini1993,
  author       = {Cucchiarini, C.}, 
  title        = {{Phonetic transcription: a methodological and empirical study}},
  institution  = {Radboud University},
  year         = 1993,
  address      = {Nijmegen, The Netherlands},
  isbn         = {9090066993},
  url           = {https://lib.ugent.be/catalog/rug01:000310899}
}

@article{Cucchiarini1996,
    title = {{Assessing Transcription Agreement: {M}ethodological Aspects}},
    year = {1996},
    journal = {Clinical Linguistics and Phonetics},
    author = {Cucchiarini, C.},
    pages = {131-155},
    volume = {10},
    doi = {https://doi.org/10.3109/02699209608985167},
}

@article{Harmsen2021,
    title={Automatic Detection and Annotation of Spelling Errors and Orthographic Properties in the Dutch BasiScript Corpus}, 
    volume={11}, 
    url={https://www.clinjournal.org/clinj/article/view/140}, 
    journal={Computational Linguistics in the Netherlands Journal}, 
    author={Harmsen, Wieke Noa and Cucchiarini, Catia and Strik, Helmer}, 
    year={2021}, 
    month={Dec.}, 
    pages={281–306}
}
