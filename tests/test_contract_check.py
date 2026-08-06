"""Unit tests for the structural contract checker ``pipeline/_contract_check.py``."""

import subprocess
import sys
from pathlib import Path

import pytest

PIPELINE_DIR = Path(__file__).resolve().parent.parent / "pipeline"
sys.path.insert(0, str(PIPELINE_DIR))

import _contract_check as contract_check  # noqa: E402


def write(path: Path, content: str) -> Path:
    """Write a file to a temp path, creating parents as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_should_parse_function_contract_when_spec_has_type_signature(tmp_path: Path) -> None:
    """Given a spec with a typed function signature, the parser extracts it."""
    spec = write(tmp_path / "spec.md", "add(a: int, b: int) -> int\n")

    symbols = contract_check.parse_spec_contracts(str(spec))

    assert len(symbols) == 1
    assert symbols[0].name == "add"
    assert symbols[0].params == ["a", "b"]
    assert symbols[0].return_type == "int"
    assert symbols[0].kind == "function"


def test_should_prefix_method_with_class_when_indented_under_class(tmp_path: Path) -> None:
    """Given an indented method under a class header, the parser qualifies its name."""
    spec = write(tmp_path / "spec.md", "Calculator:\n    add(a: int) -> int\n")

    symbols = contract_check.parse_spec_contracts(str(spec))

    assert symbols[0].name == "Calculator.add"
    assert symbols[0].kind == "method"


def test_should_skip_def_keyword_when_spec_embeds_code_snippets(tmp_path: Path) -> None:
    """Given a spec embedding a 'def' snippet, only real contracts are extracted."""
    spec = write(
        tmp_path / "spec.md",
        "def not_a_contract(x):\n    return x\nreal_contract() -> None\n",
    )

    symbols = contract_check.parse_spec_contracts(str(spec))

    assert [symbol.name for symbol in symbols] == ["real_contract"]


def test_should_return_empty_when_spec_file_is_missing(tmp_path: Path) -> None:
    """Given a nonexistent spec path, the parser returns no contracts."""
    assert contract_check.parse_spec_contracts(str(tmp_path / "missing.md")) == []


def test_should_extract_functions_and_class_methods_from_source(tmp_path: Path) -> None:
    """Given Python source with a function and a class method, both are extracted."""
    source = write(
        tmp_path / "src" / "service.py",
        "def helper(x: int) -> int:\n"
        "    return x\n"
        "\n"
        "class Greeter:\n"
        "    def greet(self, name: str) -> str:\n"
        "        return name\n",
    )

    symbols = contract_check.extract_source_symbols(str(source.parent))
    by_name = {symbol.name: symbol for symbol in symbols}

    assert "helper" in by_name
    assert by_name["helper"].kind == "function"
    assert "Greeter.greet" in by_name
    assert by_name["Greeter.greet"].kind == "method"
    assert by_name["Greeter.greet"].params == ["name"]  # self stripped
    assert by_name["Greeter.greet"].return_type == "str"


def test_should_skip_underscore_files_and_syntax_errors(tmp_path: Path) -> None:
    """Given underscore-prefixed or syntactically broken files, they are ignored."""
    write(tmp_path / "src" / "_private.py", "def hidden() -> None: pass\n")
    write(tmp_path / "src" / "broken.py", "def broken(: :\n")
    write(tmp_path / "src" / "module.py", "def visible() -> None: pass\n")

    symbols = contract_check.extract_source_symbols(str(tmp_path / "src"))

    assert [symbol.name for symbol in symbols] == ["visible"]


def test_should_parse_gherkin_endpoints_case_insensitively_and_dedupe(tmp_path: Path) -> None:
    """Given repeated Gherkin endpoints with mixed case, each endpoint appears once."""
    spec = write(
        tmp_path / "spec.md",
        "- WHEN POST /login with {} \n- when post /login with {}\n- WHEN GET /users\n",
    )

    symbols = contract_check.parse_gherkin_specs(str(spec))

    assert [symbol.name for symbol in symbols] == ["POST /login", "GET /users"]


def test_should_extract_fastapi_endpoints(tmp_path: Path) -> None:
    """Given FastAPI route decorators, the endpoints are extracted."""
    source = write(
        tmp_path / "src" / "api.py",
        '@router.get("/products")\ndef list_products(): pass\n'
        '@app.post("/checkout")\ndef checkout(): pass\n',
    )

    symbols = contract_check.extract_fastapi_endpoints(str(source.parent))

    assert [symbol.name for symbol in symbols] == ["GET /products", "POST /checkout"]


def test_should_pass_when_contracts_match_source(tmp_path: Path) -> None:
    """Given a spec contract matching the source signature, the check passes."""
    spec = write(tmp_path / "spec.md", "add(a: int, b: int) -> int\n")
    write(tmp_path / "src" / "math.py", "def add(a: int, b: int) -> int:\n    return a + b\n")

    passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"))

    assert failures == []
    assert any("'add'" in entry for entry in passes)


def test_should_fail_when_symbol_is_missing(tmp_path: Path) -> None:
    """Given a spec contract with no matching source symbol, the check fails."""
    spec = write(tmp_path / "spec.md", "missing_fn() -> None\n")
    write(tmp_path / "src" / "module.py", "def other_fn() -> None: pass\n")

    passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"))

    assert passes == []
    assert failures[0].startswith("MISSING:")


def test_should_fail_when_kind_mismatches(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Given a class contract but a source function with the same name, the check fails."""
    write(tmp_path / "src" / "module.py", "def foo() -> None:\n    pass\n")
    spec = write(tmp_path / "spec.md", "unused() -> None\n")
    fake_contract = contract_check.ContractSymbol(name="foo", kind="class")
    monkeypatch.setattr(
        contract_check,
        "parse_spec_contracts",
        lambda _spec_path: [fake_contract],
    )

    _passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"))

    assert failures[0].startswith("TYPE_MISMATCH:")


def test_should_fail_when_param_count_differs(tmp_path: Path) -> None:
    """Given a spec expecting two params but source has none, the check fails."""
    spec = write(tmp_path / "spec.md", "greet(name: str) -> str\n")
    write(tmp_path / "src" / "module.py", "def greet() -> str:\n    return 'hi'\n")

    _passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"))

    assert failures[0].startswith("PARAM_COUNT:")


def test_should_fail_when_return_type_is_missing(tmp_path: Path) -> None:
    """Given a spec requiring a return type but source has none, the check fails."""
    spec = write(tmp_path / "spec.md", "add(a: int, b: int) -> int\n")
    write(tmp_path / "src" / "module.py", "def add(a, b):\n    return a + b\n")

    _passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"))

    assert failures[0].startswith("RETURN_TYPE_MISSING:")


def test_should_ignore_self_when_comparing_method_params(tmp_path: Path) -> None:
    """Given a spec method without self and a source method with self, the check passes."""
    spec = write(tmp_path / "spec.md", "Greeter:\n    greet(name: str) -> str\n")
    write(
        tmp_path / "src" / "module.py",
        "class Greeter:\n    def greet(self, name: str) -> str:\n        return name\n",
    )

    passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"))

    assert failures == []
    assert any("'Greeter.greet'" in entry for entry in passes)


def test_should_print_usage_and_exit_when_spec_flag_is_missing() -> None:
    """Given the CLI without --spec, it prints usage and exits nonzero."""
    script = PIPELINE_DIR / "_contract_check.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Usage:" in result.stdout
