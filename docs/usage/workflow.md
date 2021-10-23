# ComPWA Workflow

:::{warning}

`pycompwa` is no longer maintained. Use the
[ComPWA](https://compwa-org.rtfd.io) packages [QRules](https://qrules.rtfd.io),
[AmpForm](https://ampform.rtfd.io), and
[TensorWaves](https://tensorwaves.rtfd.io) instead!

:::

In the following pages, we show how to use ComPWA via the Python interface. We
illustrate this workflow with the decay
$J/\psi \rightarrow \gamma \pi^0 \pi^0$, using the helicity formalism.

Usually, you go through the following four steps to perform your analysis:

```{toctree}
:glob: true
:maxdepth: 2

workflow/*
```

{doc}`Let’s go! <workflow/1_create_model>`

:::{note}

Each of these steps can be downloaded as Jupyter notebooks
[here](https://github.com/ComPWA/pycompwa/tree/main/docs/usage). The notebooks
have been written in such a way that you can rerun each of the steps separately
once you have the output files of the previous steps. As such, these notebooks
can be easily used for your own partial-wave analysis, even if they require
much computation time!

:::
