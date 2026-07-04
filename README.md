Enigma Chat:---------------------------------------------------

A working simulator of the WWII Enigma cipher machine, built from scratch to learn Python — now with a browser version too, so you can encrypt and decrypt messages with a friend without either of you installing anything.

There are two versions in this repo. They use the identical encryption logic and will always produce matching results for the same settings, so you can mix and match — you could run the Python version while your friend uses the webpage.

Files:------------------------------------------------------------

enigma.py — command-line version. Includes single-message mode and a two-person "same terminal" chat mode.
enigma.html — browser version. Open it directly in any browser (desktop or mobile, no install needed). Lights up like the real machine's lampboard as you type, with spinning rotor windows and a mechanical click.


How the encryption works:------------------------------------------

When a letter is typed, the signal passes:

keyboard -> plugboard -> rotor 1 -> rotor 2 -> rotor 3 -> reflector
         -> rotor 3 -> rotor 2 -> rotor 1 -> plugboard -> lamp lights up

Before every keypress, rotor 1 (the fastest rotor) steps forward one position, like a car odometer. When a rotor passes its "notch" letter, it also pushes the next rotor forward — this is what makes the cipher change with every letter instead of repeating a pattern.

Because the reflector sends the signal back through the same rotor positions it just came from, the machine is symmetric: encrypting a message twice with the exact same starting settings returns the original message. That's how one machine (or one webpage) can both encrypt and decrypt.

Using the Python version:---------------------------------------------------------

python3 enigma.py

You'll be asked for:


Your message
Plugboard pairs (e.g. AQ BZ — leave blank for none)
Starting positions for each of the 3 rotors (a single letter, A–Z)


Choose option 2 at the menu for a simple two-person chat mode in the same terminal.

Using the browser version:-------------------------------------------------------

Just open enigma.html in a browser — double-click it, or if using GitHub Pages, visit the hosted link.


Agree on the same rotor start letters and plugboard pairs as whoever you're chatting with — this is your shared secret key
Type a message under Compose & Encrypt, click Encrypt Message
Copy the resulting ciphertext and send it to your friend however you like (WhatsApp, SMS, email — it's just text)
They paste it into Decode Received Message on their own copy of the page, using the same settings, and get your original message back


Important: keeping both sides in sync:-----------------------------------------------------------

Both people must use identical settings — same rotor starting letters, same plugboard pairs — or decryption will produce garbage instead of the original message. Agree on these once before you start exchanging messages, the same way real Enigma operators shared a daily settings sheet.
