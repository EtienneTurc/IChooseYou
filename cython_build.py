import os

import numpy as np
from Cython.Build import cythonize
from setuptools import setup

build_html_file = True if os.environ.get("BUILD_HTML_FILE") else False

setup(
    ext_modules=cythonize(
        "server/service/wheel/cython/create_frame.pyx",
        annotate=build_html_file,
        language_level="3",
    ),
    include_dirs=[np.get_include()],
)
