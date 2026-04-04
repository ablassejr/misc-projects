/* eslint-disable @typescript-eslint/no-explicit-any */

let engine: any = null;

export async function init(): Promise<void> {
    const LinAlgEngine = (await import('../dist/engine.js')).default;
    engine = await LinAlgEngine();
}

export function createMatrix(rows: number, cols: number, data?: number[]): number {
    if (!engine) throw new Error('Engine not initialized — call init() first');
    const ptr = engine._la_matrix_new(rows, cols);
    if (data) {
        const dataPtr = engine._la_matrix_data_ptr(ptr);
        for (let i = 0; i < data.length; i++) {
            engine.HEAPF64[dataPtr / 8 + i] = data[i];
        }
    }
    return ptr;
}

export function getElement(matPtr: number, i: number, j: number): number {
    return engine._la_matrix_get(matPtr, i, j);
}

export function setElement(matPtr: number, i: number, j: number, val: number): void {
    engine._la_matrix_set(matPtr, i, j, val);
}

export function freeMatrix(matPtr: number): void {
    engine._la_matrix_free(matPtr);
}

export function matrixRows(matPtr: number): number {
    return engine._la_matrix_rows(matPtr);
}

export function matrixCols(matPtr: number): number {
    return engine._la_matrix_cols(matPtr);
}
