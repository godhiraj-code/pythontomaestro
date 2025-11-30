import logging
from .parser import PythonParser
from .mapper import MaestroMapper
from .generator import YamlGenerator

class Converter:
    def __init__(self):
        self.parser = PythonParser()
        self.mapper = MaestroMapper()
        self.generator = YamlGenerator()

    def convert(self, input_path, output_dir):
        """
        Converts a Python automation script to Maestro YAML flows.
        """
        logging.info(f"Converting {input_path} to {output_dir}")
        # 1. Parse
        test_definitions = self.parser.parse(input_path)
        
        # 2. Map
        maestro_flows = self.mapper.map(test_definitions)
        
        # 3. Generate
        import os
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        for flow in maestro_flows:
            filename = f"{flow['name']}.yaml"
            output_path = os.path.join(output_dir, filename)
            self.generator.generate(flow, output_path)
            logging.info(f"Generated {output_path}")
        
        logging.info("Conversion complete")
