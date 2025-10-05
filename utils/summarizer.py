import google.generativeai as genai
from config import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)

def summarise_sources_to_bullets(sources, max_points=8):
    """
    Takes list of sources (each has title, url, snippet, content).
    Returns a combined research summary (bulleted).
    """
    prompt_parts = [
        "You are a concise research assistant. Read the following sources and produce up to "
        f"{max_points} bullet points summarizing the most credible, important, and timely facts "
        "useful for writing a LinkedIn post. Mention source titles (short) in parentheses when appropriate.\n\n"
    ]

    for i, s in enumerate(sources, start=1):
        heading = f"Source {i}: {s.get('title')}\nURL: {s.get('url')}\n"
        snippet = s.get("snippet") or ""
        content = s.get("content") or ""
        excerpt = (content[:2000] + "...") if content and len(content) > 2000 else content

        prompt_parts.append(heading)
        if snippet:
            prompt_parts.append("Snippet: " + snippet + "\n")
        if excerpt:
            prompt_parts.append("Content excerpt:\n" + excerpt + "\n")
        prompt_parts.append("\n---\n")

    prompt_parts.append("\nNow produce the bullet points.")
    prompt = "\n".join(prompt_parts)

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
