"""Sensor holding the most recent voice satellite question and answer.

HA doesn't put Assist text on the event bus, so when a satellite starts speaking (or goes back
to idle) this reads the newest run for it from the pipeline debug log, the same data the
Settings > Voice assistants > Debug page shows.
"""

from __future__ import annotations

from typing import Any

# Not a public API: this is the store behind Settings > Voice assistants > Debug.
from homeassistant.components.assist_pipeline.pipeline import KEY_ASSIST_PIPELINE
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

MAX_STATE = 255


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the sensor."""
    async_add_entities([AssistTranscriptSensor()])


def _latest_run(hass: HomeAssistant, satellite: str) -> tuple[str, dict[str, Any]] | None:
    """Return (timestamp, event data by type) for the satellite's newest pipeline run."""
    latest = None
    for runs in hass.data[KEY_ASSIST_PIPELINE].pipeline_debug.values():
        for run in runs.values():
            if not run.events or (run.events[0].data or {}).get("satellite_id") != satellite:
                continue
            if latest is None or run.timestamp > latest.timestamp:
                latest = run
    if latest is None:
        return None
    return latest.timestamp, {e.type: e.data or {} for e in latest.events}


class AssistTranscriptSensor(SensorEntity):
    """The last question asked of a voice satellite and what it answered."""

    _attr_name = "Assist last response"
    _attr_unique_id = "assist_transcript_last_response"
    _attr_icon = "mdi:message-reply-text"
    _attr_should_poll = False

    def __init__(self) -> None:
        self._run: str | None = None
        self._attr_extra_state_attributes = {}

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            self.hass.bus.async_listen(
                EVENT_STATE_CHANGED, self._state_changed, event_filter=self._is_satellite_reply
            )
        )

    @callback
    def _is_satellite_reply(self, data: EventStateChangedData) -> bool:
        new = data["new_state"]
        return (
            data["entity_id"].startswith("assist_satellite.")
            and new is not None
            and new.state in ("responding", "idle")
        )

    @callback
    def _state_changed(self, event: Event[EventStateChangedData]) -> None:
        satellite = event.data["entity_id"]
        if (found := _latest_run(self.hass, satellite)) is None:
            return
        timestamp, events = found
        question = events.get("stt-end", {}).get("stt_output", {}).get("text") or events.get(
            "intent-start", {}
        ).get("intent_input")
        answer = (
            events.get("intent-end", {})
            .get("intent_output", {})
            .get("response", {})
            .get("speech", {})
            .get("plain", {})
            .get("speech")
        )
        if not answer and "error" in events:
            answer = events["error"].get("message")
        key = f"{timestamp}|{question}|{answer}"
        if key == self._run or not (question or answer):
            return
        self._run = key
        self._attr_native_value = (answer or "")[:MAX_STATE]
        self._attr_extra_state_attributes = {
            "question": question,
            "answer": answer,
            "satellite": satellite,
            "time": timestamp,
        }
        self.async_write_ha_state()
