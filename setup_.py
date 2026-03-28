"""Shim that forwards legacy setup.py commands to their modern equivalents.

PyTorch has migrated from setuptools to scikit-build-core. This script
intercepts common setup.py invocations and translates them to the
corresponding pip/build/spin commands.

Usage examples (all produce the same result as before):
    python setup_.py install          -> pip install . -v --no-build-isolation
    python setup_.py develop          -> pip install -e . -v --no-build-isolation
    python setup_.py bdist_wheel      -> python -m build --wheel --no-isolation
    python setup_.py clean            -> spin clean
    python setup_.py build            -> pip install -e . -v --no-build-isolation
"""

import subprocess
import sys


def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(0)

    command = args[0]

    if command == "install":
        pip_args = [sys.executable, "-m", "pip", "install", ".", "-v", "--no-build-isolation"]
        _run(pip_args, command)
    elif command == "develop":
        pip_args = [sys.executable, "-m", "pip", "install", "-e", ".", "-v", "--no-build-isolation"]
        _run(pip_args, command)
    elif command == "build":
        pip_args = [sys.executable, "-m", "pip", "install", "-e", ".", "-v", "--no-build-isolation"]
        _run(pip_args, command)
    elif command == "bdist_wheel":
        build_args = [sys.executable, "-m", "build", "--wheel", "--no-isolation"]
        _run(build_args, command)
    elif command == "clean":
        clean_args = [sys.executable, "-m", "spin", "clean"]
        _run(clean_args, command)
    else:
        print(
            f"Unknown command: {command}\n\n"
            "Supported commands: install, develop, build, bdist_wheel, clean\n"
            "See 'python setup_.py --help' for details.",
            file=sys.stderr,
        )
        sys.exit(1)


def _run(cmd: list[str], original_command: str) -> None:
    print(
        f"NOTE: 'python setup.py {original_command}' is no longer supported.\n"
        f"Forwarding to: {' '.join(cmd)}\n",
        file=sys.stderr,
    )
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
