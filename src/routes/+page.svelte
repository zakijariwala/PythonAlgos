<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import CanvasHeatmap from '$lib/components/CanvasHeatmap.svelte';
    import VectorSpacePlot from '$lib/components/VectorSpacePlot.svelte';
    import Formula from '$lib/components/Formula.svelte';

    let manifest: any = $state(null);
    let worker: Worker;
    
    // Worker state
    let isTraining = $state(false);
    let epoch = $state(0);
    let matrix: number[][] = $state([]);
    let entropy = $state(0);

    // Formula to display
    const attentionFormula = "\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V";

    onMount(async () => {
        try {
            const res = await fetch('/manifest.json');
            if (res.ok) {
                manifest = await res.json();
            }
        } catch (e) {
            console.error("Failed to load manifest", e);
        }

        // Initialize Web Worker
        worker = new Worker(new URL('$lib/workers/worker-transformer.ts', import.meta.url), { type: 'module' });
        
        worker.onmessage = (e) => {
            const { type, payload } = e.data;
            if (type === 'attention_update') {
                epoch = payload.epoch;
                matrix = payload.matrix;
                entropy = payload.entropy;
            }
        };
    });

    onDestroy(() => {
        if (worker) {
            worker.postMessage({ command: 'stop' });
            worker.terminate();
        }
    });

    function toggleTraining() {
        if (worker) {
            if (isTraining) {
                worker.postMessage({ command: 'stop' });
            } else {
                worker.postMessage({ command: 'start' });
            }
            isTraining = !isTraining;
        }
    }

    function resetTraining() {
        if (worker) {
            worker.postMessage({ command: 'reset' });
            epoch = 0;
            matrix = [];
            entropy = 0;
        }
    }
</script>

<svelte:head>
    <title>The Sentinel Visualizer</title>
</svelte:head>

<main class="dashboard">
    <header>
        <h1>The Sentinel Visualizer</h1>
        <p>Transformer & Attention Mechanism Explorer</p>
    </header>

    <div class="controls">
        <button class:active={isTraining} onclick={toggleTraining}>
            {isTraining ? 'Pause Training' : 'Start Training'}
        </button>
        <button onclick={resetTraining}>Reset</button>
        <span class="epoch">Epoch: {epoch}</span>
    </div>

    <div class="grid">
        <section class="card">
            <h2>Attention Matrix Heatmap</h2>
            <p class="desc">Real-time softmax distribution of Query × Key dot products.</p>
            <CanvasHeatmap {matrix} {entropy} {epoch} />
        </section>

        <section class="card">
            <h2>Embedding Vector Space (PCA)</h2>
            <p class="desc">3D visualization of token embeddings clustering as the model learns.</p>
            <VectorSpacePlot {epoch} />
        </section>

        <section class="card full-width">
            <h2>Scaled Dot-Product Attention</h2>
            <Formula formula={attentionFormula} />
            {#if manifest && manifest.length > 0}
                <div class="knowledge-base">
                    <h3>Parsed Knowledge Base (Python)</h3>
                    {#each manifest as file}
                        <div class="file-entry">
                            <strong>{file.file}</strong>
                            <ul>
                                {#each file.classes as cls}
                                    <li>
                                        <code>{cls.name}</code> 
                                        {#if cls.complexity}<span class="badge">{cls.complexity}</span>{/if}
                                        <p class="docstring">{cls.docstring}</p>
                                    </li>
                                {/each}
                            </ul>
                        </div>
                    {/each}
                </div>
            {/if}
        </section>
    </div>
</main>

<style>
    :global(body) {
        margin: 0;
        font-family: 'Inter', system-ui, sans-serif;
        background-color: #0a0a0a;
        color: #eaeaea;
    }
    
    .dashboard {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    header {
        text-align: center;
        margin-bottom: 2rem;
    }

    h1 {
        font-size: 2.5rem;
        background: linear-gradient(90deg, #ffd700, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .controls {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
        align-items: center;
    }

    button {
        background: #333;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
        transition: background 0.2s;
    }

    button:hover {
        background: #444;
    }

    button.active {
        background: #ffd700;
        color: #000;
    }

    .epoch {
        font-family: monospace;
        font-size: 1.2rem;
        color: #ffd700;
    }

    .grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
    }

    .card {
        background: #151515;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    }

    .full-width {
        grid-column: 1 / -1;
    }

    h2 {
        margin-top: 0;
        font-size: 1.25rem;
        color: #fff;
    }

    .desc {
        color: #aaa;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    .knowledge-base {
        margin-top: 2rem;
        border-top: 1px solid #333;
        padding-top: 1rem;
    }

    .file-entry {
        background: #111;
        padding: 1rem;
        border-radius: 6px;
        margin-top: 1rem;
    }

    .badge {
        background: #ff4500;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-family: monospace;
        margin-left: 0.5rem;
    }

    .docstring {
        font-size: 0.9rem;
        color: #888;
        white-space: pre-wrap;
        background: #000;
        padding: 0.5rem;
        border-radius: 4px;
        margin-top: 0.5rem;
    }
</style>
