'''
New recursive version of textToParts function
'''


def makeSplit(targetPartsList, origPartsList, target_text, original_text, original_space_idx, max_length):

    # Get slice to split on
    original_slice = original_text[original_space_idx-3:original_space_idx+3]

    # Find slice in target text
    target_slice_idx = target_text.find(
        original_slice)

    # If slice is found in target text
    if (target_slice_idx != -1 and len(original_slice) != 0):

        # Split the target_text and original_text on the space in the overlapping slice
        # Add the first part to the partLists
        target_space_idx = target_slice_idx+3
        targetPartsList.append(target_text[:target_space_idx])
        origPartsList.append(original_text[:original_space_idx])

        # Remove the first part from the target_text and original_text
        target_text = target_text[target_space_idx+1:]
        original_text = original_text[original_space_idx+1:]

        if (len(original_text) < 80 or len(target_text) < 80):
            # End of file reached
            targetPartsList.append(target_text)
            origPartsList.append(original_text)
            target_text = ''
            original_text = ''
            idx_of_next_space = -1

            return targetPartsList, origPartsList, target_text, original_text, idx_of_next_space, max_length
        else:
            # reset around_idx
            new_space_idx = original_text.find(" ", max_length)

            # make next split
            return makeSplit(targetPartsList, origPartsList, target_text, original_text, new_space_idx, max_length)


def textToParts(target_text, original_text):
    max_length = 50
    if len(target_text) <= max_length and len(original_text) <= max_length:
        return [target_text], [original_text]

    target_text_sent = []
    original_text_sent = []
    begin = 0

    # Check if text contains right amount of dots to split the text at the dots in text
    # on average every 150 characters a dot
    desired_nr_of_dots = int(len(original_text)/max_length)+1
    actual_nr_of_dots = original_text.count(".")

    # If text doesn't contain enough periods
    if (original_text.find(". ", begin, -1) == -1) or (desired_nr_of_dots >= actual_nr_of_dots):
        length = len(original_text)
        nr_of_splits = int(length/max_length)

        for split_idx in range(nr_of_splits):

            # We need to make a split at around_idx
            around_idx = (split_idx+1)*max_length

            for trial_idx in range(10):
                # find first space near around_idx in original
                space_idx_original = original_text.find(
                    " ", around_idx, around_idx+10)

                # save slice
                original_slice = original_text[space_idx_original -
                                               3:space_idx_original+3]

                # try to find slice in target_original
                if (target_text.find(original_slice, space_idx_original-30, space_idx_original+30) != -1):
                    # If found, save space_idx_target
                    space_idx_target = target_text.find(
                        original_slice, space_idx_original-30, space_idx_original+30)+3

                    # insert dollar sign to replace space
                    original_text = original_text[:space_idx_original] + \
                        "$"+original_text[space_idx_original+1:]
                    target_text = target_text[:space_idx_target] + \
                        "$"+target_text[space_idx_target+1:]
                    break
                else:
                    if trial_idx == 1:  # odd numbers
                        space_idx_original = original_text.find(
                            " ", around_idx-10, around_idx)
                    elif trial_idx >= 2:
                        space_idx_original = original_text.find(
                            " ", around_idx+((trial_idx-1)*10), around_idx+(trial_idx*10))

        # split opstellen at $
        original_text_sent = original_text.split("$")
        target_text_sent = target_text.split("$")

    else:
        while len(original_text) > 0 and original_text.find(". ", begin, -1) != -1:

            # Search first position of . in original
            idx = original_text.find(". ", begin, -1)

            # Save five chars before and five chars after
            dot_slice = original_text[idx-3:idx+3]

            # Find dot slice in target
            if (target_text.find(dot_slice, begin-10, idx+10) != -1):

                # dot slice is found
                idx_target = target_text.find(dot_slice, begin-10, idx+10) + 3

                # split both texts.
                sent_target = target_text[:idx_target+1]
                target_text = target_text[idx_target+2:]
                sent_original = original_text[:idx+1]
                original_text = original_text[idx+2:]

                # Add sent_target and sent_original to lists
                target_text_sent.append(sent_target)
                original_text_sent.append(sent_original)
                begin = 0

            else:
                # idx is not found in target, we should find next idx in original
                begin = idx+1

        # Add remaining parts to target_text_sent and original_text_sent
        target_text_sent.append(target_text)
        original_text_sent.append(original_text)

    return target_text_sent, original_text_sent
