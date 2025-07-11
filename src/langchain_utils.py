from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import re
from textstat import flesch_reading_ease
from datetime import datetime

load_dotenv()

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def save_output(content, output_dir, filename_prefix):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath

PRIMARY_KEYWORDS = [
    "seo", "search engine", "rank", "conversions", "website", "site speed",
    "structured data", "backlinks", "content strategy", "builder"
]
MAX_DENSITY = 0.02  # 2 % of total words
MIN_READING_SCORE = 40  # Flesch Reading Ease (higher is easier) – 40 corresponds to "fairly difficult" but acceptable for marketing copy


def _keyword_density(text: str, keyword: str) -> float:
    tokens = re.findall(r"\b\w+\b", text.lower())
    if not tokens:
        return 0.0
    kw_occurrences = len(re.findall(rf"\b{re.escape(keyword.lower())}\b", text.lower()))
    return kw_occurrences / len(tokens)


def validate_content(content: str, use_case: str | None = None) -> tuple[bool, str]:
    """Enhanced SEO validation.

    Checks:
    1. Contains at least one primary SEO keyword.
    2. Keyword density below MAX_DENSITY (spam prevention).
    3. Readability score >= MIN_READING_SCORE.
    """
    text_l = content.lower()

    present_keywords = [kw for kw in PRIMARY_KEYWORDS if kw in text_l]
    has_keyword = bool(present_keywords)

    # choose the first present keyword for density check, else the first primary
    density_kw = present_keywords[0] if present_keywords else PRIMARY_KEYWORDS[0]
    density = _keyword_density(content, density_kw)
    # Relax density rule for table-based calendars where total words are low
    if use_case == "calendar":
        # Calendar table: allow density up to 5% and max 6 occurrences
        density_ok = density <= 0.05
    else:
        density_ok = density <= MAX_DENSITY and density > 0

        # Prepare text for a more reliable readability score by removing URLs, hashtags, and emojis
    def _prepare_readability_text(txt: str) -> str:
        txt = re.sub(r"http\S+", "", txt)  # strip URLs
        txt = re.sub(r"#\w+", "", txt)    # strip hashtags
        txt = txt.encode("ascii", "ignore").decode()  # drop non-ascii (emojis)
        return txt

    cleaned = _prepare_readability_text(content)
    try:
        readability = flesch_reading_ease(cleaned)
    except Exception:
        readability = 0
    readability_ok = readability >= MIN_READING_SCORE

    passed = has_keyword and density_ok and readability_ok
    message = {
        "keywords_present": present_keywords,
        "density_kw": density_kw,
        "density": round(density, 4),
        "density_ok": density_ok,
        "flesch_score": round(readability, 2),
        "readability_ok": readability_ok,
    }
    return passed, str(message)

# Initialize LLM
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini", openai_api_key=api_key)