import argparse
import pandas as pd
import os
import glob
import re
import json

# ADAPT
import adapt.run_adapt as run_adapt
import adapt.cgn2_adapt_map as cgn2_adapt_map
import adapt.deduce_pcus_orig_phon as deduce_pcus

#ADAGT
import adagt.adagt as adagt
import adagt.deduce_pcus_orig_graph as deduce_pcus_graph

# APGA 
import graph_phon_align.graph_phon_alignment as gpa


def run(args):

    # Get alignment type
    alignmentType = args.type
    assert alignmentType in ['adapt', 'adagt', 'gpa', 'multi_phon', 'multi_graph'], "choose for the variable \'type\' from the values \'adapt\', \'adagt\', \'apga\'or \'multi\'" 

    target_graph = args.target_graphemes
    target_phon = args.target_phonemes
    realised_graph = args.realised_graphemes
    realised_phon = args.realised_phonemes

    # print("INPUTS")
    # print("target_graphemes: ", target_graph)
    # print("target_phonemes: ", target_phon)
    # print("realised_graphemes: ", realised_graph)
    # print("realised_phonemes: ", realised_phon)

    if(alignmentType == 'adapt'):
        assert target_phon != None and realised_phon != None, "To use type \"adapt\" both \"target_phonemes\" and \"realised_phonemes\" need to be specified."

        align_target_phon_cgn2, align_realised_phon_cgn2, align_target_phon_adapt, align_realised_phon_adapt = run_adapt.reverse_align_two_phone_strings(target_phon, realised_phon)
        
        print("OUTPUTS in CGN2 CPA")
        # print(align_target_phon_cgn2)
        # print(align_realised_phon_cgn2)

        print("OUTPUTS in ADAPT CPA")
        # print(align_target_phon_adapt)
        # print(align_realised_phon_adapt)

    elif(alignmentType == 'adagt'):
        assert target_graph != None and realised_graph != None, "To use type \"adagt\" both \"target_graph\" and \"realised_graph\" need to be specified."

        align_target_graph, align_realised_graph = adagt.align(target_graph, realised_graph)
        
        # print("OUTPUTS")
        # print(align_target_graph)
        # print(align_realised_graph)
        output_adagt = {"target_graphemes": target_graph,
                              "target_phonemes": target_phon,
                              "realised_graphemes": realised_graph,
                              "realised_phonemes": realised_phon,
                              "align_target_graph": align_target_graph,
                              "align_realised_graph": align_realised_graph}
        print(output_adagt)

    elif(alignmentType == 'gpa'):

        assert target_graph != None and target_phon != None, "To use type \"gpa\" both \"target_graph\" and \"target_phon\" need to be specified."

        pcu_target_graph, pcu_target_phon = gpa.align_word_and_phon_trans(target_graph, target_phon)

        # print('output', pcu_target_graph, pcu_target_phon)
        output_gpa = {"target_graphemes": target_graph,
                              "target_phonemes": target_phon,
                              "realised_graphemes": realised_graph,
                              "realised_phonemes": realised_phon,
                              "pcu_target_graph": pcu_target_graph,
                              "pcu_target_phon": pcu_target_phon}
        print(json.dumps(output_gpa))

    elif(alignmentType == 'multi_graph'):

        assert target_graph != None and realised_graph != None and target_phon != None, "To use type \"multi\" both \"target_graph\", \"realised_graph\" and \"target_phon\" need to be specified."

        # ADAGT
        align_target_graph, align_realised_graph = adagt.align(target_graph, realised_graph)

        # GPA
        pcu_target_graph, pcu_target_phon = gpa.align_word_and_phon_trans(target_graph, target_phon)

        # Combine output alignments from ADAGT and GPA
        multi_target_phon, multi_target_graph, multi_realised_graph = deduce_pcus_graph.computePCUs(align_target_graph, align_realised_graph, pcu_target_graph, pcu_target_phon, '*')

        print(multi_target_phon, multi_target_graph, multi_realised_graph)
        
    elif(alignmentType == 'multi_phon'):

        assert target_graph != None and target_phon != None and realised_phon != None, "To use type \"multi\" both \"target_graph\", \"target_phon\" and \"realised_phon\" need to be specified."

        print(target_phon, realised_phon)
        # ADAPT alignment
        align_target_phon_cgn2, align_realised_phon_cgn2, align_target_phon_adapt, align_realised_phon_adapt = run_adapt.reverse_align_two_phone_strings(target_phon, realised_phon)

        # GPA alignment
        pcu_target_graph, pcu_target_phon = gpa.align_word_and_phon_trans(target_graph, target_phon)

        # Combine output alignments from ADAPT and GPA
        multi_target_phon, multi_target_graph, multi_realised_phon = deduce_pcus.computePCUs(align_target_phon_adapt, align_realised_phon_adapt, pcu_target_graph, pcu_target_phon, '*')

        print(align_target_phon_cgn2, align_realised_phon_cgn2)
        print(align_target_phon_adapt, align_realised_phon_adapt)
        print(pcu_target_graph, pcu_target_phon)
        print(multi_target_phon, multi_target_graph, multi_realised_phon)


def main():
    parser = argparse.ArgumentParser("Message")
    parser.add_argument("--type", type=str, help = "Choose your type of alignment: adapt, adagt, gpa or multi_graph or multi_phon")
    parser.add_argument("--target_graphemes", type=str, help = "A string containing the target (correct) transcription. This is a grapheme string.")
    parser.add_argument("--target_phonemes", type=str, help = "A string containing the CGN2 phonetic transcription of the grapheme transcription of the target, specified in \'target_graphemes\', e.g. \"k EI k @\" ")
    parser.add_argument("--realised_graphemes", type=str, help = "A string containing The realised (incorrect) grapheme transcription. This is a grapheme string.")
    parser.add_argument("--realised_phonemes", type=str, help = "A string containing the CGN2 phonetic transcription of the (incorrect) realised transcription. ")
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)   

if __name__ == "__main__": 
    main()