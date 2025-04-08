import json
from config.ai_config import get_openai

# 分析程式碼並取得元件與相依關係
def ai_code_analysis(code: str) -> dict:
    prompt = f"""
    Analyze the following code and output ONLY valid JSON with:
    {{
        "components": [
            {{
                "component_name": "ClassName or ComponentName",
                "component_type": "class/component/function/module",
                "description": "Brief description",
                "attributes": ["attribute1", "attribute2"],
                "methods": ["method1", "method2"]
            }}
        ],
        "dependencies": [
            {{
                "source_component": "ComponentA",
                "target_component": "ComponentB",
                "dependency_type": "calls/imports/extends/uses"
            }}
        ]
    }}
    Code:
    {code}
    """

    try:
        client = get_openai()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a code analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=4096
        )

        ai_output = response.choices[0].message.content.strip()
        cleaned_output = ai_output.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_output)

    except Exception as e:
        return {"error": str(e)}


# 根據 prompt 回傳 PlantUML 程式碼（sequence diagram 用）
def call_plantuml_ai(prompt: str) -> str:
    try:
        client = get_openai()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert in PlantUML diagram generation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=4096
        )

        raw_output = response.choices[0].message.content.strip()
        start = raw_output.find("@startuml")
        end = raw_output.rfind("@enduml") + len("@enduml")
        return raw_output[start:end] if start != -1 and end != -1 else raw_output

    except Exception as e:
        return f"@startuml\n' Error: {str(e)}\n@enduml"