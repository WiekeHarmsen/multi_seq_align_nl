import alignment_adapt.cgn2_adapt_map as cgn2_to_adapt
import alignment_adapt.adapt as adapt
import alignment_adagt.string_manipulations as strman

"""
Function that converts two CGN2 phoneme strings to ADAPT phoneme strings, reverses them, aligns them using ADAPT and reverses the alignments back.

ref_phones  CGN2 reference string (k OE k)
hyp_phones  CGN2 hypothesis string (k o k)
"""

def reverse_align_two_phone_strings(ref_phones, hyp_phones):

    # Convert phonetic transcription from CGN2 to ADAPT
    promptPhon_ref_adapt = cgn2_to_adapt.cgn2string_to_adaptstring(ref_phones)
    phonTrans_hyp_adapt = cgn2_to_adapt.cgn2string_to_adaptstring(hyp_phones)

    # Reverse phonetic transcription
    promptPhon_ref_adapt_rev = strman.reverse(promptPhon_ref_adapt)
    phonTrans_hyp_adapt_rev = strman.reverse(phonTrans_hyp_adapt)

    # Compute optimal alignment between two ADAPT strings
    dist_score, nsub, ndel, nins, align_ref_adapt_rev, align_hyp_adapt_rev = adapt.align_dist(promptPhon_ref_adapt_rev, phonTrans_hyp_adapt_rev)

    # Reverse aligned phonetic transcription
    align_ref_adapt = strman.reverse(align_ref_adapt_rev)
    align_hyp_adapt = strman.reverse(align_hyp_adapt_rev)

    # Convert aligned phone strings back to CGN2
    align_ref = cgn2_to_adapt.adaptstring_to_cgn2string(align_ref_adapt)
    align_hyp = cgn2_to_adapt.adaptstring_to_cgn2string(align_hyp_adapt)

    return align_ref, align_hyp, align_ref_adapt, align_hyp_adapt