import re
import sys
import argparse
import subprocess

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
    if not encoded_text or not encoded_text.strip():
        return ""

    decoded_chars = []

    matches = GROOT_PATTERN.findall(encoded_text)

    expected_phrases = len(encoded_text.strip().split(' ')) 
    if not matches or len(matches) != expected_phrases:
        raise ValueError("Invalid Groot Format")

    for i_part, am_part, groot_part in matches:

        first_bit = '1' if i_part == 'I' else '0'
        remaining_bits = "".join('1' if letter.isupper() else '0' for letter in am_part + groot_part)
        binary_string = first_bit + remaining_bits

        decoded_chars.append(chr(int(binary_string, 2)))

    return "".join(decoded_chars)

def run_interactive_cli():
    intro = "i Am GrOOT i AM gRoot i AM GRooT i aM groot i AM grooT i AM GroOt i AM grOoT i aM groot i AM GRooT i AM gROOT i AM GrOoT i aM groot i AM grOot i AM grOoT i AM groOT i AM gROOT i AM grOot i AM gRooT i AM gROOt i AM grOOT i aM groot i AM GrOot i AM gRoot i AM gRooT i AM GroOT i aM GROOT"
    print(intro)

    while True:
        choice = input("\nChoose an option (or type 'exit' to quit):\n1. Encode\n2. Decode\n> ")
        if choice.lower() in ['exit', 'quit']:
            break
        if choice == '1':
            original_text = input("Enter the text to encode: ")
            encoded_message = groot_encode(original_text)
            print("\nEncoded Message:")
            print(encoded_message)
        elif choice == '2':
            groot_text = input("Enter the Groot message to decode: ")
            try:
                decoded_message = groot_decode(groot_text)
                print("\nDecoded Message:")
                print(decoded_message)
            except (ValueError, IndexError):
                print("\nError: Invalid Groot format. Please check your input.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

def run_streamlit_ui():
    import streamlit as st

    st.set_page_config(
        page_title="Groot Translator",
        page_icon="🌳",
        layout="wide"  
    )

    st.title("Groot Translator 🌳")
    st.markdown("Type in either box, and the other will update automatically. Try it out!")

    if 'plain_text' not in st.session_state:
        st.session_state.plain_text = "Hello World!"

    if 'groot_text' not in st.session_state:
        st.session_state.groot_text = groot_encode(st.session_state.plain_text)

    def update_groot_from_plain():
        st.session_state.groot_text = groot_encode(st.session_state.plain_text)

    def update_plain_from_groot():
        groot_input = st.session_state.groot_text
        try:
            decoded_message = groot_decode(groot_input)
            st.session_state.plain_text = decoded_message
        except (ValueError, IndexError):

            st.session_state.plain_text = "--- Invalid Groot Format ---"

    col1, col2 = st.columns(2)

    with col1:
        st.header("Plain Text")
        st.text_area(
            "Enter plain text here:",
            key="plain_text",
            on_change=update_groot_from_plain,
            height=400,
            label_visibility="collapsed"
        )

    with col2:
        st.header("Groot Speak")
        st.text_area(
            "Enter Groot speak here:",
            key="groot_text",
            on_change=update_plain_from_groot,
            height=400,
            label_visibility="collapsed"
        )

def main():
    parser = argparse.ArgumentParser(
        description="Groot Translator CLI, Web UI, and File.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '--run-web-app-internally', action='store_true', help=argparse.SUPPRESS
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-i', '--interactive', action='store_true', help='Run the interactive command-line interface.'
    )
    group.add_argument(
        '-w', '--web', action='store_true', help='Launch the Streamlit web UI.'
    )
    group.add_argument(
        '-fe', '--file-encode', metavar='FILEPATH', help='Encode the contents of a specified file.'
    )
    group.add_argument(
        '-fd', '--file-decode', metavar='FILEPATH', help='Decode the contents of a specified file.'
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.file_encode:
        try:
            with open(args.file_encode, 'r', encoding='utf-8') as f:
                content = f.read()
            print(groot_encode(content))
        except FileNotFoundError:
            print(f"Error: File not found at '{args.file_encode}'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred during file encoding: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.file_decode:
        try:
            with open(args.file_decode, 'r', encoding='utf-8') as f:
                content = f.read()
            print(groot_decode(content))
        except FileNotFoundError:
            print(f"Error: File not found at '{args.file_decode}'", file=sys.stderr)
            sys.exit(1)
        except (ValueError, IndexError):
            print("Error: The file content is not in a valid Groot format.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred during file decoding: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.web:
        print("Launching Streamlit web UI...", file=sys.stderr)
        try:
            subprocess.run([
                sys.executable, '-m', 'streamlit', 'run', sys.argv[0],
                '--', '--run-web-app-internally'
            ], check=True)
        except FileNotFoundError:
            print("\nError: `streamlit` command not found.", file=sys.stderr)
            print("Please install Streamlit to use the web UI: pip install streamlit", file=sys.stderr)
        except subprocess.CalledProcessError as e:
            print(f"\nAn error occurred while launching Streamlit: {e}", file=sys.stderr)

    elif args.run_web_app_internally:
        run_streamlit_ui()

    elif args.interactive:
        run_interactive_cli()

if __name__ == "__main__":
    main()
