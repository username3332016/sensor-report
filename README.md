# sensor-report

A small command-line tool that analyses sensor measurements (temperature and humidity) stored in a CSV file.
It prints statistics per sensor, detects abnormal values and draws a chart.

The goal of this repository is mainly to show how a modern build tool, **Hatch**, automates the work around a
Python project: dependency management, compilation check, version management and packaging.

## Technologies

| Tool | Role |
|------|------|
| Python >= 3.9 | language |
| [Hatch](https://hatch.pypa.io/) + hatchling | build tool and build backend |
| pandas | read the CSV and compute statistics |
| matplotlib | draw the chart |
| click | command-line interface |

## Prerequisites

* Python 3.9 or newer
* Hatch: `pip install hatch` (or `pipx install hatch`)

Nothing else to install: Hatch creates a virtual environment and installs the dependencies by itself.

## Quick start

```bash
git clone https://github.com/username3332016/sensor-report.git
cd sensor-report
hatch run demo
```

`hatch run demo` creates the environment, installs the dependencies listed in `pyproject.toml`, then runs the
three commands of the tool on `data/sample_readings.csv` (a chart `report.png` is created).

## Build, test and run

| What | Command |
|------|---------|
| Install dependencies + project (done automatically on first `hatch run`) | `hatch env create` |
| Compile all the sources to bytecode (detects syntax errors) | `hatch run compile` |
| Run the tool | `hatch run sensor-report --help` |
| Run the full demo | `hatch run demo` |
| Run automated tests | `hatch run test` |
| Compile and build the packages (sdist + wheel) | `hatch run package` |
| Build only | `hatch build` |

The packages are created in the `dist/` folder, for example `dist/sensor_report-0.1.0-py3-none-any.whl`.

### Tool usage

```bash
# statistics per sensor
hatch run sensor-report summary data/sample_readings.csv

# abnormal measurements (z-score above the threshold, default 3.0)
hatch run sensor-report anomalies data/sample_readings.csv --column temperature --threshold 3

# chart of the daily mean temperature
hatch run sensor-report plot data/sample_readings.csv --output report.png
```

The CSV file must have these columns: `timestamp,sensor_id,temperature,humidity`.
A sample file is given in `data/sample_readings.csv` (it can be regenerated with `python scripts/make_sample_data.py`).

### Test the built wheel

```bash
hatch build
python -m venv /tmp/test-env
/tmp/test-env/bin/pip install dist/*.whl
/tmp/test-env/bin/sensor-report --version
```

## Version management

The version is written in only one place: `src/sensor_report/__about__.py`.
`pyproject.toml` declares `dynamic = ["version"]` and Hatch reads it from this file.

```bash
hatch version          # show the current version
hatch version minor    # 0.1.0 -> 0.2.0
hatch version patch    # 0.2.0 -> 0.2.1
hatch version 1.0.0    # set an exact version
```

The tool also shows it: `hatch run sensor-report --version`.

## Project structure

```
sensor-report/
├── pyproject.toml            # build configuration (metadata, dependencies, Hatch)
├── README.md
├── LICENSE
├── data/sample_readings.csv  # example data
├── scripts/make_sample_data.py
└── src/sensor_report/
    ├── __about__.py          # version number
    ├── __init__.py
    ├── analysis.py           # pandas functions
    ├── plotting.py           # matplotlib chart
    └── cli.py                # click commands
```

## How `pyproject.toml` is organised

* `[build-system]`: tells pip/Hatch to build the project with `hatchling`.
* `[project]`: metadata (name, description, author, license, Python version, keywords), the **dependencies**
  (`pandas`, `matplotlib`, `click`) and the `sensor-report` command (`[project.scripts]`).
* `[tool.hatch.version]`: where the version number is read.
* `[tool.hatch.build.targets.*]`: what goes into the wheel and into the source archive (sdist).
* `[tool.hatch.envs.default.scripts]`: the shortcuts `compile`, `demo` and `package` used above.

## License

MIT, see the `LICENSE` file.
