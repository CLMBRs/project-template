# Useful Packages

Libraries we recommend for CLMBR projects. Add them with `uv add <package>`.

## Numerical computing

- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)

## Machine learning and data science

- [PyTorch](https://pytorch.org/) (see the PyTorch note in
  [project-setup.md](project-setup.md#python-environments-with-uv))
- [scikit-learn](https://scikit-learn.org/)
- [Hugging Face](https://huggingface.co/): `transformers`, `tokenizers`, `datasets`,
  `accelerate`

## Configuration management

- [Hydra](https://hydra.cc/docs/intro/): composes configs from smaller pieces and
  overrides them from the command line. Very useful for hyperparameter sweeps
  (`--multirun`). Built on OmegaConf. The template sets it up by default.
- [OmegaConf](https://omegaconf.readthedocs.io/): for custom string interpolation
  (e.g. in Hydra configs), see
  [resolvers](https://omegaconf.readthedocs.io/en/latest/custom_resolvers.html).

## Data frames

- [pandas](https://pandas.pydata.org/)
- [Polars](https://pola.rs/): faster, with a more consistent API; good for large data.

## Statistics

- [statsmodels](https://www.statsmodels.org/stable/index.html)
- [Or just use R](https://www.r-project.org).

## Visualization

- [plotnine](https://plotnine.readthedocs.io/en/stable/) (recommended): a very
  faithful port of R's [ggplot2](https://ggplot2.tidyverse.org/) (the "grammar of
  graphics"). ggplot2 has a much larger community, so when you want to know how to do
  something, search for ggplot2 answers: examples can almost always be copied into
  plotnine directly.
- [seaborn](https://seaborn.pydata.org/)
- [matplotlib](https://matplotlib.org/): powerful but verbose and fairly painful to
  write by hand. Prefer the options above unless you have very specific or unusual
  plotting needs.
- [patchworklib](https://github.com/ponnhide/patchworklib): for complex figures made
  of many sub-plots, when you need more than plotnine's `facet_wrap`.
