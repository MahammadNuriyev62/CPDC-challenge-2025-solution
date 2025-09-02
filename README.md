# Commonsense Persona-Grounded Dialogue Challenge 2025 (In progress)

![diagram.png](./assets/diagram2.png)

Our approach leveraged Qwen3 as the base model due to its superior native tool-calling capabilities and well-defined interaction format. We decomposed the challenge into three specialized tasks—tool calling, direct dialogue, and dialogue with tool response integration—each handled by a dedicated Low-Rank Adaptation (LoRA) expert module, enabling efficient GPU utilization while maintaining high performance. The system was optimized using the Unsloth framework for accelerated training and inference, achieving response times of approximately 3 seconds while using less than 30GB of VRAM. To address the limited training data, we implemented a three-tier data augmentation strategy using GPT-o4-mini-high, expanding the dataset by nearly 300% through varying levels of linguistic and structural modifications while preserving core conversational patterns.

# References

- Public Leaderboard: https://www.aicrowd.com/challenges/commonsense-persona-grounded-dialogue-challenge-2025/leaderboards
- Winners Announcement: https://discourse.aicrowd.com/t/winners-call-for-paper/17412
