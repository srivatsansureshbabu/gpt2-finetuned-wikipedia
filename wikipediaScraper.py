import wikipedia
import pandas as pd
import re
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")

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

# gets a specific page of certain topic. i.e. getSpecificPage("phone")
def getAllPages(item):
    results = wikipedia.search(item)

    # Match only titles with the whole word 'skate'
    pattern = re.compile(rf'\b{re.escape(item)}\b', re.IGNORECASE)
    filtered_results = [title for title in results if pattern.search(title)]
    pages = []
    print("Filtered results:", filtered_results)

    while filtered_results:
        title = filtered_results.pop(0)
        try:
            page = wikipedia.page(title, auto_suggest=False)  # Turn off auto-suggest
            # Ensure returned page title contains "skate" (whole word)
            if pattern.search(page.title):
                print(f"Found valid page: {page.title}")
                pages.append(page)
            else:
                print(f"Rejected page: {page.title}")
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"DisambiguationError: '{title}' ambiguous, options: {e.options[:3]}")
        except wikipedia.exceptions.PageError:
            print(f"PageError: '{title}' not found, trying next.")
        except Exception as e:
            print(f"Unexpected error for '{title}': {e}")

    if len(pages) > 0:
        print(f"Found {len(pages)} articles.")
    else:
        print("No suitable page found.")
    return pages
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

def removeLatexExpressions(df):
    def cleanText(text):
        if not isinstance(text, str):
            return text
        # Remove math environments
        text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
        text = re.sub(r"\$.*?\$", "", text, flags=re.DOTALL)
        text = re.sub(r"\\\(.*?\\\)", "", text, flags=re.DOTALL)
        text = re.sub(r"\\\[.*?\\\]", "", text, flags=re.DOTALL)
        
        # Remove common LaTeX commands but keep the argument
        text = re.sub(r"\\[a-zA-Z]+", "", text)
        
        # Remove leftover braces carefully (only remove braces not around words)
        text = re.sub(r"\{|\}", "", text)
        
        # Optional: Replace Greek letters or common commands manually
        replacements = {
            r"\\beta": "beta",
            r"\\lambda": "lambda",
            r"\\sum": "sum",
            # add more if you want
        }
        for k, v in replacements.items():
            text = re.sub(k, v, text)

        # Clean extra whitespace
        text = re.sub(r"\s+", " ", text).strip()
        return text

    df["text"] = df["text"].apply(cleanText)
    return df

def removeMathFragments(df):
    def cleanText(text):
        if not isinstance(text, str):
            return text
        
        # Remove inline and display math
        text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
        text = re.sub(r"\$.*?\$", "", text)
        text = re.sub(r"\\\(.*?\\\)", "", text)
        text = re.sub(r"\\\[.*?\\\]", "", text)
        
        # Remove common math operators and LaTeX commands
        text = re.sub(r"\\[a-zA-Z]+", "", text)  # \commands like \log, \sum, \beta
        text = re.sub(r"\^_\{\w+\}", "", text)   # superscripts or subscripts like ^_{j}
        text = re.sub(r"[_\^][\{\[]?.*?[\}\]]?", "", text)  # _{...}, ^{...}, or _x, ^x
        text = re.sub(r"\b[A-Za-z]\b", "", text)  # remove isolated single letters (like variables)
        
        # Remove curly braces leftover
        text = text.replace("{", "").replace("}", "")
        
        # Remove multiple spaces
        text = re.sub(r"\s+", " ", text)
        
        return text.strip()
    
    df["text"] = df["text"].apply(cleanText)
    return df

# does all operations
def cleanDataFrame(df):
    df = removeEmptyData(df)
    df = removeHeaders(df)
    df = removeExtraWhiteSpaces(df)
    df = removeLatexExpressions(df)
    df = removeMathFragments(df)
    return df

def returnCleanedTextOfOneArticle(keyword):
    # keyword = "skate"
    randomPage = getSpecificPage(keyword)
    randomPageDataFrame = convertPageintoDataFrame(randomPage)
    randomPageDataFrame = cleanDataFrame(randomPageDataFrame)
    page = convertDataFrametoPage(randomPageDataFrame)
    return page

def returnCleanedTextOfAllArticles(keyword):
    randomPages = getAllPages(keyword)
    cleanedArticles = []
    for randomPage in randomPages:
        # print("randomPage > ", randomPage)
        randomPageDataFrame = convertPageintoDataFrame(randomPage)
        randomPageDataFrame = cleanDataFrame(randomPageDataFrame)
        page = convertDataFrametoPage(randomPageDataFrame)
        cleanedArticles.append(page)
    return cleanedArticles

def convertDataFrametoPage(df):
    text = "\n".join(df["text"].tolist())  # join with newlines
    return text

