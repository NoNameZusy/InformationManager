import wikipedia
import warnings
import os

def select_language():
    languages = wikipedia.languages()
    print("Please select a language:")
    for code, lang in languages.items():
        print(f"{code}: {lang}")

    selected_language = input("Select the language code: ").lower()

    if selected_language == '0':
        return None

    if selected_language not in languages:
        print("Invalid language code, please try again.")
        return select_language()

    return selected_language

def search_wikipedia(text, language):
    try:
        wikipedia.set_lang(language)
        results = wikipedia.search(text)
        if len(results) == 1:
            page = wikipedia.page(results[0])
            return page.summary
        elif len(results) > 1:
            print("Multiple results found. Please select one:")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result}")
            choice = input("Enter the number corresponding to your choice: ")
            try:
                choice = int(choice)
                if 1 <= choice <= len(results):
                    page = wikipedia.page(results[choice - 1])
                    return page.summary
                else:
                    print("Invalid choice. Please enter a valid number.")
                    return search_wikipedia(text, language)
            except ValueError:
                print("Invalid choice. Please enter a valid number.")
                return search_wikipedia(text, language)
        else:
            return None
    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.page(e.options[0]).summary
    except wikipedia.exceptions.PageError:
        return None

def main():
    os.system('clear')

    try:
        with open("language.txt", "r") as file:
            language = file.read()
    except FileNotFoundError:
        language = None

    if language is None or language == '0':
        language = select_language()
        if language is None:
            return
        else:
            with open("language.txt", "w") as file:
                file.write(language)

    os.system('clear')

    while True:
        text = input("What topic do you want to get information about? (Press 0 to change language, or press Enter to exit): ")

        if text == '0':
            os.system('clear')
            language = select_language()
            if language is None:
                return
            else:
                with open("language.txt", "w") as file:
                    file.write(language)
                os.system('clear')
                main()
        elif text.strip() == '':
            return

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            answer = search_wikipedia(text, language)

        os.system('clear')

        print("\nInformation retrieved:")
        if answer:
            print(answer)
        else:
            print("Sorry, the specified topic could not be found.")

if __name__ == "__main__":
    main()
