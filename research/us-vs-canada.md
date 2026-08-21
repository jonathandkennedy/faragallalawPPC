# US Market vs. Canadian Market — Profitability Analysis

Data: Google Ads/DataForSEO via OpenSEO, pulled August 2026. Volumes = avg
monthly searches; CPCs = top-of-page estimates, **USD in both markets**. Raw
exports: `keywords-us.tsv` (164 terms), `keywords-canada.tsv` (239 terms).

## The structural difference between the two markets

**In the US, bottom-funnel searchers say "lawyer." In Canada, they mostly
don't.** Across every Canadian family/talent visa cluster we pulled (K-1,
marriage, L-1, NIW, green card — 121 terms), **zero** "lawyer/attorney" terms
surfaced. Canada's lawyer-term auction exists almost entirely in one place:
the US-bound business cluster — `e2 visa lawyer` ($61.96, competition 0.88)
and `us immigration lawyer` (880/mo @ $29.70).

Why: people already in the US face deadlines, RFEs, and status expiry — they
hire. Canadians planning a move are researching — except E-2 investors, who
have six figures at stake and hire *before* they move. That's why the tiny
Canadian E-2 lawyer auction carries the highest CPC in either market.

Second trap: most Canadian "immigration lawyer" volume is **inbound to
Canada** (`ircc login` 368k, `spousal sponsorship canada` 8,100, `immigration
lawyer toronto` 3,600 — people hiring Canadian lawyers to enter Canada). None
of it is Faragalla's market. Canadian campaigns must be built exclusively on
US-bound modifiers (us / usa / american / e-2 / tn / green card / k1) with a
heavy negative list.

## Bottom-funnel auction depth (hire-a-lawyer terms)

| Cluster | US vol/mo | US blended CPC | Canada vol/mo | Canada blended CPC |
|---|---|---|---|---|
| E-2 investor | 860 | ~$61 | 90 (+880 shared `us immigration lawyer`) | $61.96 / $29.70 |
| O-1 | 2,040 | ~$71 | — (none) | — |
| EB-2 NIW | 1,870 | ~$51 | — (none) | — |
| K-1 / fiancé(e) | 2,240 | ~$41 | — (none) | — |
| EB-1 | 880 | ~$44 | — (none) | — |
| L-1 | 470 | ~$38 | — (none) | — |
| TN | 710 | ~$30 | — (none) | — |
| Marriage GC | 1,250 | ~$29 | — (none) | — |
| Houston local | ~12,900 | ~$21 | n/a | n/a |
| Citizenship | 7,900 | ~$10 | n/a (inbound-CA trap) | n/a |
| **Total** | **~31,100/mo** | | **~1,110/mo** | |

The US bottom-funnel market is **~28x larger**. Canada's compensating asset is
cheap, thin-competition mid-funnel volume with US-bound intent:

| Canada mid-funnel cluster | Vol/mo | Blended CPC |
|---|---|---|
| E-2 research (`e2 visa` 3,600, requirements, businesses for sale…) | ~5,100 | ~$6 |
| L-1 research (`l1 visa` 2,400, l1a/l1b, requirements…) | ~5,700 | ~$8 |
| TN qualified (`tn visa for canadian citizens` 590, `tn visa to green card` 390…) | ~3,000 | ~$7 |
| US green card research (`us green card` 1,900…) | ~3,800 | ~$6 |
| EB-2 NIW (`eb2 niw` 1,900, `niw green card`…) | ~2,300 | ~$9 |
| K-1 (`k1 visa` 880 + long tail) | ~1,300 | ~$8 |

Equivalent intent costs 3–6x less in Canada than the US lawyer terms — because
US firms don't target Canada and Canadian firms sell inbound-Canada services.

## Per-case economics (modeled)

Assumptions, stated plainly: 10–12% landing page conversion (what this hub is
built for), 20–25% lead→retained for specialty clusters, 15% for volume
clusters. Retainers = typical flat-fee ranges; verify against the firm's
actual pricing.

| Campaign | Blended CPC | Est. cost/lead | Est. cost/case | Typical retainer | Return multiple |
|---|---|---|---|---|---|
| **E-2 — Canada geo** | ~$25–30 (mix of $62 lawyer terms + cheap support) | $210–300 | **$850–1,500** | $8–12k (+ biz plan) | **~7–12x** |
| **TN — Canada geo** | ~$8–12 | $70–120 | $350–600 | $1.5–3k | ~4–6x (fast cases; feeds E-2/GC work) |
| **US NIW** | ~$51 | $425–510 | $2,100–2,600 | $6–10k | ~3–4x |
| **US O-1** | ~$71 | $590–710 | $2,900–3,500 | $6–10k | ~2–3x |
| **US EB-1** | ~$44 | $370–440 | $1,800–2,200 | $10–15k | ~5–7x |
| **US L-1** | ~$38 | $320–385 | $1,600–1,900 | $8–12k | ~5–6x |
| **US E-2** | ~$61 | $510–610 | $2,000–2,400 | $8–12k | ~4–5x |
| US K-1 | ~$41 | $340–410 | $2,200–2,700 | $2.5–4k (+AOS) | ~1.5–2.5x |
| US Marriage GC | ~$29 | $240–290 | $1,600–1,900 | $3.5–5.5k | ~2–3x |
| Houston local | ~$21 | $175–210 | $1,150–1,400 | $3–6k mixed | ~2.5–4x |
| US Citizenship | ~$10 | $80–100 | $550–650 | $1.5–2.5k | ~3x |
| CA K-1/marriage (Canadian-American couples) | ~$8 | $65–80 | $450–550 | $2.5–4k (+AOS) | ~5–7x |

## Verdict

1. **Highest return per dollar: Canada, E-2/TN cluster.** ~7–12x modeled
   return — the best economics in either market, and it's the firm's exact
   specialty. Constraint: volume. Bottom-funnel CA inventory supports roughly
   2–6 signed cases/mo at realistic impression share. Timing is right: CA
   `e2 visa` interest ran ~25–80% above baseline through spring 2026 (peak
   6,600 in April) while US `e2 visa lawyer` volume cooled (480→210/mo).
2. **Largest profit pool: US talent cluster (NIW + EB-1 + O-1, in that
   order of efficiency).** ~4,800 lawyer-term searches/mo at 3–7x modeled
   returns — ~10x the case-volume ceiling of the Canadian E-2 niche. EB-1's
   $44 CPC against $10–15k retainers is quietly the best ratio in the US
   market; O-1 has the most volume but the priciest clicks.
3. **Cheapest qualified growth: Canada mid-funnel + CA K-1.** ~$6–9 CPCs on
   `e2 visa`, `l1 visa`, `tn visa for canadian citizens`, `k1 visa` — use for
   lead-magnet offers and remarketing pools feeding the bottom-funnel pages.
4. **Skip in Canada:** anything without a US-bound modifier, all
   Toronto/Brampton/Mississauga lawyer terms, all citizenship terms — that's
   inbound-Canada demand.

**Recommended starting split (first 60 days):** ~40% Canada (E-2 primary, TN
secondary, `us immigration lawyer` exact), ~50% US talent (NIW + EB-1 first,
O-1 once tracking proves lead quality), ~10% US E-2 mirror (Canadians already
stateside). Reallocate monthly by cost-per-signed-case, not cost-per-lead.
