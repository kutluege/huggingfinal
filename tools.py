import os
import re
import json
import random
from pathlib import Path

import pandas as pd
import openai
from youtube_transcript_api import YouTubeTranscriptApi

from smolagents import (
    Tool,
    PythonInterpreterTool,   # executes Python code in sandbox
    DuckDuckGoSearchTool,     # Web search
    GoogleSearchTool,         # alternative web search
    VisitWebpageTool,         # fetch page text / HTML
    SpeechToTextTool,         # transcribe short audio snippets
    FinalAnswerTool,          # wrap final-answer outputs
    UserInputTool             # prompt user for missing inputs
)

# -----------------------------------------------------------------------
# 1) Python Interpreter — for numeric & data calculations
# -----------------------------------------------------------------------
python_exec_tool = PythonInterpreterTool()
python_exec_tool.description = (
    "Executes Python code for calculations, data parsing, and processing. "
    "Useful for math, table operations, and any small script execution."
)

# -----------------------------------------------------------------------
# 2) DuckDuckGo Search — comprehensive factual search
# -----------------------------------------------------------------------
ddg_search = DuckDuckGoSearchTool()
ddg_search.description = (
    "Useful for factual questions about general knowledge, history, "
    "geography, pop culture, and other encyclopedic information."
)

# -----------------------------------------------------------------------
# 3) Google Search — alternative search engine fallback
# -----------------------------------------------------------------------
google_search = GoogleSearchTool()
google_search.description = (
    "Useful as a secondary search source for up-to-date factual queries."
)

# -----------------------------------------------------------------------
# 4) Visit Webpage — scrape page text or HTML sections
# -----------------------------------------------------------------------
visit_webpage = VisitWebpageTool()
visit_webpage.description = (
    "Fetches the text or HTML content of a given URL. "
    "Useful for reading context from news articles or documentation pages."
)

# -----------------------------------------------------------------------
# 5) SpeechToText — short audio transcription
# -----------------------------------------------------------------------
speech_to_text = SpeechToTextTool()
speech_to_text.description = (
    "Converts a short audio snippet (MP3/WAV) to text. "
    "Useful for very brief voice notes or clips."
)

# -----------------------------------------------------------------------
# 6) YouTube Transcript — custom tool for full video captions
# -----------------------------------------------------------------------
class YouTubeTranscriptTool(Tool):
    name = "youtube_transcript"
    description = "Fetches the full transcript of a YouTube video from its URL."
    inputs = {
        "video_url": {
            "type": "string",
            "description": "Full YouTube watch URL (e.g. https://www.youtube.com/watch?v=...)."
        }
    }
    output_type = "string"

    def forward(self, video_url: str) -> str:
        match = re.search(r"v=([A-Za-z0-9_-]+)", video_url)
        if not match:
            return "Invalid YouTube URL."
        vid = match.group(1)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid)
            return " ".join(seg["text"] for seg in transcript)
        except Exception as e:
            return f"Error fetching transcript: {e}"

youtube_transcript_tool = YouTubeTranscriptTool()

# -----------------------------------------------------------------------
# 7) Whisper Transcription — custom wrapper around OpenAI Whisper
# -----------------------------------------------------------------------
class WhisperTranscriptionTool(Tool):
    name = "whisper_transcription"
    description = "Transcribes an audio file using OpenAI's Whisper API."
    inputs = {
        "audio_file": {
            "type": "string",
            "description": "Path to a local audio file (mp3 or wav)."
        }
    }
    output_type = "string"

    def forward(self, audio_file: str) -> str:
        if not os.path.isfile(audio_file):
            return f"File not found: {audio_file}"
        try:
            with open(audio_file, "rb") as f:
                resp = openai.Audio.transcribe("whisper-1", f)
            return resp.get("text", "")
        except Exception as e:
            return f"Whisper error: {e}"

whisper_tool = WhisperTranscriptionTool()

# -----------------------------------------------------------------------
# 8) File Reader — read CSV / Excel / JSON attachments
# -----------------------------------------------------------------------
class FileTool(Tool):
    name = "file_reader"
    description = (
        "Reads a local CSV, Excel (.xlsx/.xls), or JSON file and returns "
        "its contents as a UTF-8 string."
    )
    inputs = {
        "file_path": {
            "type": "string",
            "description": "Absolute or relative path to the input file."
        }
    }
    output_type = "string"

    def forward(self, file_path: str) -> str:
        path = Path(file_path)
        if not path.exists():
            return f"File not found: {file_path}"
        ext = path.suffix.lower()
        try:
            if ext == ".csv":
                df = pd.read_csv(path)
                return df.to_csv(index=False)
            elif ext in (".xls", ".xlsx"):
                df = pd.read_excel(path)
                return df.to_csv(index=False)
            elif ext == ".json":
                data = json.loads(path.read_text(encoding="utf-8"))
                return json.dumps(data, indent=2)
            else:
                return f"Unsupported file type: {ext}"
        except Exception as e:
            return f"Error reading {file_path}: {e}"

file_tool = FileTool()

# -----------------------------------------------------------------------
# 9) CompletionTool — wrap up final answers if needed
# -----------------------------------------------------------------------
completion_tool = FinalAnswerTool()
completion_tool.description = (
    "Wraps the final answer string for submission without extra explanation."
)

# -----------------------------------------------------------------------
# Public list of all tools for app.py
# -----------------------------------------------------------------------
TOOLS = [
    python_exec_tool,
    ddg_search,
    google_search,
    visit_webpage,
    speech_to_text,
    youtube_transcript_tool,
    whisper_tool,
    file_tool,
    completion_tool,
    UserInputTool()  # prompt user if needed
]