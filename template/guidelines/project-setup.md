# Setting Up and Organizing a CLMBR Project

A living guide to how CLMBR research projects are set up and organized. Suggestions
are welcome: open an issue or pull request on the
[template repository](https://github.com/CLMBRs/project-template).

## Where to host the repository

Create a GitHub repository for every project from day one. It can be private to start.

- **Your personal account** is best when you are the main or only contributor, and you
  want ownership of it (for job applications, etc.).
- **The [CLMBRs organization](https://github.com/CLMBRs)** is best for projects with
  many collaborators, and for resources used by multiple projects.

## Creating a project from the template

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and git. While
the template repository is private, first let git use your GitHub login: install the
[GitHub CLI](https://cli.github.com/) and run `gh auth login` and `gh auth setup-git`.

```bash
uvx copier copy gh:CLMBRs/project-template my-project
```

Copier asks a few questions (name, license, languages, ...) and prints the next steps.
Later, to pull in improvements to the template:

```bash
uvx copier update
```

Copier merges template changes into your project. Files the project owns, such as
`README.md`, `PROJECT.md`, and everything in `src/`, `scripts/`, `config/`, and
`tests/`, are never overwritten; files the template owns, such as `AGENTS.md` and
`guidelines/`, should not be edited in the project.

## Project structure

| Path | Contents |
| --- | --- |
| `README.md` | What the project is, how the repository is organized, and **exactly what to run to reproduce every result** in the paper/thesis based on it. |
| `PROJECT.md` | Project-specific notes for collaborators and AI agents: goals, data locations, conventions. |
| `AGENTS.md` | Group-wide instructions for AI coding agents (from the template). |
| `LICENSE` | The license. We tend to use GNU GPLv3, but [there are other good options](https://choosealicense.com/licenses/). |
| `pyproject.toml`, `uv.lock` | Python project metadata, dependencies, and tool settings; exact locked versions. |
| `src/<package>/` | The project's importable Python package: all reusable code. |
| `scripts/` | Command-line entry points that use the package (e.g. the main experiment script). |
| `config/` | Configs for experiments. **We recommend [Hydra](https://hydra.cc)**; see [lm-training](https://github.com/CLMBRs/lm-training/blob/main/config/train-lm.yaml) for a modular example. |
| `tests/` | Tests for the package. |
| `notebooks/` | Exploratory analysis. |
| `data/` | Data used in the project. Not committed (see below). |
| `outputs/` | Script outputs: models, generated data, logs, figures. Not committed. |
| `docs/` | User-facing documentation for the project. |
| `guidelines/` | These group guidelines. |

### Data

- **Do not** commit publicly available datasets to the repository. Commit the scripts
  that download and preprocess them, and document them in `data/README.md`.
- **Do not** put raw data from human participants in the repository. Follow your IRB
  protocol for where it may be stored. (More group guidance on this is forthcoming.)
- Never modify raw data in place: preprocessing scripts write to new files.

## Python environments with uv

Every Python project uses [uv](https://docs.astral.sh/uv/) for its environment and
dependencies, instead of conda, pip, `requirements.txt`, or `setup.py`. uv installs
the right Python version automatically, and records exact versions of every package in
`uv.lock`, so collaborators (and your future self) get an identical environment.

| Task | Command |
| --- | --- |
| Create or update the environment | `uv sync` |
| Add a dependency | `uv add numpy` (with a version bound: `uv add "numpy>=2.0"`) |
| Add a development-only tool | `uv add --dev ipykernel` |
| Add a package from GitHub | `uv add git+https://github.com/CLMBRs/ultk` |
| Add a local package you're developing | `uv add --editable ../other-package` |
| Remove a dependency | `uv remove numpy` |
| Upgrade locked versions | `uv lock --upgrade` (or `--upgrade-package numpy`) |
| Run a script | `uv run python scripts/run_experiment.py` |
| Run a tool without installing it | `uvx <tool>` |

- Commit `pyproject.toml` and `uv.lock` together whenever dependencies change.
- `uv run` makes sure the environment is up to date before running, so you never need
  to activate it. (You can still `source .venv/bin/activate` if you prefer.)
- To use the environment in Jupyter, `uv add --dev ipykernel` and select the
  project's `.venv` as the kernel.
- **PyTorch:** the right build depends on your hardware (CPU vs CUDA version). See
  [uv's PyTorch guide](https://docs.astral.sh/uv/guides/integration/pytorch/) for how
  to configure this in `pyproject.toml`.

## Code quality

See [python-style.md](python-style.md). In short: Ruff formats and lints, ty checks
types, pytest runs tests, and pre-commit runs the checks on every commit. CI on GitHub
runs everything on every push and pull request.

## Releasing a package (optional)

If the project is a reusable library (like [ultk](https://github.com/CLMBRs/ultk)),
you can publish it to [PyPI](https://pypi.org) so others can install it with
`uv add` or `pip install`. Every project from the template is already an installable
package, so there is little extra to do.

**Use [semantic versioning](https://semver.org/).** A version looks like `1.2.3`
(MAJOR.MINOR.PATCH):

- Increment **MAJOR** for changes that are **not backwards compatible**: anything that
  could break code that uses yours, such as removing or renaming a function.
- Increment **MINOR** for **backwards-compatible** additions to the public API.
- Increment **PATCH** for changes that don't affect the public API: bug fixes,
  optimizations, documentation.
- The numbers aren't decimals: `1.10.0` comes after `1.9.0`.

To release:

```bash
uv version --bump minor              # or major / patch; updates pyproject.toml
git commit -am "Release v$(uv version --short)"
git tag -a "v$(uv version --short)" -m "Release v$(uv version --short)"
git push --follow-tags
uv build                             # build the package into dist/
uv publish                           # upload to PyPI (needs a PyPI token)
```

PyPI never lets you change or reuse a version once uploaded, so only release
well-considered versions of `main`, and do in-progress work on branches.
