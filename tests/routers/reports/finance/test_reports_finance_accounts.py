import upwork
from upwork.routers.reports.finance import accounts
from unittest.mock import patch


def test_entry_point():
    assert accounts.Gds.entry_point == "gds"


@patch.object(upwork.Client, "get")
def test_get_owned(mocked_method):
    accounts.Gds(upwork.Client).get_owned("freelancer", {"a": "b"})
    mocked_method.assert_called_with(
        "/finreports/v2/financial_account_owner/freelancer", {"a": "b"}
    )


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    accounts.Gds(upwork.Client).get_specific("entity", {"a": "b"})
    mocked_method.assert_called_with(
        "/finreports/v2/financial_accounts/entity", {"a": "b"}
    )
