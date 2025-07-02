def count_bin_prefix_occurrences(filename, bin_prefix):
    """
    Count the number of times the given BIN prefix occurs in the specified file.

    :param filename: The name of the file to search for BIN prefix occurrences.
    :param bin_prefix: The BIN prefix to search for.
    :return: The number of times the given BIN prefix occurs in the specified file.
    """
    count = 0
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith(bin_prefix):
                count += 1
    return count


def get_top_n_bin_prefixes(filename, n, digit_length):
    """
    Get a list of the top N most frequently occurring BIN prefixes of a certain digit length in the specified file.

    :param filename: The name of the file to search for BIN prefix occurrences.
    :param n: The number of top prefixes to return.
    :param digit_length: The length of the digit value to search for.
    :return: A list of the top N most frequently occurring BIN prefixes of the specified digit length in the specified file.
    """
    bin_prefix_counts = {}
    with open(filename, 'r') as file:
        for line in file:
            bin_prefix = line[:digit_length]
            if bin_prefix.isdigit() and len(bin_prefix) == digit_length:
                if bin_prefix in bin_prefix_counts:
                    bin_prefix_counts[bin_prefix] += 1
                else:
                    bin_prefix_counts[bin_prefix] = 1
    top_n_bin_prefixes = sorted(bin_prefix_counts, key=bin_prefix_counts.get, reverse=True)[:n]
    return top_n_bin_prefixes


def get_full_card_info(filename, bin_prefix):
    """
    Get a list of full card information starting with the given BIN prefix in the specified file.

    :param filename: The name of the file to search for full card information.
    :param bin_prefix: The BIN prefix to search for.
    :return: A list of full card information starting with the given BIN prefix in the specified file.
    """
    full_card_info = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith(bin_prefix):
                full_card_info.append(line.strip())
    return full_card_info


if __name__ == '__main__':
    filename = input("Please enter the name of the file to search for BIN prefixes: ")
    bin_prefix = input("Please enter a BIN prefix to search for (or leave blank to see top N prefixes): ")
    if bin_prefix:
        count = count_bin_prefix_occurrences(filename, bin_prefix)
        print(f"The BIN prefix {bin_prefix} appears {count} times in the file {filename}.")
        choice = input("Do you want to see all the card information starting with this prefix? (yes/no): ")
        if choice.lower() == "yes":
            full_card_info = get_full_card_info(filename, bin_prefix)
            print("Full card information starting with the given prefix:")
            for card_info in full_card_info:
                print(card_info)
    else:
        n = int(input("Please enter the number of top prefixes to display: "))
        digit_length = int(input("Please enter the length of the digit value to search for: "))
        top_n_bin_prefixes = get_top_n_bin_prefixes(filename, n, digit_length)
        print(f"The top {n} most frequently occurring BIN prefixes of length {digit_length} in the file are:")
        for bin_prefix in top_n_bin_prefixes:
            count = count_bin_prefix_occurrences(filename, bin_prefix)
            print(f"{bin_prefix}: {count}")
choice = input("Do you want to see all the card information for each of these prefixes? (yes/no): ")
if choice.lower() == "yes":
    for bin_prefix in top_n_bin_prefixes:
        full_card_info = get_full_card_info(filename, bin_prefix)
        print(f"\nFull card information starting with prefix {bin_prefix}:")
        for card_info in full_card_info:
            print(card_info)
