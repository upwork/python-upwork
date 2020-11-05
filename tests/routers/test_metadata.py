import upwork
from upwork.routers import metadata
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_categories_v2(mocked_method):
    """
    : return : a dict.

    Args:
        mocked_method: (todo): write your description
    """
    metadata.Api(upwork.Client).get_categories_v2()
    mocked_method.assert_called_with("/profiles/v2/metadata/categories")


@patch.object(upwork.Client, "get")
def test_get_skills(mocked_method):
    """
    Get the skills.

    Args:
        mocked_method: (todo): write your description
    """
    metadata.Api(upwork.Client).get_skills()
    mocked_method.assert_called_with("/profiles/v1/metadata/skills")


@patch.object(upwork.Client, "get")
def test_get_skills_v2(mocked_method):
    """
    Retrieve the workflows.

    Args:
        mocked_method: (todo): write your description
    """
    metadata.Api(upwork.Client).get_skills_v2({"a": "b"})
    mocked_method.assert_called_with("/profiles/v2/metadata/skills", {"a": "b"})


@patch.object(upwork.Client, "get")
def test_get_specialties(mocked_method):
    """
    Check if the special special special special special.

    Args:
        mocked_method: (todo): write your description
    """
    metadata.Api(upwork.Client).get_specialties()
    mocked_method.assert_called_with("/profiles/v1/metadata/specialties")


@patch.object(upwork.Client, "get")
def test_get_regions(mocked_method):
    """
    List all regions for the regions.

    Args:
        mocked_method: (todo): write your description
    """
    metadata.Api(upwork.Client).get_regions()
    mocked_method.assert_called_with("/profiles/v1/metadata/regions")


@patch.object(upwork.Client, "get")
def test_get_tests(mocked_method):
    """
    Get test test test.

    Args:
        mocked_method: (todo): write your description
    """
    metadata.Api(upwork.Client).get_tests()
    mocked_method.assert_called_with("/profiles/v1/metadata/tests")


@patch.object(upwork.Client, "get")
def test_get_reasons(mocked_method):
    """
    Gets the test status.

    Args:
        mocked_method: (todo): write your description
    """
    metadata.Api(upwork.Client).get_reasons({"a": "b"})
    mocked_method.assert_called_with("/profiles/v1/metadata/reasons", {"a": "b"})
