import upwork
from upwork.routers.hr import contracts
from unittest.mock import patch


@patch.object(upwork.Client, "put")
def test_suspend_contract(mocked_method):
    """
    Suspend the contract.

    Args:
        mocked_method: (todo): write your description
    """
    contracts.Api(upwork.Client).suspend_contract("reference", {"a": "b"})
    mocked_method.assert_called_with("/hr/v2/contracts/reference/suspend", {"a": "b"})


@patch.object(upwork.Client, "put")
def test_restart_contract(mocked_method):
    """
    Restart contract

    Args:
        mocked_method: (todo): write your description
    """
    contracts.Api(upwork.Client).restart_contract("reference", {"a": "b"})
    mocked_method.assert_called_with("/hr/v2/contracts/reference/restart", {"a": "b"})


@patch.object(upwork.Client, "delete")
def test_end_contract(mocked_method):
    """
    Test for contract.

    Args:
        mocked_method: (todo): write your description
    """
    contracts.Api(upwork.Client).end_contract("reference", {"a": "b"})
    mocked_method.assert_called_with("/hr/v2/contracts/reference", {"a": "b"})
