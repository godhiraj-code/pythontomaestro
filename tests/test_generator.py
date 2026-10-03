import yaml

from src.generator import YamlGenerator
from src.parser import PythonParser


def test_generate_preserves_input_and_warnings_when_reused(tmp_path):
    flow = {"name": "test_unicode", "_has_errors": True, "steps": [{"inputText": "हैलो 世界"}]}
    generator = YamlGenerator()
    for name in ("first.yaml", "second.yaml"):
        path = tmp_path / name
        generator.generate(flow, path)
        content = path.read_text(encoding="utf-8")
        assert content.startswith("# WARNING:")
        assert "हैलो 世界" in content
        assert "_has_errors" not in yaml.safe_load(content)
    assert flow["_has_errors"] is True


def test_parser_honors_declared_source_encoding(tmp_path):
    path = tmp_path / "test_latin1.py"
    path.write_bytes("# coding: latin-1\ndef test_example():\n    driver.get('https://example.com/café')\n".encode("latin-1"))
    result = PythonParser().parse(path)
    assert result[0]["name"] == "test_example"
