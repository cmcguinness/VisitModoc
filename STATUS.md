# Visit Modoc — Status

_Last updated: 2026-11-05_

## Where things stand

The site is live at https://visit-modoc.com (Railway, auto-deploy from `main`, behind Cloudflare).
It's a content site in maintenance mode: the work is keeping listings, events and links accurate,
plus adding content visitors would want. No feature work is in flight.

All work is merged and deployed. There are no open branches, locally, on GitHub or on the iMac.

## Where to look

- **`MAINTENANCE.md`** is the working document:
  - **Backlog:** open items to act on. Review it at the start of every session (see `CLAUDE.md`).
  - **Standing watch list:** questions that wait on an outside condition.
  - **Audit log:** what each refresh pass found and changed.
  - **Two checkouts:** this repo lives on the MacBook Air (`/Volumes/DataT1`) and the Mac mini
    (`/Volumes/DataT2`, over SMB). Pull before working.
- **`CLAUDE.md`:** architecture, content rules (menus, tone, accessibility), session-start steps.

## Open threads (details in MAINTENANCE.md)

1. **Standing watch list:** Valley Farm Store's own site (still "Opening soon") and modocharvest.org
   (still down). California Pines Lodge's site was found and linked 2026-11-05.
2. **Next monthly pass (early December):** confirm the Alturas Winterfest date once the Chamber
   posts it, and re-check the tentative Surprise Valley December dates.
3. **Optional:** the Tule Lake NM map embed on `/places-to-visit` may have a made-up place ID.
   It renders fine; regenerate it from Google Maps (Share → Embed) if it ever misbehaves.

No phone calls: Charles doesn't make them. Decide listings on web evidence and hedge with
"call ahead" wording when it's thin.

## Recent work

- **2026-11-05:** November refresh. Railway `railway.json` removed (Procfile is the only start
  command; the dashboard start command is deliberately empty). Content sweep of about 45 listings,
  winter details, airport facts corrected using Search Console data, and Coffee Adventure, Wild
  Mustard and the Fort Bidwell Hotel added.
- **2026-09-29:** a freshness pass run on the iMac agent (the first real use of `imac-task`), plus
  a follow-up task for Tule Lake NM. The corrections, new content and merge are in the
  MAINTENANCE.md audit log.
- **2026-09-12/13:** September refresh with evergreen event dates, fall events, California Pines
  Lodge, farmers markets checked against the flyer, a WCAG contrast fix and `llms.txt`.

## Working with the iMac agent

`imac-task start <slug> <brief>` hands a task to the iMac (see the `imac` skill). Lessons from
2026-09-29:
- Pull first. The first iMac pass ran on a checkout 8 commits behind and had to be merged by hand.
  `start` now refuses a checkout that is behind its upstream.
- After a task's branch is merged, send code-changing follow-ups as a new task whose brief quotes
  the old RESULT.md. Use `imac-task send` only for questions or review rounds.
- Delete merged `imac/*` branches on GitHub afterwards.
