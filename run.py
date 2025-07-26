from dataCleaning import *


def main():
    # randomPage = getRandomPage()
    keyword = input("Type in a keyword > ")
    randomPage = getSpecificPage(keyword)
    print(randomPage.content)
    randomPageDataFrame = convertPageintoDataFrame(randomPage)
    randomPageDataFrame = cleanDataFrame(randomPageDataFrame)
    print(randomPageDataFrame)

if __name__ == "__main__":
    main()

