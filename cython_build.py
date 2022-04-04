import os

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension, setup

build_html_file = True if os.environ.get("BUILD_HTML_FILE") else False

setup(
    ext_modules=cythonize(
        Extension(
            "create_frame",
            ["server/service/wheel/cython/create_frame.pyx"],
            include_dirs=[np.get_include()],
        ),
        annotate=build_html_file,
        language_level="3",
    ),
)
