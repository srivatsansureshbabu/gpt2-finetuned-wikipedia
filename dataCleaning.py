import wikipedia
import pandas as pd
import re

# gets a random page from wikipedia
def getRandomPage():
    while True:
        random_title = wikipedia.random()
        print(f"Trying page: {random_title}")
        try:
            page = wikipedia.page(random_title)
            return page
        except wikipedia.exceptions.PageError:
            print(f"PageError: '{random_title}' does not exist, trying again...")
            continue
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"DisambiguationError: '{random_title}' is ambiguous, options: {e.options[:3]}... trying again...")
            continue


# gets a specific page of certain topic. i.e. getSpecificPage("phone")
def getSpecificPage(item):
    results = wikipedia.search(item)

    # Match only titles with the whole word 'skate'
    pattern = re.compile(rf'\b{re.escape(item)}\b', re.IGNORECASE)
    filtered_results = [title for title in results if pattern.search(title)]
    print("Filtered results:", filtered_results)

    while filtered_results:
        title = filtered_results.pop(0)
        try:
            page = wikipedia.page(title, auto_suggest=False)  # Turn off auto-suggest
            # Ensure returned page title contains "skate" (whole word)
            if pattern.search(page.title):
                print(f"Found valid page: {page.title}")
                return page
            else:
                print(f"Rejected page: {page.title}")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"DisambiguationError: '{title}' ambiguous, options: {e.options[:3]}")
        except wikipedia.exceptions.PageError:
            print(f"PageError: '{title}' not found, trying next.")
        except Exception as e:
            print(f"Unexpected error for '{title}': {e}")

    print("No suitable page found.")
    return None
# gets skateboarding wikipedia page
def getSkateboardingPage():
    results = wikipedia.search("skate")

    # Match only titles with the whole word 'skate'
    pattern = re.compile(r'\bskate\b', re.IGNORECASE)
    filtered_results = [title for title in results if pattern.search(title)]
    print("Filtered results:", filtered_results)

    while filtered_results:
        title = filtered_results.pop(0)
        try:
            page = wikipedia.page(title, auto_suggest=False)  # Turn off auto-suggest
            # Ensure returned page title contains "skate" (whole word)
            if pattern.search(page.title):
                print(f"Found valid page: {page.title}")
                return page
            else:
                print(f"Rejected page: {page.title}")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"DisambiguationError: '{title}' ambiguous, options: {e.options[:3]}")
        except wikipedia.exceptions.PageError:
            print(f"PageError: '{title}' not found, trying next.")
        except Exception as e:
            print(f"Unexpected error for '{title}': {e}")

    print("No suitable page found.")
    return None

def convertPageintoDataFrame(page):
    lines = page.content.split('\n')  # Split into lines
    df = pd.DataFrame(lines, columns=["text"])
    return df

# removes lines that have no data
def removeEmptyData(df):
    df = df[df['text'].str.strip() != '']
    return df

# removes headers like == Header ==
def removeHeaders(df):
    # Remove lines with equal signs (existing)
    df = df[~df["text"].str.match(r"^=+.*=+$")]

    # Remove lines with fewer than 3 words (likely headers or short names)
    df = df[df["text"].str.split().str.len() >= 3]

    # Optionally, remove lines that are only uppercase or titlecase words (common for headers)
    df = df[~df["text"].str.match(r"^[A-Z][a-z]+(\s[A-Z][a-z]+)*$")]
    return df.reset_index(drop=True)

# removes junk white spaces
def removeExtraWhiteSpaces(df):
    df["text"] = df["text"].str.strip().replace(r"\s+", " ", regex=True)
    return df

# does all operations
def cleanDataFrame(df):
    df = removeEmptyData(df)
    df = removeHeaders(df)
    df = removeExtraWhiteSpaces(df)
    return df



