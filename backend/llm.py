import os
import litellm
from crewai import LLM

# --- FIX for CrewAI + Groq compatibility ---
# CrewAI injects 'cache_breakpoint' into system messages for Anthropic prompt caching.
# It does this for ALL providers, but Groq rejects it with a 400 Bad Request.
# We intercept litellm.completion and strip that field before the request reaches Groq.
_original_completion = litellm.completion

def _patched_completion(*args, **kwargs):
    if "messages" in kwargs:
        for msg in kwargs["messages"]:
            if isinstance(msg, dict):
                msg.pop("cache_breakpoint", None)
    return _original_completion(*args, **kwargs)

litellm.completion = _patched_completion
# -------------------------------------------

def get_groq_llm():
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1
    )