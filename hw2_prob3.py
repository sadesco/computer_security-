import sys
from collections import Counter, defaultdict


# index of coincidence 
def compute_ic(text_string):
    counts = Counter(text_string)
    length = len(text_string)

    numerator = sum(counts.get(chr(i + 65), 0) *
                    (counts.get(chr(i + 65), 0) - 1)
                    for i in range(26))

    return numerator / (length * (length - 1))


# vigenère decryption 
def decode_vigenere(cipher, key_word):
    decrypted = []
    key_size = len(key_word)

    for position in range(len(cipher)):
        key_shift = ord(key_word[position % key_size]) - 65
        value = (ord(cipher[position]) - 65 - key_shift) % 26
        decrypted.append(chr(value + 65))

    return "".join(decrypted)


LETTER_DISTRIBUTION = [
    0.080, 0.015, 0.030, 0.040, 0.130, 0.020, 0.015, 0.060, 0.065, 0.005,
    0.005, 0.035, 0.030, 0.070, 0.080, 0.020, 0.002, 0.065, 0.060, 0.090,
    0.030, 0.010, 0.015, 0.005, 0.020, 0.002
]


# ciphertext
raw_text = """TTEUM GQNDV EOIOL EDIRE MQTGS DAFDR CDYOX IZGZP PTAAI TUCSI XFBXY 
SUNFE SQRHI SAFHR TQRVS VQNBE EEAQG IBHDV SNARI DANSL EXESX EDSNJ 
AWEXA ODDHX EYPKS YEAES RYOET OXYZP PTAAI TUCRY BETHX UFINR"""

cipher = raw_text.replace(" ", "").replace("\n", "")
N = len(cipher)


#  check
repeated_pairs = defaultdict(int)
for index in range(N - 1):
    segment = cipher[index:index + 2]
    repeated_pairs[segment] += 1



# print("Overall IC:", compute_ic(cipher))


# try possible key lengths
for possible_length in range(1, 26):
    partitions = [[] for _ in range(possible_length)]

    for idx, letter in enumerate(cipher):
        partitions[idx % possible_length].append(letter)

    ic_values = []
    for block in partitions:
        ic_values.append(compute_ic("".join(block)))

    avg_ic = sum(ic_values) / len(ic_values)
    # print(f"Key length {possible_length} -> Avg IC: {avg_ic}")


# frequency analysis 
chosen_length = 5
columns = [[] for _ in range(chosen_length)]

for i in range(N):
    columns[i % chosen_length].append(cipher[i])


for col_number in range(chosen_length):

    frequency_count = [0] * 26
    for character in columns[col_number]:
        frequency_count[ord(character) - 65] += 1

    scores = []

    for shift in range(26):
        total_score = 0
        for letter_index in range(26):
            adjusted_index = (letter_index - shift) % 26
            total_score += (
                (frequency_count[letter_index] / N)
                * LETTER_DISTRIBUTION[adjusted_index]
            )

        scores.append((total_score, shift))

    scores.sort()
    # print(f"Column {col_number} best shifts:", scores[-3:])


# use key
final_key = "AMAZE"
message = decode_vigenere(cipher, final_key)

print("\nDecrypted Text:")
print(message)