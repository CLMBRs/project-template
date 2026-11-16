# AGENTS.md

This repository is a [Copier](https://copier.readthedocs.io/) template for CLMBR
research projects. It is **not** itself a Python project.

- `copier.yml`: the questions Copier asks, and template settings.
- `template/`: the files of a generated project. `.jinja` files are rendered with the
  answers; file and directory names are rendered too, and those that render empty are
  skipped (this is how language-specific files are made conditional).
- `template/AGENTS.md.jinja` is the group-wide agent guidance that every project gets;
  `template/guidelines/` holds the group's human-readable guidelines.
- `README.md`: how to use and change the template.

When changing the template:

- Keep generated projects passing their own checks. Test every change by generating
  projects with several answer combinations (Python with and without Hydra, and
  different license choices) and running `uv sync`, `uv run pre-commit run --all-files`,
  and `uv run pytest` in each; see `.github/workflows/test-template.yml`.
- Keep `AGENTS.md.jinja` short and imperative; detailed explanations belong in
  `template/guidelines/`. Rules that a tool can enforce belong in the tool's
  configuration in `pyproject.toml.jinja`, not in prose.
- Keep the template-owned / project-owned split described in `README.md`, and update
  `_skip_if_exists` in `copier.yml` if you add project-owned files.
- When bumping tool versions, update both `pyproject.toml.jinja` and
  `.pre-commit-config.yaml.jinja`.
