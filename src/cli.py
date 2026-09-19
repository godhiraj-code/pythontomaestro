import argparse
import sys
from .converter import Converter
from .mapper import DEFAULT_APP_ID

def main(argv=None):
    parser = argparse.ArgumentParser(description="Convert Python automation scripts to Maestro YAML.")
    parser.add_argument("input", help="Path to input Python file")
    parser.add_argument("output_dir", help="Path to output directory for YAML flows")
    parser.add_argument(
        "--app-id",
        default=DEFAULT_APP_ID,
        help=f"Target Maestro application ID (default: {DEFAULT_APP_ID})",
    )
    
    args = parser.parse_args(argv)
    
    converter = Converter()
    try:
        converter.convert(args.input, args.output_dir, app_id=args.app_id)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
