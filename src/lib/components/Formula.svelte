<script lang="ts">
    import katex from 'katex';
    import 'katex/dist/katex.min.css';

    let { formula = '' } = $props();
    let container: HTMLDivElement;

    $effect(() => {
        if (container && formula) {
            katex.render(formula, container, {
                throwOnError: false,
                displayMode: true
            });
        }
    });
</script>

<div class="formula-container" bind:this={container}></div>

<style>
    .formula-container {
        font-size: 1.2rem;
        color: white;
        background: #1a1a1a;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #333;
        overflow-x: auto;
    }
</style>
