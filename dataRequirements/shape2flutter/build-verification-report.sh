#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
. "$ROOT_DIR/dataRequirements/shape2flutter/load-env.sh"
load_nias_env "$ROOT_DIR"
SHAPE2FLUTTER_BIN="${SHAPE2FLUTTER_BIN:-/Users/christiaanpauw/shape2flutter/shape2flutter}"
OUT_BASE="${NIAS_TMP_DIR:-/tmp}"
OUT_BASE="${OUT_BASE%/}"
OUT_ROOT="${OUT_ROOT:-$OUT_BASE/nias-shape2flutter/verification-report}"
SHAPES_FILE="$ROOT_DIR/dataRequirements/shape2flutter/verification-report-ui-shapes.ttl"
COMMON_SHAPES="$ROOT_DIR/dataRequirements/shape2flutter/common-ui-shapes.ttl"
SCHEMA_DIR="$OUT_ROOT/schema"
FLUTTER_DIR="$OUT_ROOT/flutter"

ALLOWED_PREFIXES="https://nova.org.za/novaimpactaccountingstandard/,https://nova.org.za/novaimpactaccountingstandard/shape2flutter/,http://independentimpact.org/indicator-owl/,http://www.w3.org/2006/time#,http://purl.org/dc/terms/,https://hashgraphontology.xyz/core/"

mkdir -p "$SCHEMA_DIR" "$FLUTTER_DIR"

# Merge common shapes with bundle-specific shapes into a single self-contained file
MERGED_FILE="$OUT_ROOT/verification-report-merged-ui-shapes.ttl"
cat "$COMMON_SHAPES" "$SHAPES_FILE" > "$MERGED_FILE"

"$SHAPE2FLUTTER_BIN" lint \
  -allow-path-prefixes "$ALLOWED_PREFIXES" \
  "$MERGED_FILE"

"$SHAPE2FLUTTER_BIN" emit-jsonld \
  -format jsonld \
  -o "$SCHEMA_DIR/forms.jsonld" \
  "$MERGED_FILE"

"$SHAPE2FLUTTER_BIN" build \
  -outdir "$FLUTTER_DIR" \
  "$MERGED_FILE"

printf 'shape2flutter verification report output:\n'
printf '  schema: %s\n' "$SCHEMA_DIR/forms.jsonld"
printf '  dart:   %s\n' "$FLUTTER_DIR"
