"""A small client for the public USAspending API.

The USAspending API (https://api.usaspending.gov/) is free and requires no API key.
This module wraps the handful of endpoints most useful for exploring federal
contract awards and exposes them as simple Python dictionaries.
"""

from __future__ import annotations

import urllib.error
import urllib.request
import json
from dataclasses import dataclass
from typing import Any, Iterable

USASPENDING_BASE_URL = "https://api.usaspending.gov/api/v2"

# Award type codes for procurement contracts (A=BPA call, B=Purchase order,
# C=Delivery order, D=Definitive contract).
CONTRACT_AWARD_TYPES = ["A", "B", "C", "D"]


@dataclass
class Award:
    """A normalized federal contract award."""

    award_id: str
    recipient_name: str
    award_amount: float
    awarding_agency: str
    description: str

    @classmethod
    def from_api(cls, row: dict[str, Any]) -> "Award":
        return cls(
            award_id=str(row.get("Award ID", "") or row.get("generated_internal_id", "")),
            recipient_name=str(row.get("Recipient Name", "")),
            award_amount=float(row.get("Award Amount", 0) or 0),
            awarding_agency=str(row.get("Awarding Agency", "")),
            description=str(row.get("Description", "") or ""),
        )


class CivicContractsClient:
    """Client for public federal contract data.

    Example:
        >>> client = CivicContractsClient()
        >>> awards = client.search_awards(keyword="cybersecurity", limit=5)
        >>> awards[0].recipient_name  # doctest: +SKIP
    """

    def __init__(self, base_url: str = USASPENDING_BASE_URL, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "civiccontracts-data"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:  # pragma: no cover - network dependent
            body = exc.read().decode("utf-8", "replace")
            raise RuntimeError(f"USAspending API error {exc.code}: {body}") from exc

    def search_awards(
        self,
        keyword: str | None = None,
        naics_codes: Iterable[str] | None = None,
        time_period: tuple[str, str] | None = None,
        limit: int = 25,
    ) -> list[Award]:
        """Search recent federal contract awards.

        Args:
            keyword: Free-text keyword to match.
            naics_codes: Optional iterable of NAICS codes to filter by.
            time_period: Optional (start_date, end_date) as YYYY-MM-DD strings.
            limit: Max number of awards to return (1-100).
        """
        filters: dict[str, Any] = {"award_type_codes": CONTRACT_AWARD_TYPES}
        if keyword:
            filters["keywords"] = [keyword]
        if naics_codes:
            filters["naics_codes"] = list(naics_codes)
        if time_period:
            start, end = time_period
            filters["time_period"] = [{"start_date": start, "end_date": end}]

        payload = {
            "filters": filters,
            "fields": [
                "Award ID",
                "Recipient Name",
                "Award Amount",
                "Awarding Agency",
                "Description",
            ],
            "sort": "Award Amount",
            "order": "desc",
            "limit": max(1, min(limit, 100)),
            "page": 1,
        }
        result = self._post("/search/spending_by_award/", payload)
        return [Award.from_api(row) for row in result.get("results", [])]

    def top_recipients(
        self,
        keyword: str | None = None,
        naics_codes: Iterable[str] | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Return the top award recipients for a keyword/NAICS, ranked by amount."""
        awards = self.search_awards(keyword=keyword, naics_codes=naics_codes, limit=100)
        totals: dict[str, float] = {}
        for award in awards:
            totals[award.recipient_name] = totals.get(award.recipient_name, 0.0) + award.award_amount
        ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
        return [{"recipient_name": name, "total_amount": amount} for name, amount in ranked[:limit]]
