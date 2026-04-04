/**
 * Elimination Stepper — step through Gaussian elimination on a user-entered system.
 * Uses WASM engine for row operations. Renders matrix with pivot highlighting.
 */

interface StepperState {
    matPtr: number;
    rows: number;
    cols: number;
    pivotRow: number;
    pivotCol: number;
    phase: 'forward' | 'backward' | 'done';
    steps: string[];
}

export function createEliminationStepper(engine: any, container: HTMLElement): void {
    container.innerHTML = `
        <h2>Elimination Stepper</h2>
        <p>Enter an augmented matrix (rows separated by semicolons, elements by commas):</p>
        <input type="text" id="elim-input" value="1,1,2,9; 2,4,-3,1; 3,6,-5,0"
               style="width:100%;padding:8px;font-family:monospace;font-size:14px" />
        <div style="margin:10px 0">
            <button id="elim-load">Load</button>
            <button id="elim-step" disabled>Next Step</button>
            <button id="elim-all" disabled>Run All</button>
            <button id="elim-reset" disabled>Reset</button>
        </div>
        <div id="elim-matrix" style="font-family:monospace;font-size:16px;margin:10px 0"></div>
        <div id="elim-log" style="font-family:monospace;font-size:12px;color:#666;max-height:200px;overflow-y:auto"></div>
    `;

    let state: StepperState | null = null;

    const input = container.querySelector('#elim-input') as HTMLInputElement;
    const loadBtn = container.querySelector('#elim-load') as HTMLButtonElement;
    const stepBtn = container.querySelector('#elim-step') as HTMLButtonElement;
    const allBtn = container.querySelector('#elim-all') as HTMLButtonElement;
    const resetBtn = container.querySelector('#elim-reset') as HTMLButtonElement;
    const matDiv = container.querySelector('#elim-matrix') as HTMLDivElement;
    const logDiv = container.querySelector('#elim-log') as HTMLDivElement;

    function renderMatrix(): void {
        if (!state) return;
        let html = '<table style="border-collapse:collapse">';
        for (let i = 0; i < state.rows; i++) {
            html += '<tr>';
            for (let j = 0; j < state.cols; j++) {
                const val = engine._la_matrix_get(state.matPtr, i, j);
                const isPivot = (i === state.pivotRow && j === state.pivotCol);
                const isAug = (j === state.cols - 1);
                let bg = 'transparent';
                if (isPivot) bg = '#ffd700';
                else if (i === state.pivotRow) bg = '#fff3cd';
                const border = isAug ? 'border-left:2px solid #333;' : '';
                html += `<td style="padding:4px 10px;text-align:right;background:${bg};${border}">${val.toFixed(4)}</td>`;
            }
            html += '</tr>';
        }
        html += '</table>';
        matDiv.innerHTML = html;
    }

    function log(msg: string): void {
        if (!state) return;
        state.steps.push(msg);
        logDiv.innerHTML = state.steps.map(s => `<div>${s}</div>`).join('');
        logDiv.scrollTop = logDiv.scrollHeight;
    }

    function doStep(): boolean {
        if (!state || state.phase === 'done') return false;

        const m = state.matPtr;
        const numCols = state.cols - 1; // variable columns only

        if (state.phase === 'forward') {
            while (state.pivotCol < numCols && state.pivotRow < state.rows) {
                const best = engine._la_find_pivot(m, state.pivotCol, state.pivotRow);
                if (best < 0) {
                    state.pivotCol++;
                    continue;
                }
                if (best !== state.pivotRow) {
                    engine._la_swap_rows(m, state.pivotRow, best);
                    log(`R${state.pivotRow + 1} ↔ R${best + 1}`);
                }
                const pv = engine._la_matrix_get(m, state.pivotRow, state.pivotCol);
                if (Math.abs(pv - 1.0) > 1e-9) {
                    engine._la_scale_row(m, state.pivotRow, 1.0 / pv);
                    log(`R${state.pivotRow + 1} × ${(1.0 / pv).toFixed(4)}`);
                }
                let eliminated = false;
                for (let r = state.pivotRow + 1; r < state.rows; r++) {
                    const factor = engine._la_matrix_get(m, r, state.pivotCol);
                    if (Math.abs(factor) > 1e-9) {
                        engine._la_add_scaled_row(m, r, state.pivotRow, -factor);
                        log(`R${r + 1} -= ${factor.toFixed(4)} × R${state.pivotRow + 1}`);
                        eliminated = true;
                    }
                }
                state.pivotRow++;
                state.pivotCol++;
                renderMatrix();
                return true;
            }
            state.phase = 'backward';
            state.pivotRow = Math.min(state.rows, numCols) - 1;
            log('--- Back elimination ---');
        }

        if (state.phase === 'backward') {
            if (state.pivotRow < 0) {
                state.phase = 'done';
                log('RREF complete!');
                stepBtn.disabled = true;
                allBtn.disabled = true;
                renderMatrix();
                return false;
            }
            let pc = -1;
            for (let j = 0; j < numCols; j++) {
                if (Math.abs(engine._la_matrix_get(m, state.pivotRow, j)) > 1e-9) {
                    pc = j;
                    break;
                }
            }
            if (pc >= 0) {
                for (let r = state.pivotRow - 1; r >= 0; r--) {
                    const factor = engine._la_matrix_get(m, r, pc);
                    if (Math.abs(factor) > 1e-9) {
                        engine._la_add_scaled_row(m, r, state.pivotRow, -factor);
                        log(`R${r + 1} -= ${factor.toFixed(4)} × R${state.pivotRow + 1}`);
                    }
                }
            }
            state.pivotRow--;
            renderMatrix();
            return true;
        }
        return false;
    }

    loadBtn.addEventListener('click', () => {
        if (state) engine._la_matrix_free(state.matPtr);
        const rowStrs = input.value.split(';').map(s => s.trim()).filter(s => s);
        const data: number[] = [];
        const rows = rowStrs.length;
        let cols = 0;
        for (const rs of rowStrs) {
            const nums = rs.split(',').map(Number);
            cols = nums.length;
            data.push(...nums);
        }
        const buf = engine._malloc(data.length * 8);
        for (let i = 0; i < data.length; i++) engine.HEAPF64[buf / 8 + i] = data[i];
        const ptr = engine._la_matrix_from_array(rows, cols, buf);
        engine._free(buf);
        state = { matPtr: ptr, rows, cols, pivotRow: 0, pivotCol: 0, phase: 'forward', steps: [] };
        stepBtn.disabled = false;
        allBtn.disabled = false;
        resetBtn.disabled = false;
        logDiv.innerHTML = '';
        log('Matrix loaded. Click "Next Step" to begin elimination.');
        renderMatrix();
    });

    stepBtn.addEventListener('click', () => doStep());
    allBtn.addEventListener('click', () => { while (doStep()) {} });
    resetBtn.addEventListener('click', () => loadBtn.click());
}
