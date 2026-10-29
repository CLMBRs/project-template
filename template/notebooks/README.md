# Notebooks

Notebooks are for exploration and analysis, not for reusable code.

- Once code is useful in more than one place, move it into the package in `src/` and
  import it.
- Prefix names with a number or date so they sort in order, e.g.
  `01-explore-data.ipynb`, `2026-10-29-error-analysis.ipynb`.
- Read data from `data/` and results from `outputs/`; don't write results that matter
  only to a notebook. If a figure goes in a paper, generate it with a script.
- Clear large outputs before committing.
