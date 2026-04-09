AI-PM-ToolKit
A collection of AI-powered tools and experiments built by a Product Manager learning to build with AI — not just use it.

Python Claude API License

Why This Exists
Most PM resources teach you about AI. This repo is about learning to build with it.

Every project here came from a real problem I ran into as a PM — feedback overload, slow triage, repetitive user story writing, prioritization debates that should take minutes but take hours. Each one is an attempt to solve that problem with code.

I'm not a full-time engineer. I'm a PM with a dev background who believes the next generation of great product managers will understand AI deeply enough to prototype their own solutions — not just spec them out for someone else to build.

Projects
🧠 foundations/
Advanced Prompting Techniques for Product Managers

6 production-ready prompting patterns applied to real PM workflows:

Zero-shot feedback triage
Few-shot categorization for routing
Chain-of-thought feature scoring
System prompts for consistent PM persona
Structured JSON output for JIRA integration
Self-critique loop for user story refinement
cd foundations
pip install -r requirements.txt
python feedback_analyzer.py
🌱 ai-pm-sidekick/ (coming soon)
AI-Powered Behavioral PM Assitant Tool

A full product built from scratch — market research, personas, behavioral journey map, wireframes, and a React + Claude API frontend.

Designed for the 68M Americans with subprime credit who aren't stuck because they lack information — they're stuck because of shame, overwhelm, and present bias. This tool addresses the behavior change problem that every existing credit product ignores.

Full PM artifact set in /docs — personas, competitive analysis, behavioral map

Tech Stack
Tool	Used For
Python 3.9+	Backend scripts and API integration
Claude API (claude-sonnet-4-6)	AI reasoning, coaching, structured output
React + Builder.io	Frontend (Credit Health Coach)
python-dotenv	API key management
Setup
# Clone
git clone https://github.com/infi18/AI-PM-ToolKit.git
cd AI-PM-ToolKit

# Install root dependencies
pip install -r requirements.txt

# Each project has its own requirements.txt — see individual folders
About Me
Senior PM with a software development background and 5+ years in consumer credit products. Currently completing a Behavioral Design for Finance certification (Irrational Labs).

This repo is where I build things I wish existed — at the intersection of product thinking, behavioral science, and AI-native development.

Currently building: Credit Health Coach

📎 LinkedIn · 📧 siddhi.naik18@gmail.com

If you're a PM curious about building with AI — feel free to fork, copy, or reach out.
