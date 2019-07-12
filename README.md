# g2p

`g2p` is a toolkit for working on grapheme-to-phoneme (G2P) mapping.

## Local Development

### Setting Up A Development Environment

1. Create a fork of this repo on GitHub.
2. Make sure you are in some sort of a virtual environment
   (venv, virtualenv, conda, etc).
3. Download and install the library within the virtual environment:

    ```bash
    git clone git@github.com:<your-github-username>/g2p-wiktionary.git
    cd g2p-wiktionary
    pip install --upgrade pip setuptools
    pip install -r requirements.txt
    pip install --no-deps -e .
    ```

### Running Tests

```bash
pytest -vv test_g2p.py
```
