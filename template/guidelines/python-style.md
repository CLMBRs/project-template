# CLMBR Python Style Guide

How we write Python in CLMBR projects. Formatting, import order, and many lint rules
are enforced automatically by [Ruff](https://docs.astral.sh/ruff/) and type checking
by [ty](https://docs.astral.sh/ty/), all configured in `pyproject.toml` and run by
pre-commit and CI. This guide covers those tools and the conventions they can't
enforce.

## Tooling

| Task | Tool | Command |
| --- | --- | --- |
| Formatting | Ruff | `uv run ruff format` |
| Linting and import sorting | Ruff | `uv run ruff check --fix` |
| Type checking | ty | `uv run ty check` |
| Testing | pytest | `uv run pytest` |
| All of the above but tests | pre-commit | `uv run pre-commit run --all-files` |

Set up your editor to use the same tools, so you see problems as you type:

- **VS Code:** install the [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
  and [ty](https://marketplace.visualstudio.com/items?itemName=astral-sh.ty)
  extensions, enable "format on save", and select the project's `.venv` as the
  interpreter.
- **Other editors:** both `ruff server` and `ty server` are language servers.

Don't fight the formatter: if it formats something in a way you dislike, leave it.
Settings such as line length (88) are group-wide; change them in the template, not in
individual projects.

## Naming

- Name variables, functions, and classes with **full, descriptive words**, space
  permitting: `num_layers`, `hidden_size`, `sentence_embeddings`, not `nl`, `hs`,
  `se`. Short names are fine for tiny scopes and conventional math (`i`, `x`, `W`).
- Follow PEP 8 (enforced by Ruff): `snake_case` for functions and variables,
  `PascalCase` for classes, `UPPER_SNAKE_CASE` for module-level constants.
- Prefix internal helpers with `_` if they aren't part of the module's interface.
- Booleans read as predicates: `is_trained`, `has_labels`, `use_cache`.

## Comments

- **Comment code you write** wherever the *why* isn't obvious from the code itself.
  Don't restate what the code plainly does.
- Write comments in the **imperative mood**: `# cache embeddings for reuse`, not
  `# this caches the embeddings` or `# caching embeddings`.
- Add **shape comments** for tensors and N-dimensional arrays whenever shapes change:

  ```python
  # (batch, seq_len, hidden)
  hidden_states = encoder(input_ids)
  # (batch, seq_len, 1)
  mask = attention_mask.unsqueeze(-1)
  # (batch, hidden): mean-pool over the sequence, ignoring padding
  pooled = (hidden_states * mask).sum(dim=1) / mask.sum(dim=1)
  ```

- Cite the source when implementing something from a paper (`# Eq. 3 of Smith et al. 2024`).
- Use `# TODO(name): ...` for known gaps, and don't leave commented-out code behind;
  git remembers it.

## Docstrings

Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
for every public module, class, and function (Ruff checks for them in `src/` and
`scripts/`). Types go in the signature, not the docstring.

```python
def generate_training_data(filename: Path, window_size: int) -> list[tuple[str, str]]:
    """Read a raw text file and generate positive skip-gram samples.

    Args:
        filename: file to read; each line is passed to `get_positive_samples`
        window_size: how many tokens before and after the target word to use

    Returns:
        (target word, context word) pairs

    Raises:
        FileNotFoundError: if `filename` does not exist
    """
```

- The first line is a one-line summary in the imperative mood ("Read...", not
  "Reads...").
- Every module starts with a docstring saying what it's for; the package's
  `__init__.py` docstring describes the package as a whole.
- Every script's module docstring includes usage examples.

## Type hints

Type-hint every function signature (enforced by Ruff), and check with ty. Type hints
are documentation that can't go stale, and they catch many bugs before you run
anything.

- Use built-in generics and `|`: `list[float]`, `tuple[int, ...]`, `dict[str, int]`,
  `str | None`. Don't use `typing.List`, `Optional`, or `Union`.
- Accept general types, return specific ones: take `Sequence[str]` or
  `Iterable[str]` (from `collections.abc`) as arguments, return `list[str]`.
- For arrays and tensors: `numpy.typing.NDArray[np.float64]` (or `np.ndarray`) and
  `torch.Tensor`, plus a shape in the docstring or a comment.
- **Don't return long tuples** that callers must unpack positionally
  (`name1, name2, _, _, name5 = method()`) or index into (`result[3]`). Return a
  `dataclass` or `NamedTuple` with named fields instead:

  ```python
  @dataclass
  class EvaluationResult:
      accuracy: float
      loss: float
      predictions: list[int]
  ```

- Use `dataclass`es rather than plain dicts for structured data you pass around.
- Avoid `Any`; if you need it, it's usually a sign of a design that could be clearer.

## Imports

Ruff sorts imports automatically, so you never need to order them by hand. The
resulting order: standard library, then third-party packages, then this project's
package, with a blank line between groups, and within each group `import a` /
`import a as b` before `from a import b`, each alphabetized.

- Import this project's code by its package name (`from my_project.models import
  Encoder`), never by modifying `sys.path` or using relative paths to `src/`.
- Never use wildcard imports (`from x import *`).
- Use standard aliases only: `numpy as np`, `pandas as pd`, `torch.nn as nn`,
  `torch.nn.functional as F`, `matplotlib.pyplot as plt`, `plotnine as p9`.

## Code organization

- **Reusable logic lives in the package (`src/<package>/`).** Scripts in `scripts/`
  should be short: parse the config, call package functions, save results. If you copy
  code from one script to another, move it into the package.
- **No hard-coded experimental settings.** Hyperparameters, file paths, model names,
  and seeds come from the config (see `config/`), so every run is described by its
  config.
- Keep functions short and focused, with no hidden global state. Pass values in as
  arguments instead of reading globals.
- Put script logic in a `main()` function, called under `if __name__ == "__main__":`.
- Use `pathlib.Path` for file paths, not string concatenation or `os.path`.
- Use `logging` in package code, not `print`. Configure logging once, in the script
  (Hydra does this automatically).
- Don't catch exceptions you can't handle. Never write a bare `except:` or
  `except Exception: pass`, which hides bugs and corrupts results silently.
- Prefer clarity to cleverness and premature optimization. Vectorize where it matters
  (inner loops over data), not everywhere.

## Tests

- Put tests in `tests/`, named `test_<module>.py`, and run them with `uv run pytest`.
- Test the package code in `src/`, especially data processing and anything whose
  bugs would silently change results (tokenization, metrics, sampling, masking).
- Tests should be fast and need no GPU, network, or large data. Use tiny synthetic
  inputs.
- When you fix a bug, add a test that would have caught it.

## Notebooks

Use notebooks for exploration and analysis, not as the source of reusable code. See
`notebooks/README.md`. Ruff formats and lints notebooks too.
