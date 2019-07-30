from setuptools import find_packages, setup


__version__ = "0.1.0"


def main():
    setup(
        name="g2p",
        version=__version__,
        description="Scraping Wiktionary data.",
        packages=find_packages(),
        python_requires=">=3.6",
        zip_safe=False,
        install_requires=["requests", "requests-html", "iso639"],
        entry_points={"console_scripts": ["g2p = g2p:main"]},
        classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",  
    ],
        
    )


if __name__ == "__main__":
    main()




