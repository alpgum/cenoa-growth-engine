#!/bin/bash
set -euo pipefail

# Weekly PDF export for the Cortex dashboard.
#
# Output:
#   projects/cenoa-growth-engine/reports/weekly-YYYY-MM-DD.pdf
#
# Strategy:
#   1) If Puppeteer is installed (optional) -> render + save PDF automatically
#   2) Else if Chrome/Chromium is available -> headless print-to-pdf automatically
#   3) Else -> open in browser and prompt user to Cmd+P -> Save as PDF

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PM_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECTS_DIR="$(cd "$PM_DIR/.." && pwd)"

CORTEX_DIR="${CORTEX_DIR:-$PROJECTS_DIR/cenoa-growth-engine}"
INDEX_HTML="$CORTEX_DIR/index.html"

REPORTS_DIR="$PM_DIR/reports"
DATE_STR="$(date +%Y-%m-%d)"
OUT_PDF="$REPORTS_DIR/weekly-$DATE_STR.pdf"

mkdir -p "$REPORTS_DIR"

if [[ ! -f "$INDEX_HTML" ]]; then
  echo "❌ Could not find: $INDEX_HTML"
  echo "Set CORTEX_DIR to the folder that contains index.html, e.g.:"
  echo "  CORTEX_DIR=~/.openclaw/workspace/projects/cenoa-growth-engine bash scripts/weekly_pdf_export.sh"
  exit 1
fi

FILE_URL="file://$INDEX_HTML"

find_chrome() {
  local candidates=(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Chromium.app/Contents/MacOS/Chromium"
  )

  for c in "${candidates[@]}"; do
    if [[ -x "$c" ]]; then
      echo "$c"
      return 0
    fi
  done

  local cmds=(google-chrome chromium chromium-browser chrome)
  for cmd in "${cmds[@]}"; do
    if command -v "$cmd" >/dev/null 2>&1; then
      command -v "$cmd"
      return 0
    fi
  done

  return 1
}

have_puppeteer() {
  command -v node >/dev/null 2>&1 || return 1
  node -e "require('puppeteer')" >/dev/null 2>&1
}

# 1) Puppeteer (best automation fidelity)
if have_puppeteer; then
  echo "🖨️  Generating PDF via Puppeteer..."

  INDEX_HTML="$INDEX_HTML" OUT_PDF="$OUT_PDF" node <<'NODE'
const fs = require('fs');

(async () => {
  const puppeteer = require('puppeteer');

  const indexHtml = process.env.INDEX_HTML;
  const outPdf = process.env.OUT_PDF;

  if (!indexHtml || !fs.existsSync(indexHtml)) {
    console.error(`Missing INDEX_HTML: ${indexHtml}`);
    process.exit(2);
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  try {
    const page = await browser.newPage();
    await page.goto(`file://${indexHtml}`, { waitUntil: 'networkidle0' });

    // Give charts/widgets a brief moment to render.
    await page.waitForTimeout(750);

    await page.pdf({
      path: outPdf,
      format: 'A4',
      printBackground: true,
      margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' },
    });

    console.log(`✅ Saved: ${outPdf}`);
  } finally {
    await browser.close();
  }
})();
NODE

  exit 0
fi

# 2) Headless Chrome/Chromium (no Puppeteer required)
if CHROME_BIN="$(find_chrome)"; then
  echo "🖨️  Generating PDF via headless Chrome/Chromium..."

  # Note: Chrome writes a temporary PDF and exits; suppress noisy logs.
  if "$CHROME_BIN" \
      --headless \
      --disable-gpu \
      --no-sandbox \
      --print-to-pdf="$OUT_PDF" \
      "$FILE_URL" \
      >/dev/null 2>&1; then
    echo "✅ Saved: $OUT_PDF"
    exit 0
  else
    echo "⚠️  Headless Chrome failed; falling back to manual print." >&2
  fi
fi

# 3) Manual (preferred fallback): open dashboard and use browser print
OPEN_CMD=""
if command -v open >/dev/null 2>&1; then
  OPEN_CMD="open"
elif command -v xdg-open >/dev/null 2>&1; then
  OPEN_CMD="xdg-open"
fi

if [[ -n "$OPEN_CMD" ]]; then
  echo "🌐 Opening dashboard in your default browser..."
  "$OPEN_CMD" "$INDEX_HTML" >/dev/null 2>&1 || true
else
  echo "ℹ️  Could not find an 'open' command. Open this file manually:"
  echo "  $INDEX_HTML"
fi

echo ""
echo "Manual export steps:"
echo "  1) In the browser press Cmd+P (or Ctrl+P)"
echo "  2) Destination: Save as PDF"
echo "  3) Save as: $OUT_PDF"
echo ""
echo "Tip: If you want fully automated export, install Puppeteer (optional) and re-run:"
echo "  npm i puppeteer"
