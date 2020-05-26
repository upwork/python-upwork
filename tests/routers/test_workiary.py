import upwork
from upwork.routers import workdiary
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_workdiary(mocked_method):
    workdiary.Api(upwork.Client).get_workdiary("company", "date", {})
    mocked_method.assert_called_with("/team/v3/workdiaries/companies/company/date", {})


@patch.object(upwork.Client, "get")
def test_get_by_contract(mocked_method):
    workdiary.Api(upwork.Client).get_by_contract("company", "date", {})
    mocked_method.assert_called_with("/team/v3/workdiaries/contracts/company/date", {})
