# civiccontracts-data

> An open-source client for public U.S. **contract award** data — a friendly wrapper
> around the [USAspending](https://api.usaspending.gov/) API, available for both Python and TypeScript.

`civiccontracts-data` makes it easy to pull federal contract awards, search by agency
or NAICS code, and analyze government spending — without wrestling with raw API payloads.
It is maintained by the team behind [Civic AI](https://www.civiccontracts.com),
procurement intelligence for **open solicitations** (what to bid on) and **contract
awards** (competitive intel) across federal, state, and local sources.

- 🐍 **Python** client (`civiccontracts_data`)
- 🟦 **TypeScript / Node** client (`@puremetall/civiccontracts-data`)
- 📊 Built on the free, public [USAspending API](https://api.usaspending.gov/) — no API key required
- 🔎 Search awards by keyword, agency, NAICS, and time period

## Why?

Federal spending data is public and free, but the APIs are verbose and the data model
takes time to learn. This library gives you a small, well-typed surface for the most
common questions:

- "What did this agency spend on, and with whom?"
- "Which awards match this keyword / NAICS code?"
- "Who are the top recipients in my industry?"

If you want a finished product instead of raw award data, try [Civic AI](https://www.civiccontracts.com/explore)
— it unifies **open solicitations** from SAM.gov and state portals with **contract awards**
from USAspending, and lets you search both in plain English.

## Install

### Python

```bash
pip install civiccontracts-data
```

### TypeScript / Node

```bash
npm install @puremetall/civiccontracts-data
```

## Quickstart

### Python

```python
from civiccontracts_data import CivicContractsClient

client = CivicContractsClient()

# Search recent awards by keyword
awards = client.search_awards(keyword="cybersecurity", limit=10)
for award in awards:
    print(award["recipient_name"], award["award_amount"])
```

### TypeScript

```ts
import { CivicContractsClient } from "@puremetall/civiccontracts-data";

const client = new CivicContractsClient();

const awards = await client.searchAwards({ keyword: "cybersecurity", limit: 10 });
for (const award of awards) {
  console.log(award.recipientName, award.awardAmount);
}
```

## Examples

See the [`examples/`](examples) directory:

- [`examples/search_awards.py`](examples/search_awards.py) — keyword search
- [`examples/top_recipients.py`](examples/top_recipients.py) — aggregate top recipients
- [`examples/search_awards.ts`](examples/search_awards.ts) — the same in TypeScript

## Data source & attribution

Data comes from [USAspending.gov](https://www.usaspending.gov/), the official source
of U.S. federal spending data, via its public API. This project is not affiliated with
or endorsed by the U.S. government.

## Learn more

- [How to find government contracts to bid on](https://www.civiccontracts.com/blog/how-to-find-government-contracts)
- [NAICS & PSC codes guide](https://www.civiccontracts.com/blog/naics-and-psc-codes)
- [Top federal agencies by spending](https://www.civiccontracts.com/blog/top-federal-agencies-by-spending)
- [Awesome Government Contracting](https://github.com/puremetall/awesome-government-contracting) — curated resource list

## Contributing

Issues and pull requests are welcome. Please open an issue to discuss substantial changes first.

## License

[MIT](LICENSE) © Civic AI
