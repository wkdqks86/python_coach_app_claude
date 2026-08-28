import subprocess
import sys
import tempfile

TIMEOUT_SECONDS = 5.0


def run_python(code: str, stdin: str = "") -> tuple[str, str, bool]:
    """Run user code in a separate process and capture stdout/stderr.

    Uses a fresh subprocess (not exec()) so a runaway or crashing submission
    can't affect the API server itself. `stdin` is always passed explicitly
    (even when empty) so input() calls get an immediate EOF instead of the
    subprocess inheriting the server's real stdin and hanging. Runs inside a
    throwaway temp directory so file-I/O problems (level 9) can't leave
    stray files behind in the project folder.
    """
    try:
        with tempfile.TemporaryDirectory(prefix="pycoach-run-") as tmp_dir:
            proc = subprocess.run(
                [sys.executable, "-c", code],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                cwd=tmp_dir,
            )
        return proc.stdout, proc.stderr, False
    except subprocess.TimeoutExpired:
        return "", f"실행 시간이 {TIMEOUT_SECONDS:g}초를 초과했습니다. 무한 반복문이 있는지 확인해보세요.", True
