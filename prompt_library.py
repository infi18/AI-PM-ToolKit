import os
from anthropic import Anthropic
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================
# SYSTEM PROMPTS (Reusable contexts)
# ============================================

SYSTEM_PROMPTS = {
    "senior_pm": """You are a senior product manager with 10+ years experience in B2B SaaS. 
You're known for clear thinking, data-driven decisions, and balancing user needs with business goals.""",
    
    "technical_pm": """You are a technical product manager with engineering background. 
You understand system architecture, APIs, and can communicate with engineers effectively.""",
    
    "strategic_pm": """You are a strategic product leader focused on company vision and market positioning. 
You think long-term and connect product decisions to business outcomes.""",
    
    "user_advocate": """You are a product manager obsessed with user experience. 
You always consider user pain points and advocate for simplicity and usability."""
}

# ============================================
# PROMPT TEMPLATES (Fill-in-the-blank)
# ============================================

PROMPT_TEMPLATES = {
    
    # === DISCOVERY & RESEARCH ===
    
    "user_interview_analysis": """Analyze this user interview transcript and extract:

1. Key pain points (ranked by frequency/intensity)
2. Unmet needs
3. Feature requests mentioned
4. Surprising insights
5. Recommended next steps

Interview transcript:
{input}

Analysis:""",

    "competitive_analysis": """Analyze this competitor and create a structured comparison:

Competitor: {competitor_name}
Their features: {features}

Provide:
1. Their key strengths
2. Their weaknesses/gaps
3. What they're doing better than us
4. Opportunities for differentiation
5. Strategic recommendations

Analysis:""",

    "market_research_summary": """Summarize this market research into executive-friendly insights:

Research data:
{input}

Create:
1. Top 3 Market Trends
2. Customer Segment Analysis
3. Opportunities & Threats
4. Strategic Implications
5. Recommended Actions

Summary:""",

    # === PLANNING & PRIORITIZATION ===
    
    "feature_prioritization": """Evaluate this feature request using RICE framework:

Feature: {feature_description}
Context: {context}

Estimate:
- Reach (how many users affected per quarter): [estimate]
- Impact (how much it improves experience): [scale 0.25-3]
- Confidence (how sure are we): [percentage]
- Effort (person-months): [estimate]

Then calculate RICE score and give recommendation.

Return as JSON:
{
  "reach": number,
  "impact": number,
  "confidence": number,
  "effort": number,
  "rice_score": number,
  "recommendation": "Build Now/Next Quarter/Backlog/Reject",
  "reasoning": "string"
}""",

    "roadmap_generator": """Create a quarterly roadmap from these inputs:

Business Goals: {goals}
User Requests: {requests}
Technical Debt: {tech_debt}
Team Capacity: {capacity}

Generate a roadmap with:
- Q1 Focus (3-5 items)
- Q2 Focus (3-5 items)
- Rationale for prioritization
- Risk areas
- Success metrics

Roadmap:""",

    # === WRITING & DOCUMENTATION ===
    
    "prd_generator": """Create a comprehensive PRD from this information:

Feature Idea: {feature}
User Problem: {problem}
Business Context: {context}

Generate PRD with these sections:
1. Executive Summary
2. Problem Statement
3. Goals & Success Metrics
4. User Stories (3-5)
5. Functional Requirements
6. Non-Functional Requirements
7. Out of Scope
8. Open Questions

PRD:""",

    "user_story_writer": """Convert this feature into detailed user stories:

Feature: {feature}
Context: {context}

Create 3-5 user stories with:
- As a [user], I want to [action], so that [benefit]
- Acceptance criteria (3-5 per story)
- Estimated complexity (S/M/L)

User Stories:""",

    "release_notes_writer": """Write user-friendly release notes from these technical changes:

Technical Changes:
{changes}

Target Audience: {audience}

Create release notes that:
- Use friendly, non-technical language
- Focus on user benefits (not technical details)
- Are concise and scannable
- Include emojis where appropriate

Release Notes:""",

    # === STAKEHOLDER COMMUNICATION ===
    
    "executive_summary": """Convert this detailed update into an executive summary:

Details:
{input}

Create a 3-paragraph summary:
1. What we did (achievements)
2. What we learned (insights)
3. What's next (plan)

Keep it under 150 words. Focus on business impact.

Summary:""",

    "stakeholder_update_email": """Draft a stakeholder update email:

Project: {project_name}
Status: {status}
Key Updates: {updates}
Blockers: {blockers}

Create professional email that:
- Opens with clear status
- Highlights wins
- Addresses concerns
- States clear next steps
- Appropriate tone for {audience}

Email:""",

    # === DATA & ANALYSIS ===
    
    "ab_test_analyzer": """Analyze these A/B test results:

Test: {test_name}
Variant A: {variant_a_data}
Variant B: {variant_b_data}
Sample Size: {sample_size}
Duration: {duration}

Provide:
1. Statistical significance assessment
2. Winner declaration (if clear)
3. Surprising findings
4. Recommendations (ship/iterate/test longer)
5. Follow-up questions

Analysis:""",

    "metric_dashboard_review": """Review these product metrics and provide insights:

Metrics:
{metrics}

Time Period: {period}

Provide:
1. Overall health assessment
2. Concerning trends
3. Positive trends
4. Anomalies that need investigation
5. Recommended actions

Review:""",

    # === PROBLEM SOLVING ===
    
    "bug_triager": """Triage this bug report:

Bug: {bug_description}
User Impact: {impact}
Frequency: {frequency}

Provide:
- Severity (P0/P1/P2/P3)
- Recommended assignee (frontend/backend/design/etc)
- Estimated fix time
- Workaround (if any)
- Communication plan

Return as JSON:
{
  "severity": "string",
  "team": "string",
  "estimate": "string",
  "workaround": "string",
  "next_steps": ["array"]
}""",

    "technical_debt_assessor": """Assess this technical debt item:

Debt Item: {item}
Current Impact: {impact}
Proposed Solution: {solution}

Evaluate:
1. Risk if left unaddressed (scale 1-10)
2. Effort to fix (person-weeks)
3. Benefits of fixing
4. Recommended timeline (Now/Q1/Q2/Someday)
5. Mitigation strategies if deferred

Assessment:""",

    # === CUSTOMER FEEDBACK ===
    
    "feedback_synthesizer": """Synthesize these customer feedback items into themes:

Feedback (multiple items):
{feedback}

Identify:
1. Top 3 themes (with frequency)
2. Sentiment analysis
3. Feature requests extracted
4. Bug reports extracted
5. Recommended responses

Synthesis:""",

    "nps_analyzer": """Analyze these NPS survey responses:

NPS Score: {score}
Promoters said: {promoters}
Passives said: {passives}
Detractors said: {detractors}

Provide:
1. Key themes from each group
2. Main drivers of score
3. Quick wins to improve score
4. Long-term improvements needed
5. Response strategy for detractors

Analysis:""",

    # === IDEATION ===
    
    "feature_brainstorm": """Brainstorm feature ideas for this problem:

User Problem: {problem}
Constraints: {constraints}
Goals: {goals}

Generate 5 creative solutions:
- 2 obvious/safe ideas
- 2 innovative/risky ideas
- 1 wild/moonshot idea

For each: brief description + pros/cons

Ideas:""",

    "user_flow_designer": """Design a user flow for this feature:

Feature: {feature}
Entry Point: {entry}
Goal: {goal}

Create step-by-step flow with:
- Each screen/step
- User actions
- System responses
- Decision points
- Success/failure states
- Edge cases

User Flow:"""
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def call_claude(prompt, system_prompt=None, max_tokens=2000):
    """Call Claude API"""
    kwargs = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    if system_prompt:
        kwargs["system"] = system_prompt
    
    response = client.messages.create(**kwargs)
    return response.content[0].text

def use_prompt(template_name, inputs, system_prompt_name=None):
    """Use a prompt template with inputs"""
    
    if template_name not in PROMPT_TEMPLATES:
        return f"❌ Template '{template_name}' not found"
    
    # Fill in the template
    prompt = PROMPT_TEMPLATES[template_name].format(**inputs)
    
    # Get system prompt if specified
    system = SYSTEM_PROMPTS.get(system_prompt_name) if system_prompt_name else None
    
    # Call Claude
    result = call_claude(prompt, system)
    
    return result

def save_output(template_name, result):
    """Save prompt output to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("prompt_outputs", exist_ok=True)
    
    filename = f"prompt_outputs/{template_name}_{timestamp}.txt"
    
    with open(filename, "w") as f:
        f.write(f"Template: {template_name}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write("="*60 + "\n\n")
        f.write(result)
    
    return filename

# ============================================
# INTERACTIVE MODE
# ============================================

def interactive_mode():
    """Run prompts interactively"""
    print("\n" + "="*60)
    print("🚀 PM PROMPT LIBRARY - Interactive Mode")
    print("="*60)
    print("\nAvailable prompt templates:")
    
    for i, name in enumerate(PROMPT_TEMPLATES.keys(), 1):
        print(f"{i}. {name}")
    
    print("\nType 'quit' to exit\n")
    
    while True:
        choice = input("Enter template name (or number): ").strip()
        
        if choice.lower() == 'quit':
            break
        
        # Handle numeric choice
        if choice.isdigit():
            templates = list(PROMPT_TEMPLATES.keys())
            idx = int(choice) - 1
            if 0 <= idx < len(templates):
                choice = templates[idx]
            else:
                print("❌ Invalid number\n")
                continue
        
        if choice not in PROMPT_TEMPLATES:
            print(f"❌ Template '{choice}' not found\n")
            continue
        
        # Get required inputs
        template = PROMPT_TEMPLATES[choice]
        
        # Extract {variables} from template
        import re
        variables = re.findall(r'\{(\w+)\}', template)
        
        print(f"\n📝 Using template: {choice}")
        print(f"Required inputs: {', '.join(variables)}\n")
        
        inputs = {}
        for var in variables:
            value = input(f"{var}: ").strip()
            inputs[var] = value
        
        # Ask about system prompt
        print("\nUse a system prompt? (optional)")
        print("1. senior_pm")
        print("2. technical_pm")
        print("3. strategic_pm")
        print("4. user_advocate")
        print("5. None")
        
        sys_choice = input("\nChoice (1-5): ").strip()
        system_map = {
            "1": "senior_pm",
            "2": "technical_pm",
            "3": "strategic_pm",
            "4": "user_advocate",
            "5": None
        }
        system_name = system_map.get(sys_choice)
        
        # Run the prompt
        print("\n🤔 Thinking...\n")
        result = use_prompt(choice, inputs, system_name)
        
        print("="*60)
        print(result)
        print("="*60)
        
        # Save option
        save = input("\nSave this output? (y/n): ").strip().lower()
        if save == 'y':
            filename = save_output(choice, result)
            print(f"✅ Saved to: {filename}")
        
        print("\n")

# ============================================
# EXAMPLE USAGE
# ============================================

def run_examples():
    """Run example prompts"""
    print("\n🎯 RUNNING EXAMPLE PROMPTS\n")
    
    # Example 1: PRD Generation
    print("\n" + "="*60)
    print("EXAMPLE 1: Generate PRD")
    print("="*60)
    
    result1 = use_prompt(
        "prd_generator",
        {
            "feature": "Dark mode for mobile app",
            "problem": "Users complain about eye strain when using app at night",
            "context": "70% of our users use app in evening. Competitors have this feature."
        },
        system_prompt_name="senior_pm"
    )
    print(result1)
    
    input("\n[Press Enter for next example...]")
    
    # Example 2: Feature Prioritization
    print("\n" + "="*60)
    print("EXAMPLE 2: Feature Prioritization (RICE)")
    print("="*60)
    
    result2 = use_prompt(
        "feature_prioritization",
        {
            "feature_description": "Add export to Excel functionality",
            "context": "Enterprise users requesting this. We currently only support CSV export."
        },
        system_prompt_name="technical_pm"
    )
    print(result2)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "examples":
        run_examples()
    else:
        interactive_mode()