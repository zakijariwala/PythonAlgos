<script lang="ts">
    let { matrix = [], entropy = 0, epoch = 0 } = $props();

    let canvas: HTMLCanvasElement;
    let entropyHistory: { epoch: number, entropy: number }[] = $state([]);

    // Dynamically update entropy history
    $effect(() => {
        if (entropy !== undefined && epoch !== undefined) {
            entropyHistory.push({ epoch, entropy });
            if (entropyHistory.length > 50) {
                entropyHistory.shift();
            }
        }
    });

    // Render matrix
    $effect(() => {
        if (canvas && matrix.length > 0) {
            const ctx = canvas.getContext('2d');
            if (ctx) {
                const width = canvas.width;
                const height = canvas.height;
                const n = matrix.length;
                const cellW = width / n;
                const cellH = height / n;

                ctx.clearRect(0, 0, width, height);

                for (let i = 0; i < n; i++) {
                    for (let j = 0; j < n; j++) {
                        const val = matrix[i][j];
                        const r = Math.floor(val * 255);
                        const g = Math.floor(val * 215);
                        const b = 0;
                        ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
                        ctx.fillRect(j * cellW, i * cellH, cellW, cellH);
                    }
                }
            }
        }
    });
</script>

<div class="heatmap-container">
    <div class="canvas-wrapper">
        <canvas bind:this={canvas} width="300" height="300"></canvas>
    </div>
    
    <div class="entropy-stats">
        <h3>Average Attention Entropy</h3>
        <p class="value">{entropy.toFixed(4)}</p>
        <div class="chart-container">
            <svg viewBox="0 0 100 30" width="100%" height="30">
                <polyline 
                    fill="none" 
                    stroke="gold" 
                    stroke-width="2" 
                    points={entropyHistory.map((h, i) => `${(i / 50) * 100},${30 - (h.entropy / 3) * 30}`).join(' ')} 
                />
            </svg>
        </div>
    </div>
</div>

<style>
    .heatmap-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: #111;
        padding: 1rem;
        border-radius: 8px;
        color: white;
    }
    .canvas-wrapper {
        border: 1px solid #333;
        border-radius: 4px;
        overflow: hidden;
    }
    .entropy-stats {
        margin-top: 1rem;
        width: 100%;
        text-align: center;
    }
    .value {
        font-family: monospace;
        font-size: 1.5rem;
        color: gold;
        margin: 0.5rem 0;
    }
    .chart-container {
        width: 100%;
        height: 30px;
        margin-top: 0.5rem;
        background: #222;
        border-radius: 4px;
    }
</style>
