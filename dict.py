from collections import Counter


import sys


def generate_dictionary(text, min_len=20, max_len=40, top_n=1000):
    substr_counter = Counter()
    length = len(text)
    total_lengths = max_len - min_len + 1
    print("Generating dictionary, this might take a while...")

    for idx, l in enumerate(range(min_len, max_len + 1), 1):
        for i in range(length - l + 1):
            substr = text[i:i+l]
            substr_counter[substr] += 1
        progress = (idx / total_lengths) * 100
        print(
            f"Processed substrings of length {l}/{max_len} ({progress:.1f}%)")
        sys.stdout.flush()

    repeated = {k: v for k, v in substr_counter.items() if v > 1}

    ranked = sorted(repeated.items(),
                    key=lambda x: x[1] * len(x[0]), reverse=True)

    dictionary = {}
    for idx, (substr, freq) in enumerate(ranked[:top_n]):
        dictionary[f"#{idx}#"] = substr

    print(f"Dictionary generated with {len(dictionary)} entries.")
    return dictionary


def encode(text, dictionary):
    items = sorted(dictionary.items(), key=lambda x: len(x[1]), reverse=True)
    encoded = text
    for token, substr in items:
        encoded = encoded.replace(substr, token)
    return encoded


def decode(encoded_text, dictionary):
    decoded = encoded_text
    for token, substr in dictionary.items():
        decoded = decoded.replace(token, substr)
    return decoded


if __name__ == "__main__":
    with open("data.json", "r", encoding="utf-8") as f:
        data = f.read()

    dict_map = generate_dictionary(data)

    encoded = encode(data, dict_map)
    print("Encoded size:", len(encoded), "Original size:", len(data))

    decoded = decode(encoded, dict_map)
    print("Decoded matches original:", decoded == data)
