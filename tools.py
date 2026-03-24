# tools.py
import os
import requests


class SearchTool:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("Missing TAVILY_API_KEY in environment variables.")

    def search(self, query: str) -> str:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 5,
            "include_answer": True,
            "include_raw_content": False,
        }

        try:
            response = requests.post(url, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()

            lines = []

            if data.get("answer"):
                lines.append(f"Answer Summary: {data['answer']}")

            results = data.get("results", [])
            if not results:
                return "No results found."

            for i, item in enumerate(results[:5], start=1):
                title = item.get("title", "No title")
                content = item.get("content", "No content")
                url = item.get("url", "No URL")
                lines.append(f"[{i}] {title}\n{content}\nURL: {url}")

            return "\n\n".join(lines)

        except requests.exceptions.RequestException as e:
            return f"Search API error: {str(e)}"
        except Exception as e:
            return f"Unexpected search error: {str(e)}"