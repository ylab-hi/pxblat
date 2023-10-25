"""Sphinx configuration."""
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, Path.resolve(Path("..")).as_posix())


# reference:
# https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#paragraph-level-markup
# https://jbms.github.io/sphinx-immaterial/code_annotations.html#custom-tooltip-width
# https://myst-parser.readthedocs.io/en/latest/syntax/typography.html#syntax-core

project = "PxBLAT"
author = "Yangyang Li"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.extlinks",
    "sphinx_click",
    "myst_parser",
    "sphinx_togglebutton",
    "sphinx_immaterial",
    "sphinxcontrib.bibtex",
    "sphinx_immaterial.apidoc.python.apigen",
]

python_apigen_modules = {
    "pxblat": "api/",
}


python_apigen_default_groups = [
    (".*", "Public members"),
    ("class:.*", "Classes"),
    (r".*\.__(init|new)__", "Constructors"),
    (r".*\.__(str|repr)__", "String representation"),
]


rst_prolog = """
.. role python(code)
   :language: python
   :class: highlight
"""

python_apigen_rst_prolog = """
.. default-role:: py:obj

.. default-literal-role:: python

.. highlight:: python
"""


bibtex_bibfiles = ["refs.bib"]

# Add any paths that contain templates here, relative to this directory.
html_static_path = ["_static"]
templates_path = ["_templates"]
html_css_files = ["extra_css.css", "custom_font_example.css"]
html_title = "PxBLAT"
html_logo = "_static/logo.png"
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.

source_suffix = [".md", ".rst"]
html_theme = "sphinx_immaterial"
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ["_static"]


myst_heading_anchors = 3
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
    "colon_fence",
    "smartquotes",
    "replacements",
    "linkify",
    "strikethrough",
    "substitution",
    "tasklist",
]

intersphinx_mapping = {
    "mypy": ("https://mypy.readthedocs.io/en/stable/", None),
    "python": ("https://docs.python.org/3.9", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
    "biopython": ("https://biopython.org/docs/latest/api", None),
}

# https://jbms.github.io/sphinx-immaterial/customization.html
# https://bylr.info/articles/2022/05/10/api-doc-with-sphinx-autoapi/
# material theme options (see theme.conf for more information)
html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
    },
    "site_url": "https://github.com/cauliyang/pxblat",
    "repo_url": "https://github.com/cauliyang/pxblat",
    "repo_name": "PxBLAT",
    "edit_uri": "blob/main/docs",
    "globaltoc_collapse": True,
    "features": [
        "content.code.annotate",
        # "content.tabs.link",
        # "navigation.expand",
        "navigation.tabs",
        "navigation.tabs.sticky",
        "toc.integrate",
        # "navigation.sections",
        "navigation.instant",
        # "header.autohide",
        "navigation.top",
        "navigation.tracking",
        "search.highlight",
        "search.share",
        "toc.follow",
        "toc.sticky",
        "announce.dismiss",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "deep-purple",
            "accent": "light-blue",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "deep-purple",
            "accent": "lime",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
    ],
    "version_dropdown": False,
    "version_info": [
        {
            "version": "https://pxblat.readthedocs.io/en/latest",
            "title": "ReadTheDocs",
            "aliases": [],
        },
        {
            "version": "https://jbms.github.io/sphinx-immaterial",
            "title": "Github Pages",
            "aliases": [],
        },
    ],
    "toc_title_is_page_title": True,
    # BEGIN: social icons
    "social": [
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/cauliyang/pxblat",
            "name": "Source on github.com",
        },
        {
            "icon": "fontawesome/brands/python",
            "link": "https://pypi.org/project/pxblat/",
        },
    ],
    # END: social icons
}
