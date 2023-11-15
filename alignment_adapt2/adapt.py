# -*- coding: utf-8 -*-

"""
ADAPT_phon.py : ADAPT algorithm for phoneme alignments

This is the Python version of:
Adapt: Algorithm for Dynamic Alignment of Phonetic (and Graphemic) Transcriptions
This version is based on the Perl version of ADAPT for phonemes (adapt.pm ; Version 1.0 by Bram Elffers & Helmer Strik, August 2005).
 
----------------------------------------------------------------------

This version of ADAPT calculates the optimal alignment and distance between two strings of phonemes.
Requires phoneme feature definitions in 'featuresYAPA.txt'.

Lines in this file that differ from adapt_graph.py:
32, 35-36, 167-168, 240, 283, 286

@author: Wieke Harmsen
@date_file_created: 2 September 2020
@date_last_adaptations: 7 September 2020 
"""

import os.path
from os import path
import numpy as np
import pandas as pd
import re

zero_char = '-'       # 'zero' character for insertions/deletions.
wbnd_char = '|'       # 'word boundary' character in transcriptions.

features_file = "./alignment_adapt2/featuresYAPA.txt";  # data file containing grapheme features.
assert os.path.exists(features_file), "ADAPT error: Cannot find file " +features_file

num_con_feats = 11   # number of feature values per consonant
num_vow_feats = 5     # number of feature values per vowel

def align_init():
    i = 0
    j = 0
    k = 0
    kl = []
    mk = []
    char = ''
    feats = ''
    kl_chars = []
    kl_feats = {}
    mk_chars = []
    mk_feats = {}
    kl = ''
    mk = ''
    ci = ''
    cj = ''
    fi = []
    fj = []
    inn = ''
    check = {}
  
  
    #----------------------------------------------------------------------
    # read phoneme features from feature definitions file
    #----------------------------------------------------------------------
    with open(features_file, "r") as f:
        file = f.readlines()
        for s in file:
            if(s[0] != " " and s[0] != "\n" and s[0] != "\t"):
                s = s[:-1]          #Remove final new line character
                s = s.split("\t")   
                feats = s[1:]
                if(len(feats) == num_con_feats):
                    mk_chars.append(s[0])
                    mk_feats[s[0]] = [float(i) for i in s[1:]]
                elif len(feats) == num_vow_feats :
                    kl_chars.append(s[0])
                    kl_feats[s[0]] = [float(i) for i in s[1:]]
                else:
                    print("ADAPT error: Illegal number of features in ", features_file, "line of character", s)
    
    
    #----------------------------------------------------------------------
    # calculate total difference between each vowel pair
    #----------------------------------------------------------------------
    names = kl_chars + mk_chars
    names.append(zero_char)
    names.append(wbnd_char)
    
    matrix = np.zeros((len(names), len(names)))
    matrix2 = np.zeros((len(names), len(names)))
    
    diff = pd.DataFrame(matrix, columns=names, index=names)
    number_of_diffs = pd.DataFrame(matrix2, columns=names, index=names)
        
    for i in range(len(kl_chars)-1):
        ci = kl_chars[i]
        fi = kl_feats[ci]
        for j in range(i+1, len(kl_chars)):
            cj = kl_chars[j]
            fj = kl_feats[cj]

            diff.loc[ci,cj] = sum(np.absolute(np.array(fi) - np.array(fj)))
            diff.loc[cj,ci] = diff.loc[ci,cj]
       
            number_of_diffs.loc[ci,cj] = np.count_nonzero(np.absolute(np.array(fi) - np.array(fj)))
            number_of_diffs.loc[cj,ci] = number_of_diffs.loc[ci,cj]

    #----------------------------------------------------------------------
    # calculate total difference between each consonant pair
    #----------------------------------------------------------------------
    for i in range(len(mk_chars)):
        ci = mk_chars[i]
        fi = mk_feats[ci]
        
        for j in range(i+1, len(mk_chars)):
            cj = mk_chars[j]
            fj = mk_feats[cj]
            
            diff.loc[ci,cj] = sum(np.absolute(np.array(fi) - np.array(fj)))
            number_of_diffs.loc[ci,cj] = len(fi) - np.count_nonzero(np.absolute(np.array(fi) - np.array(fj)))
            
            diff.loc[cj,ci] = diff.loc[ci,cj]
            number_of_diffs.loc[cj,ci] = number_of_diffs.loc[ci,cj]
            
    
    #----------------------------------------------------------------------
    # set high differences between vowels and consonants
    #----------------------------------------------------------------------
    for i in range(len(kl_chars)):
        ci = kl_chars[i];
        for j in range(len(mk_chars)):
            cj = mk_chars[j];
            diff.loc[ci,cj] = 99;
            diff.loc[cj,ci] = 99;
            number_of_diffs.loc[cj,ci] = 99;
            number_of_diffs.loc[ci,cj] = 99;
    
    #----------------------------------------------------------------------
    # set high differences between phonemes and word boundary
    #----------------------------------------------------------------------
    diff.loc[wbnd_char,wbnd_char] = 0
    number_of_diffs.loc[wbnd_char,wbnd_char] = 0
    for ci in kl_chars:
        diff.loc[ci,wbnd_char] = 99
        diff.loc[wbnd_char,ci] = 99
        number_of_diffs.loc[ci,wbnd_char] = 99
        number_of_diffs.loc[wbnd_char][ci] = 99
        
    for ci in mk_chars:
        diff.loc[ci,wbnd_char] = 99
        diff.loc[wbnd_char,ci] = 99
        number_of_diffs.loc[ci,wbnd_char] = 99
        number_of_diffs.loc[wbnd_char,ci] = 99    

    return diff, number_of_diffs
    
