#!/usr/bin/env python3
"""Pull BigQuery AppsFlyer campaign data: installs by media source, campaign, country.

Returns a dict ready for unified data.json.
"""

import json
import os
import sys
from collections import defaultdict
from datetime import date, timedelta

from google.cloud import bigquery

PROJECT_ID = "cenoa-marketingdatawarehouse"
DATASET = "marketing_appsflyer"
TABLE_DAILY = f"{PROJECT_ID}.{DATASET}.daily_installs_campaign_tr"


def pull():
    """Pull BigQuery AppsFlyer campaign data. Returns dict for unified data.json."""
    print("  [BigQuery] Connecting...")
    client = bigquery.Client(project=PROJECT_ID)

    # Check date coverage
    cov_q = f"""
    SELECT MIN(date) AS min_date, MAX(date) AS max_date, COUNT(DISTINCT date) AS day_count
    FROM `{TABLE_DAILY}`
    """
    try:
        cov = list(client.query(cov_q))[0]
    except Exception as e:
        print(f"  [BigQuery] ERROR querying {TABLE_DAILY}: {e}", file=sys.stderr)
        return None

    min_date = cov["min_date"]
    max_date = cov["max_date"]

    if not max_date:
        print("  [BigQuery] No data in table")
        return None

    # Last 7 days of available data
    date_end = max_date
    date_start = max(min_date, max_date - timedelta(days=6))
    print(f"  [BigQuery] Pulling {date_start} → {date_end}")

    q = f"""
    SELECT media_source, campaign, SUM(installs) AS installs
    FROM `{TABLE_DAILY}`
    WHERE date BETWEEN @start_date AND @end_date
    GROUP BY 1, 2
    ORDER BY installs DESC
    """
    job = client.query(
        q,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("start_date", "DATE", date_start),
                bigquery.ScalarQueryParameter("end_date", "DATE", date_end),
            ]
        ),
    )
    rows = list(job)

    campaigns = []
    by_media = defaultdict(int)
    total_installs = 0

    for r in rows:
        media = (r.get("media_source") or "(blank)").strip()
        camp = (r.get("campaign") or "(blank)").strip()
        installs = int(r.get("installs") or 0)

        campaigns.append({
            "name": camp,
            "channel": media,
            "installs": installs,
            "country": "TR",  # table is TR-only
            "spend": None,    # cost not in this table
            "cpi": None,
        })
        by_media[media] += installs
        total_installs += installs

    print(f"    {len(campaigns)} campaigns, {total_installs} total installs")

    return {
        "campaigns": campaigns,
        "byMediaSource": dict(by_media),
        "totalInstalls": total_installs,
        "period": {"start": date_start.isoformat(), "end": date_end.isoformat()},
    }


if __name__ == "__main__":
    data = pull()
    if data:
        print(json.dumps(data, indent=2, default=str))
    else:
        print("No data")
