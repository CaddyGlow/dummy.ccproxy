"""System plugin runtime for auth_lb."""

from __future__ import annotations

from ccproxy.core.logging import get_plugin_logger
from ccproxy.core.plugins import (
    PluginManifest,
    SystemPluginFactory,
    SystemPluginRuntime,
)

from .config import DummyConfig


logger = get_plugin_logger()


class DummyRuntime(SystemPluginRuntime):
    """Runtime implementation for auth_lb."""

    def __init__(self, manifest: PluginManifest) -> None:
        super().__init__(manifest)
        self.config: DummyConfig | None = None

    async def _on_initialize(self) -> None:
        await super()._on_initialize()
        if not self.context:
            raise RuntimeError("Plugin context is not available")

        try:
            self.config = self.context.get(DummyConfig)
        except ValueError:
            self.config = DummyConfig()
            logger.debug(
                "plugin_using_default_config",
                plugin=self.name,
            )

        if not self.config.enabled:
            logger.info("plugin_disabled", plugin=self.name)
            return

        logger.info("plugin_initialized", plugin=self.name)


class DummyFactory(SystemPluginFactory):
    """Factory for the dummp system plugin."""

    def __init__(self) -> None:
        manifest = PluginManifest(
            name="dummy",
            version="0.1.0",
            description="Custom CCProxy plugin.",
            is_provider=False,
            config_class=DummyConfig,
        )
        super().__init__(manifest)

    def create_runtime(self) -> DummyRuntime:
        return DummyRuntime(self.manifest)


factory = DummyFactory()
