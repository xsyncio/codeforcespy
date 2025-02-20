from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codeforcespy",
    version="1.0",
    author="Xsyncio",
    description=(
        "A high-performance and type-safe Python library for seamless interaction "
        "with the Codeforces API. Supports both asynchronous and synchronous client "
        "handlers, enabling developers to choose the best approach for their needs."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xscynio/codeforcespy",
    packages=find_packages(include=["pycodeforces", "pycodeforces.*"]),
    include_package_data=True,
    install_requires=[
        "httpx",
        "msgspec",
    ],
    extras_require={
        "dev": [
            "ruff",
            "pytest",
            "mypy",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "python",
        "codeforces",
        "api",
        "wrapper",
        "async",
        "sync",
        "type-safe",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/xscynio/codeforcespy/issues",
        "Documentation": "https://github.com/xscynio/codeforcespy",
        "Source": "https://github.com/xscynio/codeforcespy",
    },
)
