import math

class ScaledDotProductAttention:
    """
    Computes scaled dot-product attention.
    Time Complexity: O(N^2 * D) where N is sequence length and D is embedding dimension.
    """
    def __init__(self, d_k):
        self.d_k = d_k

    def forward(self, query, key, value):
        # [Visualizable Point: Attention Scores]
        # Calculate raw attention scores
        scores = (query @ key.transpose()) / math.sqrt(self.d_k)
        
        # [Visualizable Point: Softmax]
        # Apply softmax to get attention weights
        attention_weights = self.softmax(scores)
        
        # [Visualizable Point: Context Vector]
        # Multiply weights by value
        context = attention_weights @ value
        return context, attention_weights

    def softmax(self, x):
        # Dummy softmax for illustration
        return x

class MinformerBlock:
    """
    A minimal Transformer block with Multi-Head Attention and Feed-Forward.
    Time Complexity: O(N^2 * D + N * D^2)
    """
    def __init__(self, d_model, num_heads):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.attention = ScaledDotProductAttention(self.d_k)

    def forward(self, x):
        # [Visualizable Point: QKV Projection]
        # In a real model, x is projected to Q, K, V
        q, k, v = x, x, x
        
        context, attn = self.attention.forward(q, k, v)
        return context
