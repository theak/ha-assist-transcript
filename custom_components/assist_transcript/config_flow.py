"""Config flow for Assist Transcript. There is nothing to configure; it just adds the sensor."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN


class AssistTranscriptConfigFlow(ConfigFlow, domain=DOMAIN):
    """Add the Assist Transcript sensor."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title="Assist Transcript", data={})
        return self.async_show_form(step_id="user")
