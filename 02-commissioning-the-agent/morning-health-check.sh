#!/usr/bin/env bash
# morning-health-check.sh - TEMPLATE for a script-only (no-agent) daily health check.
#
# Part of "Guide for building an autonomous agentic system administrator", part 2.
# Licensed under CC BY 4.0. Adapted from working documents developed by
# Steve Waddington and Maxi Calder, his sysadmin agent.
#
# This is a generalised starting point, not a turnkey script. It has been
# syntax-checked and dry-run with placeholder targets only. Customise it with
# your agent for your own systems, then run it by hand until you have
# received a correct report.
#
# Behaviour:
#   - checks websites, local services and (optionally) one remote host;
#   - restarts only services named in the allow-lists below;
#   - emails a report every run ("Everything is OK." or "Everything is OK, except:");
#   - prints to stdout ONLY when something serious remains. With a Hermes
#     --no-agent job, stdout is delivered to the job's --deliver target
#     (your urgent channel) and empty stdout is a silent run.
#
# Set DRY_RUN=1 to print the report instead of sending it.

set -uo pipefail

# ---- Configuration: replace these ---------------------------------------
SITES=("https://example.com" "https://www.example.com")
LOCAL_USER_SERVICES=()                 # e.g. ("hermes-gateway") - systemctl --user units
LOCAL_RESTART_ALLOWED=()               # subset of the above the script may restart
REMOTE_HOST=""                         # e.g. "agent@web1" - always user@host
REMOTE_SERVICES=()                     # e.g. ("apache2" "postfix" "dovecot")
REMOTE_RESTART_ALLOWED=()              # subset of the above the script may restart
REPORT_TO="you@example.com"
REPORT_FROM="agent@example.com"
REPORT_SUBJECT="Server Report"
SEND_CMD=(sendmail -t)                 # any command that reads a full message on stdin
DRY_RUN="${DRY_RUN:-0}"
# -------------------------------------------------------------------------

ISSUES=()     # unresolved problems
FIXES=()      # repairs made and verified
SERIOUS=0

issue()   { ISSUES+=("$2"); [ "$1" = "SERIOUS" ] && SERIOUS=$((SERIOUS + 1)); return 0; }
fixed()   { FIXES+=("$1"); }
allowed() { local item="$1"; shift; local a; for a in "$@"; do [ "$a" = "$item" ] && return 0; done; return 1; }

# Share one SSH connection for every remote check. A firewall that rate-limits
# SSH will otherwise block later checks, and a blocked check looks like a
# stopped service.
remote() {
  ssh -o BatchMode=yes -o ConnectTimeout=8 \
      -o ControlMaster=auto -o ControlPath="$HOME/.cache/health-%C" -o ControlPersist=120 \
      "$REMOTE_HOST" "$@"
}

check_site() {
  local url="$1" out code verify err
  err=$(mktemp)
  if ! out=$(curl -sS -L -o /dev/null --max-time 15 -w '%{http_code} %{ssl_verify_result}' "$url" 2>"$err"); then
    issue SERIOUS "$url: no response ($(head -n 1 "$err"))"; rm -f "$err"; return
  fi
  rm -f "$err"
  read -r code verify <<<"$out"
  [ "$code" = "200" ] || issue SERIOUS "$url: HTTP $code"
  [ "$verify" = "0" ] || issue SERIOUS "$url: TLS certificate did not verify"
}

check_local_service() {
  local svc="$1"
  systemctl --user --quiet is-active "$svc" && return
  if allowed "$svc" "${LOCAL_RESTART_ALLOWED[@]}" \
     && systemctl --user restart "$svc" && sleep 3 && systemctl --user --quiet is-active "$svc"; then
    fixed "$svc was stopped; restarted and confirmed running"
  else
    issue SERIOUS "local service $svc is not running (not restarted, or restart failed)"
  fi
}

check_remote_service() {
  local svc="$1"
  remote "systemctl --quiet is-active '$svc'" && return
  if allowed "$svc" "${REMOTE_RESTART_ALLOWED[@]}" \
     && remote "sudo -n systemctl restart '$svc' && sleep 3 && systemctl --quiet is-active '$svc'"; then
    fixed "$svc on $REMOTE_HOST was stopped; restarted and confirmed running"
  else
    issue SERIOUS "$svc on $REMOTE_HOST is not running (not restarted, or restart failed)"
  fi
}

check_remote_access() {
  remote 'sudo -n true' >/dev/null 2>&1 && return 0
  issue SERIOUS "cannot log in to $REMOTE_HOST with working sudo; remote checks skipped"
  return 1
}

compose_report() {
  if [ "${#ISSUES[@]}" -eq 0 ]; then
    printf 'Everything is OK.\n'
  else
    printf 'Everything is OK, except:\n\n'
    printf -- '- %s\n' "${ISSUES[@]}"
  fi
  if [ "${#FIXES[@]}" -gt 0 ]; then
    printf '\nFixed this morning:\n'
    printf -- '- %s\n' "${FIXES[@]}"
  fi
}

send_report() {
  local body="$1"
  local msg
  msg=$(printf 'From: %s\nTo: %s\nSubject: %s\nContent-Type: text/plain; charset=UTF-8\n\n%s\n' \
        "$REPORT_FROM" "$REPORT_TO" "$REPORT_SUBJECT" "$body")
  if [ "$DRY_RUN" = "1" ]; then
    printf '%s\n' "----- DRY RUN: report not sent -----" "$msg" >&2
    return 0
  fi
  printf '%s\n' "$msg" | "${SEND_CMD[@]}"
}

main() {
  local s
  for s in "${SITES[@]}"; do check_site "$s"; done
  for s in "${LOCAL_USER_SERVICES[@]}"; do check_local_service "$s"; done
  if [ -n "$REMOTE_HOST" ] && check_remote_access; then
    for s in "${REMOTE_SERVICES[@]}"; do check_remote_service "$s"; done
  fi

  local body
  body=$(compose_report)
  if ! send_report "$body"; then
    # The report is the heartbeat. Failing to send it is itself serious.
    printf 'Server Report could not be sent. %s\n' "$body"
    return 0
  fi

  # stdout only for serious unresolved problems: Hermes delivers it to the
  # urgent channel. Empty stdout is a silent run.
  if [ "$SERIOUS" -gt 0 ]; then
    printf 'Serious problem in this morning'"'"'s health check:\n'
    printf -- '- %s\n' "${ISSUES[@]}"
  fi
}

main "$@"
