from bs4 import BeautifulSoup, ResultSet
import requests


def get_soup_page(url: str) -> BeautifulSoup:
    page: requests.Response = requests.get(url)
    soup_page = BeautifulSoup(page.content, "html.parser")

    return soup_page


def get_citations_needed_count(soup_page: BeautifulSoup) -> int:
    paragraphs: ResultSet = soup_page.find_all(
        "a", {"title": "Wikipedia:Citation needed"})

    return(len(paragraphs))


def get_citations_needed_report(soup_page: BeautifulSoup) -> list[str]:
    output: list[str] = []

    paragraph_text = [paragraph.get_text()
                      for paragraph in soup_page.find_all('p')]

    paragraph_text = "".join([sentence.replace("\n", "")
                              for sentence in paragraph_text])

    split_text: list[str] = paragraph_text.split(".")

    filtered_text: list[str] = filter(lambda paragraph: paragraph.startswith(
        "[citation needed]"), split_text)

    for p in filtered_text:
        trimmed_text: str = p.replace("[citation needed] ", "")
        trimmed_text = trimmed_text.replace("[citation needed]", "")
        output.append(trimmed_text)

    return output


if __name__ == "__main__":
    url = 'https://en.wikipedia.org/wiki/Russo-Ukrainian_War'

    soup_page: BeautifulSoup = get_soup_page(url)

    citations_needed: int = get_citations_needed_count(soup_page)
    citations_report: list[str] = get_citations_needed_report(soup_page)

    print("Citations needed:", citations_needed)
    print("Citations report:")
    for sentence in citations_report:
        print(sentence)
