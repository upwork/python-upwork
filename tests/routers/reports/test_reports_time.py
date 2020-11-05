import upwork
from upwork.routers.reports import time
from unittest.mock import patch


def test_entry_point():
    """
    !

    Args:
    """
    assert time.Gds.entry_point == "gds"


@patch.object(upwork.Client, "get")
def test_get_by_team_full(mocked_method):
    """
    Get team team team by team

    Args:
        mocked_method: (todo): write your description
    """
    time.Gds(upwork.Client).get_by_team_full("company", "team", {"a": "b"})
    mocked_method.assert_called_with(
        "/timereports/v1/companies/company/teams/team", {"a": "b"}
    )


@patch.object(upwork.Client, "get")
def test_get_by_team_limited(mocked_method):
    """
    Get team team team team by team

    Args:
        mocked_method: (todo): write your description
    """
    time.Gds(upwork.Client).get_by_team_limited("company", "team", {"a": "b"})
    mocked_method.assert_called_with(
        "/timereports/v1/companies/company/teams/team/hours", {"a": "b"}
    )


@patch.object(upwork.Client, "get")
def test_get_by_agency(mocked_method):
    """
    Test for the test methods.

    Args:
        mocked_method: (todo): write your description
    """
    time.Gds(upwork.Client).get_by_agency("company", "agency", {"a": "b"})
    mocked_method.assert_called_with(
        "/timereports/v1/companies/company/agencies/agency", {"a": "b"}
    )


@patch.object(upwork.Client, "get")
def test_get_by_company(mocked_method):
    """
    Get the test_method

    Args:
        mocked_method: (todo): write your description
    """
    time.Gds(upwork.Client).get_by_company("company", {"a": "b"})
    mocked_method.assert_called_with("/timereports/v1/companies/company", {"a": "b"})


@patch.object(upwork.Client, "get")
def test_get_by_freelancer_limited(mocked_method):
    """
    : param freelancer tests.

    Args:
        mocked_method: (todo): write your description
    """
    time.Gds(upwork.Client).get_by_freelancer_limited("freelancer", {"a": "b"})
    mocked_method.assert_called_with(
        "/timereports/v1/providers/freelancer/hours", {"a": "b"}
    )


@patch.object(upwork.Client, "get")
def test_get_by_freelancer_full(mocked_method):
    """
    : param freelancer freelancer frequency.

    Args:
        mocked_method: (todo): write your description
    """
    time.Gds(upwork.Client).get_by_freelancer_full("freelancer", {"a": "b"})
    mocked_method.assert_called_with("/timereports/v1/providers/freelancer", {"a": "b"})
