from upwork import config


def test_config_initialization():
    cfg = config.Config(
        {
            "consumer_key": "keyxxxxxxxxxxxxxxxxxxxx",
            "consumer_secret": "secretxxxxxxxxxx",
            "access_token": "tokenxxxxxxxxxxxxxxxxxxxx",
            "access_token_secret": "tokensecretxxxxx",
        }
    )

    assert cfg.consumer_key == "keyxxxxxxxxxxxxxxxxxxxx"
    assert cfg.consumer_secret == "secretxxxxxxxxxx"
    assert cfg.access_token == "tokenxxxxxxxxxxxxxxxxxxxx"
    assert cfg.access_token_secret == "tokensecretxxxxx"
