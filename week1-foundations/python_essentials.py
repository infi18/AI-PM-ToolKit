"""
Python Essentials for AI PMs
Learn just what you need to build AI tools
"""

# ============================================
# 1. WORKING WITH FILES
# ============================================

def lesson_1_file_basics():
    """Reading and writing files"""
    print("\n" + "="*60)
    print("LESSON 1: File Operations")
    print("="*60)
    
    # Writing to a file
    with open("test_output.txt", "w") as f:
        f.write("Hello from Python!\n")
        f.write("This is line 2\n")
    
    print("✅ Created test_output.txt")
    
    # Reading from a file
    with open("test_output.txt", "r") as f:
        content = f.read()
    
    print("\nFile contents:")
    print(content)
    
    # Reading line by line (better for large files)
    print("\nReading line by line:")
    with open("test_output.txt", "r") as f:
        for line in f:
            print(f"  - {line.strip()}")
    
    # Appending to a file
    with open("test_output.txt", "a") as f:
        f.write("This is line 3 (appended)\n")
    
    print("\n✅ Appended to file")


# ============================================
# 2. WORKING WITH CSV FILES
# ============================================

def lesson_2_csv_basics():
    """CSV files are everywhere in PM work"""
    import csv
    
    print("\n" + "="*60)
    print("LESSON 2: CSV Operations")
    print("="*60)
    
    # Create sample CSV
    data = [
        ["User ID", "Feedback", "Date"],
        ["001", "Love the new feature!", "2024-10-15"],
        ["002", "App crashes on login", "2024-10-16"],
        ["003", "Please add dark mode", "2024-10-17"]
    ]
    
    # Write CSV
    with open("sample_feedback.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    print("✅ Created sample_feedback.csv")
    
    # Read CSV (method 1: as list)
    with open("sample_feedback.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    print("\nCSV contents (as list):")
    for row in rows:
        print(f"  {row}")
    
    # Read CSV (method 2: as dictionary - BETTER!)
    with open("sample_feedback.csv", "r") as f:
        reader = csv.DictReader(f)
        print("\nCSV contents (as dictionary):")
        for row in reader:
            print(f"  User {row['User ID']}: {row['Feedback']}")


# ============================================
# 3. WORKING WITH JSON
# ============================================

def lesson_3_json_basics():
    """JSON is the format AI APIs use"""
    import json
    
    print("\n" + "="*60)
    print("LESSON 3: JSON Operations")
    print("="*60)
    
    # Python dictionary
    data = {
        "feature": "Dark Mode",
        "priority": "High",
        "effort": "Medium",
        "team": "Frontend",
        "tasks": ["Design mockups", "Implement toggle", "Test on devices"]
    }
    
    # Convert to JSON string
    json_string = json.dumps(data, indent=2)
    print("\nPython dict → JSON string:")
    print(json_string)
    
    # Save to file
    with open("feature_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print("\n✅ Saved to feature_data.json")
    
    # Read from file
    with open("feature_data.json", "r") as f:
        loaded_data = json.load(f)
    
    print("\nLoaded from JSON:")
    print(f"  Feature: {loaded_data['feature']}")
    print(f"  Priority: {loaded_data['priority']}")
    print(f"  Tasks: {', '.join(loaded_data['tasks'])}")
    
    # Parse JSON string (what you get from AI APIs)
    json_response = '{"status": "success", "count": 42}'
    parsed = json.loads(json_response)
    print(f"\nParsed JSON: {parsed['status']}, {parsed['count']} items")



# ============================================
# 4. ERROR HANDLING
# ============================================

def lesson_4_error_handling():
    """Things will go wrong - handle it gracefully"""
    import json
    
    print("\n" + "="*60)
    print("LESSON 4: Error Handling")
    print("="*60)
    
    # Example 1: File not found
    print("\n1. Handling missing files:")
    try:
        with open("nonexistent.txt", "r") as f:
            content = f.read()
    except FileNotFoundError:
        print("  ⚠️  File doesn't exist - creating it instead")
        with open("nonexistent.txt", "w") as f:
            f.write("Now it exists!")
    
    # Example 2: JSON parsing errors
    print("\n2. Handling bad JSON:")
    bad_json = '{"incomplete": '
    try:
        data = json.loads(bad_json)
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Invalid JSON: {e}")
        print("  Using default values instead")
        data = {"status": "error"}
    
    # Example 3: Multiple exceptions
    print("\n3. Handling multiple error types:")
    def divide_numbers(a, b):
        try:
            result = a / b
            return result
        except ZeroDivisionError:
            print("  ⚠️  Can't divide by zero!")
            return None
        except TypeError:
            print("  ⚠️  Need numbers, not text!")
            return None
        except Exception as e:
            print(f"  ⚠️  Unexpected error: {e}")
            return None
    
    print(f"  10 / 2 = {divide_numbers(10, 2)}")
    print(f"  10 / 0 = {divide_numbers(10, 0)}")
    print(f"  'text' / 2 = {divide_numbers('text', 2)}")

# ============================================
# 5. LISTS AND LOOPS
# ============================================

def lesson_5_lists_and_loops():
    """Processing multiple items efficiently"""
    print("\n" + "="*60)
    print("LESSON 5: Lists and Loops")
    print("="*60)
    
    feedback_items = [
        "Love the new UI!",
        "App crashes on startup",
        "Please add export feature",
        "Login is too slow"
    ]
    
    # Basic loop
    print("\n1. Basic loop:")
    for item in feedback_items:
        print(f"  - {item}")
    
    # Loop with index
    print("\n2. Loop with index:")
    for i, item in enumerate(feedback_items, 1):
        print(f"  {i}. {item}")
    
    # List comprehension (powerful!)
    print("\n3. List comprehension (filter + transform):")
    urgent = [item for item in feedback_items if "crash" in item.lower()]
    print(f"  Urgent items: {urgent}")
    
    # Transform all items
    print("\n4. Transform all items:")
    uppercase = [item.upper() for item in feedback_items]
    print(f"  Uppercase: {uppercase[0]}")
    
    # Filter and count
    print("\n5. Filtering and counting:")
    bug_count = len([item for item in feedback_items if "crash" in item.lower() or "slow" in item.lower()])
    print(f"  Bug reports: {bug_count}")

# ============================================
# 6. DICTIONARIES (KEY-VALUE PAIRS)
# ============================================

def lesson_6_dictionaries():
    """Dictionaries are perfect for structured data"""
    print("\n" + "="*60)
    print("LESSON 6: Dictionaries")
    print("="*60)
    
    # Creating a dictionary
    feature = {
        "name": "Dark Mode",
        "status": "In Progress",
        "team": "Frontend",
        "effort_days": 5,
        "priority": "High"
    }
    
    print("\n1. Accessing values:")
    print(f"  Feature: {feature['name']}")
    print(f"  Status: {feature['status']}")
    
    # Safe access (won't crash if key missing)
    print("\n2. Safe access with .get():")
    print(f"  Deadline: {feature.get('deadline', 'Not set')}")
    
    # Updating values
    print("\n3. Updating values:")
    feature["status"] = "Completed"
    feature["completed_date"] = "2024-10-20"
    print(f"  New status: {feature['status']}")
    
    # Iterating through dictionary
    print("\n4. Iterating through key-value pairs:")
    for key, value in feature.items():
        print(f"  {key}: {value}")
    
    # List of dictionaries (common pattern!)
    print("\n5. List of dictionaries:")
    features = [
        {"name": "Dark Mode", "priority": "High"},
        {"name": "Export", "priority": "Medium"},
        {"name": "Search", "priority": "High"}
    ]
    
    high_priority = [f for f in features if f["priority"] == "High"]
    print(f"  High priority features: {[f['name'] for f in high_priority]}")

# ============================================
# 7. STRING MANIPULATION
# ============================================

def lesson_7_strings():
    """Working with text (you'll do this A LOT)"""
    print("\n" + "="*60)
    print("LESSON 7: String Operations")
    print("="*60)
    
    feedback = "  The LOGIN feature is BROKEN!! Please fix ASAP.  "
    
    print("\n1. Cleaning strings:")
    print(f"  Original: '{feedback}'")
    print(f"  Stripped: '{feedback.strip()}'")
    print(f"  Lowercase: '{feedback.lower()}'")
    print(f"  Uppercase: '{feedback.upper()}'")
    
    print("\n2. Checking content:")
    print(f"  Contains 'login': {('login' in feedback.lower())}")
    print(f"  Starts with 'The': {feedback.strip().startswith('The')}")
    print(f"  Ends with '.': {feedback.strip().endswith('.')}")
    
    print("\n3. Replacing text:")
    cleaned = feedback.strip().replace("!!", "").lower()
    print(f"  Cleaned: '{cleaned}'")
    
    print("\n4. Splitting text:")
    words = feedback.split()
    print(f"  Words: {words}")
    print(f"  Word count: {len(words)}")
    
    print("\n5. Joining text:")
    tags = ["bug", "urgent", "login"]
    joined = ", ".join(tags)
    print(f"  Tags: {joined}")
    
    print("\n6. Formatting strings (f-strings):")
    user = "Alice"
    count = 5
    print(f"  {user} has {count} unread messages")
    print(f"  That's {count * 10}% of her inbox!")

# ============================================
# 8. WORKING WITH DATES
# ============================================

def lesson_8_dates():
    """Dates come up in PM work constantly"""
    from datetime import datetime, timedelta
    
    print("\n" + "="*60)
    print("LESSON 8: Working with Dates")
    print("="*60)
    
    # Current date/time
    now = datetime.now()
    print(f"\n1. Current datetime: {now}")
    print(f"   Formatted: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Date only: {now.strftime('%Y-%m-%d')}")
    
    # Parsing dates from strings
    print("\n2. Parsing dates:")
    date_string = "2024-10-20"
    parsed = datetime.strptime(date_string, "%Y-%m-%d")
    print(f"   Parsed: {parsed}")
    
    # Date arithmetic
    print("\n3. Date calculations:")
    tomorrow = now + timedelta(days=1)
    last_week = now - timedelta(days=7)
    print(f"   Tomorrow: {tomorrow.strftime('%Y-%m-%d')}")
    print(f"   Last week: {last_week.strftime('%Y-%m-%d')}")
    
    # Comparing dates
    sprint_end = datetime(2024, 10, 25)
    days_left = (sprint_end - now).days
    print(f"\n4. Days until sprint end: {days_left}")

# ============================================
# RUN ALL LESSONS
# ============================================

if __name__ == "__main__":
    print("\n🎓 PYTHON ESSENTIALS FOR AI PMs\n")
    
    lesson_1_file_basics()
    input("\n[Press Enter for next lesson...]")
    
    lesson_2_csv_basics()
    input("\n[Press Enter for next lesson...]")
    
    lesson_3_json_basics()
    input("\n[Press Enter for next lesson...]")
    
    lesson_4_error_handling()
    input("\n[Press Enter for next lesson...]")
    
    lesson_5_lists_and_loops()
    input("\n[Press Enter for next lesson...]")
    
    lesson_6_dictionaries()
    input("\n[Press Enter for next lesson...]")
    
    lesson_7_strings()
    input("\n[Press Enter for next lesson...]")
    
    lesson_8_dates()
    
    print("\n\n🎉 Python Essentials Complete!")
    print("You now know enough Python to build AI tools.\n")