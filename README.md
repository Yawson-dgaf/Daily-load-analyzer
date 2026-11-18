# Daily Load Analyzer

A Python project that reads electricity meter records from CSV files, summarizes usage by region, and saves a JSON report.

## What it does

- Reads CSV files from the project folder
- Checks and categorizes records
- Summarizes electricity usage by region
- Identifies high consumption readings
- Writes a report to `data_reports.json`

## Requirements

Python 3. The script uses built-in Python libraries.

## Input data

Place CSV files in the same folder as `daily_load_analyzer.py`. They should contain these columns:

`timestamp`, `meter_id`, `region`, `consumption_kwh`

## Run

```bash
python daily_load_analyzer.py
