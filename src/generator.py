import yaml

class YamlGenerator:
    def generate(self, flow_data, output_path):
        """
        Writes the Maestro flow data to a YAML file.
        """
        output = {key: value for key, value in flow_data.items() if key != "_has_errors"}
        with open(output_path, "w", encoding="utf-8") as f:
            if flow_data.get("_has_errors", False):
                f.write("# WARNING: This flow contains unsupported actions (TODOs). Manual review required.\n")
            yaml.safe_dump(output, f, sort_keys=False, allow_unicode=True)
