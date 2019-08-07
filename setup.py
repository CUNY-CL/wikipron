import os
import setuptools


if getattr(setuptools, "__version__", "0") < "39":
    # v36.4.0+ needed to automatically include README.md in packaging
    # v38.6.0+ needed for long_description_content_type in setup()
    raise EnvironmentError(
        "Your setuptools is too old. "
        "Please run 'pip install --upgrade pip setuptools'."
    )


_THIS_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(_THIS_DIR, "README.md")) as f:
    _LONG_DESCRIPTION = f.read().strip()


__version__ = "0.1.0"


def main():
    setuptools.setup(
        name="wikipron",
        version=__version__,
        description="Scraping Wiktionary data.",
        long_description=_LONG_DESCRIPTION,
        license="Apache 2.0",
        packages=setuptools.find_packages(),
        python_requires=">=3.6",
        zip_safe=False,
        install_requires=["requests", "requests-html", "iso639"],
        entry_points={"console_scripts": ["wikipron = wikipron:main"]},
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Development Status :: 3 - Alpha"
            "Environment :: Console"
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Topic :: Text Processing :: Linguistic",
        ],
    )


if __name__ == "__main__":
    main()
