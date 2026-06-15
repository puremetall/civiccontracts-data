"""Aggregate the top recipients for a given NAICS code.

Run:
    python examples/top_recipients.py
"""

from civiccontracts_data import CivicContractsClient


def main() -> None:
    client = CivicContractsClient()
    # 541512 = Computer Systems Design Services
    recipients = client.top_recipients(naics_codes=["541512"], limit=10)

    print("Top recipients for NAICS 541512 (Computer Systems Design Services):\n")
    for rank, item in enumerate(recipients, start=1):
        print(f"  {rank:>2}. ${item['total_amount']:>15,.0f}  {item['recipient_name']}")


if __name__ == "__main__":
    main()
