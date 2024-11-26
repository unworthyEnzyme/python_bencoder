def decode_integer(input_string: str, index: int):
    assert len(input_string) > 0, "input string must be non-empty"
    assert input_string[index] == "i", "input string must start with an 'i'"

    # find the e
    index_of_e = input_string.find("e", index)
    if index_of_e == -1:
        raise ValueError("e was not found")

    # convert to the int
    try:
        the_number = int(input_string[index + 1 : index_of_e])
    except ValueError:
        raise ValueError("Invalid Integer format")

    # return
    return the_number, index_of_e + 1


def decode_string(input_string: str, index: int):
    assert len(input_string) > 0, "input string must be non-empty"
    assert input_string[index].isdigit(), "input string must start with a digit"

    # find the place of colon
    index_of_colon = input_string.find(":", index)
    if index_of_colon == -1:
        raise ValueError("there is no colon at the start.")

    # parse the length of string
    try:
        length_of_string = int(input_string[index:index_of_colon])
    except ValueError:
        raise ValueError("invalid length")

    # parse the string itself
    the_last_index = index_of_colon + 1 + length_of_string
    the_string = input_string[index_of_colon + 1 : the_last_index]

    # return the string
    return the_string, the_last_index


def decode_list(input_string: str, index: int):
    assert len(input_string) > 0, "input string must be non-empty"
    assert input_string[index] == "l", "input string must start with an 'l'"

    # raise index by one to get past l
    index += 1

    # init array
    the_list = []

    # start loop
    while index < len(input_string) and input_string[index] != "e":

        # decode integers
        if input_string[index] == "i":
            the_number, returned_index = decode_integer(input_string, index)
            index = returned_index
            the_list.append(the_number)

        # decode strings
        elif input_string[index].isdigit():
            the_string, returned_index = decode_string(input_string, index)
            index = returned_index
            the_list.append(the_string)

        # decode lists
        elif input_string[index] == "l":
            returned_list, returned_index = decode_list(input_string, index)
            index = returned_index
            the_list.append(returned_list)

        else:
            raise ValueError(f"Invalid character '{input_string[index]}' in list")

    return the_list, index + 1


def decode_dictionary(input_string: str, index: int) -> tuple[dict, int]:
    assert len(input_string) > 0, "input string must be non-empty"
    assert input_string[index] == "d", "input string must start with a 'd'"

    # raise index by one to get past d
    index += 1

    # init a dictionary
    the_dict = {}

    # start loop
    while index < len(input_string) and input_string[index] != "e":
        # decode the key(must be string)
        if input_string[index].isdigit():
            key_string, returned_index = decode_string(input_string, index)
            index = returned_index
        # error check
        else:
            raise ValueError("key must be string")
        # decode integers
        if input_string[index] == "i":
            value, returned_index = decode_integer(input_string, index)
            index = returned_index

        # decode strings
        elif input_string[index].isdigit():
            value, returned_index = decode_string(input_string, index)
            index = returned_index

        # decode lists
        elif input_string[index] == "l":
            value, returned_index = decode_list(input_string, index)
            index = returned_index

        elif input_string[index] == "d":
            value, returned_index = decode_dictionary(input_string, index)
            index = returned_index

        else:
            raise ValueError(f"Invalid character '{input_string[index]}' in dictionary")

        the_dict[key_string] = value

    return the_dict, index + 1


def read_torrent_file(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
    return content.decode("ISO-8859-1")


def bencode(file_path: str):
    input_string = read_torrent_file(file_path)

    decoded_data, _ = decode_dictionary(input_string, 0)
    return decoded_data
