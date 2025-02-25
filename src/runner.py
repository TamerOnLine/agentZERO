import os

# Dictionary of available scripts
SCRIPTS = {
    "1": r"src\Selenium.py",
    "2": r"src\Session.py",
    "3": r"src\User-Agent.py"
}

# Display available script options
print("Select the script you want to run:\n")
for key, script in SCRIPTS.items():
    print(f"{key}. {script}")

# Get user input
choice = input("\nEnter the number of the script to execute: ").strip()

# Execute the selected script
if choice in SCRIPTS:
    script_to_run = SCRIPTS[choice]
    print(f"\n🔹 Running {script_to_run}...\n")
    os.system(f"python {script_to_run}")
else:
    print("\n Invalid choice. Please select a valid number.")
