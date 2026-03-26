# DFT & Machine Learning Resources (Tsuji Lab / IGSES-Tsuji)

This repository curates learning materials, links, and notes related to **Density Functional Theory (DFT)** and **Machine Learning (ML) for materials / computational chemistry**. The content is primarily sourced from the public webpage maintained by **Tsuji Lab (IGSES-Tsuji)** and reorganized here for easier navigation.

- Primary source (upstream): https://sites.google.com/view/igses-tsuji/home

> Note: This repository is a curated compilation for learning purposes. If there is any discrepancy, please refer to the upstream page as the source of truth.

---

## Overview

- **DFT**: Entry points to core concepts and typical workflows (structure optimization, band structure / DOS, surfaces & defects, and post-processing).
- **Machine Learning**: Entry points to ML for property prediction, feature engineering, model training/evaluation, and ML interatomic potentials (if applicable).
- **Goal**: Provide a clear, searchable structure that reduces the barrier to getting started and helps with reproducibility.

---

## Source & Acknowledgement

Most of the referenced materials come from:

- **Tsuji Lab (IGSES-Tsuji)**: https://sites.google.com/view/igses-tsuji/home

Many thanks to Tsuji Lab for making these resources publicly available.

---

## Repository Structure

> The layout below is a suggested structure. Adjust this section to match your actual repository.

- `dft/` — DFT-related resources (concepts, tutorials, workflows, FAQs)
- `ml/` — ML-related resources (models, data, features, evaluation, potentials)
- `papers/` — Reading list and citations (recommended: store references/links rather than copyrighted PDFs)
- `notes/` — Study notes and summaries
- `scripts/` — Utility scripts (data processing, feature extraction, plotting, job automation, etc.)
- `examples/` — Reproducible examples (input templates, minimal working cases)
- `data/` — Dataset index and descriptions (for large files, consider Git LFS or external hosting)

---

## How to Use

1. Start with the upstream page for context and the full collection:  
   https://sites.google.com/view/igses-tsuji/home
2. Browse this repository by topic:
   - For DFT: begin with `dft/` and `examples/`
   - For ML: begin with `ml/` and `scripts/`
3. When adding a reproducible workflow/result:
   - Create a dedicated subfolder (e.g., `examples/<topic>/`)
   - Document dependencies, inputs, commands, outputs, and reference links

---

## Copyright & License

- This repository aims to include **links, bibliographic references, original notes, and original code/scripts**.
- If you plan to copy/mirror substantial upstream text or files, please verify upstream licensing/permission requirements and clearly attribute the source here.
- For any third-party content, add per-directory `LICENSE`/`NOTICE` files or explicit source statements.

> Recommendation: choose a license for your own contributions (e.g., MIT / Apache-2.0 / CC BY 4.0) and include a root-level `LICENSE`.

---

## Contributing

PRs are welcome, including:

- Fixing or adding links and short descriptions/tags
- Adding reproducible examples and utility scripts
- Adding FAQs / troubleshooting notes

If you want to add large datasets, prefer external download instructions + checksums, or use Git LFS.

---

## Contact

For upstream resource ownership, corrections, takedown, or attribution requests, please refer to the upstream page:  
https://sites.google.com/view/igses-tsuji/home