# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "pvpltools"
copyright = "2024, Anton Driesse"
author = "Anton Driesse"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx_gallery.gen_gallery",
    "sphinx_toggleprompt",
    "sphinx_favicon",
]

templates_path = ["templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# suppress unreferenced footnote warnings
suppress_warnings = ["ref.footnote"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["static"]
html_logo = "static/pvpltools_logo.png"

# -- Options for sphinx-gallery ----------------------------------------------
# https://sphinx-gallery.github.io/stable/configuration.html

sphinx_gallery_conf = {
    "examples_dirs": "../examples",
    "gallery_dirs": "autogen_examples",
    "filename_pattern": r"\.py",
    # directory where function/class granular galleries are stored
    'backreferences_dir': 'api_reference/generated/gallery_backreferences',

    # Modules for which function/class level galleries are created.
    # Tuple of str
    'doc_module': ('pvpltools',),

    # https://sphinx-gallery.github.io/dev/configuration.html#removing-config-comments  # noqa: E501
    'remove_config_comments': True,
}

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "pvlib": ("https://pvlib-python.readthedocs.io/en/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
}

# -- Options for mathjax extension -------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/math.html

mathjax3_config = {
    "chtml": {"displayAlign": "left", "displayIndent": "2em"},
}

# -- Options for pydata-sphinx-theme -----------------------------------------
# https://pydata-sphinx-theme.rtfd.io/en/latest/user_guide/configuring.html

html_theme_options = {
    "github_url": "https://github.com/pvplabs/pvpltools",
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/pvpltools/",
            "icon": "fab fa-python",
        },
    ],
}  # noqa: E501
# -- Options for autodoc/autosummary extensions ------------------------------

autodoc_default_flags = [
    "members",
    "undoc-members",
    "show-inheritance",
    "inherited-members",
]
