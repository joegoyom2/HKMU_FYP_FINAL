import os

UPLOAD_FILE = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FILE, exist_ok=True)

VALID_COMPONENT_TYPES = {"class", "function", "module", "external_library"}

VALID_DEPENDENCY_TYPES = {"uses", "calls", "imports", "extends"}

PLANTUML_JAR_PATH = "C:\\PlantUML\\plantuml-1.2025.1.jar"