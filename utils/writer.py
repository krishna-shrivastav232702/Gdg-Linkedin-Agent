import google.generativeai as genai
import re
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

# --- Helper function to make text bold (Unicode bold letters) ---
def to_bold(text: str) -> str:
    bold_map = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
        "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
    )
    return text.translate(bold_map)


def write_linkedin_post(research_summary, tone="professional", length="short"):
    """
    Generate a LinkedIn post draft from research summary with real bold and emojis.
    """
    if length == "short":
        word_target = "100-160"
    elif length == "medium":
        word_target = "160-260"
    else:
        word_target = "260-350"

    prompt = (
        f"You are an expert LinkedIn content writer specializing in creating engaging, "
        f"visually appealing posts for professionals and learners.\n\n"
        f"Using the research summary below, write a compelling LinkedIn post that is polished, "
        f"professional, and formatted for maximum readability.\n\n"
        f"Tone: {tone}\nTarget length: {word_target} words.\n\n"
        "Formatting & style guidelines:\n"
        "• Start with a 1-2 line attention-grabbing hook.\n"
        "• Use emojis naturally to emphasize key ideas (2-6 total).\n"
        "• Use **bold markdown** for important terms — e.g., **AI**, **Innovation**, **Learning**.\n"
        "• Keep paragraphs short (1-3 lines).\n"
        "• End with a reflective question or CTA.\n"
        "• Add 3-5 relevant hashtags.\n\n"
        f"Research summary:\n{research_summary}\n\n"
        "Return only the final formatted post (no extra notes)."
    )

   
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    post = response.text.strip()

    # Convert **bold markdown** to Unicode bold
    post = re.sub(r"\*\*(.*?)\*\*", lambda m: to_bold(m.group(1)), post)

    return post
