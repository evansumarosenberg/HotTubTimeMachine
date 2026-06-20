# HotTubTimeMachine
## Purpose
A Python abstraction of the Bestway cloud API to control and monitor a Lay-Z-Spa hot tub.

Fuelled by frustration at the limited control offered by the
Bestway API and Android app, the aim is to provide a level
of automation for Bestway / Lay-Z-Spa hot tubs.

In an effort to ensure the widest compatibility,
and easiest deployment, no additional libraries are used -
using only those shipped with Python.

## How to Use
Two main library elements are provided:
* Configuration - manage a JSON file to store key configuration data
* bestway - Package providing the API abstraction itself
Take a look at tub_control.py for more clues as to how this is used

Create a local configuration file from the default template:

```
cp default_configuration.json configuration.json
```

Edit `configuration.json` and set the Bestway app username and password.
The local `configuration.json` file is ignored by git.

The configuration element `gizwits_url` selects the Bestway/Gizwits API
hostname. The default template uses the USA instance:

```
"gizwits_url": "https://usapi.gizwits.com"
```

For EU accounts, set it to:

```
"gizwits_url": "https://euapi.gizwits.com"
```

Discover the device ID for the configured Bestway account and save it to
`configuration.json`:

```
python tub_discover.py --save
```

Check current status:

```
python tub_status.py
```

Basic controls are available through `tub_control.py`.

| Short option | Long option | Values | Description |
| --- | --- | --- | --- |
| `-P` | `--pump` | `on`, `off` | Turn the filter pump on or off. |
| `-H` | `--heat` | `on`, `off` | Turn the heater on or off. |
| `-T` | `--temp` | integer | Set the target water temperature. |
| `-B` | `--bubbles` | `off`, `low`, `high`, `on` | Set Airjet massage. `on` is an alias for `high`. |
| `-S` | `--schedule` | delay duration | Schedule heater start delay and runtime, in minutes. |
| `-c` | `--cfgfile` | path | Use a specific configuration file. |
| `-l` | `--loglevel` | logging level | Set logging verbosity, such as `INFO` or `DEBUG`. |

## History
This project started out as an experiment to talk to the Bestway cloud API from Python.
It has taken inspiration from the Home Automation plugin
for Bestway:
https://github.com/cdpuk/ha-bestway/blob/main/custom_components/bestway/bestway.py

It has grown from a proof-of-concept (which initially could only successfully log in)
and now boasts a state logger: tub_log.py
and tub controls for pump on/off, heat on/off, etc.: tub_control.py

These are designed to be run periodically (e.g. from cron)
to automatically turn the filter pump on and off at set times
or to record a history of tub status: temperature and pump/heat on/off

Recent fixes include first-run token bootstrap, device discovery, correct
handling for explicit off commands, target temperature controls, zero-delay
schedules, and Airjet_V01 massage control using the `wave` datapoint.

## Future Plans
The ambition is to expand the capabilities to include:
* control for turning the heater
on and off according to a configured schedule
* smart heating to automatically turn heater on in good time to
reach a set temperature at a given time
