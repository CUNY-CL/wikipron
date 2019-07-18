from setuptools import find_packages, setup


__version__ = "0.0.0"


def main():
    setup(
        name="g2p",
        version=__version__,
        description="Scraping Wiktionary data.",
        packages=find_packages(),
        python_requires=">=3.7",
        zip_safe=False,
        install_requires=["requests", "requests-html", "iso639"],
        entry_points={"console_scripts": ["g2p = g2p:main"]},
    )


if __name__ == "__main__":
    main()




