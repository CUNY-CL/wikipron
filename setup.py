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

with open(os.path.join(_THIS_DIR, "wikipron", "_version.py")) as f:
    # get __version__
    exec(f.read())

with open(os.path.join(_THIS_DIR, "README.md")) as f:
    _LONG_DESCRIPTION = f.read().strip()


def main():
    setuptools.setup(
        name="wikipron",
        version=__version__,  # noqa: F821
        author="Kyle Gorman, Jackson Lee, Elizabeth Garza",
        author_email="kylebgorman@gmail.com",
        description="Scraping grapheme-to-phoneme data from Wiktionary.",
        long_description=_LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url="https://github.com/kylebgorman/wikipron",
        keywords=[
            "computational linguistics",
            "natural language processing",
            "phonology",
            "phonetics",
            "speech",
            "language",
            "Wiktionary",
        ],
        license="Apache 2.0",
        packages=setuptools.find_packages(),
        python_requires=">=3.6",
        zip_safe=False,
        install_requires=["requests", "requests-html", "iso639"],
        entry_points={"console_scripts": ["wikipron = wikipron.cli:main"]},
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Topic :: Text Processing :: Linguistic",
        ],
        data_files=[(".", ["LICENSE.txt"])],
    )


if __name__ == "__main__":
    main()
