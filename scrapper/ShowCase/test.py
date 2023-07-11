def replace_spaces_and_commas(string):
    # Split the string into words
    words = string.split()

    # If there are exactly two words
    if len(words) == 2:
        # Reverse the order and join with a slash
        new_string = "/".join(words[::-1])
    elif len(words) > 2:
        # If there are more than two words, last one should go to first with '/' like 'word/' and rest having spaces should replaced with '-' so final string can be 'word/word-word'
        new_string = words[-1] + "/"
        for i in range(len(words) - 1):
            new_string += words[i] + "-"
        new_string = new_string[:-1]





    else:
        # If there are more than two words, replace the comma with a dash
        new_string = string.replace(",", "-")

    if new_string[0] == "/":
        print(f"new stirng = {new_string}")
        # remove it
        new_string = new_string[1] + new_string[2:]

    print(f"new stirng = {new_string}")

    return new_string


print(replace_spaces_and_commas("East Orange NJ"))