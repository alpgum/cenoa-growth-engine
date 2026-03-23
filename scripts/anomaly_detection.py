#!/usr/bin/env python3
"""Anomaly detection for Cenoa weekly KPIs.

Reads data.json, flags KPIs where |deltaPct| exceeds a threshold,
writes anomalies.json and prints a readable summary.

Usage:
    python anomaly_detection.py [--input PATH] [--threshold PCT]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_INPUT = os.path.join(
    os.path.dirname(__file__), "..", "data.json"
)
DEFAULT_OUTPUT = os.path.join(
    os.path.dirname(__file__), "..", "data", "anomalies.json"
)
DEFAULT_THRESHOLD = 20


def classify_severity(abs_delta: float, threshold: float) -> str:
    """Return severity: critical (>40%), warning (threshold-40%), or None."""
    if abs_delta > 40:
        return "critical"
    elif abs_delta >= threshold:
        return "warning"
    return None


def detect_anomalies(data: dict, threshold: float) -> list:
    """Return list of anomaly dicts for KPIs exceeding threshold."""
    anomalies = []
    for kpi, info in data.get("kpis", {}).items():
        delta = info.get("deltaPct", 0)
        abs_delta = abs(delta)
        severity = classify_severity(abs_delta, threshold)
        if severity:
            anomalies.append({
                "kpi": kpi,
                "value": info["value"],
                "prev": info["prev"],
                "deltaPct": delta,
                "severity": severity,
            })
    # Sort: critical first, then by abs delta descending
    order = {"critical": 0, "warning": 1}
    anomalies.sort(key=lambda a: (order[a["severity"]], -abs(a["deltaPct"])))
    return anomalies


def print_summary(anomalies: list, week: str, threshold: float):
    """Print human-readable anomaly summary."""
    if not anomalies:
        print(f"✅ No anomalies detected (threshold: ±{threshold}%)")
        return

    critical = [a for a in anomalies if a["severity"] == "critical"]
    warnings = [a for a in anomalies if a["severity"] == "warning"]

    print(f"⚠️  Anomaly Report — {week}")
    print(f"   Threshold: ±{threshold}%")
    print(f"   Found: {len(critical)} critical, {len(warnings)} warning\n")

    for a in anomalies:
        icon = "🔴" if a["severity"] == "critical" else "🟡"
        direction = "↓" if a["deltaPct"] < 0 else "↑"
        print(
            f"  {icon} {a['kpi']:.<28s} {a['value']:>8} "
            f"(prev {a['prev']:>8})  {direction} {a['deltaPct']:+.1f}%  "
            f"[{a['severity']}]"
        )
    print()


def main():
    parser = argparse.ArgumentParser(description="KPI anomaly detection")
    parser.add_argument(
        "--input", "-i", default=DEFAULT_INPUT, help="Path to data.json"
    )
    parser.add_argument(
        "--output", "-o", default=DEFAULT_OUTPUT, help="Path to anomalies.json"
    )
    parser.add_argument(
        "--threshold", "-t", type=float, default=DEFAULT_THRESHOLD,
        help="Delta %% threshold (default: 20)"
    )
    args = parser.parse_args()

    # Read input
    input_path = os.path.realpath(args.input)
    if not os.path.isfile(input_path):
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path) as f:
        data = json.load(f)

    week = data.get("week", "unknown")
    anomalies = detect_anomalies(data, args.threshold)

    # Build output
    result = {
        "detected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "week": week,
        "threshold": args.threshold,
        "anomalies": anomalies,
    }

    # Write output
    output_path = os.path.realpath(args.output)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    # Print summary
    print_summary(anomalies, week, args.threshold)
    print(f"📁 Written to {output_path}")


if __name__ == "__main__":
    main()
