import anthropic
import json
from config import CLAUDE_API_KEY, MODEL

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def generate_test_cases(page_data):
    try:
        prompt = f"""
You are a Senior QA Engineer.

Analyze the following website structure and generate HIGH-QUALITY test cases.

Website Data:
Inputs: {page_data.get('inputs', [])}
Buttons: {page_data.get('buttons', [])}
Links: {page_data.get('links', [])}
APIs: {page_data.get('apis', [])}

Generate test cases in STRICT JSON format:

{{
  "feature": "Feature name",
  "test_cases": [
    {{
      "title": "",
      "type": "positive | negative | edge | security",
      "steps": [],
      "expected_result": "",
      "priority": "high | medium | low"
    }}
  ]
}}

Rules:
- Cover UI + API scenarios
- Include edge cases (empty input, max length, invalid format)
- Include security cases (SQL injection, XSS)
- Do NOT return anything outside JSON
"""

        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        raw_output = response.content[0].text

        # Strip markdown code fences if present
        cleaned = raw_output.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```", 2)[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.rsplit("```", 1)[0].strip()

        try:
            parsed = json.loads(cleaned)
            return parsed
        except Exception as parse_err:
            print("⚠️ JSON parsing failed:", parse_err)
            print("Raw output:", raw_output[:300])
            return None

    except Exception as e:
        print("Claude Error:", e)
        return None