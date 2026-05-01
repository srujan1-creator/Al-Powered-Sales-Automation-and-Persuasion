import os
from google import genai
from google.genai import types
from config import settings
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
import re

logger = logging.getLogger("aura-ai.engine")

# Configure the Gemini API
client = None
if settings.gemini_api_key:
    client = genai.Client(api_key=settings.gemini_api_key)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _call_gemini(prompt: str, use_search: bool = False, system_instruction: str = None) -> str:
    if not client:
        raise ValueError("Gemini API key not configured")
        
    config_kwargs = {}
    if use_search:
        config_kwargs["tools"] = [{"google_search": {}}]
    if system_instruction:
        config_kwargs["system_instruction"] = system_instruction
        
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs)
    )
    return response.text.strip()

def generate_intro_pitch(company_size: str, industry: str, pain_points: str) -> str:
    if not client:
        return "Hello! I'm Aura. I see you're looking for solutions to your current challenges. How can our Enterprise AI Suite help you today?"
        
    system_instruction = "You are 'Aura', a top-tier B2B AI Sales Representative for an Enterprise AI Productivity Suite. Keep responses concise (max 3 sentences)."
    prompt = f"""
    You are talking to a lead with the following context:
    - Company Size: {company_size}
    - Industry: {industry}
    - Current Pain Points: {pain_points}
    
    Use your Google Search grounding capability to briefly lookup a recent trend or challenge in the {industry} industry. 
    Craft a personalized, engaging, and persuasive introductory pitch that references this real-world trend. 
    Be conversational and end with a question to engage them.
    """
    try:
        return _call_gemini(prompt, use_search=True, system_instruction=system_instruction)
    except Exception as e:
        logger.error(f"Generation Error in intro pitch: {e}")
        return "Hello! I'm Aura. I see you're looking for solutions to your current challenges. How can our Enterprise AI Suite help you today?"

def generate_sales_response(chat_history: list, new_message: str) -> str:
    if not client:
        return "I completely understand. Tell me more about what you're looking for."
        
    system_instruction = "You are 'Aura', a highly persuasive B2B AI Sales Representative. Use the SPIN selling framework subtly. Handle objections logically and professionally. Keep responses concise and conversational (max 3 sentences)."
    history_text = "\n".join([f"{msg['sender'].capitalize()}: {msg['content']}" for msg in chat_history])
    
    prompt = f"""
    If the user mentions a specific company, competitor, or technology, use your Google Search grounding to bring up real-world, up-to-date facts to strengthen your pitch.
    
    Conversation History:
    {history_text}
    
    User's latest message: "{new_message}"
    
    Aura's response:
    """
    try:
        return _call_gemini(prompt, use_search=True, system_instruction=system_instruction)
    except Exception as e:
        logger.error(f"Generation Error in sales response: {e}")
        return "I completely understand. Tell me more about what you're looking for."

def analyze_lead_score(chat_history: list) -> float:
    if not client:
        return 50.0
        
    system_instruction = "You are an analytical AI. Analyze the conversation and determine the lead's level of interest on a scale of 0 to 100. Respond ONLY with a number."
    history_text = "\n".join([f"{msg['sender'].capitalize()}: {msg['content']}" for msg in chat_history[-5:]]) # Last 5 messages
    prompt = f"""
    Conversation:
    {history_text}
    """
    try:
        score_str = _call_gemini(prompt, use_search=False, system_instruction=system_instruction)
        # Use regex to find the first number in the response
        match = re.search(r"(\d+(\.\d+)?)", score_str)
        if match:
            score = float(match.group(1))
            return min(max(score, 0.0), 100.0)
        return 50.0
    except Exception as e:
        logger.error(f"Scoring Error: {e}")
        return 50.0
