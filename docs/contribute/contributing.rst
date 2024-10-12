How to contribute
=================

Thanks for considering contributing to the project! We welcome contributions from
everyone. Please read the following guidelines before contributing, and in case
of any questions, don't hesitate to reach out.

.. contents::
   :local:
   :backlinks: none

Reporting issues
----------------

If you find a bug or have a feature request, please open an issue on the
`GitHub issue tracker`_. When reporting a bug, please include a minimal
reproducible example and the OS, Python, and package versions you are using.

.. _GitHub issue tracker:
    https://github.com/pvplabs/pvpltools/issues

Setting up the development environment
--------------------------------------

To set up the development environment, clone the repository and install all the
optional dependencies in editable mode:

.. code-block:: bash

    git clone https://github.com/pvplabs/pvpltools.git
    cd pvpltools

Consider creating a virtual environment before installing the dependencies:

.. code-block:: bash

    python -m venv .venv
    source .venv/bin/activate  # for Linux
    .venv\Scripts\activate  # for Windows

Install the optional dependencies in editable mode:

.. code-block:: bash

    pip install -e .[all]

Code style
----------

Line-length should be limited to 79 characters. In general, try to follow the
`PEP 8`_ style guide.

.. _PEP 8: https://pep8.org/

We use `flake8`_ to enforce the code style. To check the code style, run the
following command from the root of the repository:

.. code-block:: bash

    python -m flake8

.. _flake8: https://flake8.pycqa.org/en/latest/

Testing
-------

We use `pytest`_ for testing. Please make sure that all tests pass before
submitting a pull request.

.. _pytest: https://docs.pytest.org/en/stable/

To run the tests, run the following command from the root of the repository:

.. code-block:: bash

    pytest

Documentation
-------------

We use `Sphinx`_ for documentation with the numpydoc style.

To build the documentation, run the following
command from the root of the repository (``pvpltools/``):

.. code-block:: bash

    cd docs
    make html

The documentation will be built in the ``docs/_build/html`` directory.

.. _Sphinx: https://www.sphinx-doc.org/en/master/

Pull requests and CI/CD workflows
---------------------------------

This project uses GitHub Actions to make sure the previous guidelines are
followed. When you submit a pull request, the CI/CD workflows will run
automatically and check the code style, run the tests, and build the
documentation.

You will be able to see the status of the workflows on the pull request page,
as well to a link to the documentation build.

If the workflows fail, please check the logs and fix the issues.

Repository structure
--------------------

A quick overview, subject to change:

- ``pvpltools/``
    Python package directory containing the code and tests.

    - ``power_conversion.py`` (work in progress)
        - functions related to PV inverters and other power conversion devices

    - ``module_efficiency.py``
        - a collection of models for PV module efficiency (at MPP)
        - includes the new ADR model and others
        - also includes a model fitting function
        - demonstrations in a Jupyter Notebook in examples directory

    - ``iec61853.py``
        - reliable functions for Climate-Specific Energy Rating (CSER) calculations
        - incident angle modifier for direct and diffuse irradiance
        - spectral correction/mismatch factor
        - module operating temperature
        - efficiency matrix interpolation/extrapolation

    - ``dataplusmeta.py``
        - a simple way to pack data and essential meta-data into a single text file

    - ``data/``
        - ``nrel_mpert/``
            - module measurements, model parameters and other data in DataPlusMeta style

    - ``tests/``
        - test files for the functions in the main module, to be run with ``pytest``

    - ``__init__.py``
        - to make the directory a package and publish the submodules' names

- ``examples/``
    - ``data/``
        - data files for the examples
    - other folders
        - with plain Python Jupyter-like Notebooks demonstrating use of the package

- ``docs/``
    - sphinx project files and documentation auxiliary files, this user guide, etc.

- ``.github/``
    - GitHub Actions workflows

- ``ci/``
    - data files for the CI/CD workflows

- ``pyproject.toml``
    - configuration file for the project, including dependencies
