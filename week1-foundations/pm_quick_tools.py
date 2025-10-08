import os
from anthropic import Anthropic
from dotenv import load_dotenv
import datetime

# Load your API key
load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def call_claude(prompt, user_input):
    """Helper function to call Claude with a prompt"""
    full_prompt = prompt.format(input=user_input)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": full_prompt
        }]
    )
    
    return response.content[0].text

def save_result(tool_name, result):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/{tool_name}_{timestamp}.txt"
    
    # Create outputs folder if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    
    with open(filename, "w") as f:
        f.write(result)
    
    print(f"\n💾 Saved to: {filename}")

# Tool 1: Extract Action Items
def extract_action_items():
    print("\n📝 MEETING NOTES → ACTION ITEMS")
    print("=" * 50)
    print("Paste your meeting notes below (press Enter twice when done):\n")
    
    # Multi-line input
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    notes = "\n".join(lines)
    
    prompt = """Analyze these meeting notes and extract clear action items.

For each action item, specify:
- What needs to be done
- Who should do it (if mentioned)
- Any deadline (if mentioned)

Format as a bulleted list.

Meeting notes:
{input}

Action items:"""
    
    print("\n🤔 Analyzing...\n")
    result = call_claude(prompt, notes)
    print(result)
    print("\n" + "=" * 50 + "\n")
    save_result("action_items", result)

# Tool 2: Generate User Stories
def generate_user_stories():
    print("\n💡 FEATURE IDEA → USER STORIES")
    print("=" * 50)
    print("Describe your feature idea:\n")
    
    feature = input("> ")
    
    prompt = """Convert this feature idea into 3 user stories using the format:
"As a [user type], I want to [action], so that [benefit]."

Also add acceptance criteria for each story.

Feature idea: {input}

User stories:"""
    
    print("\n🤔 Generating...\n")
    result = call_claude(prompt, feature)
    print(result)
    print("\n" + "=" * 50 + "\n")
    save_result("user_stories", result)

# Tool 3: Stakeholder Updates
def convert_technical_documentation():
    print("\n📝 COnvert Technical Documentation into User-Friendly Content")
    print("=" * 50)
    print("Paste your technical documentation below (press Enter twice when done):\n")
    
    # Multi-line input
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    notes = "\n".join(lines)
    
    prompt = """Analyze these technical documentation and convert it into user-friendly content.

Technical documentation:
{input}

Action items:"""
    
    print("\n🤔 Analyzing...\n")
    result = call_claude(prompt, notes)
    print(result)
    print("\n" + "=" * 50 + "\n")
    save_result("technical_documentation", result)

# Tool 4: Assess Bug Severity
def assess_bug_severity():
    print("\n🐛 BUG REPORT → SEVERITY ASSESSMENT")
    print("=" * 50)
    print("Paste the bug report below (press Enter twice when done):\n")
    
    # Multi-line input
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    bug_report = "\n".join(lines)
    
    prompt = """Analyze this bug report and provide:

1. Severity Level (Critical/High/Medium/Low) with reasoning
2. Impact Assessment (who is affected, how many users)
3. Suggested Priority (P0/P1/P2/P3)
4. Recommended Next Steps

Bug report:
{input}

Assessment:"""
    
    print("\n🤔 Analyzing...\n")
    result = call_claude(prompt, bug_report)
    print(result)
    print("\n" + "=" * 50 + "\n")
    save_result("bug_severity", result)



# Main Menu
def main():
    print("\n" + "=" * 50)
    print("🚀 PM QUICK TOOLS - AI-Powered PM Assistant")
    print("=" * 50)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Extract action items from meeting notes")
        print("2. Generate user stories from feature idea")
        print("3. Convert technical documentation into user-friendly content")
        print("4. Assess bug severity")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            extract_action_items()
        elif choice == "2":
            generate_user_stories()
        elif choice == "3":
            convert_technical_documentation()
        elif choice == "4":
            assess_bug_severity()  
        elif choice == "5":
            print("\n👋 Thanks for using PM Quick Tools!\n")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()


