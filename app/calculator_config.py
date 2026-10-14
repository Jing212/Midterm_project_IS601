import codecs
import os
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions import ConfigurationError


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class CalculatorConfig:
    log_dir: Path
    history_dir: Path
    log_file: str
    history_file: str
    max_history_size: int
    auto_save: bool
    precision: int
    max_input_value: Decimal
    default_encoding: str

    @property
    def log_path(self) -> Path:
        return self.log_dir / self.log_file

    @property
    def history_path(self) -> Path:
        return self.history_dir / self.history_file

    @classmethod
    def from_env(cls, env_file=None):
        """Load and validate calculator settings."""

        env_path = (
            Path(env_file)
            if env_file is not None
            else PROJECT_ROOT / ".env"
        )

        load_dotenv(dotenv_path=env_path, override=True)

        def get_int(name, default, minimum=0):
            value = os.getenv(name, str(default))
            try:
                number = int(value)
            except (TypeError, ValueError) as error:
                raise ConfigurationError(
                    f"{name} must be an integer."
                ) from error

            if number < minimum:
                raise ConfigurationError(
                    f"{name} must be at least {minimum}."
                )
            return number

        def get_dir(name, default):
            path = Path(os.getenv(name, default)).expanduser()
            if not path.is_absolute():
                path = PROJECT_ROOT / path
            return path.resolve()

        def get_filename(name, default):
            value = os.getenv(name, default)

            if (
                not value
                or value in (".", "..")
                or Path(value).name != value
                or "/" in value
                or "\\" in value
            ):
                raise ConfigurationError(
                    f"{name} must be a filename, not a path."
                )

            return value

        auto_save_text = os.getenv(
            "CALCULATOR_AUTO_SAVE", "true"
        ).strip().lower()

        if auto_save_text not in ("true", "false"):
            raise ConfigurationError(
                "CALCULATOR_AUTO_SAVE must be true or false."
            )

        try:
            max_input_value = Decimal(
                os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000")
            )
        except InvalidOperation as error:
            raise ConfigurationError(
                "CALCULATOR_MAX_INPUT_VALUE must be numeric."
            ) from error

        if (
            not max_input_value.is_finite()
            or max_input_value <= 0
        ):
            raise ConfigurationError(
                "CALCULATOR_MAX_INPUT_VALUE must be positive and finite."
            )

        encoding = os.getenv(
            "CALCULATOR_DEFAULT_ENCODING", "utf-8"
        )

        try:
            codecs.lookup(encoding)
        except LookupError as error:
            raise ConfigurationError(
                f"Unsupported encoding: {encoding}"
            ) from error

        precision = get_int(
            "CALCULATOR_PRECISION", 4, minimum=0
        )

        if precision > 28:
            raise ConfigurationError(
                "CALCULATOR_PRECISION cannot exceed 28."
            )

        return cls(
            log_dir=get_dir("CALCULATOR_LOG_DIR", "logs"),
            history_dir=get_dir(
                "CALCULATOR_HISTORY_DIR", "history"
            ),
            log_file=get_filename(
                "CALCULATOR_LOG_FILE", "calculator.log"
            ),
            history_file=get_filename(
                "CALCULATOR_HISTORY_FILE",
                "calculator_history.csv"
            ),
            max_history_size=get_int(
                "CALCULATOR_MAX_HISTORY_SIZE",
                100,
                minimum=1,
            ),
            auto_save=(auto_save_text == "true"),
            precision=precision,
            max_input_value=max_input_value,
            default_encoding=encoding,
        )