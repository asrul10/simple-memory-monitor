# Memory Monitor

A lightweight Python utility that monitors system memory usage and alerts when memory thresholds are exceeded.

## Features

- Monitors system memory usage in real-time
- Alerts when memory usage exceeds configurable thresholds for extended periods
- Detects and reports swap memory usage
- Monitors for OOM (Out Of Memory) kill events
- Logs all events to a log file for later analysis

## Requirements

- Python 3.6+
- psutil library

## Installation

1. Clone this repository or download the script:

```bash
git clone https://github.com/asrul10/simple-memory-monitor.git
cd simple-memory-monitor
```

2. Install the required dependencies:

```bash
pip install psutil
```

## Usage

Run the script with Python:

```bash
python main.py
```

The script will start monitoring your system memory and provide alerts when:
- Memory usage exceeds 80% for 2 minutes or more
- Any swap memory is being used
- OOM kill events are detected

All alerts are displayed in the console and also logged to `memory_monitor.log`.

## Configuration

You can modify the following variables in the `main()` function to adjust monitoring thresholds:

- `high_memory_threshold`: Percentage of memory usage that triggers an alert (default: 80%)
- `high_memory_min_duration`: Minimum duration in seconds that memory must remain high to trigger an alert (default: 120 seconds)

## Log File

The script creates a log file named `memory_monitor.log` in the same directory. This file contains all monitoring events with timestamps.
