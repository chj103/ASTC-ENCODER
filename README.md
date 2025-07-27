# ASTC-ENCODER
An efficient implementation of the ASTC (Adaptive Scalable Texture Compression) Encoder for compressing high-quality image textures in embedded graphics applications.

About:
This project implements the ASTC compression algorithm, a modern texture compression format developed by ARM. ASTC allows scalable image compression with fine control over bitrate and quality, making it suitable for embedded GPUs, mobile SoCs, and graphics-intensive applications.

The encoder transforms raw image data into compressed ASTC blocks using a block-based encoding strategy, optimizing for visual fidelity and memory efficiency.

 Features:
-> Supports multiple block sizes (e.g., 4x4, 5x5, etc.)

-> Efficient encoding for RGBA images

-> Bitrate scalability with quality trade-offs

-> Suitable for embedded and real-time applications

-> Compatible with ARM GPUs and Vulkan/OpenGL
