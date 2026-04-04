/**
 * Gram-Schmidt Visualizer — step through orthonormalization in 2D
 * (simplified from 3D for browser compatibility without Three.js).
 * Shows projection, subtraction, and normalization steps.
 */

export function createGramSchmidtViz(engine: any, container: HTMLElement): void {
    container.innerHTML = `
        <h2>Gram-Schmidt Orthonormalization</h2>
        <p>Enter vectors (2D) and step through the process.</p>
        <div style="display:flex;gap:20px;align-items:flex-start">
            <canvas id="gs-canvas" width="500" height="500"
                    style="border:1px solid #ccc;background:#fafafa"></canvas>
            <div>
                <p><b>v₁:</b>
                    <input type="number" id="v1x" value="2" step="0.5" style="width:50px" />
                    <input type="number" id="v1y" value="1" step="0.5" style="width:50px" />
                </p>
                <p><b>v₂:</b>
                    <input type="number" id="v2x" value="1" step="0.5" style="width:50px" />
                    <input type="number" id="v2y" value="2" step="0.5" style="width:50px" />
                </p>
                <div style="margin:10px 0">
                    <button id="gs-step">Next Step</button>
                    <button id="gs-reset">Reset</button>
                </div>
                <div id="gs-log" style="font-family:monospace;font-size:12px;line-height:1.6;max-height:300px;overflow-y:auto"></div>
            </div>
        </div>
    `;

    const canvas = container.querySelector('#gs-canvas') as HTMLCanvasElement;
    const ctx = canvas.getContext('2d')!;
    const v1x = container.querySelector('#v1x') as HTMLInputElement;
    const v1y = container.querySelector('#v1y') as HTMLInputElement;
    const v2x = container.querySelector('#v2x') as HTMLInputElement;
    const v2y = container.querySelector('#v2y') as HTMLInputElement;
    const logDiv = container.querySelector('#gs-log') as HTMLDivElement;

    const cx = 250, cy = 250, scale = 80;
    let step = 0;
    let u1: number[] = [];
    let u2: number[] = [];
    let proj: number[] = [];
    let logs: string[] = [];

    function toScreen(x: number, y: number): [number, number] {
        return [cx + x * scale, cy - y * scale];
    }

    function drawArrow(from: number[], to: number[], color: string, label: string, dashed = false): void {
        const [sx, sy] = toScreen(from[0], from[1]);
        const [ex, ey] = toScreen(to[0], to[1]);
        ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 2.5;
        if (dashed) ctx.setLineDash([5, 5]); else ctx.setLineDash([]);
        ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(ex, ey); ctx.stroke();
        ctx.setLineDash([]);
        const angle = Math.atan2(sy - ey, ex - sx);
        ctx.beginPath();
        ctx.moveTo(ex, ey);
        ctx.lineTo(ex - 8 * Math.cos(angle - 0.3), ey + 8 * Math.sin(angle - 0.3));
        ctx.lineTo(ex - 8 * Math.cos(angle + 0.3), ey + 8 * Math.sin(angle + 0.3));
        ctx.closePath(); ctx.fill();
        ctx.font = '13px sans-serif';
        ctx.fillText(label, ex + 8, ey - 8);
    }

    function draw(): void {
        const v1 = [parseFloat(v1x.value) || 0, parseFloat(v1y.value) || 0];
        const v2 = [parseFloat(v2x.value) || 0, parseFloat(v2y.value) || 0];

        ctx.clearRect(0, 0, 500, 500);

        // Grid
        ctx.strokeStyle = '#eee'; ctx.lineWidth = 1;
        for (let i = -3; i <= 3; i++) {
            ctx.beginPath(); ctx.moveTo(...toScreen(i, -3)); ctx.lineTo(...toScreen(i, 3)); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(...toScreen(-3, i)); ctx.lineTo(...toScreen(3, i)); ctx.stroke();
        }
        ctx.strokeStyle = '#999'; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(500, cy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, 500); ctx.stroke();

        // Original vectors (faded)
        drawArrow([0, 0], v1, 'rgba(214,51,132,0.3)', 'v₁', true);
        drawArrow([0, 0], v2, 'rgba(13,110,253,0.3)', 'v₂', true);

        if (step >= 1 && u1.length) {
            drawArrow([0, 0], u1, '#d63384', `u₁(${u1[0].toFixed(2)},${u1[1].toFixed(2)})`);
        }
        if (step >= 2 && proj.length) {
            drawArrow([0, 0], proj, '#ffc107', 'proj', true);
            ctx.strokeStyle = 'rgba(255,193,7,0.5)'; ctx.lineWidth = 1; ctx.setLineDash([3, 3]);
            ctx.beginPath(); ctx.moveTo(...toScreen(v2[0], v2[1])); ctx.lineTo(...toScreen(proj[0], proj[1])); ctx.stroke();
            ctx.setLineDash([]);
        }
        if (step >= 3 && u2.length) {
            drawArrow([0, 0], u2, '#0d6efd', `u₂(${u2[0].toFixed(2)},${u2[1].toFixed(2)})`);
        }

        logDiv.innerHTML = logs.map(l => `<div>${l}</div>`).join('');
    }

    function doStep(): void {
        const v1 = [parseFloat(v1x.value) || 0, parseFloat(v1y.value) || 0];
        const v2 = [parseFloat(v2x.value) || 0, parseFloat(v2y.value) || 0];

        step++;
        if (step === 1) {
            const n = Math.sqrt(v1[0] ** 2 + v1[1] ** 2);
            u1 = n > 1e-9 ? [v1[0] / n, v1[1] / n] : [0, 0];
            logs.push(`Step 1: u₁ = v₁/||v₁|| = (${u1[0].toFixed(4)}, ${u1[1].toFixed(4)})`);
        } else if (step === 2) {
            const d = v2[0] * u1[0] + v2[1] * u1[1];
            proj = [d * u1[0], d * u1[1]];
            logs.push(`Step 2: proj = (v₂·u₁)u₁ = (${proj[0].toFixed(4)}, ${proj[1].toFixed(4)})`);
        } else if (step === 3) {
            const w = [v2[0] - proj[0], v2[1] - proj[1]];
            const n = Math.sqrt(w[0] ** 2 + w[1] ** 2);
            u2 = n > 1e-9 ? [w[0] / n, w[1] / n] : [0, 0];
            const dot = u1[0] * u2[0] + u1[1] * u2[1];
            logs.push(`Step 3: u₂ = (v₂ - proj)/||...|| = (${u2[0].toFixed(4)}, ${u2[1].toFixed(4)})`);
            logs.push(`Verify: u₁·u₂ = ${dot.toFixed(9)} ≈ 0 ✓`);
        }
        draw();
    }

    container.querySelector('#gs-step')!.addEventListener('click', () => {
        if (step < 3) doStep();
    });
    container.querySelector('#gs-reset')!.addEventListener('click', () => {
        step = 0; u1 = []; u2 = []; proj = []; logs = [];
        draw();
    });

    [v1x, v1y, v2x, v2y].forEach(el => el.addEventListener('input', () => {
        step = 0; u1 = []; u2 = []; proj = []; logs = [];
        draw();
    }));

    draw();
}
