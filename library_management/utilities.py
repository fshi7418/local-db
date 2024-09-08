from fuzzywuzzy import fuzz


def is_fuzzy_match(new_name, existing_names, threshold=80):
    """
    Check if the new_name is similar to any name in existing_names
    using fuzzy matching.

    :param new_name: The name to check
    :param existing_names: List of existing names
    :param threshold: Similarity threshold (0-100)
    :return: True if a match is found, False otherwise
    """
    for name in existing_names:
        if fuzz.ratio(new_name.lower(), name.lower()) >= threshold:
            return True
    return False
