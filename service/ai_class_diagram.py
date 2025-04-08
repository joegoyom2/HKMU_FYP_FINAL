import json
from config.ai_config import get_openai

def class_diagram_from_code(code: str) -> dict:
    prompt = f"""
    Analyze the following Python code and extract all class definitions, including:

    - Class name
    - Attributes (e.g., self.attr and commonly used variables in methods)
    - Methods (with visibility and return type)

    Return ONLY valid JSON in this format, with NO explanation or extra text:

    ```json
    {{
        "classes": [
            {{
                "class_name": "ClassName",
                "attributes": [
                    {{"name": "attr1", "type": "str"}},
                    {{"name": "attr2", "type": "int"}}
                ],
                "methods": [
                    {{"name": "method1", "visibility": "public", "return_type": "void"}},
                    {{"name": "method2", "visibility": "private", "return_type": "str"}}
                ]
            }}
        ]
    }}
    ```

    Python Code:
    ```python
    {code}
    ```
    """

    try:
        client = get_openai()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a code analysis assistant. Always return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=4096
        )

        raw_output = response.choices[0].message.content.strip()
        cleaned_output = raw_output.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_output)

    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error:", e)
        print("⚠️ AI Output:", raw_output)
        return {"error": f"Invalid JSON format: {str(e)}"}

    except Exception as e:
        return {"error": str(e)}