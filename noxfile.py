import nox  # type: ignore
from pathlib import Path

nox.options.sessions = ["tests", "lint", "build"]

python = ["3.9"]


lint_dependencies = [
    "-e",
    ".",
    "black",
    "flake8",
    "flake8-bugbear",
    "mypy",
    "check-manifest",
]


@nox.session(python=python)
def tests(session):
    session.install("-e", ".", "pytest", "pytest-cov")
    tests = session.posargs or ["tests"]
    session.run(
        "pytest", "--cov=upwork", "--cov-config", ".coveragerc", "--cov-report=", *tests
    )
    session.notify("cover")


@nox.session
def cover(session):
    """Coverage analysis"""
    session.install("coverage")
    session.run("coverage", "report", "--show-missing", "--fail-under=0")
    session.run("coverage", "erase")


@nox.session(python="3.9")
def lint(session):
    session.install(*lint_dependencies)
    files = ["tests"] + [str(p) for p in Path(".").glob("*.py")]
    session.run("black", "--check", *files)
    session.run("flake8", *files)
    session.run("mypy", *files)
    session.run("python", "setup.py", "check", "--metadata", "--strict")
    if "--skip_manifest_check" in session.posargs:
        pass
    else:
        session.run("check-manifest")


@nox.session(python="3.9")
def build(session):
    session.install("setuptools")
    session.install("wheel")
    session.install("twine")
    session.install("types-requests")
    session.run("rm", "-rf", "dist", "build", external=True)
    session.run("python", "setup.py", "--quiet", "sdist", "bdist_wheel")


@nox.session(python="3.9")
def publish(session):
    build(session)
    print("REMINDER: Has the changelog been updated?")
    session.run("python", "-m", "twine", "upload", "dist/*")
