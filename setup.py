import os
from setuptools import find_packages, setup


_PACKAGE_NAME = "g2p"
_THIS_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(_THIS_DIR, _PACKAGE_NAME, "__init__.py")) as f:
    # get __version__ and __doc__
    exec(f.read())


def main():
    setup(
        name=_PACKAGE_NAME,
        version=__version__,
        description=__doc__,
        packages=find_packages(),
        python_requires=">=3.7",
        zip_safe=False,
        install_requires=["click", "numpy", "requests", "requests-html"],
        entry_points={"console_scripts": ["g2p = g2p.__main__:cli"]},
    )


if __name__ == "__main__":
    main()
