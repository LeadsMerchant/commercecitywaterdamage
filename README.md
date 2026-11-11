# commercecitywaterdamage.com

Static pay-per-call referral site (plain HTML/CSS) for GitHub Pages. Same setup as rioranchowaterdamage.com.

## Before going live

1. Get the tracking number and run:
   ```bash
   ./replace_phone.sh "(303) XXX-XXXX" 303XXXXXXX
   ```
2. Point the domain DNS to GitHub Pages (4 A records 185.199.108-111.153, www CNAME -> <user>.github.io).
3. Upload this folder to a public GitHub repo and enable Pages (root). Tick Enforce HTTPS once the cert is issued.
4. Confirm the `CNAME` file still contains `commercecitywaterdamage.com`.

## Honesty rules baked in

- Site is a **referral connection service**, not a contractor.
- Footer disclosure + per-page referral disclosure.
- No address, reviews, licenses, years in business, or guarantees.
- "Call any time" wording is paired with "provider availability varies". Only keep 24/7 wording if the tracking number actually routes 24/7.
- Contact is phone-only (no form).

## Regenerate pages

```bash
python3 _build.py   # uses _sitekit.py (shared templates)
```
Then re-run `replace_phone.sh` (the build restores the {{PHONE}} placeholders).
