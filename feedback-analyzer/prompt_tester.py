import os
from anthropic import Anthropic
from dotenv import load_dotenv
from prompt_library import PROMPT_TEMPLATES, use_prompt
import time

load_dotenv()

def test_prompt_consistency(template_name, inputs, runs=3):
    """Test if a prompt gives consistent results"""
    print(f"\n🧪 Testing: {template_name}")
    print(f"Running {runs} times to check consistency...\n")
    
    results = []
    
    for i in range(runs):
        print(f"Run {i+1}/{runs}...")
        result = use_prompt(template_name, inputs)
        results.append(result)
        time.sleep(1)  # Rate limiting
    
    print("\n" + "="*60)
    print("RESULTS COMPARISON:")
    print("="*60)
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Run {i} ---")
        print(result[:200] + "..." if len(result) > 200 else result)
    
    # Simple consistency check
    print("\n" + "="*60)
    if len(set(results)) == 1:
        print("✅ PERFECTLY CONSISTENT (all runs identical)")
    elif len(set(results)) == runs:
        print("⚠️  HIGH VARIATION (all runs different)")
    else:
        print("📊 MODERATE VARIATION (some similarity)")
    print("="*60)

def test_prompt_length(template_name, inputs):
    """Test how prompt length affects output"""
    print(f"\n📏 Testing prompt length impact: {template_name}\n")
    
    result = use_prompt(template_name, inputs)
    
    print(f"Input tokens (approx): {len(str(inputs)) // 4}")
    print(f"Output tokens (approx): {len(result) // 4}")
    print(f"Output length: {len(result)} characters")
    print(f"Output word count: {len(result.split())}")

if __name__ == "__main__":
    # Test consistency
    test_prompt_consistency(
        "user_story_writer",
        {
            "feature": "Password reset via email",
            "context": "Users currently can't reset passwords themselves"
        },
        runs=3
    )
    
    # Test another
    input("\n[Press Enter to test another...]")
    
    test_prompt_length(
        "prd_generator",
        {
            "feature": "Two-factor authentication",
            "problem": "Account security concerns from enterprise clients",
            "context": "Required for SOC 2 compliance"
        }
    )