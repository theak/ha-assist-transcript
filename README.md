# Home Assistant Assist Transcript Sensor

There's annoyingly no built-in way in Home Assistant to show a dashboard card with the last question / answer you asked to your Assistant entity (like a Voice PE), so this custom integration solves that problem by storing the last question you asked + the answer in a sensor that you can render as a card in your dashboard:

<img width="522" height="114" alt="image" src="https://github.com/user-attachments/assets/90a3850a-d295-4b6e-b39f-bd64f672b28b" />


> [!WARNING]
> This reads Home Assistant's **internal voice debug log**, the data behind
> **Settings → Voice assistants → ⋮ → Debug**. That isn't a public API, so a Home Assistant
> update could change it and break this integration, but I've confirmed it works as of version `2026.8.2`.

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
