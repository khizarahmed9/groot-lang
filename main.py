import re

GROOT_PATTERN = re.compile(r'([Ii])\s(\w{2})\s(\w{5})')
BASE_PHRASE = "amgroot"

def groot_encode(text: str) -> str:
    encoded_phrases = []
    for char in text:
        binary = f'{ord(char):08b}'
        i_case = 'I' if binary[0] == '1' else 'i'

        amgroot_cased = "".join(
            letter.upper() if bit == '1' else letter.lower()
            for bit, letter in zip(binary[1:], BASE_PHRASE)
        )
        encoded_phrases.append(f"{i_case} {amgroot_cased[:2]} {amgroot_cased[2:]}")

    return " ".join(encoded_phrases)


def groot_decode(encoded_text: str) -> str:
    return "".join(
        chr(int(
            ('1' if i_part == 'I' else '0') +
            "".join('1' if letter.isupper() else '0' for letter in am_part + groot_part),
            2
        ))
        for i_part, am_part, groot_part in GROOT_PATTERN.findall(encoded_text)
    )


def main():
    print("i Am GrOOT i AM gRoot i AM GRooT i aM groot i AM grooT i AM GroOt i AM grOoT i aM groot i AM GRooT i AM gROOT i AM GrOoT i aM groot i AM grOot i AM grOoT i AM groOT i AM gROOT i AM grOot i AM gRooT i AM gROOt i AM grOOT i aM groot i AM GrOot i AM gRoot i AM gRooT i AM GroOT i aM GROOT")
    while True:
        choice = input("\nChoose an option:\n1. Encode\n2. Decode\n")
        if choice == '1':
            original_text = input("Enter the text to encode: ")
            encoded_message = groot_encode(original_text)
            print("\nEncoded Message:")
            print(encoded_message)
        elif choice == '2':
            groot_text = input("Enter the Groot message to decode: ")
            decoded_message = groot_decode(groot_text)
            print("\nDecoded Message:")
            print(decoded_message)
        else:
            print("Invalid choice. Please enter 1 or two")
            return


if __name__ == "__main__":
    main()
