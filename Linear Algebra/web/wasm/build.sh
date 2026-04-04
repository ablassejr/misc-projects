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
        '_la_matrix_rows','_la_matrix_cols','_la_matrix_identity',\
        '_la_matrix_copy','_la_matrix_print',\
        '_la_swap_rows','_la_scale_row','_la_add_scaled_row',\
        '_la_find_pivot','_la_to_ref','_la_to_rref','_la_solve',\
        '_la_matrix_add','_la_matrix_scalar_mul','_la_matrix_mul',\
        '_la_matrix_transpose','_la_matrix_inverse',\
        '_la_lu_factorize','_la_forward_sub','_la_back_sub',\
        '_la_det_cofactor','_la_det_elimination',\
        '_la_minor','_la_cofactor','_la_adjoint',\
        '_la_rank','_la_nullity',\
        '_la_dot','_la_norm','_la_normalize','_la_distance','_la_angle',\
        '_la_are_orthogonal','_la_cross_product',\
        '_la_gram_schmidt','_la_orthogonal_projection','_la_least_squares',\
        '_malloc','_free'\
    ]" \
    -s EXPORTED_RUNTIME_METHODS="['ccall','cwrap','getValue','setValue','HEAPF64']" \
    -s MODULARIZE=1 \
    -s EXPORT_NAME="LinAlgEngine" \
    -s ALLOW_MEMORY_GROWTH=1 \
    -O2

echo "WASM build complete: $OUT_DIR/engine.js + engine.wasm"
