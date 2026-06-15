/**
 * Search recent federal contract awards by keyword (TypeScript).
 *
 * Run with a TS runner, e.g.:
 *   npx tsx examples/search_awards.ts
 */
import { CivicContractsClient } from "../typescript/src/index.js";

async function main(): Promise<void> {
  const client = new CivicContractsClient();
  const awards = await client.searchAwards({ keyword: "cybersecurity", limit: 10 });

  console.log(`Top ${awards.length} cybersecurity awards by amount:\n`);
  for (const award of awards) {
    const amount = award.awardAmount.toLocaleString("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    });
    console.log(`  ${amount}  ${award.recipientName}`);
    console.log(`  ${award.awardingAgency}\n`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
