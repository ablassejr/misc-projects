/**
 * Transform Playground — visualize 2D linear transformations.
 * User enters a 2x2 matrix; unit square is transformed in real time.
 */

export function createTransformPlayground(engine: any, container: HTMLElement): void {
    container.innerHTML = `
        <h2>Transform Playground</h2>
        <div style="display:flex;gap:20px;align-items:flex-start">
            <div>
                <canvas id="transform-canvas" width="500" height="500"
                        style="border:1px solid #ccc;background:#fafafa"></canvas>
            </div>
            <div>
                <p>2×2 Matrix:</p>
                <table style="border-collapse:collapse">
                    <tr>
                        <td><input type="number" id="m00" value="1" step="0.1" style="width:60px" /></td>
                        <td><input type="number" id="m01" value="0" step="0.1" style="width:60px" /></td>
                    </tr>
                    <tr>
                        <td><input type="number" id="m10" value="0" step="0.1" style="width:60px" /></td>
                        <td><input type="number" id="m11" value="1" step="0.1" style="width:60px" /></td>
                    </tr>
                </table>
                <p id="det-display" style="font-family:monospace;margin-top:10px">det = 1.0000</p>
                <div style="margin-top:10px">
                    <label><input type="checkbox" id="show-vectors" checked /> Show column vectors</label>
                </div>
                <div style="margin-top:10px">
                    <button id="preset-rot">Rotation 45°</button>
                    <button id="preset-shear">Shear</button>
                    <button id="preset-reflect">Reflect x</button>
                    <button id="preset-scale">Scale 2x</button>
                </div>
            </div>
        </div>
    `;

    const canvas = container.querySelector('#transform-canvas') as HTMLCanvasElement;
    const ctx = canvas.getContext('2d')!;
    const m00 = container.querySelector('#m00') as HTMLInputElement;
    const m01 = container.querySelector('#m01') as HTMLInputElement;
    const m10 = container.querySelector('#m10') as HTMLInputElement;
    const m11 = container.querySelector('#m11') as HTMLInputElement;
    const detDisplay = container.querySelector('#det-display') as HTMLParagraphElement;
    const showVec = container.querySelector('#show-vectors') as HTMLInputElement;

    const cx = 250, cy = 250, scale = 60;

    function toScreen(x: number, y: number): [number, number] {
        return [cx + x * scale, cy - y * scale];
    }

    function draw(): void {
        const a = parseFloat(m00.value) || 0;
        const b = parseFloat(m01.value) || 0;
        const c = parseFloat(m10.value) || 0;
        const d = parseFloat(m11.value) || 0;

        const buf = engine._malloc(32);
        engine.HEAPF64[buf / 8] = a;
        engine.HEAPF64[buf / 8 + 1] = b;
        engine.HEAPF64[buf / 8 + 2] = c;
        engine.HEAPF64[buf / 8 + 3] = d;
        const ptr = engine._la_matrix_from_array(2, 2, buf);
        const det = engine._la_det_elimination(ptr);
        engine._la_matrix_free(ptr);
        engine._free(buf);

        detDisplay.textContent = `det = ${det.toFixed(4)} (area scale: ${Math.abs(det).toFixed(4)})`;

        ctx.clearRect(0, 0, 500, 500);

        // Grid
        ctx.strokeStyle = '#eee';
        ctx.lineWidth = 1;
        for (let i = -4; i <= 4; i++) {
            const [sx, sy] = toScreen(i, -4);
            const [ex, ey] = toScreen(i, 4);
            ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey); ctx.stroke();
            const [sx2, sy2] = toScreen(-4, i);
            const [ex2, ey2] = toScreen(4, i);
            ctx.beginPath(); ctx.moveTo(sx2, sy2); ctx.lineTo(ex2, ey2); ctx.stroke();
        }

        // Axes
        ctx.strokeStyle = '#999';
        ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(500, cy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, 500); ctx.stroke();

        // Original unit square
        const sq = [[0,0],[1,0],[1,1],[0,1]];
        ctx.strokeStyle = 'rgba(0,0,255,0.3)';
        ctx.fillStyle = 'rgba(0,0,255,0.05)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        sq.forEach((p, i) => {
            const [sx, sy] = toScreen(p[0], p[1]);
            i === 0 ? ctx.moveTo(sx, sy) : ctx.lineTo(sx, sy);
        });
        ctx.closePath(); ctx.fill(); ctx.stroke();

        // Transformed shape
        const tsq = sq.map(([x, y]) => [a*x + b*y, c*x + d*y]);
        ctx.strokeStyle = 'rgba(255,50,50,0.8)';
        ctx.fillStyle = det >= 0 ? 'rgba(255,50,50,0.15)' : 'rgba(255,50,50,0.3)';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        tsq.forEach((p, i) => {
            const [sx, sy] = toScreen(p[0], p[1]);
            i === 0 ? ctx.moveTo(sx, sy) : ctx.lineTo(sx, sy);
        });
        ctx.closePath(); ctx.fill(); ctx.stroke();

        // Column vectors
        if (showVec.checked) {
            const drawArrow = (ex: number, ey: number, color: string, label: string) => {
                const [sx, sy] = toScreen(0, 0);
                const [esx, esy] = toScreen(ex, ey);
                ctx.strokeStyle = color;
                ctx.fillStyle = color;
                ctx.lineWidth = 3;
                ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(esx, esy); ctx.stroke();
                const angle = Math.atan2(sy - esy, esx - sx);
                ctx.beginPath();
                ctx.moveTo(esx, esy);
                ctx.lineTo(esx - 10 * Math.cos(angle - 0.3), esy + 10 * Math.sin(angle - 0.3));
                ctx.lineTo(esx - 10 * Math.cos(angle + 0.3), esy + 10 * Math.sin(angle + 0.3));
                ctx.closePath(); ctx.fill();
                ctx.font = '14px sans-serif';
                ctx.fillText(label, esx + 5, esy - 5);
            };
            drawArrow(a, c, '#d63384', `col₁(${a.toFixed(1)},${c.toFixed(1)})`);
            drawArrow(b, d, '#0d6efd', `col₂(${b.toFixed(1)},${d.toFixed(1)})`);
        }
    }

    [m00, m01, m10, m11, showVec].forEach(el =>
        el.addEventListener('input', draw)
    );

    const setMatrix = (a: number, b: number, c: number, d: number) => {
        m00.value = String(a); m01.value = String(b);
        m10.value = String(c); m11.value = String(d);
        draw();
    };

    container.querySelector('#preset-rot')!.addEventListener('click', () => {
        const c45 = Math.cos(Math.PI / 4), s45 = Math.sin(Math.PI / 4);
        setMatrix(+c45.toFixed(4), -s45.toFixed(4) as any, +s45.toFixed(4) as any, +c45.toFixed(4));
    });
    container.querySelector('#preset-shear')!.addEventListener('click', () => setMatrix(1, 1, 0, 1));
    container.querySelector('#preset-reflect')!.addEventListener('click', () => setMatrix(1, 0, 0, -1));
    container.querySelector('#preset-scale')!.addEventListener('click', () => setMatrix(2, 0, 0, 2));

    draw();
}
