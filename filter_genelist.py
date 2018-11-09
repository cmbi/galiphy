


filter_genelist(clientinput_str):
    clieninput_filtered = filter(lambda char: char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", clientinput_str)
    return clientinput_filtered


