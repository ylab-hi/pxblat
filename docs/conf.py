"""Sphinx configuration."""
from datetime import datetime

from recommonmark.transform import AutoStructify

project = "pxblat"
author = "Yangyang Li"
copyright = f"{datetime.now().year}, {author}"
extensions = [
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
    # "sphinxcontrib_bibtex",
]


# autosummary_generate = True
# autoclass_content = "class"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = "monokailight"

source_suffix = [".rst", ".md"]
autodoc_typehints = "description"
html_theme = "sphinx_material"
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ["_static"]

# html_logo = "_static/logo.png"

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
    "python": ("https://docs.python.org/3.8", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}


# Material theme options (see theme.conf for more information)
html_theme_options = {
    # Set the name of the project to appear in the navigation.
    "nav_title": "PxBLAT",
    # Set you GA account ID to enable tracking
    "google_analytics_account": "UA-XXXXX",
    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    "base_url": "https://github.com/cauliyang/pxblat",
    # Set the color and the accent color
    "color_primary": "purple",
    "color_accent": "light-blue",
    # Set the repo location to get a badge with stats
    "repo_url": "https://github.com/cauliyang/pxblat",
    "repo_name": "PxBLAT",
    # Visible levels of the global TOC; -1 means unlimited
    "globaltoc_depth": 3,
    # If False, expand all TOC entries
    "globaltoc_collapse": False,
    # If True, show hidden TOC entries
    "globaltoc_includehidden": False,
    "html_prettify": True,
    "css_minify": True,
}

html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

html_show_sourcelink = True


def setup(app):
    # app.add_css_file(app, "css/main.css")
    app.add_config_value(
        "recommonmark_config",
        {"enable_math": True, "enable_inline_math": True, "enable_eval_rst": True},
        True,
    )
    app.add_transform(AutoStructify)
    app.add_object_type(
        "confval",
        "confval",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
    )
