from dotenv import load_dotenv
from sqlalchemy.future import Engine
from sqlmodel import create_engine
from pydantic import PostgresDsn, SecretStr, EmailStr
from typing import get_type_hints
from utils import parse_bool

import os


class AppConfigError(Exception):
    pass


class AppSettings:
    """Application settings."""

    APP_NAME: str = "Uncanny"
    APP_VERSION: str = "0.1.0"
    SUPPORT_EMAIL: EmailStr = EmailStr("support@uncanny.app")

    DEBUG: bool = True
    ENV: str = "development"
    DB_HOST: str
    DB_USER: str
    DB_PORT: str
    DB_PASSWORD: SecretStr

    engine: Engine

    def __repr__(self):
        return "<AppSettings: {}>".format(self.__dict__)

    def __init__(self, env):
        self.__load_env_variables(env)
        self.__init_db_engine()

    def __load_env_variables(self, env):
        """
        Load, validate and transform environment variables from .env file.
        """
        for field in self.__annotations__:
            # if the value is uppercase, it's an environment variable
            if not field.isupper():
                continue

            # Raise AppConfigError if required field not supplied
            default_value = getattr(self, field, None)
            if default_value is None and field not in env:
                raise AppConfigError(f"Missing environment variable: {field}")

            # Cast env var value to expected type and raise AppConfigError on failure
            variable_type = get_type_hints(AppSettings)[field]

            try:
                if variable_type == bool:
                    value = parse_bool(env.get(field, default_value))
                else:
                    value = variable_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                raise AppConfigError(
                    'Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                        env[field], variable_type, field
                    )
                )

    def __init_db_engine(self):
        """
        Initialize SQLModel engine.
        """
        db_connection_string = PostgresDsn.build(
            scheme="postgresql",
            user=self.DB_USER,
            password=self.DB_PASSWORD.get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
        )
        self.engine = create_engine(db_connection_string, echo=True)


# load the environment variables from .env file
load_dotenv()

# initialize the settings
Config = AppSettings(os.environ)
