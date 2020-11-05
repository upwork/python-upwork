import nox  # type: ignore
from pathlib import Path

nox.options.sessions = ["tests", "lint", "build"]

python = ["3.8"]


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
    """
    Run tests.

    Args:
        session: (todo): write your description
    """
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


@nox.session(python="3.8")
def lint(session):
    """
    Run lint.

    Args:
        session: (todo): write your description
    """
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


@nox.session(python="3.8")
def build(session):
    """
    Build and install.

    Args:
        session: (todo): write your description
    """
    session.install("setuptools")
    session.install("wheel")
    session.install("twine")
    session.run("rm", "-rf", "dist", "build", external=True)
    session.run("python", "setup.py", "--quiet", "sdist", "bdist_wheel")


@nox.session(python="3.8")
def publish(session):
    """
    Publish the build.

    Args:
        session: (todo): write your description
    """
    build(session)
    print("REMINDER: Has the changelog been updated?")
    session.run("python", "-m", "twine", "upload", "dist/*")
