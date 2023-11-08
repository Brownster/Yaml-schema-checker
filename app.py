import os
from ruamel.yaml import YAML
from pykwalify.core import Core

# Replace with the actual path to your schema files
schema_directory = "/path/to/your/schemas"

# Replace with the actual path to the YAML file you want to validate
yaml_file_path = '/path/to/your/yaml/file.yaml'

# Mapping of exporter types to their respective schema files
schema_mapping = {
    "linux_exporter": "linux_exporter_schema.yaml",
    "exporter_blackbox": "exporter_blackbox_schema.yaml",
    # Add more mappings as needed
}

def validate_yaml(yaml_content, schema_file):
    with open(schema_file, 'r') as file:
        schema = file.read()
    c = Core(source_data=yaml_content, schema_data=schema)
    c.validate(raise_exception=True)

def determine_schema(yaml_section_name):
    # Simple mapping lookup by section name to determine the schema file
    return schema_mapping.get(yaml_section_name)

def load_yaml_file(yaml_file_path):
    yaml = YAML(typ='safe')
    with open(yaml_file_path, 'r') as file:
        return yaml.load(file)

# Load and validate the YAML file
yaml_content = load_yaml_file(yaml_file_path)

if yaml_content:  # Check if YAML content is successfully loaded
    # Iterate through top-level sections to match and validate against schemas
    for section_name, configuration in yaml_content.items():
        schema_file_name = determine_schema(section_name)
        if schema_file_name:
            schema_file_path = os.path.join(schema_directory, schema_file_name)
            try:
                validate_yaml({section_name: configuration}, schema_file_path)
                print(f"Validation passed for {section_name}")
            except Exception as e:
                print(f"Validation failed for {section_name}: {e}")
        else:
            print(f"No specific schema for {section_name}, performing basic checks...")
            # Perform basic checks here (if needed)
else:
    print(f"Failed to load YAML content from {yaml_file_path}")

