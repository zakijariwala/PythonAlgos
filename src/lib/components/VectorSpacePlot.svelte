<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import * as THREE from 'three';

    let { epoch = 0 } = $props();
    
    let container: HTMLDivElement;
    let scene: THREE.Scene;
    let camera: THREE.PerspectiveCamera;
    let renderer: THREE.WebGLRenderer;
    let points: THREE.Points;
    let animationId: number;

    const numPoints = 100;
    const basePositions = new Float32Array(numPoints * 3);
    const targetPositions = new Float32Array(numPoints * 3);

    for (let i = 0; i < numPoints * 3; i++) {
        basePositions[i] = (Math.random() - 0.5) * 10;
        const cluster = i % 2 === 0 ? 3 : -3;
        targetPositions[i] = (Math.random() - 0.5) * 2 + cluster;
    }

    onMount(() => {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 15;

        renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(basePositions), 3));

        const material = new THREE.PointsMaterial({ 
            color: 0xffd700,
            size: 0.2 
        });

        points = new THREE.Points(geometry, material);
        scene.add(points);

        const animate = () => {
            animationId = requestAnimationFrame(animate);
            
            points.rotation.x += 0.002;
            points.rotation.y += 0.005;

            const positions = points.geometry.attributes.position.array as Float32Array;
            const factor = Math.min(epoch / 200, 1.0);

            for (let i = 0; i < positions.length; i++) {
                positions[i] = basePositions[i] + (targetPositions[i] - basePositions[i]) * factor;
            }
            points.geometry.attributes.position.needsUpdate = true;

            renderer.render(scene, camera);
        };

        animate();

        const handleResize = () => {
            if (container) {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }
        };
        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    });

    onDestroy(() => {
        if (animationId) cancelAnimationFrame(animationId);
        if (renderer) renderer.dispose();
    });
</script>

<div class="vector-space-container" bind:this={container}>
</div>

<style>
    .vector-space-container {
        width: 100%;
        height: 300px;
        background: #111;
        border-radius: 8px;
        border: 1px solid #333;
    }
</style>