#----------------------------------------------------------------------
# align_init routine is called only once, upon inclusion of the module
# in your Perl script. It reads Align's phoneme specification files,
# and memorises a hash list containing the total difference between
# every possible pair of phonemes. Don't call this yourself.
#----------------------------------------------------------------------
diff, number_of_diffs = align_init() 

#----------------------------------------------------------------------
# Sets penalty scores for the align subroutine,
# for insertions, deletions, and substitutions.
#----------------------------------------------------------------------
fon_ins_cost = 4 # corrected to 3 by 'distance' routine
fon_del_cost = 4 # corrected to 3 by 'distance' routine
    
#----------------------------------------------------------------------
# Call align_dist to return the Align distance measure between two
# arguments as well as aligned norm and realisation transcriptions.
# See documentation for details.
# This routine is a placeholder for the former align_dist routine,
# which is now split into the 'align' and 'dist' routines.
# If you need alignments only, call 'align ($norm, $real)' instead.
#----------------------------------------------------------------------
def align_dist(ref_line, hyp_line):
    alnorm, alreal = align(ref_line,hyp_line)
    dist_score, nsub, ndel, nins = distance(alnorm, alreal);
    
    return dist_score, nsub, ndel, nins, alnorm, alreal
    
#----------------------------------------------------------------------
# Takes a norm and realisation transcription, and dynamically aligns
# the two according to phonetic feature distances. Returns the aligned
# norm and realisation transcriptions, with insertions and deletions
# marked by '-' ($zero_char) in norm and realisation, respectively.
# Call sub align_dist if you need distance measures as well.
#----------------------------------------------------------------------
def align(norm_input, real_input):   
    lnorm = len(norm_input)
    lreal = len(real_input)
    i = 0
    j = 0
    real_i = ''
    norm_j = ''
    dist = []
    op = 0
    real = []
    norm = []
    dist = 0
    nsub = 0
    ndel = 0
    nins = 0
    aln = ''
    alr = ''
    
    #----------------------------------------------------------------------
    # Initialise edges of search space.
    #----------------------------------------------------------------------
    dist = np.zeros((lnorm+1, lreal+1))
    dist = pd.DataFrame(dist)
    real = np.array([[''] * (lreal+1)] * (lnorm+1))
    real = pd.DataFrame(real)
    norm = np.array([[''] * (lreal+1)] * (lnorm+1))
    norm = pd.DataFrame(norm)

    
    for i in range(1,lreal+1):
        dist[i][0] = i*fon_del_cost
        real[i][0] = real[i-1][0] + real_input[i-1:i]
        norm[i][0] = norm[i-1][0] + zero_char
        
    for j in range(1,lnorm+1):
        dist[0][j] = j*fon_ins_cost
        real[0][j] = real[0][j-1] + zero_char
        norm[0][j] = norm[0][j-1] + norm_input[j-1:j]

    #-------------------------------------------------------
    # Construct search space and alignment.
    #----------------------------------------------------------------------
    for i in range(1,lreal+1):
        for j in range(1, lnorm+1):
            real_i = real_input[i-1:i]
            norm_j = norm_input[j-1:j]
            
            dist[i][j], op = min_func([
                dist[i-1][j] + fon_del_cost,    # deletion
                dist[i-1][j-1] + diff[real_i][norm_j],    #substitution
                dist[i][j-1] + fon_ins_cost])   #insertion
            
            if(op == 0):        #deletion
                real[i][j] = real[i-1][j] + real_i
                norm[i][j] = norm[i-1][j] + zero_char
            elif(op == 1):      #substitution
                real[i][j] = real[i-1][j-1] + real_i
                norm[i][j] = norm[i-1][j-1] + norm_j
            else:               #insertion
                real[i][j] = real[i][j-1] + zero_char
                norm[i][j] = norm[i][j-1] + norm_j
    
    aln = norm[lreal][lnorm];  
    alr = real[lreal][lnorm];
    
    #----------------------------------------------------------------------
    # Verify alignment and return results.
    #----------------------------------------------------------------------
    aln, alr = verify_alignment(aln, alr)
    
    
    return aln, alr

