"""
feedback_analyzer.py
====================
Day 3 Project: Advanced Prompting Techniques for Product Managers

Demonstrates 6 core prompting patterns using real PM workflows:
  1. Zero-Shot       — direct questions, no examples
  2. Few-Shot        — guided output with examples
  3. Chain-of-Thought — step-by-step reasoning
  4. System Prompts  — role and persona assignment
  5. Structured Output — JSON extraction for downstream use
  6. Self-Critique   — multi-turn refinement loop

Use case: Analyzing user feedback and feature requests
Model: claude-sonnet-4-6
"""

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# ── Core helper ──────────────────────────────────────────────────

def call_claude(prompt: str, system_prompt: str = None, max_tokens: int = 2000) -> str:
    """
    Call Claude with an optional system prompt.
    Returns the text content of the first response block.
    """
    kwargs = {
        "model": "claude-sonnet-4-6",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt

    response = client.messages.create(**kwargs)
    return response.content[0].text


def section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ── Technique 1: Zero-Shot ───────────────────────────────────────

def technique_1_zero_shot():
    """
    Zero-Shot: Ask directly with no examples.
    Best for: Quick analysis, open-ended questions, first-pass triage.
    PM use case: Identify the primary pain point in raw user feedback.
    """
    section("TECHNIQUE 1: ZERO-SHOT")
    print("→ No examples given. Model uses general knowledge.")
    print("→ PM use case: Triage incoming user feedback\n")

    prompt = """Analyze this user feedback and identify the single most critical pain point.
Be concise — one sentence maximum.

Feedback:
"The app keeps logging me out every 10 minutes. Super frustrating when I'm in the
middle of something important. Also the search feels really slow."

Most critical pain point:"""

    result = call_claude(prompt)
    print(result)


# ── Technique 2: Few-Shot ────────────────────────────────────────

def technique_2_few_shot():
    """
    Few-Shot: Provide labeled examples before the target.
    Best for: Classification tasks, formatting consistency, pattern matching.
    PM use case: Categorize feedback before routing to the right team.
    """
    section("TECHNIQUE 2: FEW-SHOT (With Examples)")
    print("→ Examples teach the model the expected output format.")
    print("→ PM use case: Auto-categorize feedback for routing\n")

    prompt = """Categorize each piece of user feedback into exactly one of:
Bug | Feature Request | Complaint | Praise

Examples:
Feedback: "The login button doesn't respond on mobile Safari"
Category: Bug

Feedback: "Would love to see dark mode — my eyes hurt at night"
Category: Feature Request

Feedback: "Support took 4 days to respond to my ticket"
Category: Complaint

Feedback: "Onboarding was super smooth, best I've seen!"
Category: Praise

Now categorize this:
Feedback: "Can you add bulk CSV export for all my reports?"
Category:"""

    result = call_claude(prompt)
    print(result)


# ── Technique 3: Chain-of-Thought ───────────────────────────────

def technique_3_chain_of_thought():
    """
    Chain-of-Thought: Ask the model to reason step-by-step.
    Best for: Complex decisions, prioritization, trade-off analysis.
    PM use case: Feature feasibility scoring before backlog grooming.
    """
    section("TECHNIQUE 3: CHAIN-OF-THOUGHT (Step-by-Step Reasoning)")
    print("→ Breaking the problem into steps improves output quality.")
    print("→ PM use case: Feature feasibility scoring\n")

    prompt = """A feature request just came in: "Add video upload to user profiles"

Evaluate this request by working through each step:

Step 1 — User problem: What specific user need does this solve?
Step 2 — Technical considerations: What are the main engineering challenges?
Step 3 — Effort estimate: Small (1–2 sprints) / Medium (3–5) / Large (6+)?
Step 4 — Risk assessment: What could go wrong?
Step 5 — Recommendation: Build Now / Defer / Reject — and why?

Think through each step carefully:"""

    result = call_claude(prompt)
    print(result)


# ── Technique 4: System Prompts ─────────────────────────────────

def technique_4_system_prompts():
    """
    System Prompts: Set the model's role, persona, and constraints.
    Best for: Consistent voice, domain expertise, audience-specific output.
    PM use case: Sprint planning trade-off decisions.
    """
    section("TECHNIQUE 4: SYSTEM PROMPTS (Role Assignment)")
    print("→ System prompt sets context that persists across the conversation.")
    print("→ PM use case: Simulate a senior PM's prioritization instincts\n")

    system = """You are a senior product manager at a B2B SaaS company with 10 years of experience.
You make data-driven decisions and communicate with precision.
You always evaluate decisions across three dimensions: business impact, user need, and technical cost.
Your recommendations are direct — you don't hedge."""

    prompt = """We have 100 hours of engineering capacity this sprint. Two competing requests:

A) Enterprise client ($50k ARR) is threatening to churn if we don't add SSO by end of quarter
B) 50 free-tier users are asking for dark mode in our Canny board

What do we build, and how do we frame the trade-off to leadership?"""

    result = call_claude(prompt, system_prompt=system)
    print(result)


# ── Technique 5: Structured Output ──────────────────────────────

def technique_5_structured_output():
    """
    Structured Output: Extract data as JSON for programmatic use.
    Best for: Integration with other tools, consistent schema, data pipelines.
    PM use case: Auto-populate JIRA fields from feature requests.
    """
    section("TECHNIQUE 5: STRUCTURED OUTPUT (JSON Extraction)")
    print("→ Structured output enables downstream automation.")
    print("→ PM use case: Auto-populate JIRA tickets from Slack feedback\n")

    prompt = """Analyze this feature request and return ONLY valid JSON — no explanation, no markdown, no commentary.

Feature request: "Users want to schedule posts in advance for specific dates and times"

Return this exact structure:
{
  "feature_name": "string",
  "user_problem": "string",
  "estimated_effort": "Small | Medium | Large",
  "business_value": "Low | Medium | High",
  "technical_risk": "Low | Medium | High",
  "recommendation": "Build | Defer | Reject",
  "reasoning": "string (2 sentences max)"
}

JSON:"""

    result = call_claude(prompt)
    print(result)

    # Attempt to parse and use the structured data
    try:
        data = json.loads(result)
        print("\n✅ JSON parsed successfully")
        print(f"\n  Feature     : {data['feature_name']}")
        print(f"  Effort      : {data['estimated_effort']}")
        print(f"  Value       : {data['business_value']}")
        print(f"  Recommend   : {data['recommendation']}")
        print(f"  Reasoning   : {data['reasoning']}")
    except json.JSONDecodeError:
        print("\n⚠️  JSON parse failed — model added extra text")
        print("    Fix: Add 'Return ONLY the JSON object, nothing else' to prompt")


# ── Technique 6: Self-Critique Loop ─────────────────────────────

def technique_6_self_critique():
    """
    Self-Critique: Multi-turn loop where the model reviews its own output.
    Best for: High-stakes writing, user stories, PRDs, error checking.
    PM use case: Iterative user story refinement before sprint planning.
    """
    section("TECHNIQUE 6: SELF-CRITIQUE (Multi-Turn Refinement)")
    print("→ Two-pass approach: generate then critique.")
    print("→ PM use case: Refine user stories before handing to engineering\n")

    # Pass 1: Generate
    prompt_generate = """Write 3 user stories for a 'password reset' feature.
Use standard format: As a [user], I want [action], so that [benefit]."""

    print("── PASS 1: Initial generation ──")
    draft = call_claude(prompt_generate)
    print(draft)

    # Pass 2: Critique
    prompt_critique = f"""Review these user stories and identify:
1. Missing acceptance criteria
2. Vague or unmeasurable language
3. Any user types or edge cases not covered
4. One specific rewrite recommendation

User stories to review:
{draft}

Your critique:"""

    print("\n── PASS 2: Self-critique ──")
    critique = call_claude(prompt_critique)
    print(critique)


# ── Main ─────────────────────────────────────────────────────────

def main():
    print("\n" + "="*60)
    print("  AI-PM MASTERY — DAY 3")
    print("  Advanced Prompting Techniques for Product Managers")
    print("  6 patterns, real PM workflows, Claude API")
    print("="*60)

    techniques = [
        ("1. Zero-Shot",          technique_1_zero_shot),
        ("2. Few-Shot",           technique_2_few_shot),
        ("3. Chain-of-Thought",   technique_3_chain_of_thought),
        ("4. System Prompts",     technique_4_system_prompts),
        ("5. Structured Output",  technique_5_structured_output),
        ("6. Self-Critique",      technique_6_self_critique),
    ]

    for label, fn in techniques:
        fn()
        try:
            input(f"\n  [Enter] → next technique...")
        except (EOFError, KeyboardInterrupt):
            # Allows running non-interactively (e.g. CI, piped output)
            pass

    print("\n" + "="*60)
    print("  ✅ All 6 techniques complete")
    print()
    print("  Key takeaways:")
    print("  • Zero-shot: fast triage and open questions")
    print("  • Few-shot: classification and formatting")
    print("  • Chain-of-thought: complex decisions")
    print("  • System prompts: consistent persona and domain expertise")
    print("  • Structured output: automation and tool integration")
    print("  • Self-critique: higher quality on high-stakes deliverables")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()