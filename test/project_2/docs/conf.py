"""Configuration file for the Sphinx documentation builder"""
import datetime
import os
import sys

# Set the correct path for building
sys.path.insert(0, os.path.abspath(".."))

# Figure out the current year
current_year = datetime.datetime.now().year

# -- Project information -----------------------------------------------------

project = "Project 2"
copyright = f"{current_year}, F.Sherratt"
author = "F.Sherratt"

# -- General configuration ---------------------------------------------------

# Add a nicer theme, process code and markdown parsing
extensions = [
    "sphinx_rtd_theme",
]
templates_path = ["_templates"]

# So we can include markdown files, especially the README
source_suffix = [".rst", ".md"]

# -- Options for HTML output -------------------------------------------------

# Set the theme
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
}
