from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

    class Config:
        """Here we create a class `Config` inside of our Pydantic `Settings`
        class, and set the `env_file` to the filename with the dotenv file
        we want to use
        """
        env_file = ".env"


settings = Settings()
