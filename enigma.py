
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Historical rotor wirings (these are the real Enigma I rotor wirings).
ROTOR_WIRINGS = {
    "I":   "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II":  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
}

# The notch is the letter that, when a rotor rotates past it,
# causes the NEXT rotor over to step forward too.
ROTOR_NOTCHES = {
    "I": "Q",
    "II": "E",
    "III": "V",
}

REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


# ---------------------------------------------------------------------------
# PLUGBOARD
# ---------------------------------------------------------------------------
def plugboard_swap(letter, pairs):
    """Swap a letter with its plugboard partner, if it has one."""
    if letter in pairs:
        return pairs[letter]
    return letter


def build_plug_pairs(pair_text):
    """
    Turns something like "AQ BZ" into a dictionary:
    {"A": "Q", "Q": "A", "B": "Z", "Z": "B"}
    """
    pairs = {}
    for pair in pair_text.upper().split():
        if len(pair) == 2:
            a, b = pair[0], pair[1]
            pairs[a] = b
            pairs[b] = a
    return pairs


# ---------------------------------------------------------------------------
# ROTOR
# ---------------------------------------------------------------------------
class Rotor:
    def __init__(self, name, start_letter="A"):
        self.name = name
        self.wiring = ROTOR_WIRINGS[name]
        self.notch = ROTOR_NOTCHES[name]
        self.position = ALPHABET.index(start_letter)  # 0-25

    def rotate(self):
        """Step this rotor forward by one position (wraps A->Z back to A)."""
        self.position = (self.position + 1) % 26

    def at_notch(self):
        """True if this rotor is currently sitting on its notch letter."""
        return ALPHABET[self.position] == self.notch

    def forward(self, letter):
        """Signal passing through the rotor on the way TO the reflector."""
        shifted_index = (ALPHABET.index(letter) + self.position) % 26
        wired_letter = self.wiring[shifted_index]
        unshifted_index = (ALPHABET.index(wired_letter) - self.position) % 26
        return ALPHABET[unshifted_index]

    def backward(self, letter):
        """Signal passing through the rotor on the way BACK from the reflector."""
        shifted_index = (ALPHABET.index(letter) + self.position) % 26
        shifted_letter = ALPHABET[shifted_index]
        wired_index = self.wiring.index(shifted_letter)
        unshifted_index = (wired_index - self.position) % 26
        return ALPHABET[unshifted_index]


def reflect(letter):
    """Bounce the signal back through the reflector (one-directional, fixed)."""
    position = ALPHABET.index(letter)
    return REFLECTOR_B[position]


# ---------------------------------------------------------------------------
# ROTOR STEPPING
# ---------------------------------------------------------------------------
def step_rotors(rotor1, rotor2, rotor3):
    """
    rotor1 = rightmost/fastest rotor, steps every single keypress.
    rotor2 steps when rotor1 is on its notch.
    rotor3 steps when rotor2 is on its notch.
    (This also reproduces the real "double-stepping" quirk of Enigma:
    if rotor2 is on its own notch, it steps again along with rotor3.)
    """
    rotor2_will_step = rotor1.at_notch() or rotor2.at_notch()
    rotor3_will_step = rotor2.at_notch()

    if rotor3_will_step:
        rotor3.rotate()
    if rotor2_will_step:
        rotor2.rotate()
    rotor1.rotate()


# ---------------------------------------------------------------------------
# FULL ENCRYPTION
# ---------------------------------------------------------------------------
def encrypt_letter(letter, plug_pairs, rotor1, rotor2, rotor3):
    letter = plugboard_swap(letter, plug_pairs)
    letter = rotor1.forward(letter)
    letter = rotor2.forward(letter)
    letter = rotor3.forward(letter)
    letter = reflect(letter)
    letter = rotor3.backward(letter)
    letter = rotor2.backward(letter)
    letter = rotor1.backward(letter)
    letter = plugboard_swap(letter, plug_pairs)
    return letter


