def replace_invalid_characters_with_space(input_string):
    invalid_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_characters:
        input_string = input_string.replace(char, '_')

    return input_string
