# news-image-20261122 — "THE WORLD TODAY"

One image summing up Sunday 22 November 2026's world news, drawn as a
newspaper front page: a lead story, three features, a locator map with
13 numbered dots, and 33 short stories grouped by region (11 Asia &
the Pacific, 11 Europe & the Middle East, 11 Africa & the Americas).
1024×1024 PNG, drawn in code with Pillow — no photographs, no AI
imagery.

## The day's stories

**Lead — The Gulf.** Iran's Revolutionary Guards say they struck two
US bases in Bahrain on Saturday night — Sheikh Isa air base and the
Navy's Juffair facility, home of the Fifth Fleet — as a tanker is hit
off Oman and shipping through the Strait of Hormuz stays under fire.

**Features.** NATO chief Mark Rutte, in Warsaw after Russian missiles
fell in Poland, vows the alliance will defend every inch of Polish
soil; COP31 climate talks in Antalya spill into overtime, deadlocked
over fossil fuels and finance; Trump and Xi meet in Shenzhen at the
APEC summit.

**Asia & the Pacific.** EU–Indonesia trade deal signed after ten
years; Hong Kong votes for its Election Committee; Japanese troops to
train live-fire in India, a first; Cyclone Akvan cancels flights at
Ranchi; Modi opens Nitish Setu in Bihar; India face New Zealand in
Wellington; Cummins keeps the Australia Test captaincy; Australia
edge England in a T20 thriller at the MCG; snow traps 1,500 in
Fukushima; South Korea's $75,000 exam-cheating bounty; India's ICMR
reaches 100 technology transfers.

**Europe & the Middle East.** Estonia to shut its Russia border
crossings for six months; Lviv counts two dead after a Russian
strike; drones hit the Russian cargo ship Sparta II in the Gulf of
Finland; France turns to the UN Security Council over Myanmar's
rejection of the ICJ ruling; UK–EU youth mobility, food trade and
carbon deals; EU floats a 3% levy on big tech; four killed in Gaza
ceasefire breaches; Saudi Arabia shoots down Houthi missiles aimed
at Riyadh; Houthi strikes hit Riyadh; Denmark blames Russia for a
murder plot; Zelensky floats G20 peace talks.

**Africa & the Americas.** A 6.7 earthquake shakes Peru's Andes;
Bolsonaro is taken to intensive care in Brasilia; Mexico seizes
cartel boss 'El Chapo Isidro' as 11 die in Sinaloa; a UN report
finds one in four partnered women cannot refuse sex; England thrash
the All Blacks; US airlines are warned of a terror threat before
Thanksgiving; bed bugs shut FEMA's HQ office; Trump curbs federal
contractors' contact with Congress; a third US aircraft carrier
reaches the Middle East; Hegseth redraws US–Canada defence ties;
Melania Trump seeks more ceasefires before Christmas.

Sources: Reuters, AFP, AP, BBC, Al Jazeera, Euronews, UKMTO and
national wires, as reported on 22 November 2026 (or late on 21
November in the Americas). Figures are as reported; claims that were
not independently verified are labelled as claims in the image.

## How it is built

- `draw_front_page.py` — the generator. Run it to rebuild `entry.png`:
  `python3 draw_front_page.py entry.png`. It is deterministic: two
  runs write byte-identical output.
- `entry.png` — the front page itself.
- `main.ts` — the entrypoint (Node 22, standard library only). It
  copies `entry.png` to `/output/entry.png` (or
  `$MAKEFUN_OUTPUT_DIR` outside the grader). Two runs write the same
  bytes.

## Verification

- PNG loads, exactly 1024×1024, 179,562 bytes (under the 1 MiB cap).
- Generator run twice: byte-identical output.
- `main.ts` run twice: byte-identical `/output/entry.png`.

## License

MIT — see `LICENSE`.
