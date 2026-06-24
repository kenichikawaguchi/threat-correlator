#!/bin/bash
# run_nvd_pipeline.sh
# NVD CVEデータの日次取得 + レポート生成パイプライン

set -euo pipefail

REPO_DIR="$HOME/repo/threat-correlator"
VENV="$REPO_DIR/.venv/bin/python"
LOG_DIR="$REPO_DIR/logs"
LOG_FILE="$LOG_DIR/nvd_pipeline_$(date +%Y%m%d).log"

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "=== NVD pipeline start ==="

cd "$REPO_DIR"

# NVD_API_KEY が環境変数になければ .env から読む（任意）
if [ -f "$REPO_DIR/.env" ]; then
    set -a
    # shellcheck source=/dev/null
    source "$REPO_DIR/.env"
    set +a
fi

# ── Step 1: CVE取得 ──────────────────────────────────────────────────────────
log "Fetching CVEs from NVD ..."
if ! "$VENV" nvd_latest_fetch.py >> "$LOG_FILE" 2>&1; then
    log "ERROR: nvd_latest_fetch.py failed (exit $?). Aborting pipeline."
    exit 1
fi

# ── Step 2: レポート生成 ─────────────────────────────────────────────────────
log "Generating CVE report ..."
if ! "$VENV" nvd_report.py >> "$LOG_FILE" 2>&1; then
    log "WARNING: nvd_report.py failed (exit $?). CVEs were fetched but report was not generated."
fi

log "=== NVD pipeline done ==="

# 30日より古いログを削除
find "$LOG_DIR" -name "nvd_pipeline_*.log" -mtime +30 -delete

# 90日より古いレポートを削除
find "$REPO_DIR/reports" -name "nvd_report_*.md" -mtime +90 -delete 2>/dev/null || true

# レポートをGitHubにpush
log "Pushing report to GitHub ..."
git add reports/
if git diff --cached --quiet; then
    log "No new report to commit."
else
    git commit -m "report: NVD $(date +%Y-%m-%d)"
    git push origin main
fi

