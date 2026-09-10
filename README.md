# RPi_HEMS

Monitors and manages the energy used in a typical household, using a Raspberry
Pi communicating with sensors via off-the-shelf RF modules. It reads household
power draw, stores it as a time series, and switches an appliance off when
demand approaches a peak — a complete sensor-to-actuator loop rather than a
monitoring dashboard.

Final year project, BEng Computer Engineering (DT021A/4), TU Dublin, 2019.

## What it does

```
energy meter ──Modbus TCP──┐
                           ├──→ InfluxDB ──→ Grafana
Z-Wave sensors ──OpenZWave─┘        │
                                    ↓
                            peak detection
                                    ↓
                    Z-Wave smart plug (switch off)
```

**Peak shaving** is the point. The idea is to defer one large load — an
immersion heater, a kettle — off the top of a demand peak, reducing peak draw
without reducing what the household actually uses. The system's job is deciding
when that moment has arrived.

## How it works

**Reading the meter** (`Modbus/esm_read.py`). An energy meter is polled over
Modbus TCP. Its measurements are 32-bit values split across two 16-bit input
registers, so each read fetches a register pair and reassembles it
big-endian, with sign extension for negatives:

```python
response = m_client.read_input_registers(Address, 2)
ReturnValue = ((response.getRegister(0) << 16) + response.getRegister(1))
if (ReturnValue & 0x80000000):    # MSB set, so negative
```

Real power, voltage, energy, apparent power and power factor are read per
channel at documented register addresses (`0x1204`, `0x1200`, `0x120b`, …) and
averaged over a short interval before storage, since instantaneous readings are
too noisy to threshold against.

**Z-Wave devices** (`Misc/zwave_test.py`). The network is brought up through
OpenZWave, which is asynchronous — nodes are interrogated only once the network
reports `STATE_AWAKED`, then `STATE_READY`, each with a 300-second ceiling so a
missing device degrades rather than hangs. Nodes are enumerated by command
class to separate sensors (readable) from switches (actuable); sensor values go
straight to InfluxDB.

**Peak detection** (`Peaks/peak_shave.py`). Developed against real
[EirGrid](https://www.eirgrid.ie/) national demand data — 15-minute actual and
forecast MW readings — before being pointed at live meter readings, so the
algorithm could be validated against a full month of known peaks:

```python
peak_times = peakutils.indexes(demand_needed, thres=0.8, min_dist=10)
peak_avg   = np.mean([demand_needed[j] for j in peak_times])
thresh     = peak_avg - peak_avg / 20      # 95% of the mean peak
```

`min_dist` prevents one broad peak from being counted as several, and the
threshold is set relative to the *mean of the day's peaks* rather than an
absolute MW figure, so it adapts to seasonal load instead of needing
recalibration.

**Storage and display.** InfluxDB holds the readings, with Grafana pointed at
it for dashboards. A `DataFrameClient` reads history back into pandas so
detection can run over a window rather than a single sample. OpenHAB was used
to bring the smart plug onto the network during development (see
`Pics/OpenHAB PHY.png`); the switching logic here talks to OpenZWave directly.

## Stack

Raspberry Pi · Python 3.6 · `pymodbus` · `python-openzwave` · InfluxDB ·
Grafana · OpenHAB · pandas / NumPy / SciPy / PeakUtils · Z-Wave USB controller
on `/dev/ttyACM0`

## Layout

| Path | Contents |
| --- | --- |
| `Modbus/` | Meter polling over Modbus TCP; register decode |
| `ZWave/` | Z-Wave protocol stack notes and diagrams |
| `Peaks/` | Peak detection, plus the EirGrid demand datasets |
| `Misc/` | OpenZWave network control, InfluxDB helpers, scratch tests |
| `Pics/` | Architecture diagrams and result screenshots |

## Status

Complete and archived — this was submitted for assessment in May 2019 and is
not maintained. Some caveats worth naming rather than leaving to be discovered:

- Connection details (broker IP, database name, OpenZWave config path) are
  hardcoded, including an absolute path under the original user's home
  directory. Nothing here is configurable without editing the source.
- A Python virtualenv was committed to the repository, which is why the history
  reports over a million lines changed. The project's own code is a few
  thousand.
- `Misc/` accumulated as a scratch directory; `Peaks/peak_shave.py` and
  `Misc/peak_shave.py` diverged and the one in `Peaks/` is authoritative.
- Peak detection ran against EirGrid *national* demand as a stand-in for
  household demand. The shapes are comparable enough to develop against, but a
  single home's load is far spikier, and the thresholds were never re-tuned on
  real household data.
