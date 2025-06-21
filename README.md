---
title: Template Final Assignment
emoji: 🕵🏻‍♂️
colorFrom: indigo
colorTo: indigo
sdk: gradio
sdk_version: 5.25.2
app_file: app.py
pinned: false
hf_oauth: true
# optional, default duration is 8 hours/480 minutes. Max duration is 30 days/43200 minutes.
hf_oauth_expiration_minutes: 480
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

## GAIA Evaluation Instructions

This template provides a minimal agent setup for the GAIA benchmark. To submit
your answers to the evaluation server:

1. Duplicate this Space to your account and modify `BasicAgent` in `app.py` with
   your own logic and tools.
2. Ensure the Space is **public** so the scoring server can verify your code.
3. Run the Space and click **Run Evaluation & Submit All Answers** after logging
   in with your Hugging Face account. The app will fetch the question list from
   the scoring API and submit the agent's responses.

The submission payload includes your username, the link to your Space's code
(`agent_code`), and the list of answers. The scoring API expects an exact match
with the ground truth answers, so make sure your agent responds with only the
final answer text.
