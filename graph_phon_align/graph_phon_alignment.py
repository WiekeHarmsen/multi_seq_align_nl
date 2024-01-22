# -*- coding: utf-8 -*-
"""
graph_phon_alignment.py : algorithm to align a grapheme with a phoneme string (written in CGN2.0)

Run: 
import graph_phon_alignment as gpa
graph_align, phon_align = gpa.align_word_and_phon_trans("thuis", "t UI s")

@author: Wieke Harmsen
@date_last_adaptations: 11 January 2022 
"""

import numpy as np
import constants.constants_basiscript as constants

"""
This function creates three possibilities of grapheme strings that could match the phoneme.
gr_string  string
begin      variable that keeps track of where in the gr_string we are
"""
def create_possibilities(gr_string, begin):
    poss1 = gr_string[begin:begin+1]
    poss2 = gr_string[begin:begin+2]
    poss3 = gr_string[begin:begin+3]
    if len(poss2) != 2:
        poss2 = ""
    if len(poss3) != 3:
        poss3 = ""
    return poss1, poss2, poss3

"""
This function finds which (sequence of) grapheme(s) matches the phoneme(sequence).
f           phoneme(sequence)
next_f      next phoneme
gr_string   grapheme string written in dutch letter symbols
begin       variable that keeps track of where in the gr_string we are
combi_phon  whether f is a sequence or not
"""
def find_graphemes_belonging_to_phon(f, next_f, gr_string, begin, combi_phon):
    
    #Get all graphemes belonging to the phoneme
    corr_gr = constants.phon_dict[f]
    corr_gr_first_letters = [x[0] for x in corr_gr]
    
    phoneme = ""
    pcu = ""
    found = False
    extra_pcu = ""
    extra_phoneme = ""
    
    while not found:       

        #Create possibilities
        poss1, poss2, poss3 = create_possibilities(gr_string, begin)
        
        #empty possibilities if they may not be chosen
        if combi_phon == False and f in constants.multi_graph_dict.keys():
            if next_f == constants.multi_graph_dict[f][0] or next_f == constants.multi_graph_dict[f][2]:
                poss = constants.multi_graph_dict[f][1]
                if poss == 2:
                    poss2 = ""
                elif poss == 3:
                    poss3 = ""
        
        #in case of foreign words/abbreviations
        if poss1 == "":
            pcu = "NaN"
            phoneme = "NaN"
            found = True
            combi_phon = "False"

        #Check if there is a right possibility
        elif poss3 in corr_gr:
            pcu = poss3
            phoneme = f
            begin = begin+3
            found = True
        elif poss2 in corr_gr:
            pcu = poss2
            phoneme = f
            begin = begin+2
            found = True
        elif poss1 in corr_gr:
            pcu = poss1
            phoneme = f
            begin = begin+1
            found = True
        else:
            try: 
                next_g = poss2[1]
            except: 
                next_g = ""
            if(next_g in corr_gr or next_g in corr_gr_first_letters):
                #Grapheme not pronounced
                extra_pcu = poss1
                extra_phoneme = constants.zero_char
                begin = begin+1
            else:
                #Phoneme not pronounced
                combi_phon = False
                pcu = constants.zero_char
                phoneme = f
                found=True
            
    return combi_phon, phoneme, pcu, begin, extra_pcu, extra_phoneme


"""
Remove wordboundary character (*) if it is inserted at the same index for all three variables
"""
def remove_redundant_zerochars(graphemes, phonemes):
    indices_to_remove = []
    length = min(len(graphemes), len(phonemes))
    for i in range(length-1):
        if graphemes[i] == phonemes[i] == constants.zero_char:
            indices_to_remove.append(i)

    for index in reversed(indices_to_remove):
        graphemes = graphemes[:index] + graphemes[index+1:]
        phonemes = phonemes[:index] + phonemes[index+1:]
    return graphemes, phonemes


"""
This function aligns a grapheme string with its phonetic transcription.
gr_string  grapheme string written in dutch letter symbols
f_string   phonetic string written in CGN2 symbols
"""
def align_word_and_phon_trans(gr_string, f_string):
    
    #Preprocessing 1: all graphemes to lower case
    gr_string = gr_string.lower()
    
    #preprocessing 2: save all phonemes in list
    f_list = f_string.split(" ")
    f_list = [x for x in f_list if x !='']
    begin = 0
    
    already_found_phon_counter = 0
    idx_phon = 0
    gr_align = []
    ph_align = []

    #For every phoneme, find the corresponding graphemes
    for idx in range(len(f_list)):
        
        combi_phon = False
        idx_phon = idx+already_found_phon_counter
        
        if idx_phon < len(f_list):
        
            #Select the phoneme
            f = f_list[idx_phon]

            #Check if the phoneme exists 
            if f == "PRONUNCIATION_NOT_FOUND":
                return np.nan, np.nan
            
            #Get the next phoneme
            try:
                next_f = f_list[idx_phon+1]
            except:
                next_f = ""
            
            #Check if the phoneme is part of a phoneme combination
            if f in constants.multi_phon_dict.keys() and idx_phon != len(f_list)-1:
                
                if next_f in constants.multi_phon_dict[f]:
                    #Create combined phoneme
                    combined_f = f + next_f
                    combi_phon = True
                    combi_phon, phoneme, pcu, begin, extra_pcu, extra_phoneme = find_graphemes_belonging_to_phon(combined_f, next_f, gr_string, begin, combi_phon)
                    
            if combi_phon:
                already_found_phon_counter = already_found_phon_counter + len(phoneme)-1
            else:
                combi_phon, phoneme, pcu, begin, extra_pcu, extra_phoneme = find_graphemes_belonging_to_phon(f, next_f, gr_string, begin, combi_phon)

            
            #If a grapheme is written, but not pronounced, we need this function
            if extra_pcu != "" and extra_phoneme != "":
                gr_align.append(extra_pcu)
                ph_align.append(extra_phoneme)
            
            gr_align.append(pcu)
            ph_align.append(phoneme)
    
    #If something goes wrong, the whole alignment is NaN
    if gr_align[-1] == "NaN" and ph_align[-1] == "NaN":
        gr_align = ["NaN"]
        ph_align = ["NaN"]
    
    #Adds the remaining graphemes to the alignment, if we're out of phonemes
    if len(gr_string) > begin:
        #Check if remaining part is PCU:
        remaining_gr = gr_string[begin:len(gr_string)]
        if remaining_gr in constants.pcus:
            gr_align.append(gr_string[begin:len(gr_string)])
            ph_align.append(constants.zero_char)        
        else:
            gr_align = ["NaN"]
            ph_align = ["NaN"]

    gr_align, ph_align = remove_redundant_zerochars(gr_align, ph_align)

    return gr_align, ph_align