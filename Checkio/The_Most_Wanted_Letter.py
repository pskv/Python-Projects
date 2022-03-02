def checkio(text: str) -> str:
    alph = set(map(chr, range(ord('a'), ord('z')+1)))
    letters_from_text = dict()
    for letter in text.lower():
        if letter in alph:
            letters_from_text[letter] = letters_from_text.setdefault(letter, 0) + 1
    return sorted(letters_from_text, key=lambda x: (-letters_from_text[x], x))[0]

if __name__ == '__main__':
    print("Example:")
    print(checkio("Hello World!"))

    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio("Hello World!") == "l", "Hello test"
    assert checkio("How do you do?") == "o", "O is most wanted"
    assert checkio("One") == "e", "All letter only once."
    assert checkio("Oops!") == "o", "Don't forget about lower case."
    assert checkio("AAaooo!!!!") == "a", "Only letters."
    assert checkio("abe") == "a", "The First."
    print("Start the long test")
    assert checkio("a" * 9000 + "b" * 1000) == "a", "Long."
    print("The local tests are done.")
