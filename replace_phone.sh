#!/usr/bin/env bash
# Replace {{PHONE}} / {{PHONE_TEL}} placeholders across the site.
# Usage:
#   ./replace_phone.sh "(303) 555-1234"
#   ./replace_phone.sh "(303) 555-1234" "3035551234"
# If only one argument is given, digits are extracted for the tel: link.
set -euo pipefail
cd "$(dirname "$0")"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"(303) 555-1234\" [tel_digits]"
  echo "Example: $0 \"(303) 555-1234\" 3035551234"
  exit 1
fi

DISPLAY_NUM="$1"
if [[ $# -ge 2 ]]; then
  TEL_NUM="$2"
else
  TEL_NUM="$(echo "$DISPLAY_NUM" | tr -cd '0-9+')"
fi

if [[ -z "$TEL_NUM" ]]; then
  echo "Could not derive tel digits from: $DISPLAY_NUM"
  exit 1
fi

echo "Setting display phone to: $DISPLAY_NUM"
echo "Setting tel: href digits to: $TEL_NUM"

# Portable in-place replace across html (and any leftover in sh docs)
find . -type f \( -name '*.html' \) -print0 | while IFS= read -r -d '' f; do
  # Use python for reliable literal replace
  DISPLAY_NUM="$DISPLAY_NUM" TEL_NUM="$TEL_NUM" FILE="$f" python3 - <<'PY'
import os
from pathlib import Path
p = Path(os.environ["FILE"])
text = p.read_text(encoding="utf-8")
text2 = text.replace("{{PHONE}}", os.environ["DISPLAY_NUM"]).replace("{{PHONE_TEL}}", os.environ["TEL_NUM"])
if text2 != text:
    p.write_text(text2, encoding="utf-8")
    print(f"  updated {p}")
PY
done

echo "Done. Spot-check index.html for the new number."
