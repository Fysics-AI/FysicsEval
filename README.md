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

The following table reports aggregated model performance on **FysicsEval**. `Reasoning×20` shows the original reasoning score scaled by 20. `Average` is the mean of `Prediction`, `Reasoning×20`, and `Understanding`. The table is sorted by `Average` (descending).

| Model                         | Size | Prediction | Reasoning×20 | Understanding | Average |
|:------------------------------|:----:|:----------:|:------------:|:-------------:|:-------:|
| GPT-5                        |  -   | 40.30       | 69.60        | 89.90          | 66.60   |
| **OmniFysics (Ours)**                   | 3B   | 32.60       | 64.40        | 94.70          | 63.90   |
| Gemini-2.5-flash             |  -   | 19.80       | 62.00        | 89.40          | 57.07   |
| Qwen3-VL-8B-Instruct         | 8B   | 20.10       | 53.00        | 90.10          | 54.40   |
| Ovis2.5                      | 2B   | 20.40       | 49.20        | 89.50          | 53.03   |
| SAIL-VL2                     | 2B   | 21.90       | 51.60        | 84.70          | 52.73   |
| Claude-4.5-Haiku             |  -   | 35.30       | 57.80        | 60.30          | 51.13   |
| InternVL3.5-8B               | 8B   | 21.70       | 50.60        | 80.70          | 51.00   |
| Qwen2.5-Omni                 | 3B   | 18.10       | 34.20        | 87.50          | 46.60   |

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

