import os
import openai
import requests
from bs4 import BeautifulSoup

# openai.api_key = os.getenv("OPENAI_API_KEY")


def web_search(query: str) -> str:
    try:
        print("IT RAN>>>>>>>>>>")
        url = "https://www.drugs.com/search.php"
        params = {
            "searchterm": f"{query}",
            "a": "1"
        }
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        first_result = soup.find("div", class_="ddc-media-list ddc-search-results").find("a")
        if first_result:
            href = first_result.get("href")
            if href:
                response = requests.get(href)
                soup = BeautifulSoup(response.content, "html.parser")
                result = soup.find("div", class_="contentBox")
                if result:
                    return result.text
    except Exception as e:
        print('\nError: ', e)
        return "I’m sorry, we’re having technical difficulties, can you please ask your question again?"
