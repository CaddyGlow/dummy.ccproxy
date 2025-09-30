"""Configuration for the Dummy plugin."""

from pydantic import BaseModel, Field


class DummyConfig(BaseModel):
    """Runtime configuration toggles for dummy."""

    enabled: bool = Field(
        default=True,
        description="Enable the plugin once configured.",
    )
