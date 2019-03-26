import logging
import os

import pytest

from perp.config import Config


@pytest.fixture
def mock_config_file_path():
    dirname = os.path.dirname(os.path.abspath(__file__))
    relative_path = "assets/mock_configuration.ini"
    file_path = os.path.join(dirname, relative_path)
    return file_path


@pytest.mark.parametrize("section,option,expected", [
    ("database", "user", "db_user"),
    ("database", "port", "db_port"),
    ("other_section", "some_key", "some_value"),
    ("database", "invalid_option", None),
    ("invalid_section", "db_user", None),
])
def test_get_config_option_from_file(
        section,
        option,
        expected,
        mock_config_file_path,
        mocker
):
    def open_side_effect(path, **kwargs):
        if path == "/etc/perp/configuration.ini":
            raise FileNotFoundError
        return mocker.DEFAULT

    expected_config_paths = (
        "/etc/perp/configuration.ini",
        "/usr/local/etc/perp/configuration.ini"
    )
    open_mocker = mocker.patch(
        "builtins.open",
        side_effect=open_side_effect,
        return_value=open(mock_config_file_path)
    )

    config = Config()

    assert open_mocker.call_count == 2
    for expected_path in expected_config_paths:
        open_mocker.assert_any_call(expected_path, encoding=None)

    value = config.get_config_option(section, option)
    assert value == expected


@pytest.mark.parametrize("section,option,expected", [
    ("database", "user", "db_user"),
    ("database", "port", "db_port"),
    ("other_section", "some_key", "some_value"),
])
def test_get_config_option_from_env(
        section,
        option,
        expected,
        mocker,
        caplog
):
    env_override_fmt = f"PERP_{section.upper()}_{option.upper()}"
    os.environ[env_override_fmt] = expected

    mocker.patch(
        "builtins.open", side_effect=FileNotFoundError
    )

    expected_msg = (
        "No configuration file found"
    )
    with caplog.at_level(logging.WARN):
        config = Config()
        assert caplog.records[0].message == expected_msg

    value = config.get_config_option(section, option)
    assert value == expected