import re


def split_alignments_in_segments(align_ref_rev, align_hyp_rev, align_ref, align_hyp):
    indices_rev = [0] + [i.start() for i in re.finditer("\|",
                                                        align_ref_rev)] + [len(align_ref_rev)] + [9999]
    align_ref_rev_list = [align_ref_rev[indices_rev[idx]: indices_rev[idx+1]]
                          for idx, item in enumerate(indices_rev) if item != 9999][:-1]
    align_hyp_rev_list = [align_hyp_rev[indices_rev[idx]: indices_rev[idx+1]]
                          for idx, item in enumerate(indices_rev) if item != 9999][:-1]

    indices = [0] + [i.start() for i in re.finditer("\|", align_ref)
                     ] + [len(align_ref)] + [9999]
    align_ref_list = [align_ref[indices[idx]: indices[idx+1]]
                      for idx, item in enumerate(indices) if item != 9999][:-1]
    align_hyp_list = [align_hyp[indices[idx]: indices[idx+1]]
                      for idx, item in enumerate(indices) if item != 9999][:-1]

    return align_ref_rev_list, align_hyp_rev_list, align_hyp_list
