import pytest
from pxblat import find_free_port


def test_find_free_port():
    with pytest.raises(ValueError):
        find_free_port(host="localhost", start=0, end=0)
