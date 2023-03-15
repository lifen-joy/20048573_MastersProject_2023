def main():
    print("Please enter the text you want to analyze:")
    user_input = input()

    # Clean and tokenize the text
    cleaned_text = clean_text(user_input)
    tokenized_text = tokenize_text(cleaned_text)

    # Analyze the text
    fem_words = find_gendered_words(tokenized_text, feminine_words)
    masc_words = find_gendered_words(tokenized_text, masculine_words)
    fem_pronouns = find_gendered_words(tokenized_text, feminine_pronouns)
    masc_pronouns = find_gendered_words(tokenized_text, masculine_pronouns)

    fem_total = len(fem_pronouns) * 2 + len(fem_words)
    masc_total = len(masc_pronouns) * 2 + len(masc_words)

    # Display the results
    if fem_total == 0 and masc_total == 0:
        print("The text is neutral.")
    elif fem_total > masc_total:
        print("The text is feminine.")
    else:
        print("The text is masculine.")

    print("Feminine words:", fem_words)
    print("Masculine words:", masc_words)
    print("Feminine pronouns:", fem_pronouns)
    print("Masculine pronouns:", masc_pronouns)

if __name__ == "__main__":
    main()
