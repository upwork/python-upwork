import upwork
from upwork.routers import messages
from unittest.mock import patch


@patch.object(upwork.Client, "get")
def test_get_rooms(mocked_method):
    """
    Get the rooms.

    Args:
        mocked_method: (todo): write your description
    """
    messages.Api(upwork.Client).get_rooms("company")
    mocked_method.assert_called_with("/messages/v3/company/rooms", {})


@patch.object(upwork.Client, "get")
def test_get_room_details(mocked_method):
    """
    Retrieves the details of a room.

    Args:
        mocked_method: (todo): write your description
    """
    messages.Api(upwork.Client).get_room_details("company", "room_id")
    mocked_method.assert_called_with("/messages/v3/company/rooms/room_id", {})


@patch.object(upwork.Client, "get")
def test_get_room_messages(mocked_method):
    """
    Retrieves room.

    Args:
        mocked_method: (todo): write your description
    """
    messages.Api(upwork.Client).get_room_messages("company", "room_id")
    mocked_method.assert_called_with("/messages/v3/company/rooms/room_id/stories", {})


@patch.object(upwork.Client, "get")
def test_get_room_by_offer(mocked_method):
    """
    Gets the given room.

    Args:
        mocked_method: (todo): write your description
    """
    messages.Api(upwork.Client).get_room_by_offer("company", "offer_id")
    mocked_method.assert_called_with("/messages/v3/company/rooms/offers/offer_id", {})


@patch.object(upwork.Client, "get")
def test_get_room_by_application(mocked_method):
    """
    Get the room exists.

    Args:
        mocked_method: (todo): write your description
    """
    messages.Api(upwork.Client).get_room_by_application("company", "application_id")
    mocked_method.assert_called_with(
        "/messages/v3/company/rooms/applications/application_id", {}
    )


@patch.object(upwork.Client, "get")
def test_get_room_by_contract(mocked_method):
    """
    Test if the room.

    Args:
        mocked_method: (todo): write your description
    """
    messages.Api(upwork.Client).get_room_by_contract("company", "contract_id")
    mocked_method.assert_called_with(
        "/messages/v3/company/rooms/contracts/contract_id", {}
    )


@patch.object(upwork.Client, "post")
def test_create_room(mocked_method):
    """
    Create a new room.

    Args:
        mocked_method: (todo): write your description
    """
    messages.Api(upwork.Client).create_room("company")
    mocked_method.assert_called_with("/messages/v3/company/rooms", {})


@patch.object(upwork.Client, "post")
def test_send_message_to_room(mocked_method):
    """
    Sends a message to a room.

    Args:
        mocked_method: (todo): write your description
    """
    messages.Api(upwork.Client).send_message_to_room("company", "room_id")
    mocked_method.assert_called_with("/messages/v3/company/rooms/room_id/stories", {})


@patch.object(upwork.Client, "post")
def test_send_message_to_rooms(mocked_method):
    """
    Send a message to a rooms. rooms. message.

    Args:
        mocked_method: (todo): write your description
    """
    messages.Api(upwork.Client).send_message_to_rooms("company")
    mocked_method.assert_called_with("/messages/v3/company/stories/batch", {})


@patch.object(upwork.Client, "put")
def test_get_update_room_settings(mocked_method):
    """
    Updates update of the room.

    Args:
        mocked_method: (todo): write your description
    """
    messages.Api(upwork.Client).update_room_settings("company", "room_id", "username")
    mocked_method.assert_called_with(
        "/messages/v3/company/rooms/room_id/users/username", {}
    )


@patch.object(upwork.Client, "put")
def test_get_update_room_metadata(mocked_method):
    """
    Updates the metadata of a room.

    Args:
        mocked_method: (todo): write your description
    """
    messages.Api(upwork.Client).update_room_metadata("company", "room_id")
    mocked_method.assert_called_with("/messages/v3/company/rooms/room_id", {})
