import upwork
from upwork.routers import payments
from unittest.mock import patch


@patch.object(upwork.Client, "post")
def test_submit_bonus(mocked_method):
    """
    Submit a submit submit to submit the method will be sent to submit.

    Args:
        mocked_method: (todo): write your description
    """
    payments.Api(upwork.Client).submit_bonus(1234, {"a": "b"})
    mocked_method.assert_called_with("/hr/v2/teams/1234/adjustments", {"a": "b"})
