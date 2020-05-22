import upwork
from upwork.routers.hr import milestones
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_active_milestone(mocked_method):
    milestones.Api(upwork.Client).get_active_milestone("contract")
    mocked_method.assert_called_with(
        "/hr/v3/fp/milestones/statuses/active/contracts/contract"
    )


@patch.object(upwork.Client, "get")
def test_get_submissions(mocked_method):
    milestones.Api(upwork.Client).get_submissions("milestone")
    mocked_method.assert_called_with("/hr/v3/fp/milestones/milestone/submissions")


@patch.object(upwork.Client, "post")
def test_create(mocked_method):
    milestones.Api(upwork.Client).create({"a": "b"})
    mocked_method.assert_called_with("/hr/v3/fp/milestones", {"a": "b"})


@patch.object(upwork.Client, "put")
def test_edit(mocked_method):
    milestones.Api(upwork.Client).edit("milestone", {"a": "b"})
    mocked_method.assert_called_with("/hr/v3/fp/milestones/milestone", {"a": "b"})


@patch.object(upwork.Client, "put")
def test_activate(mocked_method):
    milestones.Api(upwork.Client).activate("milestone", {"a": "b"})
    mocked_method.assert_called_with(
        "/hr/v3/fp/milestones/milestone/activate", {"a": "b"}
    )


@patch.object(upwork.Client, "put")
def test_approve(mocked_method):
    milestones.Api(upwork.Client).approve("milestone", {"a": "b"})
    mocked_method.assert_called_with(
        "/hr/v3/fp/milestones/milestone/approve", {"a": "b"}
    )


@patch.object(upwork.Client, "delete")
def test_delete(mocked_method):
    milestones.Api(upwork.Client).delete("milestone")
    mocked_method.assert_called_with("/hr/v3/fp/milestones/milestone")
