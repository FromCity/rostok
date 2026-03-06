from pydantic_settings import BaseSettings
from toml_config import NumConfig
from env_config import DatabaseConfig

from pydantic_settings import TomlConfigSettingsSource
from pydantic import Field




class Config(BaseSettings):
    db:  DatabaseConfig = Field(default_factory=DatabaseConfig)
    synonims: NumConfig
    antomyms: NumConfig

    @classmethod
    def load(cls) -> "Config":
        return cls()

    @classmethod
    def settings_customise_sources(cls, settings_cls, **kwargs):
        return (TomlConfigSettingsSource(settings_cls, "settings/config.toml"),)