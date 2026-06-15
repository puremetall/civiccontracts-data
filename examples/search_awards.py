"""Search recent federal contract awards by keyword.

Run:
    python examples/search_awards.py
"""

from civiccontracts_data import CivicContractsClient


def main() -> None:
    client = CivicContractsClient()
    awards = client.search_awards(keyword="cybersecurity", limit=10)

    print(f"Top {len(awards)} cybersecurity awards by amount:\n")
    for award in awards:
        print(f"  ${award.award_amount:>15,.0f}  {award.recipient_name}")
        print(f"  {' ' * 17}{award.awarding_agency}")
        print()


if __name__ == "__main__":
    main()
