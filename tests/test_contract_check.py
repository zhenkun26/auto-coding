"""Unit tests for the structural contract checker ``scripts/check_python_contracts.py``."""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import check_python_contracts as contract_check


@pytest.fixture
def diagnostics() -> contract_check.DiagnosticCollector:
    """Provide a fresh diagnostic collector for each test."""
    return contract_check.DiagnosticCollector()


def write(path: Path, content: str) -> Path:
    """Write a file to a temp path, creating parents as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_should_parse_function_contract_when_spec_has_type_signature(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given a spec with a typed function signature, the parser extracts it."""
    spec = write(tmp_path / "spec.md", "add(a: int, b: int) -> int\n")

    symbols = contract_check.parse_spec_contracts(str(spec), diagnostics)

    assert len(symbols) == 1
    assert symbols[0].name == "add"
    assert symbols[0].params == ["a", "b"]
    assert symbols[0].return_type == "int"
    assert symbols[0].kind == "function"


def test_should_prefix_method_with_class_when_indented_under_class(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given an indented method under a class header, the parser qualifies its name."""
    spec = write(tmp_path / "spec.md", "Calculator:\n    add(a: int) -> int\n")

    symbols = contract_check.parse_spec_contracts(str(spec), diagnostics)

    assert symbols[0].name == "Calculator.add"
    assert symbols[0].kind == "method"


def test_should_not_qualify_method_under_lowercase_class(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given a lowercase header that is not a class declaration, no prefix is added."""
    spec = write(tmp_path / "spec.md", "lower:\n    foo() -> None\n")

    symbols = contract_check.parse_spec_contracts(str(spec), diagnostics)

    assert symbols[0].name == "foo"


def test_should_skip_def_keyword_when_spec_embeds_code_snippets(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given a spec embedding a 'def' snippet, only real contracts are extracted."""
    spec = write(
        tmp_path / "spec.md",
        "def not_a_contract(x):\n    return x\nreal_contract() -> None\n",
    )

    symbols = contract_check.parse_spec_contracts(str(spec), diagnostics)

    assert [symbol.name for symbol in symbols] == ["real_contract"]


def test_should_ignore_signature_like_prose_outside_fenced_blocks(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given signature-looking prose outside code fences, it is not a contract."""
    spec = write(
        tmp_path / "spec.md",
        "The endpoint calls validate(user: str) -> bool before saving.\n"
        "When finished, cleanup(temp: str) -> None runs automatically.\n"
        "```\n"
        "real_contract(name: str) -> str\n"
        "```\n",
    )

    symbols = contract_check.parse_spec_contracts(str(spec), diagnostics)

    assert [symbol.name for symbol in symbols] == ["real_contract"]


def test_should_parse_contracts_inside_fenced_blocks(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given contracts inside a fenced code block, they are extracted."""
    spec = write(
        tmp_path / "spec.md",
        "## Interface contracts\n"
        "```python\n"
        "Service:\n"
        "    authorize(user: str, amount: int) -> bool\n"
        "```\n",
    )

    symbols = contract_check.parse_spec_contracts(str(spec), diagnostics)

    assert [symbol.name for symbol in symbols] == ["Service.authorize"]
    assert symbols[0].kind == "method"


def test_should_fall_back_to_full_text_when_spec_has_no_fences(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given a spec without fenced blocks, full-text parsing still works."""
    spec = write(tmp_path / "spec.md", "plain_contract(x: int) -> int\n")

    symbols = contract_check.parse_spec_contracts(str(spec), diagnostics)

    assert [symbol.name for symbol in symbols] == ["plain_contract"]


def test_should_return_empty_when_spec_file_is_missing(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given a nonexistent spec path, the parser returns no contracts."""
    assert contract_check.parse_spec_contracts(str(tmp_path / "missing.md"), diagnostics) == []


def test_should_extract_functions_and_class_methods_from_source(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
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

    symbols = contract_check.extract_source_symbols(str(source.parent), diagnostics)
    by_name = {symbol.name: symbol for symbol in symbols}

    assert "helper" in by_name
    assert by_name["helper"].kind == "function"
    assert by_name["Greeter"].kind == "class"
    assert "Greeter.greet" in by_name
    assert by_name["Greeter.greet"].kind == "method"
    assert by_name["Greeter.greet"].params == ["name"]  # self stripped
    assert by_name["Greeter.greet"].return_type == "str"


def test_should_skip_underscore_files_and_syntax_errors(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given underscore-prefixed or syntactically broken files, they are ignored."""
    write(tmp_path / "src" / "_private.py", "def hidden() -> None: pass\n")
    write(tmp_path / "src" / "broken.py", "def broken(: :\n")
    write(tmp_path / "src" / "module.py", "def visible() -> None: pass\n")

    symbols = contract_check.extract_source_symbols(str(tmp_path / "src"), diagnostics)

    assert [symbol.name for symbol in symbols] == ["visible"]


def test_should_parse_gherkin_endpoints_case_insensitively_and_dedupe(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given repeated Gherkin endpoints with mixed case, each endpoint appears once."""
    spec = write(
        tmp_path / "spec.md",
        "- WHEN POST /login with {} \n- when post /login with {}\n- WHEN GET /users\n",
    )

    symbols = contract_check.parse_gherkin_specs(str(spec), diagnostics)

    assert [symbol.name for symbol in symbols] == ["POST /login", "GET /users"]


def test_should_extract_fastapi_endpoints(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given FastAPI route decorators, the endpoints are extracted."""
    source = write(
        tmp_path / "src" / "api.py",
        '@router.get("/products")\ndef list_products(): pass\n'
        '@app.post("/checkout")\ndef checkout(): pass\n',
    )

    symbols = contract_check.extract_fastapi_endpoints(str(source.parent), diagnostics)

    assert [symbol.name for symbol in symbols] == ["GET /products", "POST /checkout"]


def test_should_extract_fastapi_endpoints_from_async_handlers(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given async route handlers, the endpoints are extracted via AST."""
    source = write(
        tmp_path / "src" / "api.py",
        '@router.get("/items")\nasync def list_items(): pass\n',
    )

    symbols = contract_check.extract_fastapi_endpoints(str(source.parent), diagnostics)

    assert [symbol.name for symbol in symbols] == ["GET /items"]


def test_should_pass_when_contracts_match_source(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given a spec contract matching the source signature, the check passes."""
    spec = write(tmp_path / "spec.md", "add(a: int, b: int) -> int\n")
    write(tmp_path / "src" / "math.py", "def add(a: int, b: int) -> int:\n    return a + b\n")

    passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"), diagnostics)

    assert failures == []
    assert any("'add'" in entry for entry in passes)


def test_should_fail_when_symbol_is_missing(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given a spec contract with no matching source symbol, the check fails."""
    spec = write(tmp_path / "spec.md", "missing_fn() -> None\n")
    write(tmp_path / "src" / "module.py", "def other_fn() -> None: pass\n")

    passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"), diagnostics)

    assert passes == []
    assert failures[0].startswith("MISSING:")


def test_should_fail_when_kind_mismatches(
    tmp_path: Path,
    diagnostics: contract_check.DiagnosticCollector,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Given a class contract but a source function with the same name, the check fails."""
    write(tmp_path / "src" / "module.py", "def foo() -> None:\n    pass\n")
    spec = write(tmp_path / "spec.md", "unused() -> None\n")
    fake_contract = contract_check.ContractSymbol(name="foo", kind="class")
    monkeypatch.setattr(
        contract_check,
        "parse_spec_contracts",
        lambda _spec_path, _diagnostics: [fake_contract],
    )

    _passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"), diagnostics)

    assert failures[0].startswith("TYPE_MISMATCH:")


def test_should_fail_when_param_count_differs(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given a spec expecting two params but source has none, the check fails."""
    spec = write(tmp_path / "spec.md", "greet(name: str) -> str\n")
    write(tmp_path / "src" / "module.py", "def greet() -> str:\n    return 'hi'\n")

    _passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"), diagnostics)

    assert failures[0].startswith("PARAM_COUNT:")


def test_should_fail_when_return_type_is_missing(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given a spec requiring a return type but source has none, the check fails."""
    spec = write(tmp_path / "spec.md", "add(a: int, b: int) -> int\n")
    write(tmp_path / "src" / "module.py", "def add(a, b):\n    return a + b\n")

    _passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"), diagnostics)

    assert failures[0].startswith("RETURN_TYPE_MISSING:")


def test_should_ignore_self_when_comparing_method_params(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given a spec method without self and a source method with self, the check passes."""
    spec = write(tmp_path / "spec.md", "Greeter:\n    greet(name: str) -> str\n")
    write(
        tmp_path / "src" / "module.py",
        "class Greeter:\n    def greet(self, name: str) -> str:\n        return name\n",
    )

    passes, failures = contract_check.run_check(str(spec), str(tmp_path / "src"), diagnostics)

    assert failures == []
    assert any("'Greeter.greet'" in entry for entry in passes)


def test_should_print_usage_and_exit_when_spec_flag_is_missing() -> None:
    """Given the CLI without --spec, it prints usage and exits nonzero."""
    script = SCRIPTS_DIR / "check_python_contracts.py"

    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Usage:" in result.stdout


def test_should_report_parse_failure_instead_of_silently_skipping(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given an unparseable source file, a diagnostic is recorded instead of silence."""
    write(tmp_path / "src" / "broken.py", "def broken(: :\n")
    write(tmp_path / "src" / "module.py", "def visible() -> None: pass\n")

    symbols = contract_check.extract_source_symbols(str(tmp_path / "src"), diagnostics)

    assert [symbol.name for symbol in symbols] == ["visible"]
    assert any("parse error" in diagnostic for diagnostic in diagnostics.messages)


def test_should_report_unreadable_file_instead_of_crashing(
    tmp_path: Path, diagnostics: contract_check.DiagnosticCollector
) -> None:
    """Given a non-UTF-8 source file, a diagnostic is recorded instead of a crash."""
    broken = tmp_path / "src" / "binary.py"
    broken.parent.mkdir(parents=True, exist_ok=True)
    broken.write_bytes(b"\xff\xfe\x00bad encoding\xff")

    symbols = contract_check.extract_source_symbols(str(broken.parent), diagnostics)

    assert symbols == []
    assert any("read error" in diagnostic for diagnostic in diagnostics.messages)


def test_should_exit_usage_when_spec_flag_has_no_value() -> None:
    """Given --spec without a value, the CLI exits nonzero with usage."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "check_python_contracts.py"), "--spec"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Usage:" in result.stdout


def test_should_exit_error_when_spec_file_is_missing(tmp_path: Path) -> None:
    """Given a nonexistent spec file, the CLI exits nonzero with a stderr message."""
    write(tmp_path / "src" / "module.py", "def visible() -> None: pass\n")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "check_python_contracts.py"),
            "--spec",
            str(tmp_path / "missing.md"),
            "--source",
            str(tmp_path / "src"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Spec file not found" in result.stderr


def test_should_exit_error_when_source_directory_is_missing(tmp_path: Path) -> None:
    """Given a nonexistent --source, the CLI exits nonzero instead of a false pass."""
    spec = write(tmp_path / "spec.md", "visible() -> None\n")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "check_python_contracts.py"),
            "--spec",
            str(spec),
            "--source",
            str(tmp_path / "no-such-dir"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Source directory not found" in result.stderr


def test_should_parse_cli_args_with_defaults() -> None:
    """Given no arguments, the parser returns an empty spec and default source."""
    spec_path, src_dir = contract_check.parse_cli_args([])

    assert spec_path == ""
    assert src_dir == "src/"


def test_should_exit_usage_from_parser_on_unknown_flag() -> None:
    """Given an unknown flag, the parser exits with SystemExit and prints usage."""
    with pytest.raises(SystemExit) as exc_info:
        contract_check.parse_cli_args(["--unknown"])

    assert exc_info.value.code == 1


def test_should_return_usage_code_when_spec_omitted(capsys: pytest.CaptureFixture) -> None:
    """Given no --spec, main returns 1 and prints usage."""
    exit_code = contract_check.main([])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Usage:" in captured.out


def test_should_return_success_for_valid_spec_source(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Given a valid spec/source pair, main returns 0 and verifies the contract."""
    spec = write(tmp_path / "spec.md", "add(a: int, b: int) -> int\n")
    write(tmp_path / "src" / "math.py", "def add(a: int, b: int) -> int:\n    return a + b\n")

    exit_code = contract_check.main(["--spec", str(spec), "--source", str(tmp_path / "src")])

    assert exit_code == 0
    assert "All 1 contracts structurally verified." in capsys.readouterr().out


def test_should_return_failure_code_when_contract_mismatches(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Given a mismatched contract, main returns 1 and reports the failure."""
    spec = write(tmp_path / "spec.md", "add(a: int, b: int) -> int\n")
    write(tmp_path / "src" / "math.py", "def add(a: int) -> int:\n    return a\n")

    exit_code = contract_check.main(["--spec", str(spec), "--source", str(tmp_path / "src")])

    assert exit_code == 1
    assert "PARAM_COUNT" in capsys.readouterr().out


def test_should_return_error_when_source_directory_missing(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Given a missing --source, main returns 1 with a stderr message."""
    spec = write(tmp_path / "spec.md", "add(a: int, b: int) -> int\n")

    exit_code = contract_check.main(["--spec", str(spec), "--source", str(tmp_path / "nope")])

    assert exit_code == 1
    assert "Source directory not found" in capsys.readouterr().err


def test_should_pass_1000_concurrent_invocations(tmp_path: Path) -> None:
    """Given a valid spec/source pair, 1000 concurrent CLI calls all exit zero."""
    spec = write(tmp_path / "spec.md", "add(a: int, b: int) -> int\n")
    write(tmp_path / "src" / "math.py", "def add(a: int, b: int) -> int:\n    return a + b\n")
    command = partial(
        subprocess.run,
        [
            sys.executable,
            str(SCRIPTS_DIR / "check_python_contracts.py"),
            "--spec",
            str(spec),
            "--source",
            str(tmp_path / "src"),
        ],
        capture_output=True,
        check=False,
    )

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(lambda _index: command(), range(1000)))

    assert len(results) == 1000
    assert all(result.returncode == 0 for result in results)
