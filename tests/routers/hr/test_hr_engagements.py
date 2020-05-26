import upwork
from upwork.routers.hr import engagements
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_list(mocked_method):
    engagements.Api(upwork.Client).get_list({"a": "b"})
    mocked_method.assert_called_with("/hr/v2/engagements", {"a": "b"})


@patch.object(upwork.Client, "get")
def test_get_specific(mocked_method):
    engagements.Api(upwork.Client).get_specific("reference")
    mocked_method.assert_called_with("/hr/v2/engagements/reference")
