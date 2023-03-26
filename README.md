# Robotto
Using LLM to practice languages (listening/reading/speaking)

# Note
You're gonna need an OpenAI and Azure API keys to run this as is.
Over time I want to make a fully open source version of this, but right now it's just too slow unless you have a ton of GPUs (which is also expensive).

This relies on 3 things:
- Speech Recognition
  - We are already using Whisper, which is open-source, but usually slow if running locally.
  - For this reason we're using the paid API version of Whisper-large
  - Might be able to get away with using whisper.cpp but I have no idea if that is actually faster than having multiple GPU
- Large Language Model (LLM):
  - We're using the GPT-3.5-turbo API (ChatGPT)
  - Open-source alternatives could include something like Alpaca but I'm not sure how good alpaca is at languages besides English, and it also has the same speed problem mentioned
- Text to Speech (TTS):
  - This is the trickiest one. We're using Azure TTS for this.
  - Could use TortoiseTTS for open-source, but it is slow.
  - Coqui and other similar ones don't seem to have quality as high.
  - VITS based models seem to have better performance only for Japanese and Chinese, not English, but still run quite slow even on A100.
  - Could use other APIs (e.g., ElevenLabs) for better voices, but they're more expensive.

If you can think of a way of recreating this with fully open-source stuff that runs in a feasible speed let me know! 👀
