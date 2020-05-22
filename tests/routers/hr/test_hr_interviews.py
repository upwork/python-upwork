import upwork
from upwork.routers.hr import interviews
from unittest.mock import patch


@patch.object(upwork.Client, "post")
def test_invite(mocked_method):
    interviews.Api(upwork.Client).invite("key", {"a": "b"})
    mocked_method.assert_called_with("/hr/v1/jobs/key/candidates", {"a": "b"})
