import subprocess
import sys

TIMEOUT_SECONDS = 5.0


def run_python(code: str) -> tuple[str, str, bool]:
    """Run user code in a separate process and capture stdout/stderr.

    Returns (stdout, stderr, timed_out). Uses a fresh subprocess (not exec())
    so a runaway or crashing submission can't affect the API server itself.
    """
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        return proc.stdout, proc.stderr, False
    except subprocess.TimeoutExpired:
        return "", f"실행 시간이 {TIMEOUT_SECONDS:g}초를 초과했습니다. 무한 반복문이 있는지 확인해보세요.", True
