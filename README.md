# Assist Transcript

A Home Assistant sensor that holds the last question you asked a voice satellite (such as the
Home Assistant Voice Preview Edition) and the answer it gave. Use it to show the conversation on
a dashboard, for example on a wall tablet next to the speaker.

Home Assistant doesn't publish what was said to Assist as events or entities, so there's no
built-in way to show it outside the voice debug page.

> [!WARNING]
> This reads Home Assistant's **internal voice debug log**, the data behind
> **Settings → Voice assistants → ⋮ → Debug**. That isn't a public API, so a Home Assistant
> update could change it and break this integration. If the sensor stops updating after an
> upgrade, check the [issues](https://github.com/theak/ha-assist-transcript/issues). A weekly
> check in this repo runs against the newest Home Assistant release to catch that early.

## What you get

`sensor.assist_last_response`

| | |
|---|---|
| State | The answer, cut to 255 characters (Home Assistant's limit for states) |
| `question` attribute | What you said, as transcribed |
| `answer` attribute | The full answer |
| `satellite` attribute | The `assist_satellite` entity that heard you |
| `time` attribute | When the request started (UTC, ISO 8601) |

It updates when a satellite starts speaking its answer, or goes back to idle after an error.
Questions typed into the Assist dialog aren't included, because they don't come from a satellite.

## Install with HACS

1. HACS → ⋮ → **Custom repositories** → add `https://github.com/theak/ha-assist-transcript`
   with type **Integration**.
2. Download **Assist Transcript** and restart Home Assistant.
3. **Settings → Devices & services → Add integration → Assist Transcript.**

To install by hand instead, copy `custom_components/assist_transcript` into your
`config/custom_components/` folder and continue from step 2.

## Dashboard example

A Markdown card that shows the latest exchange:

```yaml
type: markdown
content: |
  {{ state_attr('sensor.assist_last_response', 'question') }}

  **Assist:** {{ state_attr('sensor.assist_last_response', 'answer') }}
```

To show it only while you're talking to the speaker, add a
[visibility condition](https://www.home-assistant.io/dashboards/cards/#showing-or-hiding-a-card-conditionally)
on the satellite's state, or on a helper your automations turn on and off.

## License

MIT
