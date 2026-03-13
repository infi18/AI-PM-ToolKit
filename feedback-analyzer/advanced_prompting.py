import os
from dotenv import load_dotenv
from anthropic import Anthropic
import json


load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def call_claude(prompt, system_prompt=None):
    """Helper to call Claude with optional system prompt"""
    messages = [{"role": "user", "content": prompt}]
    
    kwargs = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2000,
        "messages": messages
    }
    
    if system_prompt:
        kwargs["system"] = system_prompt
    
    response = client.messages.create(**kwargs)
    return response.content[0].text

# ============================================
# TECHNIQUE 1: Zero-Shot (What you did yesterday)
# ============================================

def technique_1_zero_shot():
    """Basic prompt - no examples"""
    print("\n" + "="*60)
    print("TECHNIQUE 1: ZERO-SHOT (Basic)")
    print("="*60)
    
    prompt = """Analyze this user feedback and identify the main pain point:

"The app keeps logging me out every 10 minutes. Super frustrating when I'm in the middle of something. Also the search is slow."

Main pain point:"""
    
    result = call_claude(prompt)
    print(result)

# ============================================
# TECHNIQUE 2: Few-Shot (Show examples)
# ============================================

def technique_2_few_shot():
    """Give examples of what you want"""
    print("\n" + "="*60)
    print("TECHNIQUE 2: FEW-SHOT (With Examples)")
    print("="*60)
    
    prompt = """Categorize user feedback into: Bug, Feature Request, or Complaint.

Examples:
Feedback: "The button doesn't work on mobile"
Category: Bug

Feedback: "Would love dark mode!"
Category: Feature Request

Feedback: "Support took 3 days to respond"
Category: Complaint

Now categorize this:
Feedback: "Can you add bulk export functionality?"
Category:"""
    
    result = call_claude(prompt)
    print(result)

# ============================================
# TECHNIQUE 3: Chain-of-Thought (Show reasoning)
# ============================================

def technique_3_chain_of_thought():
    """Ask Claude to show its reasoning"""
    print("\n" + "="*60)
    print("TECHNIQUE 3: CHAIN-OF-THOUGHT (Step-by-step reasoning)")
    print("="*60)
    
    prompt = """A feature request came in: "Add video upload to profiles"

Analyze this using these steps:
1. What problem does this solve for users?
2. What are the technical considerations?
3. What's the estimated complexity (Small/Medium/Large)?
4. What's your recommendation (Build Now/Later/Never)?

Think through each step:"""
    
    result = call_claude(prompt)
    print(result)

# ============================================
# TECHNIQUE 4: System Prompts (Role assignment)
# ============================================

def technique_4_system_prompts():
    """Use system prompts to set context/personality"""
    print("\n" + "="*60)
    print("TECHNIQUE 4: SYSTEM PROMPTS (Role & Personality)")
    print("="*60)
    
    system = """You are a senior product manager at a B2B SaaS company with 10 years of experience. 
You're known for data-driven decisions and clear communication. 
You always consider business impact, user needs, and technical feasibility."""
    
    prompt = """We have 100 hours of engineering time this sprint. Two requests:
A) Enterprise client wants SSO (they pay $50k/year)
B) 50 users want dark mode (free tier users)

What should we prioritize and why?"""
    
    result = call_claude(prompt, system_prompt=system)
    print(result)

# ============================================
# TECHNIQUE 5: Structured Output with XML/JSON
# ============================================

def technique_5_structured_output():
    """Get consistent, parseable output"""
    print("\n" + "="*60)
    print("TECHNIQUE 5: STRUCTURED OUTPUT (JSON)")
    print("="*60)
    
    prompt = """Analyze this feature request and return ONLY valid JSON with no other text:

Feature: "Users want to schedule posts in advance"

Return this exact structure:
{
  "feature_name": "string",
  "user_problem": "string",
  "estimated_effort": "Small/Medium/Large",
  "business_value": "Low/Medium/High",
  "technical_risk": "Low/Medium/High",
  "recommendation": "Build/Defer/Reject",
  "reasoning": "string"
}

JSON:"""
    
    result = call_claude(prompt)
    print(result)
    
    # Try to parse it
    try:
        data = json.loads(result)
        print("\n✅ Successfully parsed JSON!")
        print(f"Recommendation: {data['recommendation']}")
        print(f"Reasoning: {data['reasoning']}")
    except:
        print("\n❌ Failed to parse as JSON")

# ============================================
# TECHNIQUE 6: Multi-Turn Reasoning (Advanced)
# ============================================

def technique_6_self_critique():
    """Ask Claude to critique its own output"""
    print("\n" + "="*60)
    print("TECHNIQUE 6: SELF-CRITIQUE (Multi-step)")
    print("="*60)
    
    # First: Generate
    prompt1 = """Write 3 user stories for a "password reset" feature."""
    
    result1 = call_claude(prompt1)
    print("INITIAL OUTPUT:")
    print(result1)
    
    # Second: Critique
    prompt2 = f"""Review these user stories and identify any issues or missing elements:

{result1}

Critique:"""
    
    result2 = call_claude(prompt2)
    print("\n\nCRITIQUE:")
    print(result2)

# ============================================
# Run all examples
# ============================================

if __name__ == "__main__":
    print("\n🚀 ADVANCED PROMPTING TECHNIQUES DEMO\n")
    
    technique_1_zero_shot()
    input("\n[Press Enter to see next technique...]")
    
    technique_2_few_shot()
    input("\n[Press Enter to see next technique...]")
    
    technique_3_chain_of_thought()
    input("\n[Press Enter to see next technique...]")
    
    technique_4_system_prompts()
    input("\n[Press Enter to see next technique...]")
    
    technique_5_structured_output()
    input("\n[Press Enter to see next technique...]")
    
    technique_6_self_critique()
    
    print("\n\n🎉 You've now seen 6 advanced techniques!")
    print("Next: Build your prompt library with these patterns\n")