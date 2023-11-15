# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 10:40:08 2020

@author: wieke
"""
import os
import glob
import textgrids as tg
import re
import pandas as pd
import alignment_helper
import adapt_graph


def getAlignmentsPromptAsrTrans(prompt, asrTrans):
    # Preprocess strings -> replace spaces with |
    prompt = prompt.replace(" ", "|")
    asrTrans = asrTrans.replace(" ", "|")

    # Apply reversed alignment process
    align_ref_rev, align_hyp_rev = alignment_helper.applyReversedAlignment(
        prompt, asrTrans)

    # Apply normal alignment process
    dist_score, nsub, ndel, nins, align_ref, align_hyp = adapt_graph.align_dist(
        prompt, asrTrans)

    # Split alignments into segments that match the prompt
    align_ref_rev_list, align_hyp_rev_list, align_hyp_list = splitAlignmentsIntoSegments(
        align_ref_rev, align_hyp_rev, align_ref, align_hyp)

    # Create output DataFrame
    outputDF = pd.DataFrame()
    outputDF['prompt'] = pd.Series(align_ref_rev_list).apply(
        removeInsertions).apply(trimPipesAndSpaces)
    outputDF['aligned_asrTrans'] = pd.Series(
        align_hyp_list).apply(trimPipesAndSpaces)
    outputDF['reversed_aligned_asrTrans'] = pd.Series(
        align_hyp_rev_list).apply(trimPipesAndSpaces)
    outputDF['correct'] = outputDF.apply(determineCorrectness, axis=1)

    outputDF = outputDF.set_index("prompt")
    print(outputDF)
    return outputDF