def encrypt_message(message, plug_pairs, rotor1, rotor2, rotor3):
    result = ""
    for letter in message.upper():
        if letter not in ALPHABET:
            # leave spaces, numbers, punctuation untouched (real Enigma
            # couldn't handle these either, so this is a friendly extra)
            result += letter
            continue
        step_rotors(rotor1, rotor2, rotor3)
        result += encrypt_letter(letter, plug_pairs, rotor1, rotor2, rotor3)
    return result


# ---------------------------------------------------------------------------
# MAIN PROGRAM: single message mode
# ---------------------------------------------------------------------------
def run_single_message():
    print("=== ENIGMA MACHINE SIMULATOR ===\n")

    message = input("Enter your message: ")

    plug_text = input(
        "Enter plugboard pairs, e.g. 'AQ BZ' (or press Enter for none): "
    )
    plug_pairs = build_plug_pairs(plug_text)

    print("\nChoose starting positions for each rotor (a single letter A-Z).")
    start1 = input("Rotor 1 start letter [default A]: ").upper() or "A"
    start2 = input("Rotor 2 start letter [default A]: ").upper() or "A"
    start3 = input("Rotor 3 start letter [default A]: ").upper() or "A"

    rotor1 = Rotor("I", start1)
    rotor2 = Rotor("II", start2)
    rotor3 = Rotor("III", start3)

    output = encrypt_message(message, plug_pairs, rotor1, rotor2, rotor3)

    print("\nResult:", output)
    print(
        "\nTo decrypt this, run the program again with the SAME plugboard "
        "pairs and the SAME rotor start letters, entering the result above "
        "as your message."
    )


# ---------------------------------------------------------------------------
# MAIN PROGRAM: two-person chat mode
# ---------------------------------------------------------------------------
def run_chat():
    print("=== ENIGMA CHAT ===\n")
    print("Both people must agree on the SAME settings below before chatting,")
    print("just like real Enigma operators sharing a daily codebook.\n")

    plug_text = input(
        "Shared plugboard pairs, e.g. 'AQ BZ' (or press Enter for none): "
    )
    plug_pairs = build_plug_pairs(plug_text)

    print("\nShared rotor starting positions (a single letter A-Z each).")
    start1 = input("Rotor 1 start letter [default A]: ").upper() or "A"
    start2 = input("Rotor 2 start letter [default A]: ").upper() or "A"
    start3 = input("Rotor 3 start letter [default A]: ").upper() or "A"

    print("\nSettings locked in. Type 'quit' at any time to stop.\n")

    turn = 1
    while True:
        speaker = "Person A" if turn % 2 == 1 else "Person B"
        message = input(f"{speaker} types: ")
        if message.strip().upper() == "QUIT":
            print("Chat ended.")
            break

        # Reset rotors to the shared starting position for EVERY message.
        # This keeps both sides in sync, the same way real operators agreed
        # on a fresh starting position for each message they sent.
        rotor1 = Rotor("I", start1)
        rotor2 = Rotor("II", start2)
        rotor3 = Rotor("III", start3)

        encrypted = encrypt_message(message, plug_pairs, rotor1, rotor2, rotor3)
        print(f"  -> sent over the wire as: {encrypted}")

        # Simulate the other side receiving and decrypting it.
        rotor1 = Rotor("I", start1)
        rotor2 = Rotor("II", start2)
        rotor3 = Rotor("III", start3)
        decrypted = encrypt_message(encrypted, plug_pairs, rotor1, rotor2, rotor3)
        other = "Person B" if turn % 2 == 1 else "Person A"
        print(f"  -> {other} reads: {decrypted}\n")

        turn += 1


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
def main():
    print("1) Encrypt/decrypt a single message")
    print("2) Chat mode (two people, same terminal)")
    choice = input("Choose 1 or 2: ").strip()

    if choice == "2":
        run_chat()
    else:
        run_single_message()


if __name__ == "__main__":
    main()