/**
 * civiccontracts-data — an open client for public U.S. government contract data.
 *
 * Wraps the free, public USAspending API (https://api.usaspending.gov/), which
 * requires no API key. Maintained by Civic AI (https://www.civiccontracts.com).
 */

const USASPENDING_BASE_URL = "https://api.usaspending.gov/api/v2";

/** Award type codes for procurement contracts. */
const CONTRACT_AWARD_TYPES = ["A", "B", "C", "D"];

export interface Award {
  awardId: string;
  recipientName: string;
  awardAmount: number;
  awardingAgency: string;
  description: string;
}

export interface SearchAwardsOptions {
  keyword?: string;
  naicsCodes?: string[];
  timePeriod?: { startDate: string; endDate: string };
  limit?: number;
}

export interface TopRecipient {
  recipientName: string;
  totalAmount: number;
}

export class CivicContractsClient {
  private readonly baseUrl: string;

  constructor(baseUrl: string = USASPENDING_BASE_URL) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  private async post<T>(path: string, payload: unknown): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "User-Agent": "civiccontracts-data",
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const body = await res.text();
      throw new Error(`USAspending API error ${res.status}: ${body}`);
    }
    return (await res.json()) as T;
  }

  /** Search recent federal contract awards. */
  async searchAwards(options: SearchAwardsOptions = {}): Promise<Award[]> {
    const { keyword, naicsCodes, timePeriod, limit = 25 } = options;

    const filters: Record<string, unknown> = {
      award_type_codes: CONTRACT_AWARD_TYPES,
    };
    if (keyword) filters.keywords = [keyword];
    if (naicsCodes?.length) filters.naics_codes = naicsCodes;
    if (timePeriod) {
      filters.time_period = [
        { start_date: timePeriod.startDate, end_date: timePeriod.endDate },
      ];
    }

    const payload = {
      filters,
      fields: [
        "Award ID",
        "Recipient Name",
        "Award Amount",
        "Awarding Agency",
        "Description",
      ],
      sort: "Award Amount",
      order: "desc",
      limit: Math.max(1, Math.min(limit, 100)),
      page: 1,
    };

    const result = await this.post<{ results: Record<string, unknown>[] }>(
      "/search/spending_by_award/",
      payload,
    );

    return (result.results ?? []).map((row) => ({
      awardId: String(row["Award ID"] ?? row["generated_internal_id"] ?? ""),
      recipientName: String(row["Recipient Name"] ?? ""),
      awardAmount: Number(row["Award Amount"] ?? 0),
      awardingAgency: String(row["Awarding Agency"] ?? ""),
      description: String(row["Description"] ?? ""),
    }));
  }

  /** Return the top award recipients for a keyword/NAICS, ranked by amount. */
  async topRecipients(options: SearchAwardsOptions = {}): Promise<TopRecipient[]> {
    const awards = await this.searchAwards({ ...options, limit: 100 });
    const totals = new Map<string, number>();
    for (const award of awards) {
      totals.set(
        award.recipientName,
        (totals.get(award.recipientName) ?? 0) + award.awardAmount,
      );
    }
    const limit = options.limit ?? 10;
    return [...totals.entries()]
      .map(([recipientName, totalAmount]) => ({ recipientName, totalAmount }))
      .sort((a, b) => b.totalAmount - a.totalAmount)
      .slice(0, limit);
  }
}
