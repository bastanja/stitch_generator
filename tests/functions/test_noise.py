import sys

import pytest

from stitch_generator.functions import noise


def test_noise_without_noise_package(monkeypatch):
    # setting the module to None makes importing it raise an ImportError
    monkeypatch.setitem(sys.modules, "noise", None)

    with pytest.raises(ImportError, match=r"stitch_generator\[noise\]"):
        noise()(0.5)
