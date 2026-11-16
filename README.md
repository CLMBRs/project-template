# CLMBR Project Template

The default starting point for research projects in
[CLMBR](https://clmbr.shane.st). It is also the canonical home of the group's
guidelines for organizing projects and writing code: see
[`template/guidelines/`](template/guidelines/).

A new project comes with:

- **[uv](https://docs.astral.sh/uv/)** for Python environments and dependencies (no conda,
  pip, or `requirements.txt`)
- **`src/` layout**: the project is an installable package that scripts and tests import
- **[Ruff](https://docs.astral.sh/ruff/)** (formatting and linting), **[ty](https://docs.astral.sh/ty/)**
  (type checking), and **[pytest](https://docs.pytest.org/)**, run by
  **[pre-commit](https://pre-commit.com/)** on every commit and by **GitHub Actions** on
  every push
- **[Hydra](https://hydra.cc)** experiment configs with an example experiment script
- **`AGENTS.md`** (and `CLAUDE.md`) instructing AI coding agents on group conventions
- **Group guidelines** for project setup, Python style, and recommended packages

## Creating a project

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and git. While
this repository is private, let git use your GitHub login first (once per machine):
install the [GitHub CLI](https://cli.github.com/), then run
`gh auth login` and `gh auth setup-git`.

```bash
uvx copier copy gh:CLMBRs/project-template my-project
```

Answer the questions, then follow the printed next steps:

```bash
cd my-project
git init -b main
uv sync
uv run pre-commit install
uv run pytest
git add -A && git commit -m "Initial commit from CLMBR project template"
```

Finally, create the GitHub repository and push (e.g.
`gh repo create CLMBRs/my-project --private --source . --push`), then fill in
`README.md` and `PROJECT.md`.

## Updating a project

When the template improves, pull the changes into an existing project:

```bash
uvx copier update
```

Copier merges the changes, and marks any conflicts for you to resolve. To keep updates
painless, the files in a generated project are split by owner:

| Owned by the template (don't edit in projects) | Owned by the project (edit freely) |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md`, `guidelines/`, `.pre-commit-config.yaml`, CI workflow | `README.md`, `PROJECT.md`, `src/`, `scripts/`, `config/`, `tests/`, `docs/`, `data/README.md` |

Project-owned files are never overwritten by `copier update`. `pyproject.toml` is
shared: projects add dependencies, the template updates tool settings, and Copier
merges the two.

## Changing the template

The template lives in [`template/`](template/), and the questions Copier asks are in
[`copier.yml`](copier.yml). Files ending in `.jinja` are rendered with the answers;
files or directories whose names render empty (e.g.
`{% if license == 'MIT' %}LICENSE{% endif %}`) are skipped. Python is included in
every project; conditional names can be used for future optional languages.

Projects created from older versions without Python can remain on their existing
template release; updating them to the Python-first template is not supported.

To test changes, generate a project from your working copy and run its checks:

```bash
uvx copier copy --defaults -d project_name=test-project -d author_name=Test \
    -d author_email=test@example.com . /tmp/test-project
cd /tmp/test-project && git init && uv sync && git add -A \
    && uv run pre-commit run --all-files && uv run pytest
```

CI does this for several combinations of answers on every push.

**Releasing:** `copier copy` and `copier update` use the latest
[version tag](https://semver.org/), so tag a release after changes are merged:

```bash
git tag -a v0.2.0 -m "Describe the change" && git push --follow-tags
```

### Adding a language

1. Add an optional question to `copier.yml`; Python remains included in every project.
2. Add its files under `template/`, with conditional names where appropriate (e.g.
   `{% if use_r %}renv.lock{% endif %}`). Mark any new project-owned files in
   `_skip_if_exists`.
3. Add relevant guidelines, agent instructions, checks, and CI steps. Document and
   test generated projects both with and without the additional language.

### Roadmap

Topics we'd like to add to the guidelines:

- Managing data, especially from human participants
- Using the cluster (hyak, patas)
- Designing experiments with Hydra (sweeps, structured configs)
- Writing: LaTeX, Quarto, and resources such as
  [Experimentology](https://experimentology.io/)
- The research process beyond code: finding a question, writing up results
