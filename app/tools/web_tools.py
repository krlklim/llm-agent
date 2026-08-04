# app/tools/web_tools.py
import re
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from googlesearch import search as google_search_lib
from youtube_transcript_api import YouTubeTranscriptApi

def duckduckgo_web_search(query: str, max_results: int = 5) -> str:
    try:
        results = []
        with DDGS() as ddgs:
            ddg_results = list(ddgs.text(query, max_results=max_results))
            for r in ddg_results:
                results.append(
                    f"Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}\n"
                )

        if not results:
            return "Nothing found in DuckDuckGo."
        return "\n---\n".join(results)
    except Exception as e:
        return f"DuckDuckGo Search Error: {e}"

def google_web_search(query: str, max_results: int = 5) -> str:
    try:
        results = []
        search_results = google_search_lib(
            query, num_results=max_results, advanced=True
        )

        for r in search_results:
            results.append(
                f"Title: {r.title}\nURL: {r.url}\nSnippet: {r.description}\n"
            )

        if not results:
            return "Nothing found in Google."
        return "\n---\n".join(results)
    except Exception as e:
        return f"Google Search Error: {e}"

def fetch_web_page(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        for element in soup(["script", "style", "nav", "header", "footer"]):
            element.decompose()
            
        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(lines)
        
        return clean_text[:8000] + "\n...[cut]" if len(clean_text) > 8000 else clean_text
    except Exception as e:
        return f"Error with {url}: {e}"

def get_youtube_transcript(url_or_video_id: str) -> str:
    try:
        video_id = url_or_video_id.strip()
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url_or_video_id)
        if match:
            video_id = match.group(1)

        api = YouTubeTranscriptApi()
        
        transcript_list_obj = api.list(video_id)
        
        first_transcript = next(iter(transcript_list_obj))
        
        transcript_data = first_transcript.fetch()

        lines = []
        for item in transcript_data:
            if hasattr(item, 'text'):
                lines.append(item.text)
            elif isinstance(item, dict) and 'text' in item:
                lines.append(item['text'])
            else:
                lines.append(str(item))

        full_transcript = " ".join(lines)
        if not full_transcript.strip():
            return f"Transcript for video '{video_id}' is empty."

        return full_transcript[:10000] + "\n...[cut]" if len(full_transcript) > 10000 else full_transcript

    except Exception as e:
        return f"Could not retrieve transcript for video ID '{video_id}'. Error: {str(e)}"
