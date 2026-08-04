#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
. "$ROOT_DIR/dataRequirements/shape2form/load-env.sh"
load_nias_env "$ROOT_DIR"
SHAPE2FORM_BIN="${SHAPE2FORM_BIN:-shape2form}"
OUT_BASE="${NIAS_TMP_DIR:-/tmp}"
OUT_BASE="${OUT_BASE%/}"
OUT_ROOT="${OUT_ROOT:-$OUT_BASE/nias-shape2form/validation-verification}"
SHAPES_FILE="$ROOT_DIR/dataRequirements/shape2form/archive/validation-verification-ui-shapes.ttl"
SCHEMA_DIR="$OUT_ROOT/schema"
FLUTTER_DIR="$OUT_ROOT/flutter"

ALLOWED_PREFIXES="https://nova.org.za/novaimpactaccountingstandard/,https://nova.org.za/novaimpactaccountingstandard/shape2form/,http://independentimpact.org/indicator-owl/,http://www.w3.org/2006/time#,http://purl.org/dc/terms/,https://hashgraphontology.xyz/core/"

mkdir -p "$SCHEMA_DIR" "$FLUTTER_DIR"

"$SHAPE2FORM_BIN" lint \
  -allow-path-prefixes "$ALLOWED_PREFIXES" \
  "$SHAPES_FILE"

"$SHAPE2FORM_BIN" emit-jsonld \
  -format jsonld \
  -o "$SCHEMA_DIR/forms.jsonld" \
  "$SHAPES_FILE"

"$SHAPE2FORM_BIN" build \
  -outdir "$FLUTTER_DIR" \
  "$SHAPES_FILE"

printf 'shape2form validation/verification output:\n'
printf '  schema: %s\n' "$SCHEMA_DIR/forms.jsonld"
printf '  dart:   %s\n' "$FLUTTER_DIR"
