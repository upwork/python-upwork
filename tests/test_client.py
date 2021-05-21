import requests
import unittest
from upwork import config
from upwork import client
from unittest.mock import patch, Mock


class TestClient(unittest.TestCase):
    @patch.object(
        requests,
        "post",
        return_value=Mock(
            status_code=200, content=b"oauth_token=token&oauth_token_secret=secret"
        ),
    )
    def test_get_request_token(self, mocked_post):
        cfg = config.Config(
            {
                "consumer_key": "keyxxxxxxxxxxxxxxxxxxxx",
                "consumer_secret": "secretxxxxxxxxxx",
            }
        )
        cl = client.Client(cfg)
        cl.get_request_token()

        assert cl.request_token == "token"
        assert cl.request_token_secret == "secret"

    @patch.object(requests, "post", side_effect=Exception("error"))
    def test_get_request_token_failed_post(self, mocked_post):
        cfg = config.Config(
            {
                "consumer_key": "keyxxxxxxxxxxxxxxxxxxxx",
                "consumer_secret": "secretxxxxxxxxxx",
            }
        )
        cl = client.Client(cfg)
        with self.assertRaises(Exception):
            cl.get_request_token()

    @patch.object(
        requests,
        "post",
        return_value=Mock(
            status_code=200, content=b"oauth_token=token&oauth_token_secret=secret"
        ),
    )
    def test_get_access_token(self, mocked_post):
        cfg = config.Config(
            {
                "consumer_key": "keyxxxxxxxxxxxxxxxxxxxx",
                "consumer_secret": "secretxxxxxxxxxx",
            }
        )
        cl = client.Client(cfg)
        cl.request_token = "request_token"
        cl.request_token_secret = "request_secret"
        cl.get_access_token("verifier")

        assert cl.config.access_token == "token"
        assert cl.config.access_token_secret == "secret"

    def test_get_access_token_not_ready(self):
        cl = client.Client(object)

        with self.assertRaises(Exception):
            cl.get_access_token("verifier")

    @patch.object(requests, "post", side_effect=Exception("error"))
    def test_get_access_token_failed_post(self, mocked_post):
        cfg = config.Config(
            {
                "consumer_key": "keyxxxxxxxxxxxxxxxxxxxx",
                "consumer_secret": "secretxxxxxxxxxx",
            }
        )
        cl = client.Client(cfg)
        cl.request_token = "request_token"
        cl.request_token_secret = "request_secret"

        with self.assertRaises(Exception):
            cl.get_access_token("verifier")

    @patch.object(
        requests, "get", return_value=Mock(status_code=200, json=lambda: {"a": "b"})
    )
    @patch.object(
        requests, "post", return_value=Mock(status_code=200, json=lambda: {"a": "b"})
    )
    @patch.object(
        requests, "put", return_value=Mock(status_code=200, json=lambda: {"a": "b"})
    )
    @patch.object(
        requests, "delete", return_value=Mock(status_code=200, json=lambda: {"a": "b"})
    )
    def test_send_request(self, mocked_get, mocked_post, mocked_put, mocked_delete):
        cfg = config.Config(
            {
                "consumer_key": "keyxxxxxxxxxxxxxxxxxxxx",
                "consumer_secret": "secretxxxxxxxxxx",
                "access_token": "tokenxxxxxxxxxxxxxxxxxxxx",
                "access_token_secret": "tokensecretxxxxx",
            }
        )
        cl = client.Client(cfg)
        cl.requests = requests
        assert cl.get("/test/uri", {}) == {"a": "b"}
        assert cl.post("/test/uri", {}) == {"a": "b"}
        assert cl.put("/test/uri", {}) == {"a": "b"}
        assert cl.delete("/test/uri", {}) == {"a": "b"}

        with self.assertRaises(ValueError):
            cl.send_request("/test/uri", "method", {})

    def test_get_authorization_url(self):
        cl = client.Client(object)
        cl.request_token = "token"

        assert (
            cl.get_authorization_url("https://callback")
            == "https://www.upwork.com/services/api/auth?oauth_token=token&oauth_callback=https%3A%2F%2Fcallback"
        )
        assert (
            cl.get_authorization_url()
            == "https://www.upwork.com/services/api/auth?oauth_token=token"
        )

    def test_full_url(self):
        assert client.full_url("/test/uri") == "https://www.upwork.com/api/test/uri"
        assert (
            client.full_url("/test/uri", "gds") == "https://www.upwork.com/gds/test/uri"
        )

    def test_get_uri_with_format(self):
        assert client.get_uri_with_format("/test/uri", "api") == "/test/uri.json"
        assert client.get_uri_with_format("/test/uri", "gds") == "/test/uri"
