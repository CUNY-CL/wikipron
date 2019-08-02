import os
from setuptools import find_packages, setup


<<<<<<< HEAD
_THIS_DIR = os.path.dirname(os.path.realpath('README.md'))

with open(os.path.join(_THIS_DIR, 'README.md')) as f:
    _LONG_DESCRIPTION = f.read().strip()


=======
>>>>>>> 94b1b52f6df76633e6dcdc06ce340d6cf9630a2e
__version__ = "0.1.0"


def main():
    setup(
        name="wikipron",
        version=__version__,
        description="Scraping Wiktionary data.",
        long_description=_LONG_DESCRIPTION,
        license='Apache 2.0',
        packages=find_packages(),
        python_requires=">=3.6",
        zip_safe=False,
        install_requires=["requests", "requests-html", "iso639"],
<<<<<<< HEAD
        entry_points={"console_scripts": ["wikipron = wikipron:main"]},
        classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha"
        "Environment :: Console"
=======
        entry_points={"console_scripts": ["g2p = g2p:main"]},
        classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
>>>>>>> 94b1b52f6df76633e6dcdc06ce340d6cf9630a2e
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",  
    ],
        
    )


if __name__ == "__main__":
    main()
