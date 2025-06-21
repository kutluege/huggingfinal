# test_tools.py -----------------------------------------------------
# Simple test harness for verifying each smolagents tool works as expected
# Run this locally (e.g. python test_tools.py) after installing requirements.
# ------------------------------------------------------------------

import os
from tools import (
    python_exec_tool,
    ddg_search,
    google_search,
    visit_webpage,
    speech_to_text,
    youtube_transcript_tool,
    whisper_tool,
    file_tool,
    completion_tool,
    UserInputTool
)

# 1) Test PythonInterpreterTool
print("\n=== Testing PythonInterpreterTool ===")
try:
    out = python_exec_tool.forward("""
result = 2 + 2
print(result)
""")
    print("Output:", out)
except Exception as e:
    print("Error:", e)

# 2) Test DuckDuckGoSearchTool
print("\n=== Testing DuckDuckGoSearchTool ===")
try:
    out = ddg_search("What is the capital of Italy?")
    print("Output:", out)
except Exception as e:
    print("Error:", e)

# 3) Test GoogleSearchTool
print("\n=== Testing GoogleSearchTool ===")
try:
    out = google_search("Eiffel Tower height")
    print("Output:", out)
except Exception as e:
    print("Error:", e)

# 4) Test VisitWebpageTool
print("\n=== Testing VisitWebpageTool ===")
try:
    out = visit_webpage("https://example.com")
    print("Output snippet:", out[:200])
except Exception as e:
    print("Error:", e)

# 5) Test SpeechToTextTool (requires a short audio file)
print("\n=== Testing SpeechToTextTool ===")
audio_path = "sample_short.wav"
if os.path.exists(audio_path):
    try:
        out = speech_to_text(audio_path)
        print("Output:", out)
    except Exception as e:
        print("Error:", e)
else:
    print(f"Skip: no file {audio_path}")

# 6) Test YouTubeTranscriptTool
print("\n=== Testing YouTubeTranscriptTool ===")
try:
    out = youtube_transcript_tool.forward("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print("Output snippet:", out[:200])
except Exception as e:
    print("Error:", e)

# 7) Test WhisperTranscriptionTool (requires an audio file)
print("\n=== Testing WhisperTranscriptionTool ===")
audio_file = "sample_long.mp3"
if os.path.exists(audio_file):
    try:
        out = whisper_tool.forward(audio_file)
        print("Output:", out)
    except Exception as e:
        print("Error:", e)
else:
    print(f"Skip: no file {audio_file}")

# 8) Test FileTool
print("\n=== Testing FileTool ===")
# create quick CSV
csv_path = "test.csv"
with open(csv_path, "w") as f:
    f.write("col1,col2\n1,2\n3,4\n")
try:
    out = file_tool.forward(csv_path)
    print("Output CSV:", out)
except Exception as e:
    print("Error:", e)

# 9) Test CompletionTool
print("\n=== Testing CompletionTool ===")
try:
    prompt = "Answer with only the number: What is 10 * 15?"
    out = completion_tool.forward(prompt)
    print("Output:", out)
except Exception as e:
    print("Error:", e)

# 10) FinalAnswerTool + UserInputTool are used in Agent; manual tests only
print("\n=== Tests Completed ===")
