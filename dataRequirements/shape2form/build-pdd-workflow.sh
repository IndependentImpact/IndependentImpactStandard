#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
. "$ROOT_DIR/dataRequirements/shape2form/load-env.sh"
load_nias_env "$ROOT_DIR"
SHAPE2FORM_BIN="${SHAPE2FORM_BIN:-shape2form}"
OUT_BASE="${NIAS_TMP_DIR:-/tmp}"
OUT_BASE="${OUT_BASE%/}"
OUT_ROOT="${OUT_ROOT:-$OUT_BASE/nias-shape2form/pdd-workflow}"
SHAPES_FILE="$ROOT_DIR/dataRequirements/shape2form/pdd-workflow-ui-shapes.ttl"
COMMON_SHAPES="$ROOT_DIR/dataRequirements/shape2form/common-ui-shapes.ttl"
COMMON_ANNOTATIONS="$ROOT_DIR/dataRequirements/shape2form/common-annotations.ttl"
SHAPES_ANNOTATIONS="${SHAPES_FILE%-ui-shapes.ttl}-annotations.ttl"
SCHEMA_DIR="$OUT_ROOT/schema"
FLUTTER_DIR="$OUT_ROOT/flutter"

ALLOWED_PREFIXES="https://nova.org.za/novaimpactaccountingstandard/,https://nova.org.za/novaimpactaccountingstandard/shape2form/,http://w3id.org/aiao#,http://w3id.org/claimont#,http://w3id.org/impactont#,http://independentimpact.org/indicator-owl/,http://purl.org/dc/terms/,https://schema.org/,http://www.w3.org/1999/02/22-rdf-syntax-ns#,http://www.w3.org/2000/01/rdf-schema#,http://www.w3.org/2006/time#,https://hashgraphontology.xyz/core/"

mkdir -p "$SCHEMA_DIR" "$FLUTTER_DIR"

# Merge structure bundles with their machine-generated annotation siblings
# (ADR-003: presentation lives beside the pure-structure bundles) into a
# single self-contained file
MERGED_FILE="$OUT_ROOT/pdd-workflow-merged-ui-shapes.ttl"
cat "$COMMON_SHAPES" "$COMMON_ANNOTATIONS" "$SHAPES_FILE" "$SHAPES_ANNOTATIONS" > "$MERGED_FILE"

"$SHAPE2FORM_BIN" lint \
  -allow-path-prefixes "$ALLOWED_PREFIXES" \
  "$MERGED_FILE"

"$SHAPE2FORM_BIN" emit-jsonld \
  -format jsonld \
  -o "$SCHEMA_DIR/forms.jsonld" \
  "$MERGED_FILE"

"$SHAPE2FORM_BIN" build \
  -outdir "$FLUTTER_DIR" \
  "$MERGED_FILE"

printf 'shape2form PDD workflow output:\n'
printf '  schema: %s\n' "$SCHEMA_DIR/forms.jsonld"
printf '  dart:   %s\n' "$FLUTTER_DIR"
