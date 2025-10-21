import os
import csv
import json
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv
from tqdm import tqdm
load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================
# CONFIGURATION
# ============================================

INPUT_FILE = "user_feedback.csv"
OUTPUT_DIR = "analysis_results"
BATCH_SIZE = 5  # Process N items at a time

# ============================================
# AI ANALYSIS FUNCTIONS
# ============================================

def categorize_feedback(feedback_text):
    """Categorize a single feedback item"""
    
    prompt = f"""Analyze this user feedback and return ONLY valid JSON with no other text:

Feedback: "{feedback_text}"

Return this exact structure:
{{
  "category": "Bug|Feature Request|Praise|Complaint|Question",
  "sentiment": "Positive|Neutral|Negative",
  "priority": "High|Medium|Low",
  "themes": ["theme1", "theme2"],
  "summary": "one sentence summary"
}}

JSON:"""
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        
        # Try to parse JSON
        data = json.loads(result)
        return data
        
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "category": "Unknown",
            "sentiment": "Neutral",
            "priority": "Medium",
            "themes": [],
            "summary": feedback_text[:100]
        }
    except Exception as e:
        print(f"  ⚠️  Error analyzing feedback: {e}")
        return None

def generate_summary(all_feedback):
    """Generate overall summary from all feedback"""
    
    # Prepare data for summary
    categories = {}
    sentiments = {}
    priorities = {}
    all_themes = []
    
    for item in all_feedback:
        if 'analysis' in item and item['analysis']:
            analysis = item['analysis']
            
            # Count categories
            cat = analysis.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            # Count sentiments
            sent = analysis.get('sentiment', 'Neutral')
            sentiments[sent] = sentiments.get(sent, 0) + 1
            
            # Count priorities
            pri = analysis.get('priority', 'Medium')
            priorities[pri] = priorities.get(pri, 0) + 1
            
            # Collect themes
            all_themes.extend(analysis.get('themes', []))
    
    # Count theme frequency
    theme_counts = {}
    for theme in all_themes:
        theme_counts[theme] = theme_counts.get(theme, 0) + 1
    
    # Sort themes by frequency
    top_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Create summary prompt
    summary_data = {
        "total_items": len(all_feedback),
        "categories": categories,
        "sentiments": sentiments,
        "priorities": priorities,
        "top_themes": top_themes
    }
    
    prompt = f"""Create an executive summary of this user feedback analysis:

Data:
{json.dumps(summary_data, indent=2)}

Create a summary with:
1. Overall Sentiment (1-2 sentences)
2. Top Issues (bullet points)
3. Top Requests (bullet points)
4. Recommended Actions (3-5 bullets)
5. Risk Areas (if any)

Keep it concise and actionable.

Summary:"""
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
        
    except Exception as e:
        print(f"⚠️  Error generating summary: {e}")
        return "Error generating summary"

# ============================================
# FILE OPERATIONS
# ============================================

def read_feedback_csv(filename):
    """Read feedback from CSV file"""
    feedback_items = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                feedback_items.append(row)
        
        print(f"✅ Loaded {len(feedback_items)} feedback items")
        return feedback_items
        
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return []
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return []

