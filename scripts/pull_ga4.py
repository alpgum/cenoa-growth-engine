#!/usr/bin/env python3
"""Pull GA4 traffic data: sessions, users, traffic source, country.

Returns a dict ready for unified data.json.
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    OrderBy,
    RunReportRequest,
)
from google.oauth2 import service_account

DEFAULT_CREDENTIALS = os.path.expanduser(
    "~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json"
)


def _get_client(creds_path=None):
    creds_path = creds_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", DEFAULT_CREDENTIALS)
    scopes = ["https://www.googleapis.com/auth/analytics.readonly"]
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
    return BetaAnalyticsDataClient(credentials=creds)


def _parse_value(v):
    if v is None:
        return None
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    try:
        return float(v)
    except ValueError:
        return v


def _run_report(client, property_id, dims, mets, start_date, end_date, limit=50, order_by_metric=None):
    order_bys = []
    if order_by_metric:
        order_bys = [OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_by_metric), desc=True)]

    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=d) for d in dims],
        metrics=[Metric(name=m) for m in mets],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        limit=limit,
        order_bys=order_bys,
    )
    resp = client.run_report(req)

    rows = []
    for row in resp.rows:
        d = {}
        for i, dn in enumerate(dims):
            d[dn] = row.dimension_values[i].value
        for j, mn in enumerate(mets):
            d[mn] = _parse_value(row.metric_values[j].value)
        rows.append(d)
    return rows


def _iso_week_range():
    today = datetime.utcnow().date()
    last_sunday = today - timedelta(days=today.weekday() + 1)
    last_monday = last_sunday - timedelta(days=6)
    return last_monday.isoformat(), last_sunday.isoformat()


def pull(property_id=None, creds_path=None):
    """Pull GA4 traffic data. Returns dict for unified data.json."""
    property_id = property_id or os.environ.get("GA4_PROPERTY_ID")
    if not property_id:
        print("  [GA4] SKIPPED — GA4_PROPERTY_ID not set")
        return None

    client = _get_client(creds_path)
    start, end = _iso_week_range()
    print(f"  [GA4] Pulling {start} → {end}")

    # 1) Totals
    print("    sessions + users...", flush=True)
    totals_rows = _run_report(client, property_id, [], ["sessions", "totalUsers"], start, end)
    sessions = totals_rows[0]["sessions"] if totals_rows else 0
    users = totals_rows[0]["totalUsers"] if totals_rows else 0

    # 2) By source/medium
    print("    by source/medium...", flush=True)
    by_source = _run_report(
        client, property_id,
        ["sessionSourceMedium"],
        ["sessions", "totalUsers", "engagementRate"],
        start, end, limit=20, order_by_metric="sessions",
    )

    # 3) By country
    print("    by country...", flush=True)
    by_country = _run_report(
        client, property_id,
        ["country"],
        ["sessions", "totalUsers"],
        start, end, limit=20, order_by_metric="sessions",
    )

    return {
        "sessions": sessions,
        "users": users,
        "bySource": by_source,
        "byCountry": by_country,
        "period": {"start": start, "end": end},
    }


if __name__ == "__main__":
    data = pull()
    if data:
        print(json.dumps(data, indent=2, default=str))
    else:
        print("No data (GA4_PROPERTY_ID not set)")
