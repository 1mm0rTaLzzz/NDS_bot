from environs import Env
from dataclasses import dataclass


# Dataclass for bot settings
@dataclass
class Bots:
    bot_token: str
    admin_id: int


# Dataclass for all settings
@dataclass
class Settings:
    bots: Bots


# Function to get settings from environment variables
def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id="7726136736"
        )
    )


# Get settings from the specified file
settings = get_settings('input')
print(settings)
