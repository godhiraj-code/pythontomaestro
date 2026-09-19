from pathlib import Path

import yaml

from src.cli import main
from src.mapper import DEFAULT_APP_ID, MaestroMapper


def test_mapper_keeps_legacy_default_app_id():
    flows = MaestroMapper().map([{"name": "test_empty", "steps": []}])

    assert flows[0]["appId"] == DEFAULT_APP_ID == "com.example.app"


def test_cli_custom_app_id_matches_golden_file(tmp_path):
    source = tmp_path / "test_checkout.py"
    output_dir = tmp_path / "flows"
    source.write_text(
        "def test_checkout():\n"
        "    driver.get('https://example.com/checkout')\n",
        encoding="utf-8",
    )

    main([str(source), str(output_dir), "--app-id", "com.acme.shop"])

    generated = (output_dir / "test_checkout.yaml").read_text(encoding="utf-8")
    golden = (Path(__file__).parent / "golden" / "custom_app_flow.yaml").read_text(
        encoding="utf-8"
    )
    assert yaml.safe_load(generated) == yaml.safe_load(golden)
