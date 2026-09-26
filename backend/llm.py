import os
import litellm
from crewai import LLM

''' Patch litellm.completion to remove CrewAI's 
Anthropic cache_breakpoint field before sending requests to Gemini. '''

_original_completion = litellm.completion

def _patched_completion(*args, **kwargs):
    if "messages" in kwargs:
        for msg in kwargs["messages"]:
            if isinstance(msg, dict):
                msg.pop("cache_breakpoint", None)
    return _original_completion(*args, **kwargs)

litellm.completion = _patched_completion
# -------------------------------------------

def get_gemini_llm():
    return LLM(
        model="gemini/gemini-3.1-flash-lite",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.1
    )