def save_results(feedback_items, summary, output_dir):
    """Save analysis results to files"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save detailed results as JSON
    json_file = f"{output_dir}/analysis_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(feedback_items, f, indent=2)
    
    print(f"✅ Saved detailed results: {json_file}")
    
    # Save detailed results as CSV
    csv_file = f"{output_dir}/analysis_{timestamp}.csv"
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['ID', 'User', 'Feedback', 'Date', 'Source', 
                      'Category', 'Sentiment', 'Priority', 'Themes', 'Summary']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in feedback_items:
            if 'analysis' in item and item['analysis']:
                analysis = item['analysis']
                writer.writerow({
                    'ID': item.get('ID', ''),
                    'User': item.get('User', ''),
                    'Feedback': item.get('Feedback', ''),
                    'Date': item.get('Date', ''),
                    'Source': item.get('Source', ''),
                    'Category': analysis.get('category', ''),
                    'Sentiment': analysis.get('sentiment', ''),
                    'Priority': analysis.get('priority', ''),
                    'Themes': ', '.join(analysis.get('themes', [])),
                    'Summary': analysis.get('summary', '')
                })
    
    print(f"✅ Saved CSV results: {csv_file}")
    
    # Save executive summary
    summary_file = f"{output_dir}/summary_{timestamp}.txt"
    with open(summary_file, 'w') as f:
        f.write("="*60 + "\n")
        f.write("USER FEEDBACK ANALYSIS - EXECUTIVE SUMMARY\n")
        f.write("="*60 + "\n\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Feedback Items: {len(feedback_items)}\n\n")
        f.write("="*60 + "\n\n")
        f.write(summary)
        f.write("\n\n" + "="*60 + "\n")
    
    print(f"✅ Saved summary: {summary_file}")
    
    return json_file, csv_file, summary_file

# ============================================
# MAIN ANALYZER
# ============================================

def analyze_feedback(input_file):
    """Main analysis function"""
    
    print("\n" + "="*60)
    print("🔍 FEEDBACK ANALYZER")
    print("="*60 + "\n")
    
    # Step 1: Load feedback
    print("Step 1: Loading feedback...")
    feedback_items = read_feedback_csv(input_file)
    
    if not feedback_items:
        print("❌ No feedback to analyze")
        return
    
    # Step 2: Analyze each item
    print(f"\nStep 2: Analyzing {len(feedback_items)} items...\n")
    for item in tqdm(feedback_items, desc="Analyzing feedback"):
        feedback_text = item.get('Feedback', '')
        analysis = categorize_feedback(feedback_text)
        item['analysis'] = analysis
 
    
    # Step 3: Generate summary
    print("\nStep 3: Generating executive summary...")
    summary = generate_summary(feedback_items)
    
    # Step 4: Save results
    print("\nStep 4: Saving results...")
    json_file, csv_file, summary_file = save_results(feedback_items, summary, OUTPUT_DIR)
    
    # Step 5: Display summary
    print("\n" + "="*60)
    print("EXECUTIVE SUMMARY")
    print("="*60 + "\n")
    print(summary)
    print("\n" + "="*60)
    
    print(f"\n✅ Analysis complete!")
    print(f"\nResults saved to:")
    print(f"  - {json_file}")
    print(f"  - {csv_file}")
    print(f"  - {summary_file}")
    
    return feedback_items, summary

# ============================================
# STATISTICS DISPLAY
# ============================================

def display_statistics(feedback_items):
    """Display quick statistics"""
    
    categories = {}
    sentiments = {}
    priorities = {}
    
    for item in feedback_items:
        if 'analysis' in item and item['analysis']:
            analysis = item['analysis']
            
            cat = analysis.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
            
            sent = analysis.get('sentiment', 'Neutral')
            sentiments[sent] = sentiments.get(sent, 0) + 1
            
            pri = analysis.get('priority', 'Medium')
            priorities[pri] = priorities.get(pri, 0) + 1
    
    print("\n" + "="*60)
    print("QUICK STATISTICS")
    print("="*60)
    
    print("\n📊 By Category:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")
    
    print("\n😊 By Sentiment:")
    for sent, count in sorted(sentiments.items(), key=lambda x: x[1], reverse=True):
        emoji = "😊" if sent == "Positive" else "😐" if sent == "Neutral" else "😞"
        print(f"  {emoji} {sent}: {count}")
    
    print("\n🎯 By Priority:")
    for pri, count in sorted(priorities.items(), key=lambda x: x[1], reverse=True):
        print(f"  {pri}: {count}")
    
    print("\n" + "="*60)

# ============================================
# RUN IT
# ============================================

if __name__ == "__main__":
    # Run the analysis
    feedback_items, summary = analyze_feedback(INPUT_FILE)
    
    # Show statistics
    if feedback_items:
        display_statistics(feedback_items)
    
    print("\n🎉 Done!\n")