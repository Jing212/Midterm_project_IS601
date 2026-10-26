import pytest
from decimal import Decimal

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


@pytest.fixture
def env_file(tmp_path):
    file = tmp_path / ".env"

    file.write_text(
        "\n".join([
            f"CALCULATOR_LOG_DIR={tmp_path / 'logs'}",
            f"CALCULATOR_HISTORY_DIR={tmp_path / 'history'}",
            "CALCULATOR_LOG_FILE=test.log",
            "CALCULATOR_HISTORY_FILE=test.csv",
            "CALCULATOR_MAX_HISTORY_SIZE=5",
            "CALCULATOR_AUTO_SAVE=true",
            "CALCULATOR_PRECISION=3",
            "CALCULATOR_MAX_INPUT_VALUE=500",
            "CALCULATOR_DEFAULT_ENCODING=utf-8",
        ]),
        encoding="utf-8",
    )

    return file


def test_load_config(env_file):
    config = CalculatorConfig.from_env(env_file)

    assert config.max_history_size == 5
    assert config.auto_save is True
    assert config.precision == 3
    assert config.max_input_value == Decimal("500")


def test_config_paths(env_file):
    config = CalculatorConfig.from_env(env_file)

    assert config.log_path.name == "test.log"
    assert config.history_path.name == "test.csv"
    assert config.log_path.parent.name == "logs"
    assert config.history_path.parent.name == "history"


def test_invalid_history_size(env_file, monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "abc")

    # Remove the setting from the .env file so the override applies.
    text = env_file.read_text()
    text = text.replace(
        "CALCULATOR_MAX_HISTORY_SIZE=5\n", ""
    )
    env_file.write_text(text)

    with pytest.raises(ConfigurationError):
        CalculatorConfig.from_env(env_file)


def test_invalid_precision(env_file):
    text = env_file.read_text()
    text = text.replace(
        "CALCULATOR_PRECISION=3",
        "CALCULATOR_PRECISION=-1",
    )
    env_file.write_text(text)

    with pytest.raises(ConfigurationError):
        CalculatorConfig.from_env(env_file)


def test_invalid_autosave(env_file):
    text = env_file.read_text()
    text = text.replace(
        "CALCULATOR_AUTO_SAVE=true",
        "CALCULATOR_AUTO_SAVE=maybe",
    )
    env_file.write_text(text)

    with pytest.raises(ConfigurationError):
        CalculatorConfig.from_env(env_file)


def test_invalid_input_limit(env_file):
    text = env_file.read_text()
    text = text.replace(
        "CALCULATOR_MAX_INPUT_VALUE=500",
        "CALCULATOR_MAX_INPUT_VALUE=-10",
    )
    env_file.write_text(text)

    with pytest.raises(ConfigurationError):
        CalculatorConfig.from_env(env_file)

def test_invalid_encoding(env_file):
    text = env_file.read_text()
    text = text.replace(
        "CALCULATOR_DEFAULT_ENCODING=utf-8",
        "CALCULATOR_DEFAULT_ENCODING=invalid-encoding-xyz",
    )
    env_file.write_text(text)

    with pytest.raises(ConfigurationError):
        CalculatorConfig.from_env(env_file)


def test_invalid_log_filename(env_file):
    text = env_file.read_text()
    text = text.replace(
        "CALCULATOR_LOG_FILE=test.log",
        "CALCULATOR_LOG_FILE=../test.log",
    )
    env_file.write_text(text)

    with pytest.raises(ConfigurationError):
        CalculatorConfig.from_env(env_file)


def test_precision_too_large(env_file):
    text = env_file.read_text()
    text = text.replace(
        "CALCULATOR_PRECISION=3",
        "CALCULATOR_PRECISION=100",
    )
    env_file.write_text(text)

    with pytest.raises(ConfigurationError):
        CalculatorConfig.from_env(env_file)