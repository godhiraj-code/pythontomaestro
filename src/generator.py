import yaml

class YamlGenerator:
    def generate(self, flow_data, output_path):
        """
        Writes the Maestro flow data to a YAML file.
        """
        with open(output_path, "w") as f:
            if flow_data.pop("_has_errors", False):
                f.write("# WARNING: This flow contains unsupported actions (TODOs). Manual review required.\n")
            yaml.dump(flow_data, f, sort_keys=False)
