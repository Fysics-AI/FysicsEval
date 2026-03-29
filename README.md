<p align="center" width="100%">
<a target="_blank"><img src="assets/fudan-fysics.jpg" alt="" style="width: 75%; min-width: 200px; display: block; margin: auto;"></a>
</p>

<div align="center">
<br>
<h1>FysicsEval: A Unified Benchmark for Physical Perception, Prediction, Reasoning, and Understanding</h1>

<h5 align="center"> If you like our project, please give us a star ⭐ on GitHub for the latest update.</h5>


<font size=7><div align='center' >
[[🏠 Project Page](https://github.com/Fysics-AI/FysicsEval)]
[[📖 Paper](https://arxiv.org/pdf/2602.07064)]
[[🤗 Dataset](https://huggingface.co/datasets/Fysics-AI/FysicsEval)]
[[🏆 Leaderboard](#leaderboard_link)]
[[🀄 中文版](README_zh.md)]
</div></font>

</div>

##  🚀   News
- **`2026-02-09`** We release **FysicsEval**, a unified benchmark for physical perception, prediction, reasoning, and understanding.

## 🎯  Overview
Existing physics benchmarks predominantly target theoretical problem-solving or qualitative scenario analysis, limiting their scope to intuitive physics or question-answering proficiency, which are insufficient for the next generation of generalist Physical AI designed to interact with physical reality. To address this gap, **FysicsEval** emphasizes quantitative prediction and reasoning grounded in physical laws, aiming to meet the demands of generalist models interacting with the physical world.

<img src="assets/bmk.png" width="100%" height="100%">


**FysicsEval** is a focused benchmark designed to measure multimodal models' abilities in physical perception, quantitative prediction, explainable reasoning, and cross-modal physical understanding. Compared to prior datasets that concentrate on qualitative intuition or isolated domains, **FysicsEval** emphasizes rigorous, multi-granular evaluation across three core capabilities:

- Quantitative prediction of physical attributes from real-world multimodal evidence.
- Interpretable physical reasoning grounded in conservation laws and causal mechanics.
- Cross-modal physical-consistency understanding and physical-hallucination detection.


## 🔮 Composition and Task Taxonomy

**FysicsEval** contains 3,854 samples and 3,781 real-world images, spanning rigid bodies, soft bodies, and fluids, and an 11-category attribute space including *stiffness, density, mass, static/kinetic friction coefficients, restitution, Young’s modulus, Poisson’s ratio, viscosity, surface tension, and yield stress*. **FysicsEval** provides three complementary tasks to probe physical intelligence:

- **Perception & Prediction of Physical Attributes** — quantitative numeric prediction.
- **Explainable Physical Reasoning** — open-ended question and answer.
- **Cross-modal Physical Consistent Understanding** — MCQs for physically inconsistent statements understanding.

Queries are diversified (numeric prediction, open-ended, MCQ) and stratified into three difficulty levels to prevent memorization and encourage robust generalization.

## 🔍 Evaluation Protocols

- Physical attribute predictions are scored with Mean Relative Accuracy (MRA).
- Consistency understanding uses standard accuracy on MCQs.
- Open-ended reasoning is judged by an LLM-based rubric across six dimensions (semantic consistency, parameter precision, causal validity, mechanism identification, chain completeness, quantitative–qualitative alignment). GPT-5 is used as the standardized automated judge under a fixed prompt and scoring protocol.
- All evaluation scripts and scoring protocols are shown in `metrics`.


## 🏆 Leaderboard <a id="leaderboard_link"></a>
**MedMCBench** 评测基准在线排行榜，评测结果定期更新，评测指标为 Accuracy (%)。
| 模型                          | 模型类型 | 平均分 | 多项选择题 | 是非判断题 | 开放式问题 |
|:------------------------------|:----:|:-------:|:----------:|:------------:|:-------------:|
| GPT-5  🥇                         | Closed-source | 66.73   | 67.95      | 69.83        | 62.41         |
| Gemini 3 Flash  🥈                | Closed-source | 58.62   | 58.60      | 65.15        | 52.10         |
| GLM-4.6V-106B  🥉               | Open-source   | 56.79   | 56.86      | 63.16        | 50.35         |
| Kimi K2.5                     | Open-source   | 56.75   | 58.65      | 61.75        | 49.85         |
| Qwen3-VL-32B-Instruct         | Open-source   | 55.52   | 55.49      | 61.85        | 49.22         |
| Gemini 2.5 Flash              | Closed-source | 54.68   | 54.90      | 61.30        | 47.85         |
| Qwen2.5-VL-32B-Instruct       | Open-source   | 52.88   | 53.75      | 57.24        | 47.65         |
| Seed-1.6                      | Closed-source | 49.62   | 49.80      | 56.45        | 42.62         |
| Qwen3-VL-7B-Instruct          | Open-source   | 47.32   | 47.30      | 54.12        | 40.55         |
| Qwen2.5-VL-7B-Instruct        | Open-source   | 45.74   | 45.91      | 52.61        | 38.70         |
| LLaVA-Med-7B                  | Open-source   | 38.47   | 38.55      | 45.60        | 31.25         |
| Med-Flamingo                  | Open-source   | 33.48   | 34.27      | 41.35        | 24.83         |
| LLaVA-NeXT-7B                 | Open-source   | 33.07   | 33.82      | 40.25        | 25.15         |
| LLaVA-1.5-7B                  | Open-source   | 29.25   | 29.65      | 36.40        | 21.71         |


Notes:

- `Prediction`: Mean Relative Accuracy (higher is better).
- `Reasoning×20`: original `Reasoning` score × 20. (original `Reasoning` is score from 1 to 5)
- `Understanding`: MCQ accuracy in percent (higher is better).
- `Average` = mean(`Prediction`, `Reasoning×20`, `Understanding`).


## 🕹️ Usage

1. Download the dataset from [**here**](https://huggingface.co/datasets/Fysics-AI/FysicsEval). QA files are shown in `data`
2. Run your model and evaluate outputs following the scripts in `metrics`.

## 📖 Citation
If you use **FysicsEval** in your work, please cite:

```bibtex
@article{han2026exploringphysical,
    title={Exploring Physical Intelligence Emergence via Omni-Modal Architecture and Physical Data Engine},
    author={Han, Minghao and Yang, Dingkang and Jiang, Yue and Liu, Yizhou and Zhang, Lihua},
    journal={arXiv preprint arXiv:2602.07064},
    year={2026}
}
```

