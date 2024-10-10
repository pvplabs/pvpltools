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
