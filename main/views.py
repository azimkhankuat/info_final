import random

from django.shortcuts import render
from django.http import HttpResponse
import string


# Create your views here.

def index(request):
    return render(request, "main/index.html")


def otp_encrypt(request):
    abc = string.ascii_lowercase
    one_time_pad = list(abc)
    ciphertext = ''
    msg = request.GET['input_text']
    key = request.GET['otp_key']
    for idx, char in enumerate(msg):
        charIdx = abc.index(char)
        keyIdx = one_time_pad.index(key[idx])

        cipher = (keyIdx + charIdx) % len(one_time_pad)
        ciphertext += abc[cipher]

    return render(request, "main/index.html", {'ciphertext': ciphertext})


def huffmanEncode(request):
    # START - PART1
    input_text = request.GET['otp_encrypted']
    f = {}  # all frequencies
    prob = {}  # probability

    for x in input_text:  # find frequencies
        if x in f:
            f[x] = f[x] + 1
        else:
            f[x] = 1

    all_chars = sum(f.values())  # find total chars

    for x in input_text:  # find probabilities
        prob[x] = f[x] / all_chars
    # END - PART1

    # START - PART2
    values = []
    symbols = []
    for key, val in sorted(prob.items(), key=lambda prob: prob[1], reverse=True):
        values.append(val)
        symbols.append(key)

    def divideList(list1):
        left = 0
        right = 0
        m = 0
        arr1 = []
        arr2 = []
        for i in range(0, len(list1)):
            if len(list1) - m <= i:
                break
            left += list1[i]
            arr1.append(list1[i])
            for j in range(m + 1, len(list1)):
                if len(list1) - i == j:
                    m = j
                    break
                right += list1[-j]
                arr2.insert(0, list1[-j])
                if left <= right:
                    m = j
                    break
                m = j
        return arr1, arr2

    code = []

    def labeling(list1, t1):
        arr1, arr2 = divideList(list1)
        if len(arr1) != 1:
            labeling(arr1, t1 + '0')
        else:
            code.append(t1 + '0')
        if len(arr2) != 1:
            labeling(arr2, t1 + '1')
        else:
            code.append(t1 + '1')

    labeling(values, '')

    dictionary_result = dict(zip(symbols, code))
    for key in dictionary_result:
        print(key, "-", dictionary_result[key])

    encoded = []
    huffman_encoded = ''
    for i in input_text:
        for j in range(len(symbols)):
            if i == symbols[j]:
                print(code[j], end='')
                encoded.append(code[j])
                huffman_encoded += code[j]

    # CALCULATING COMPRESSION RATION
    b1 = 0
    b0 = all_chars
    for symbol, freq in f.items():
        for key, value in dictionary_result.items():
            if symbol == key:
                b1 += freq * len(value)

    comp_ratio = b0 / b1

    return render(request, "main/index.html",
                  {'huffman_encoded': huffman_encoded, 'dictionary_result': dictionary_result, 'comp_ratio': comp_ratio})


def huffmanDecode(request):
    def listToString(s):
        # initialize an empty string
        str1 = ""

        # traverse in the string
        for element in s:
            str1 += element

        return str1

    decode_input = request.GET['huffman_encoded']
    dictionary_result = eval(request.GET['dictionary_result'])

    temp = []
    huffman_decoded = []

    for code in decode_input:
        temp.append(code)
        for key, value in dictionary_result.items():
            if listToString(temp) == value:
                huffman_decoded.append(key)
                temp = []

    return render(request, "main/index.html",
                  {'huffman_encoded': decode_input, 'huffman_decoded': listToString(huffman_decoded),
                   'dictionary_result': dictionary_result})


def hammingEncode(request):
    dictionary_result = request.GET['dictionary_result']
    input_hamming = request.GET['huffman_encoded3']

    # Indexes of each bit:
    # i1 = 0, i2 = 1, i3 = 2, i4 = 3
    def hamming_encode(binary):
        r1 = compute_parity(binary, [0, 1, 2])  # i1, i2, i3
        r2 = compute_parity(binary, [1, 2, 3])  # i2, i3, i4
        r3 = compute_parity(binary, [0, 1, 3])  # i1, i2, i4
        result = binary + r1 + r2 + r3
        return result

    def compute_parity(s, indexes):
        sub = ''
        for i in indexes:
            sub += s[i]
        return str(str.count(sub, "1") % 2)

    divided_into_four = []
    for i in range(0, len(input_hamming), 4):
        divided_into_four.append(input_hamming[i: i + 4])

    hamming_encoded = ''
    print("Input for Hamming: " + input_hamming)
    for i in divided_into_four:
        if len(i) >= 4:
            output = hamming_encode(i)
            hamming_encoded += output

    print("Output for Hamming:" + hamming_encoded)
    print("")

    return render(request, "main/index.html",
                  {'hamming_encoded': hamming_encoded, 'dictionary_result': dictionary_result})


