/* eslint-disable @typescript-eslint/no-explicit-any */

let engine: any = null;

export async function init(): Promise<void> {
    // @ts-ignore - Emscripten-generated module
    const LinAlgEngine = (await import('../dist/engine.js')).default;
    engine = await LinAlgEngine();
}

export function getEngine(): any {
    if (!engine) throw new Error('Engine not initialized — call init() first');
    return engine;
}

/* Matrix lifecycle */
export function createMatrix(rows: number, cols: number, data?: number[]): number {
    const e = getEngine();
    if (data) {
        const buf = e._malloc(data.length * 8);
        for (let i = 0; i < data.length; i++)
            e.HEAPF64[buf / 8 + i] = data[i];
        const ptr = e._la_matrix_from_array(rows, cols, buf);
        e._free(buf);
        return ptr;
    }
    return e._la_matrix_new(rows, cols);
}

export function freeMatrix(ptr: number): void {
    getEngine()._la_matrix_free(ptr);
}

export function getElement(ptr: number, i: number, j: number): number {
    return getEngine()._la_matrix_get(ptr, i, j);
}

export function setElement(ptr: number, i: number, j: number, val: number): void {
    getEngine()._la_matrix_set(ptr, i, j, val);
}

export function matrixRows(ptr: number): number {
    return getEngine()._la_matrix_rows(ptr);
}

export function matrixCols(ptr: number): number {
    return getEngine()._la_matrix_cols(ptr);
}

export function matrixToArray(ptr: number): number[][] {
    const rows = matrixRows(ptr);
    const cols = matrixCols(ptr);
    const result: number[][] = [];
    for (let i = 0; i < rows; i++) {
        const row: number[] = [];
        for (let j = 0; j < cols; j++)
            row.push(getElement(ptr, i, j));
        result.push(row);
    }
    return result;
}

/* Ch.1: Elimination */
export function swapRows(ptr: number, i: number, j: number): void {
    getEngine()._la_swap_rows(ptr, i, j);
}

export function scaleRow(ptr: number, i: number, s: number): void {
    getEngine()._la_scale_row(ptr, i, s);
}

export function addScaledRow(ptr: number, target: number, source: number, s: number): void {
    getEngine()._la_add_scaled_row(ptr, target, source, s);
}

export function toRref(ptr: number): number {
    return getEngine()._la_to_rref(ptr);
}

/* Ch.2: Operations */
export function matMul(a: number, b: number): number {
    return getEngine()._la_matrix_mul(a, b);
}

export function matTranspose(a: number): number {
    return getEngine()._la_matrix_transpose(a);
}

export function matInverse(a: number): number {
    return getEngine()._la_matrix_inverse(a);
}

/* Ch.3: Determinants */
export function detElimination(ptr: number): number {
    return getEngine()._la_det_elimination(ptr);
}

/* Ch.5: Inner products */
export function dot(u: number[], v: number[]): number {
    const e = getEngine();
    const n = u.length;
    const ub = e._malloc(n * 8);
    const vb = e._malloc(n * 8);
    for (let i = 0; i < n; i++) {
        e.HEAPF64[ub / 8 + i] = u[i];
        e.HEAPF64[vb / 8 + i] = v[i];
    }
    const r = e._la_dot(ub, vb, n);
    e._free(ub);
    e._free(vb);
    return r;
}

export function norm(v: number[]): number {
    const e = getEngine();
    const n = v.length;
    const buf = e._malloc(n * 8);
    for (let i = 0; i < n; i++) e.HEAPF64[buf / 8 + i] = v[i];
    const r = e._la_norm(buf, n);
    e._free(buf);
    return r;
}

export function gramSchmidt(vectors: number[][], dim: number): number[][] {
    const e = getEngine();
    const numVec = vectors.length;
    const inBuf = e._malloc(numVec * dim * 8);
    const outBuf = e._malloc(numVec * dim * 8);
    for (let v = 0; v < numVec; v++)
        for (let i = 0; i < dim; i++)
            e.HEAPF64[inBuf / 8 + v * dim + i] = vectors[v][i];

    e._la_gram_schmidt(inBuf, outBuf, numVec, dim);

    const result: number[][] = [];
    for (let v = 0; v < numVec; v++) {
        const vec: number[] = [];
        for (let i = 0; i < dim; i++)
            vec.push(e.HEAPF64[outBuf / 8 + v * dim + i]);
        result.push(vec);
    }
    e._free(inBuf);
    e._free(outBuf);
    return result;
}
