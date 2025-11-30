import argparse
import sys
from .converter import Converter

def main():
    parser = argparse.ArgumentParser(description="Convert Python automation scripts to Maestro YAML.")
    parser.add_argument("input", help="Path to input Python file")
    parser.add_argument("output_dir", help="Path to output directory for YAML flows")
    
    args = parser.parse_args()
    
    converter = Converter()
    try:
        converter.convert(args.input, args.output_dir)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
