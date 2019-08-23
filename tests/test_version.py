import os
import re

import wikipron


_REPO_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def test_version_number_match_with_changelog():
    """__version__ and CHANGELOG.md match for the latest version number."""
    changelog = open(os.path.join(_REPO_DIR, "CHANGELOG.md")).read()
    # latest version number in changelog = the 1st occurrence of '[x.y.z]'
    version_in_changelog = (
        re.search(r"\[\d+\.\d+\.\d+\]", changelog).group().strip("[]")
    )
    assert wikipron.__version__ == version_in_changelog, (
        f"Make sure both __version__ ({wikipron.__version__}) and "
        f"CHANGELOG ({version_in_changelog}) "
        "are updated to match the latest version number"
    )