def addError(request):
    dictionary_result = request.GET['dictionary_result']

    def listToString(s):
        # initialize an empty string
        str1 = ""

        # traverse in the string
        for element in s:
            str1 += element

        return str1

    def makeError(array):
        array_with_errors = []
        for ele in array:
            random_index = random.randint(0, 6)
            # print(random_index)
            if ele[random_index] == '0':
                before = ele[:random_index]
                after = ele[random_index + 1:]
                substr = before + ele[random_index].replace('0', '1') + after
                array_with_errors.append(substr)
            else:
                before = ele[:random_index]
                after = ele[random_index + 1:]
                substr = before + ele[random_index].replace('1', '0') + after
                array_with_errors.append(substr)

        return array_with_errors

    hamming_encoded = request.GET['hamming_encoded2']
    divided_into_seven = []
    for i in range(0, len(hamming_encoded), 7):
        divided_into_seven.append(hamming_encoded[i: i + 7])

    withError = makeError(divided_into_seven)
    print("With parities:")
    print(divided_into_seven)
    print("With errors:")
    print(withError)

    # print("String with parities:" + hamming_encoded)
    string_with_error = listToString(withError)
    # print("String with parities and errors: " + string_with_error)
    print("")

    return render(request, "main/index.html", {'with_error': withError, 'string_with_error': string_with_error,
                                               'dictionary_result': dictionary_result})


def hammingDecode(request):
    dictionary_result = eval(request.GET['dictionary_result'])
    withError = request.GET['error_added2']

    divided_by_seven = []
    for i in range(0, len(withError), 7):
        divided_by_seven.append(withError[i: i + 7])
    print("Divided by 7: ", divided_by_seven)

    def listToString(s):
        # initialize an empty string
        str1 = ""

        # traverse in the string
        for element in s:
            str1 += element

        return str1

    def hamming_decode(binary):
        s1 = syndrome(binary, [4, 0, 1, 2])
        s2 = syndrome(binary, [5, 1, 2, 3])
        s3 = syndrome(binary, [6, 0, 1, 3])
        result = s1 + s2 + s3
        return result

    def syndrome(s, indexes):
        sub = ''
        for i in indexes:
            sub += s[i]
        return str(str.count(sub, "1") % 2)

    decode_syndromes = []
    for i in divided_by_seven:
        if len(i) >= 7:
            out = hamming_decode(i)
            decode_syndromes.append(out)

    print("Syndromes:")
    print(decode_syndromes)
    # i1 = 0, i2 = 1, i3 = 2, i4 = 3, r1 = 4, r2 = 5, r3 = 6
    syndromes = {'001': 6, '010': 5, '011': 3, '100': 4, '101': 0, '110': 2, '111': 1}
    syndrome_indexes = []
    for ele in decode_syndromes:
        for key, value in syndromes.items():
            if ele == key:
                syndrome_indexes.append(value)

    print("Error syndrome indexes:")
    print(syndrome_indexes)
    hamming_decoded = []

    for i, j in zip(divided_by_seven, syndrome_indexes):
        if i[j] == '0':
            str1 = i[:j] + '1' + i[j + 1:]
            hamming_decoded.append(str1)
        else:
            str1 = i[:j] + '0' + i[j + 1:]
            hamming_decoded.append(str1)

    print("Array with corrected errors: ", hamming_decoded)
    print("String with corrected errors: ", listToString(hamming_decoded))
    parities_deleted = ''
    for i in hamming_decoded:
        parities_deleted += i[:4]

    print("String with corrected errors and deleted parities: ", parities_deleted)
    print("")

    part6_temp = []
    part6_decode_output = []

    for code in parities_deleted:
        part6_temp.append(code)
        for key, value in dictionary_result.items():
            if listToString(part6_temp) == value:
                part6_decode_output.append(key)
                part6_temp = []

    return render(request, "main/index.html", {'hamming_decoded': listToString(part6_decode_output)})


def otp_decrypt(request):
    abc = string.ascii_lowercase
    one_time_pad = list(abc)

    def decrypt(ciphertext, key):
        if ciphertext == '' or key == '':
            return ''

        charIdx = abc.index(ciphertext[0])
        keyIdx = one_time_pad.index(key[0])

        cipher = (charIdx - keyIdx) % len(one_time_pad)
        char = abc[cipher]

        return char + decrypt(ciphertext[1:], key[1:])

    ciphertext = request.GET['hamming_decoded2']
    key = request.GET['decrypt_key']

    otp_decrypted = decrypt(ciphertext, key)
    return render(request, "main/index.html", {'otp_decrypted': otp_decrypted})