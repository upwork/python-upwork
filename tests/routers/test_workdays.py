import upwork
from upwork.routers import workdays
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_by_company(mocked_method):
    """
    Gets the test for a particular test method.

    Args:
        mocked_method: (todo): write your description
    """
    workdays.Api(upwork.Client).get_by_company("company", "from", "till", {})
    mocked_method.assert_called_with(
        "/team/v3/workdays/companies/company/from,till", {}
    )


@patch.object(upwork.Client, "get")
def test_get_by_contract(mocked_method):
    """
    Get the test for a contract.

    Args:
        mocked_method: (todo): write your description
    """
    workdays.Api(upwork.Client).get_by_contract("company", "from", "till", {})
    mocked_method.assert_called_with(
        "/team/v3/workdays/contracts/company/from,till", {}
    )
