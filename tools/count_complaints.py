"""
count_complaints – IBM watsonx Orchestrate ADK tool
Returns complaint counts and top-5 issues per company from the bundled CSV.

The CSV file (complaints_clean.csv) must sit in the same directory as this
module so it is packaged correctly when uploaded to Orchestrate.
"""

import csv
import os
from collections import Counter
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

# ---------------------------------------------------------------------------
# Path to the CSV bundled alongside this module
# ---------------------------------------------------------------------------
_CSV_PATH = os.path.join(os.path.dirname(__file__), "complaints_clean.csv")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _load_data(company_filter: Optional[str]) -> dict[str, list]:
    """
    Read complaints_clean.csv and return rows grouped by company.

    If *company_filter* is provided the match is case-insensitive and
    uses a substring search so callers don't need to type the full legal name.
    """
    grouped: dict[str, list] = {}

    with open(_CSV_PATH, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            company = row["Company"].strip()
            if company_filter:
                if company_filter.lower() not in company.lower():
                    continue
            grouped.setdefault(company, []).append(row["Issue"].strip())

    return grouped


def _summarise(company: str, issues: list[str]) -> dict:
    """Build the summary dict for a single company."""
    total = len(issues)
    counter = Counter(issues)
    top5 = counter.most_common(5)

    top_issues = [
        {
            "rank": rank,
            "issue": issue,
            "count": count,
            "percentage": round(count / total * 100, 1),
        }
        for rank, (issue, count) in enumerate(top5, start=1)
    ]

    return {
        "company": company,
        "total_complaints": total,
        "top_5_issues": top_issues,
    }


# ---------------------------------------------------------------------------
# ADK tool
# ---------------------------------------------------------------------------

@tool
def count_complaints(company_name: Optional[str] = None) -> list[dict]:
    """
    Return complaint statistics from the consumer-complaints dataset.

    For every matching company the result contains:
      - company: the exact company name as it appears in the data
      - total_complaints: total number of complaint records
      - top_5_issues: list of the five most-reported issues, each with
          rank, issue text, raw count, and percentage of that company's total

    Args:
        company_name: Optional partial or full company name to filter results
                      (case-insensitive). Omit or pass None to get statistics
                      for every company in the dataset.

    Returns:
        A list of company-level summary dictionaries, one entry per company.
    """
    grouped = _load_data(company_name)

    if not grouped:
        hint = f" matching '{company_name}'" if company_name else ""
        return [{"error": f"No complaints found{hint}. Check the company name and try again."}]

    return [_summarise(company, issues) for company, issues in sorted(grouped.items())]
