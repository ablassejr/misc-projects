/**
 * Determinant Visualizer — drag two 2D vectors to see parallelogram area = |det|.
 */

export function createDetVisualizer(engine: any, container: HTMLElement): void {
    container.innerHTML = `
        <h2>Determinant Visualizer</h2>
        <p>Drag the vector endpoints. Parallelogram area = |det|.</p>
        <canvas id="det-canvas" width="500" height="500"
                style="border:1px solid #ccc;background:#fafafa;cursor:crosshair"></canvas>
        <p id="det-info" style="font-family:monospace;font-size:14px"></p>
    `;

    const canvas = container.querySelector('#det-canvas') as HTMLCanvasElement;
    const ctx = canvas.getContext('2d')!;
    const info = container.querySelector('#det-info') as HTMLParagraphElement;

    const cx = 250, cy = 250, scale = 60;
    let vectors = [[2, 1], [1, 2]];
    let dragging = -1;

    function toScreen(x: number, y: number): [number, number] {
        return [cx + x * scale, cy - y * scale];
    }
    function fromScreen(sx: number, sy: number): [number, number] {
        return [(sx - cx) / scale, (cy - sy) / scale];
    }

    function draw(): void {
        const [u, v] = vectors;
        const a = u[0], b = v[0], c = u[1], d = v[1];

        const buf = engine._malloc(32);
        engine.HEAPF64[buf / 8] = a;
        engine.HEAPF64[buf / 8 + 1] = b;
        engine.HEAPF64[buf / 8 + 2] = c;
        engine.HEAPF64[buf / 8 + 3] = d;
        const ptr = engine._la_matrix_from_array(2, 2, buf);
        const det = engine._la_det_elimination(ptr);
        engine._la_matrix_free(ptr);
        engine._free(buf);

        ctx.clearRect(0, 0, 500, 500);

        // Grid
        ctx.strokeStyle = '#eee';
        for (let i = -4; i <= 4; i++) {
            ctx.beginPath(); ctx.moveTo(...toScreen(i, -4)); ctx.lineTo(...toScreen(i, 4)); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(...toScreen(-4, i)); ctx.lineTo(...toScreen(4, i)); ctx.stroke();
        }
        ctx.strokeStyle = '#999'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(500, cy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, 500); ctx.stroke();

        // Parallelogram
        const pts: [number, number][] = [
            toScreen(0, 0), toScreen(u[0], u[1]),
            toScreen(u[0] + v[0], u[1] + v[1]), toScreen(v[0], v[1])
        ];
        ctx.fillStyle = Math.abs(det) < 0.01 ? 'rgba(255,0,0,0.1)' : 'rgba(100,200,100,0.2)';
        ctx.strokeStyle = 'rgba(0,0,0,0.3)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        pts.forEach((p, i) => i === 0 ? ctx.moveTo(...p) : ctx.lineTo(...p));
        ctx.closePath(); ctx.fill(); ctx.stroke();

        // Vectors
        const drawVec = (vec: number[], color: string, label: string) => {
            const [sx, sy] = toScreen(0, 0);
            const [ex, ey] = toScreen(vec[0], vec[1]);
            ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey); ctx.stroke();
            ctx.beginPath(); ctx.arc(ex, ey, 6, 0, Math.PI * 2); ctx.fill();
            ctx.font = '14px sans-serif';
            ctx.fillText(label, ex + 10, ey - 10);
        };
        drawVec(u, '#d63384', `u(${u[0].toFixed(1)},${u[1].toFixed(1)})`);
        drawVec(v, '#0d6efd', `v(${v[0].toFixed(1)},${v[1].toFixed(1)})`);

        info.textContent = `det = ${det.toFixed(4)} | Area = ${Math.abs(det).toFixed(4)}` +
            (Math.abs(det) < 0.01 ? ' ⚠ Vectors nearly parallel!' : '');
    }

    canvas.addEventListener('mousedown', (e) => {
        const rect = canvas.getBoundingClientRect();
        const [mx, my] = fromScreen(e.clientX - rect.left, e.clientY - rect.top);
        for (let i = 0; i < 2; i++) {
            const dx = mx - vectors[i][0], dy = my - vectors[i][1];
            if (dx * dx + dy * dy < 0.3) { dragging = i; return; }
        }
    });

    canvas.addEventListener('mousemove', (e) => {
        if (dragging < 0) return;
        const rect = canvas.getBoundingClientRect();
        const [mx, my] = fromScreen(e.clientX - rect.left, e.clientY - rect.top);
        vectors[dragging] = [Math.round(mx * 4) / 4, Math.round(my * 4) / 4];
        draw();
    });

    canvas.addEventListener('mouseup', () => { dragging = -1; });
    canvas.addEventListener('mouseleave', () => { dragging = -1; });

    draw();
}
