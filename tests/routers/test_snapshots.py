import upwork
from upwork.routers import snapshots
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_by_contract(mocked_method):
    """
    Test if the contract for the contract exists.

    Args:
        mocked_method: (todo): write your description
    """
    snapshots.Api(upwork.Client).get_by_contract("1234", "1234")
    mocked_method.assert_called_with("/team/v3/snapshots/contracts/1234/1234")


@patch.object(upwork.Client, "put")
def test_update_by_contract(mocked_method):
    """
    Update the contract of the contract

    Args:
        mocked_method: (todo): write your description
    """
    snapshots.Api(upwork.Client).update_by_contract("1234", "1234", {"a": "b"})
    mocked_method.assert_called_with(
        "/team/v3/snapshots/contracts/1234/1234", {"a": "b"}
    )


@patch.object(upwork.Client, "delete")
def test_delete_by_contract(mocked_method):
    """
    Test if contracts by contract.

    Args:
        mocked_method: (todo): write your description
    """
    snapshots.Api(upwork.Client).delete_by_contract("1234", "1234")
    mocked_method.assert_called_with("/team/v3/snapshots/contracts/1234/1234")
