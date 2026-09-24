# G12 · Current 2026 economy and access check

Desk research/retrieval: **24 September 2026**. Status: **candidate evidence for independent editorial and source review**. These are official observations of monitored prices and reported crop area, **not measured consequences of the June–23 September rainfall departure**. All cached HTML is ignored under `data/candidates/g12_economy/`; keep it out of the public build. No household interview, income loss, yield loss or water-service interruption has been verified here.

## A current, reproducible price example

The Department of Consumer Affairs (DCA) [Price Monitoring Division centrewise report](https://fcainfoweb.nic.in/Reports/DB/ReportCommoditywiseCenterwise.aspx) returns these values when the public form is set to commodity **Onion**, state **Karnataka**, the selected date below, and the row named **Bengaluru** (not “Bengaluru (East Range)” or “Bangalore Rural”):

| Observation date | Bengaluru centre retail onion price | Source response SHA-256 |
| --- | ---: | --- |
| 23 September 2025 | ₹23/kg | `288e0414aed651021fab78f6c4a1c8a4c8da92dafe3020615fbb0894bb7eab09` |
| 16 September 2026 | ₹53/kg | `2778734440afc6b357e60e87e0145bdcee74a0af37ddad137b51deb29a4ce339` |
| 23 September 2026 | ₹57/kg | `72c9fe4a305e34229550a9734cd904e7e33b0bf10388fc127b300e4025e0596f` |

**Check:** ₹57 − ₹23 = **₹34/kg** more than the same calendar date a year earlier; `(57 / 23 − 1) × 100 = 147.8%` from the rounded reported prices. The week-on-week difference is ₹4/kg, or 7.5% from displayed values. The [DCA home page](https://fcainfoweb.nic.in/Default.aspx) labels the national onion retail average as **₹54.27/kg on 23 September 2026**, matching the “All India Average” row in the selected centrewise result; this cross-check supports treating the centre values as **retail ₹/kg** even though the centrewise result itself abbreviates its third column to “Price.” DCA says monitored quality/variety may differ *between* centres but remains the same *for a given centre*; choosing the same named centre avoids a changing national basket as the primary comparison. DCA home snapshot SHA-256: `21a58b6a1d3f17b20536c64c28957c6647002a4bd30953c378de74495cbd64fd`.

**Proposed public wording:** “At the Department of Consumer Affairs' monitored **Bengaluru** centre, the reported retail onion price was **₹57/kg on 23 September 2026**, up from **₹23/kg on the same date in 2025**. The price record shows a marked rise at this centre; it does not identify the cause.” Link the claim to the centrewise form and give the selection settings; a public source card should name both dates, unit, the exact centre and the 24 September retrieval time. A static tiny two-point comparison or three discrete dots is appropriate. Do **not** draw a continuous daily line between these dates or call this a Bengaluru-wide transaction average or a national consumer bill.

**Cautions:** The site does not disclose the sample or transaction volume behind a centre entry. These are official *reported prices* at a named monitoring centre, not a panel of all city shops. The 2025 historical value is what the website returned on 24 September 2026 and may reflect later corrections. DCA's report menu says weekend/holiday data are provisional until the next working day; the three dates above are weekdays. A fourth retrieved value, **₹43/kg on Sunday 23 August 2026**, is retained in the cache (`1cf8542e80d7300f733d8d4f53882404f9810d530dac5147fadf751b203c4870`) but omitted from proposed public copy pending confirmation that the weekend record was finalized. Do not calculate a household cost from a single commodity point without observed quantities.

### How to reproduce without a scraper

1. Open the centrewise DCA form linked above.
2. Enter `23/09/2025`, choose `Onion` and `Karnataka`, submit, and find the row with centre exactly `Bengaluru`: `23`.
3. Repeat for `16/09/2026` and `23/09/2026`: `53` and `57`.
4. Open the DCA home page and verify the current all-India onion **retail** average matches the result's all-India row (it was `54.27` when retrieved). The home page is mutable; this cross-check may no longer work after the reporting day rolls forward.

Automated GET of the DCA retail and wholesale summary endpoints timed out through the browser, Python `requests` and a bounded `curl` attempt. The normal public centrewise form responded to GET and POST; no CAPTCHA or access control was bypassed. Initial form GET SHA-256: `e96a1d91d7f9c0cc1f9a33c39ab9ecf8a16a8c7310089a7d2d360341dbd838c9`. No unattended price updater should be built from the mutable form until its rights, stability, error behaviour and date handling are tested. The downloaded response hashes identify what was inspected, not a licence to republish bulk records.

## Current crop-area context, with a different clock

The Ministry of Agriculture & Farmers Welfare's [CWWG progressive kharif area report as of **4 September 2026**](https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2307791&lang=1&reg=3) was published **8 September 2026 at 14:22 IST**. The report's table uses **lakh hectares** and compares cumulative area sown at the corresponding point in 2025. Retrieved HTML SHA-256: `4251814d278559ea3302f2632efd000954e658fdcf48b6ef1a435067378b126b`.

| Measure | 2026 coverage | Corresponding 2025 coverage | Official difference | Meaning |
| --- | ---: | ---: | ---: | --- |
| Rice | 421.82 lakh ha | 438.19 lakh ha | −16.37 lakh ha | About 3.7% less **area reported sown**, not yield or crop damage. |
| Total pulses | 117.13 lakh ha | 115.30 lakh ha | +1.84 lakh ha | A countervailing increase; the displayed inputs subtract to +1.83 due source rounding. |
| All covered kharif crops | 1,086.31 lakh ha | 1,104.00 lakh ha | −17.69 lakh ha | About 1.6% less reported total area, with offsetting crop changes. |

The official text says the reported rice-area decrease includes Karnataka (−4.28 lakh ha) and Telangana (−3.61 lakh ha), while rice area increased in Assam (+0.52 lakh ha) and Odisha (+0.29 lakh ha). Those are reported *state area differences*, not district locations of failed crops. No state denominator is given in this release for a state percentage. Rice sowing can change with rainfall timing, irrigation, prices, crop choice, reporting and other factors; the document does not attribute the difference to the 2026 rainfall deficit. It also predates the IMD 23 September cut-off by 19 days, so do not overlay these values as if observed simultaneously.

**Proposed public wording:** “The agriculture ministry's 4 September kharif area report showed **16.37 lakh fewer hectares of rice reported sown** than at the corresponding 2025 point, while **pulse area was 1.84 lakh hectares higher**. These are planting-area returns, not harvest losses or evidence of why farmers changed what they planted.” The reported pulse difference should be quoted as the source printed it, with a rounding note in methodology.

## Causal and economic disposition

- The current evidence establishes a **monitored price rise at one Bengaluru centre** and **mixed national crop-area changes** at different dates. It does not connect them to each other or to the IMD rainfall departure. Onions are not rice or pulses; presenting the price and sowing charts side by side needs an explicit “different indicators, no established causal link” caption.
- No current official, matched household water-delivery/coping-cost, employment, wage, crop-condition, final output, or income-loss figure was verified here. Do not say the crop is failing, prices are rising *because of drought*, or millions have lost work. Seek district-level sowing/yield updates, market arrivals and stocks, trade/transport conditions, and local rainfall/irrigation before attribution.
- Counterevidence matters: total pulses coverage grew; rice area increased in Assam and Odisha; a single high onion price does not show all foods rising; water-service or irrigation improvements may offset exposure. The [RBI's 2024 vegetable-price working paper](https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=22723) identifies availability, inputs, rainfall and wages as distinct price drivers in its study period. It is context, not a cause assignment for this monitored 2026 price.
- If published, use an **observed price card** and a **reported sowing-area card** with separate source/observation/retrieval stamps. Each is suitable for a vivid but bounded feature. A chart of losses, future food prices or class-specific economic impact still lacks data.
