import * as tf from '@tensorflow/tfjs';
import '@tensorflow/tfjs-backend-wasm';

// Ensure the WASM backend is set up
tf.setBackend('wasm').then(() => {
    console.log('TFJS using WASM backend');
}).catch(() => {
    // Fallback to webgl or cpu if wasm fails
    tf.setBackend('webgl').catch(() => tf.setBackend('cpu'));
});

// A simplified 2-layer, 4-head Transformer ("Minformer") implementation using TFJS
class Minformer {
    d_model: number;
    num_heads: number;
    d_k: number;
    seq_length: number;

    constructor(d_model = 64, num_heads = 4, seq_length = 16) {
        this.d_model = d_model;
        this.num_heads = num_heads;
        this.d_k = d_model / num_heads;
        this.seq_length = seq_length;
    }

    // A single attention block step simulating the forward pass to get Attention Matrix
    simulateAttention(epoch: number) {
        return tf.tidy(() => {
            // Generate random Q and K embeddings (simulating the weights)
            // As epoch increases, we simulate convergence by making the dot product more "peaky" (lower entropy)
            
            // Random base
            const q = tf.randomNormal([this.seq_length, this.d_k]);
            const k = tf.randomNormal([this.seq_length, this.d_k]);

            // Simulate training progress by artificially clustering keys and queries over time
            const convergence_factor = Math.min(epoch / 100, 1.0) * 5.0; // scale up to 5
            
            const scaled_q = q.mul(1 + convergence_factor);
            const scaled_k = k.mul(1 + convergence_factor);

            // Attention Score: (Q * K^T) / sqrt(d_k)
            const scores = tf.matMul(scaled_q, scaled_k, false, true).div(Math.sqrt(this.d_k));
            
            // Softmax
            const attention_matrix = tf.softmax(scores, -1);
            
            // Calculate Average Entropy
            // Entropy = -sum(p * log(p))
            const epsilon = 1e-9;
            const entropy = tf.sum(attention_matrix.mul(tf.log(attention_matrix.add(epsilon))).mul(-1), -1);
            const avg_entropy = entropy.mean().dataSync()[0];

            return {
                matrix: attention_matrix.arraySync(),
                entropy: avg_entropy
            };
        });
    }
}

const model = new Minformer();
let epoch = 0;
let isTraining = false;
let intervalId: any = null;

// Worker message handler
self.onmessage = (e) => {
    const { command } = e.data;
    
    if (command === 'start') {
        if (!isTraining) {
            isTraining = true;
            intervalId = setInterval(() => {
                const { matrix, entropy } = model.simulateAttention(epoch);
                // Send attention matrix back to main thread every 10th batch
                if (epoch % 10 === 0) {
                    self.postMessage({
                        type: 'attention_update',
                        payload: {
                            epoch,
                            matrix,
                            entropy
                        }
                    });
                }
                epoch++;
            }, 50); // 20 frames per second for training simulation
        }
    } else if (command === 'stop') {
        isTraining = false;
        if (intervalId) {
            clearInterval(intervalId);
            intervalId = null;
        }
    } else if (command === 'reset') {
        epoch = 0;
    }
};
