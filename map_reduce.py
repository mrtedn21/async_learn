import functools


def map_frequency(text: str) -> dict[str, int]:
    frequencies = {}
    for word in text.split():
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies


def merge_dicts(first_dict, second_dict):
    for key, value in first_dict.items():
        second_dict[key] = second_dict.get(key, 0) + value
    return second_dict


lines = [
    'i know what i know',
    'i know what i know',
    'i dont know much',
    'they dont know much',
]


dicts = [map_frequency(line) for line in lines]
[print(d) for d in dicts]
print(functools.reduce(merge_dicts, dicts))

