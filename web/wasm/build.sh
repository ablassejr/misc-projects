#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENGINE_DIR="$SCRIPT_DIR/../../engine"
OUT_DIR="$SCRIPT_DIR/../dist"

mkdir -p "$OUT_DIR"

emcc \
    "$ENGINE_DIR"/src/*.c \
    -I"$ENGINE_DIR"/include \
    -o "$OUT_DIR/engine.js" \
    -s EXPORTED_FUNCTIONS="[\
        '_la_matrix_new','_la_matrix_free','_la_matrix_from_array',\
        '_la_matrix_get','_la_matrix_set','_la_matrix_data_ptr',\
        '_la_matrix_rows','_la_matrix_cols','_la_matrix_identity'\
    ]" \
    -s EXPORTED_RUNTIME_METHODS="['ccall','cwrap','getValue','setValue']" \
    -s MODULARIZE=1 \
    -s EXPORT_NAME="LinAlgEngine" \
    -s ALLOW_MEMORY_GROWTH=1 \
    -O2

echo "WASM build complete: $OUT_DIR/engine.js + engine.wasm"
