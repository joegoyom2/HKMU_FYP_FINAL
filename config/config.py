import os

# 上傳資料夾位置
UPLOAD_FILE = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FILE, exist_ok=True)

# 允許的元件類型
VALID_COMPONENT_TYPES = {"class", "function", "module", "external_library"}

# 允許的相依關係類型
VALID_DEPENDENCY_TYPES = {"uses", "calls", "imports", "extends"}

# PlantUML JAR 路徑（你需要根據你實際位置修改）
PLANTUML_JAR_PATH = "C:\\PlantUML\\plantuml-1.2025.1.jar"