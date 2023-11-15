# ADAPT,,CGN2,#name

adapt_to_cgn2_dict = {
    "p":"p", #p_in_pak
    "b":"b", #b_in_bak
    "t":"t", #t_in_tak,
    "d":"d", #d_in_dak,
    "k":"k", #k_in_kap,
    "g":"g", #g_in_goal
    "f":"f", #f_in_fel
    "v":"v", #v_in_vel
    "s":"s", #s_in_sein
    "z":"z", #z_in_zijn
    "S":"S", #sh_in_show
    "Z":"Z", #ge_in_bagage
    "G":"G", #g_in_goed
    "x":"x", #ch_in_toch
    "h":"h", #h_in_hand
    "m":"m", #m_in_met
    "n":"n", #n_in_net
    "N":"N", #ng_in_bang
    "l":"l", #l_in_land
    "r":"r", #r_in_rand
    "w":"w", #w_in_wit
    "j":"j", #j_in_ja
    "J":"J", #gn_in_campagne
    "i":"i", #ie_in_vier
    "e":"e", #ee_in_veer
    "a":"a", #aa_in_naam
    "o":"o", #oo_in_voor
    "u":"u", #oe_in_voer
    "y":"y", #uu_in_vuur
    "2":"EU", #eu_in_deur
    "I":"I", #i_in_pit
    "E":"E", #e_in_pet
    "A":"A", #a_in_pad
    "O":"O", #o_in_pot
    "Y":"U", #u_in_put
    "@":"@", #e_in_gemak
    "&":"EI", #ij_in_fijn
    "1":"UI", #ui_in_huis
    "3":"AU", #ou_in_goud
    "4":"E2", #e_in_creme
    "6":"O", #o_in_roze
    "-":"*", #insertion/deletion
    "*":"*", #insertion/deletion
}

cgn2_to_adapt_dict = {
    "p":"p", #p_in_pak
    "b":"b", #b_in_bak
    "t":"t", #t_in_tak
    "d":"d", #d_in_dak
    "k":"k", #k_in_kap
    "g":"g", #g_in_goal
    "f":"f", #f_in_fel
    "v":"v", #v_in_vel
    "s":"s", #s_in_sein
    "z":"z", #z_in_zijn
    "S":"S", #sh_in_show
    "Z":"Z", #ge_in_bagage
    "G":"G", #g_in_goed
    "x":"x", #ch_in_toch
    "h":"h", #h_in_hand
    "m":"m", #m_in_met
    "n":"n", #n_in_net
    "N":"N", #ng_in_bang
    "l":"l", #l_in_land
    "r":"r", #r_in_rand
    "w":"w", #w_in_wit
    "j":"j", #j_in_ja
    "J":"J", #gn_in_campagne
    "i":"i", #ie_in_vier
    "e":"e", #ee_in_veer
    "a":"a", #aa_in_naam
    "o":"o", #oo_in_voor
    "u":"u", #oe_in_voer
    "y":"y", #uu_in_vuur
    "EU":"2", #eu_in_deur
    "I":"I", #i_in_pit
    "E":"E", #e_in_pet
    "A":"A", #a_in_pad
    "O":"O", #o_in_pot
    "U":"Y", #u_in_put
    "@":"@", #e_in_gemak
    "EI":"&", #ij_in_fijn
    "UI":"1", #ui_in_huis
    "AU":"3", #ou_in_goud
    "E2":"4", #e_in_creme
    "O":"6", #o_in_roze
    "-":"-", #insertion/deletion
    "*":"-", #insertion/deletion
}

def cgn2string_to_adaptstring(cgn2_string):
    adapt_string = ''
    cgn2_phone_list = cgn2_string.split(' ')
    for phone in cgn2_phone_list:
        adapt_string += cgn2_to_adapt_dict[phone]
    return adapt_string

def adaptstring_to_cgn2string(adapt_string):
    cgn2_list = []
    for phone in adapt_string:
        cgn2_list.append(adapt_to_cgn2_dict[phone])
    return " ".join(cgn2_list)


