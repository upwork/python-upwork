import upwork
from upwork.routers import metadata
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_categories_v2(mocked_method):
    metadata.Api(upwork.Client).get_categories_v2()
    mocked_method.assert_called_with("/profiles/v2/metadata/categories")


@patch.object(upwork.Client, "get")
def test_get_skills(mocked_method):
    metadata.Api(upwork.Client).get_skills()
    mocked_method.assert_called_with("/profiles/v1/metadata/skills")


@patch.object(upwork.Client, "get")
def test_get_skills_v2(mocked_method):
    metadata.Api(upwork.Client).get_skills_v2({"a": "b"})
    mocked_method.assert_called_with("/profiles/v2/metadata/skills", {"a": "b"})


@patch.object(upwork.Client, "get")
def test_get_specialties(mocked_method):
    metadata.Api(upwork.Client).get_specialties()
    mocked_method.assert_called_with("/profiles/v1/metadata/specialties")


@patch.object(upwork.Client, "get")
def test_get_regions(mocked_method):
    metadata.Api(upwork.Client).get_regions()
    mocked_method.assert_called_with("/profiles/v1/metadata/regions")


@patch.object(upwork.Client, "get")
def test_get_tests(mocked_method):
    metadata.Api(upwork.Client).get_tests()
    mocked_method.assert_called_with("/profiles/v1/metadata/tests")


@patch.object(upwork.Client, "get")
def test_get_reasons(mocked_method):
    metadata.Api(upwork.Client).get_reasons({"a": "b"})
    mocked_method.assert_called_with("/profiles/v1/metadata/reasons", {"a": "b"})
