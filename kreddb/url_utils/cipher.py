ID_MAP = ['z', 'Q', 'x', 'J', 'k', 'V', 'b', 'P', 'y', 'G']


def cipher_id(digit_id: str):
    letter_id = ['_']
    for digit in digit_id:
        letter_id.append(ID_MAP[int(digit)])
    return ''.join(letter_id)


def decipher_id(letter_id) -> str:
    digit_id = list()
    for letter in letter_id[1:]:
        digit_id.append(str(ID_MAP.index(letter)))
    return ''.join(digit_id)