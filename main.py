import sys
import os

# 👇 ADD THIS AT THE VERY TOP
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crawler.scraper import scrape_website
from ai.claude_generator import generate_test_cases
from utils.exporter import export_to_excel
from config import TARGET_URL, OUTPUT_FILE

def run_agent():
    try:
        print("🔍 Scraping website...")
        data = scrape_website(TARGET_URL)

        if not data:
            print("❌ Scraping failed")
            return

        print("🧠 Generating test cases via Claude...")
        test_data = generate_test_cases(data)

        if not test_data:
            print("❌ Test generation failed")
            return

        print("📊 Exporting...")
        export_to_excel(test_data, OUTPUT_FILE)

        print("🚀 QA Agent completed successfully!")

    except Exception as e:
        print("Agent Error:", e)

if __name__ == "__main__":
    run_agent()