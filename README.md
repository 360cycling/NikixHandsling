# Nicola Quaye × Handsling — Track Proposal (password-locked)

A single-page, self-contained proposal to **Handsling Bikes** for a **TR3evo endurance track frame**
to back Manx rider **Nicola Quaye**'s move to the track after her 2026 Curlew Cup (National A) win.

## Files
- `index.html` — the **password-locked** page to publish/share. It contains only encrypted content;
  visitors see a passphrase screen and only the correct passphrase decrypts it (client-side). Safe to host publicly.
- `index.src.html` — editable source (relative asset paths). Not published.
- `assets/img/` — source photography.
- `index.plain.html` — the readable build (gitignored). **Never publish this** — it's the unlocked page.

## Rebuild / re-lock
```
python build_standalone.py          # -> index.plain.html (readable, self-contained)
python lock.py "your passphrase"    # -> index.html (locked, deploy this)
```
The passphrase is **not** stored in this repo. Share it with the recipient separately (e.g. in the email).

## Publish (unlisted + locked)
Upload **only `index.html`** to a repo, enable GitHub Pages. `noindex` keeps it out of search;
the passphrase keeps the content private even though the URL is public. Give a random repo name so the URL isn't guessable.

**Photo rights:** race images by **Olly Hassell / SWpix.com**, for proposal review only — license or replace before public/commercial use.
