import os
import pandas as pd

def export_to_excel(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        rows = []

        for tc in data.get("test_cases", []):
            rows.append({
                "Title": tc.get("title"),
                "Type": tc.get("type"),
                "Steps": " | ".join(tc.get("steps", [])),
                "Expected": tc.get("expected_result"),
                "Priority": tc.get("priority")
            })

        df = pd.DataFrame(rows)
        df.to_excel(file_path, index=False)

        print(f"✅ Saved structured test cases to {file_path}")

    except Exception as e:
        print("Export Error:", e)