#----------------------------------------------------------------------
# Once we have the aligned norm and real, we can calculate the S/D/I
# and phonetic distance by comparing the two strings. This saves us
# the hassle of having to calculate them in search space.
# Returns total distance, #sub, #del, and #ins.
# Adaptation for grapheme-grapheme alignment: dist += 1 for insertion and deletion
#----------------------------------------------------------------------
def distance(alnorm, alreal):
    alnorm_out = getCharList(alnorm)
    alreal_out = getCharList(alreal)
    
    dist_score = 0
    n_ins = 0
    n_del = 0
    n_sub = 0
    
    for i in range(len(alnorm)):
        if(alnorm[i] == zero_char):
            n_ins += 1
            dist_score += 3/fon_ins_cost * fon_ins_cost
        elif(alreal[i] == zero_char):
            n_del += 1
            dist_score += 3/fon_del_cost * fon_del_cost
        elif(alnorm[i] != alreal[i]):
            n_sub += 1
            dist_score += diff[alnorm[i]][alreal[i]]
    
    return dist_score, n_sub, n_del, n_ins


#----------------------------------------------------------------------
# Returns the minimum value of its arguments, and the index of the
# minimum value in the argument array.
#----------------------------------------------------------------------
def min_func(input_list):
    min_i = 999.0
    pos_i = 0
    
    for i in range(len(input_list)):
        value1 = float(input_list[i])
        value2 = min_i
        
        if (value1 < value2):
            min_i = value1
            pos_i = i
            
    return min_i, pos_i

#----------------------------------------------------------------------
# Returns the input string s as a list of characters.
#----------------------------------------------------------------------
def getCharList(s):
    return [char for char in s]

#----------------------------------------------------------------------
# Verify placement of deletions/insertions in pre-aligned norm and
# realisation transcriptions. This fixes a bug causing misalignments,
# and considers the number of phoneme feature differences in case of
# equal phoneme distances.
#----------------------------------------------------------------------
def verify_alignment (alnorm, alreal):
    alnorm_out = getCharList(alnorm)
    alreal_out = getCharList(alreal)
    changes = 0
    i = 0
    p = 0
    
    #----------------------------------------------------------------------
    # Exit early if norm and real are equal, or if norm/real do not
    # contain zero characters (nothing to realign).
    #----------------------------------------------------------------------
    if (alnorm == alreal):
        return (alnorm, alreal)
    
    #----------------------------------------------------------------------
    # Verify insertions, skip if no insertions are found.
    #----------------------------------------------------------------------
    if (alnorm.find(zero_char) != -1):
        for i in range(len(alnorm)-1, 0, -1):
            if (alnorm[i] == zero_char):
                p = i
                #find first index where there is no zero_char in norm, save index in var p
                while (alnorm[p] == zero_char and p > 0):
                    p = p-1
                if(diff[alnorm[p]][alreal[p]] == diff[alnorm[p]][alreal[i]]):
                    if (number_of_diffs[alnorm[p]][alreal[p]] > number_of_diffs[alnorm[p]][alreal[i]]):
                        alnorm_out[p] = alnorm[i]
                        alnorm_out[i] = alnorm[p]
                        changes += 1
                        
                        
        for i in range(len(alnorm)):
            if (alnorm[i] == zero_char):
                p = i
                while (p < len(alnorm)-1 and alnorm[p] == zero_char):
                    p += 1
                if (diff[alnorm[p]][alreal[p]] == diff[alnorm[p]][alreal[i]]):
                    if (number_of_diffs[alnorm[p]][alreal[p]] > number_of_diffs[alnorm[p]][alreal[i]]):
                        alnorm_out[p] = alnorm[i]
                        alnorm_out[i] = alnorm[p]
                        changes += 1
                
    #----------------------------------------------------------------------
    # Verify deletions, skip if no deletions are found.
    #----------------------------------------------------------------------
    if(alreal.find(zero_char) != -1):
        for i in range(len(alreal)-1, 0, -1):
            if (alreal[i] == zero_char):
                p = i
                #find first index where there is no zero_char in norm, save index in var p
                while (alreal[p] == zero_char and p > 0):
                    p = p-1
                if (diff[alnorm[p]][alreal[p]] == diff[alnorm[i]][alreal[p]]):
                    if (number_of_diffs[alnorm[p]][alreal[p]] > number_of_diffs[alnorm[i]][alreal[p]]):
                        alreal_out[p] = alreal[i]
                        alreal_out[i] = alreal[p]
                        changes += 1
                      
        for i in range(len(alreal)):
            if (alreal[i] == zero_char):
                p = i
                while (p < len(alnorm)-1 and alreal[p] == zero_char ):
                    p += 1
                if (diff[alnorm[p]][alreal[p]] == diff[alnorm[i]][alreal[p]]):
                    if (number_of_diffs[alnorm[p]][alreal[p]] > number_of_diffs[alnorm[i]][alreal[p]]):
                        alreal_out[p] = alreal[i]
                        alreal_out[i] = alreal[p]
                        alreal_out[p], alreal_out[i] = alreal[i], alreal[p]
                        changes += 1
    
    #Convert alnorm_out and alreal_out to strings
    alnorm_out = "".join(alnorm_out)
    alreal_out = "".join(alreal_out)
    
    return alnorm_out, alreal_out

    
            
    


 
  
  
  
  
  