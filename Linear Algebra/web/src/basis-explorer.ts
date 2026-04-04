/**
 * Basis Explorer — view a point's coordinates in both standard and custom bases.
 */

export function createBasisExplorer(engine: any, container: HTMLElement): void {
    container.innerHTML = `
        <h2>Basis Explorer</h2>
        <p>Set custom basis vectors and click to see coordinates in both bases.</p>
        <div style="display:flex;gap:20px;align-items:flex-start">
            <canvas id="basis-canvas" width="500" height="500"
                    style="border:1px solid #ccc;background:#fafafa;cursor:crosshair"></canvas>
            <div>
                <p><b>Basis vector b₁:</b></p>
                <input type="number" id="b1x" value="1" step="0.5" style="width:50px" />
                <input type="number" id="b1y" value="0.5" step="0.5" style="width:50px" />
                <p><b>Basis vector b₂:</b></p>
                <input type="number" id="b2x" value="0" step="0.5" style="width:50px" />
                <input type="number" id="b2y" value="1" step="0.5" style="width:50px" />
                <div id="basis-coords" style="font-family:monospace;margin-top:15px;line-height:1.8"></div>
            </div>
        </div>
    `;

    const canvas = container.querySelector('#basis-canvas') as HTMLCanvasElement;
    const ctx = canvas.getContext('2d')!;
    const b1x = container.querySelector('#b1x') as HTMLInputElement;
    const b1y = container.querySelector('#b1y') as HTMLInputElement;
    const b2x = container.querySelector('#b2x') as HTMLInputElement;
    const b2y = container.querySelector('#b2y') as HTMLInputElement;
    const coordsDiv = container.querySelector('#basis-coords') as HTMLDivElement;

    const cx = 250, cy = 250, scale = 60;
    let point = [2, 1.5];

    function toScreen(x: number, y: number): [number, number] {
        return [cx + x * scale, cy - y * scale];
    }

    function draw(): void {
        const bv1 = [parseFloat(b1x.value) || 0, parseFloat(b1y.value) || 0];
        const bv2 = [parseFloat(b2x.value) || 0, parseFloat(b2y.value) || 0];

        ctx.clearRect(0, 0, 500, 500);

        // Standard grid (gray)
        ctx.strokeStyle = '#eee'; ctx.lineWidth = 1;
        for (let i = -4; i <= 4; i++) {
            ctx.beginPath(); ctx.moveTo(...toScreen(i, -4)); ctx.lineTo(...toScreen(i, 4)); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(...toScreen(-4, i)); ctx.lineTo(...toScreen(4, i)); ctx.stroke();
        }

        // Custom basis grid (colored)
        ctx.lineWidth = 0.5;
        for (let t = -5; t <= 5; t++) {
            ctx.strokeStyle = 'rgba(214,51,132,0.2)';
            const ox = t * bv1[0], oy = t * bv1[1];
            ctx.beginPath();
            ctx.moveTo(...toScreen(ox - 5 * bv2[0], oy - 5 * bv2[1]));
            ctx.lineTo(...toScreen(ox + 5 * bv2[0], oy + 5 * bv2[1]));
            ctx.stroke();

            ctx.strokeStyle = 'rgba(13,110,253,0.2)';
            const ox2 = t * bv2[0], oy2 = t * bv2[1];
            ctx.beginPath();
            ctx.moveTo(...toScreen(ox2 - 5 * bv1[0], oy2 - 5 * bv1[1]));
            ctx.lineTo(...toScreen(ox2 + 5 * bv1[0], oy2 + 5 * bv1[1]));
            ctx.stroke();
        }

        // Axes
        ctx.strokeStyle = '#999'; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(500, cy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, 500); ctx.stroke();

        // Basis vectors
        const drawArrow = (v: number[], color: string, label: string) => {
            const [sx, sy] = toScreen(0, 0);
            const [ex, ey] = toScreen(v[0], v[1]);
            ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 2.5;
            ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey); ctx.stroke();
            ctx.beginPath(); ctx.arc(ex, ey, 4, 0, Math.PI * 2); ctx.fill();
            ctx.font = '13px sans-serif';
            ctx.fillText(label, ex + 5, ey - 5);
        };
        drawArrow(bv1, '#d63384', 'b₁');
        drawArrow(bv2, '#0d6efd', 'b₂');

        // Point
        const [px, py] = toScreen(point[0], point[1]);
        ctx.fillStyle = '#333';
        ctx.beginPath(); ctx.arc(px, py, 5, 0, Math.PI * 2); ctx.fill();

        // Compute coordinates in custom basis using WASM inverse
        const det = bv1[0] * bv2[1] - bv1[1] * bv2[0];
        let bCoords = 'singular basis!';
        if (Math.abs(det) > 1e-9) {
            const buf = engine._malloc(32);
            engine.HEAPF64[buf / 8] = bv1[0];
            engine.HEAPF64[buf / 8 + 1] = bv2[0];
            engine.HEAPF64[buf / 8 + 2] = bv1[1];
            engine.HEAPF64[buf / 8 + 3] = bv2[1];
            const bMat = engine._la_matrix_from_array(2, 2, buf);
            const invPtr = engine._la_matrix_inverse(bMat);
            engine._free(buf);

            if (invPtr) {
                const c1 = engine._la_matrix_get(invPtr, 0, 0) * point[0] +
                           engine._la_matrix_get(invPtr, 0, 1) * point[1];
                const c2 = engine._la_matrix_get(invPtr, 1, 0) * point[0] +
                           engine._la_matrix_get(invPtr, 1, 1) * point[1];
                bCoords = `(${c1.toFixed(3)}, ${c2.toFixed(3)})`;
                engine._la_matrix_free(invPtr);
            }
            engine._la_matrix_free(bMat);
        }

        coordsDiv.innerHTML = `
            <b>Point:</b> <span style="color:#333">(${point[0].toFixed(2)}, ${point[1].toFixed(2)})</span><br/>
            <b>Standard coords:</b> (${point[0].toFixed(3)}, ${point[1].toFixed(3)})<br/>
            <b>Custom basis coords:</b> ${bCoords}
        `;
    }

    canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();
        point = [(e.clientX - rect.left - cx) / scale, (cy - (e.clientY - rect.top)) / scale];
        draw();
    });

    [b1x, b1y, b2x, b2y].forEach(el => el.addEventListener('input', draw));
    draw();
}
