import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = PROJECT_ROOT / "vatli1.py"
CASE_DIRECTORY = Path(__file__).parent / "cases"


def extract_result_lines(stdout):
    marker = "====== KẾT QUẢ TÍNH LỰC ĐIỆN TÁC DỤNG TỪNG ĐIỆN TÍCH ======"
    if marker not in stdout:
        raise AssertionError("The CLI did not print its force-results section.")

    result_section = stdout.split(marker, maxsplit=1)[1]
    return "\n".join(
        line
        for line in result_section.splitlines()
        if line.startswith("--- Điện tích q")
        or line.startswith("Fx = ")
        or line.startswith("Fy = ")
        or line.startswith("F = ")
    )


def run_case(input_file):
    expected_file = input_file.with_suffix(".out")
    if not expected_file.is_file():
        raise FileNotFoundError(f"Missing expected-output fixture: {expected_file}")

    input_text = input_file.read_text(encoding="utf-8")
    expected_text = expected_file.read_text(encoding="utf-8").rstrip()
    with tempfile.TemporaryDirectory(prefix="vatli1-test-") as temp_dir:
        working_dir = Path(temp_dir)
        cli_copy = working_dir / "vatli1.py"
        shutil.copyfile(SOURCE_SCRIPT, cli_copy)
        completed = subprocess.run(
            [sys.executable, str(cli_copy)],
            input=input_text,
            text=True,
            encoding="utf-8",
            capture_output=True,
            cwd=working_dir,
            timeout=30,
            check=False,
        )

    if completed.returncode != 0:
        raise RuntimeError(
            f"{input_file.name}: CLI exited with {completed.returncode}.\n"
            f"stderr:\n{completed.stderr}\nstdout:\n{completed.stdout}"
        )

    actual_text = extract_result_lines(completed.stdout)
    if actual_text != expected_text:
        raise AssertionError(
            f"{input_file.name}: CLI output differs from {expected_file.name}.\n"
            f"Expected:\n{expected_text}\nActual:\n{actual_text}"
        )


def main():
    case_files = sorted(CASE_DIRECTORY.glob("*.in"))
    if not case_files:
        raise RuntimeError("No .in test cases found in tests/cases.")

    for case_file in case_files:
        run_case(case_file)
        print(f"PASS {case_file.stem}")

    print(f"{len(case_files)} case(s) passed.")


if __name__ == "__main__":
    main()
