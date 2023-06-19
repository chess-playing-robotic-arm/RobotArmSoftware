def uciToArmCommands(uci_notation):
    first_sq = uci_notation[:2]  # Get the first two characters
    target_sq = uci_notation[2:]  # Get the remaining characters starting from index 2
    return [first_sq,target_sq]

