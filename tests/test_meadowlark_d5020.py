#!/usr/bin/env python

"""Tests for `meadowlark_d5020` package."""

import pytest


from meadowlark_d5020 import core


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/alba-synchrotron/cookiecutter-albalib')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
