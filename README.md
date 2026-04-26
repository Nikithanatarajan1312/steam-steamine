# SteaMine

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Notebook](https://img.shields.io/badge/Main%20Artifact-main_notebook.ipynb-success)
![Status](https://img.shields.io/badge/Project-Final%20Deliverable-brightgreen)

SteaMine studies a core discovery paradox in the Steam marketplace: **many games are liked, but only a small fraction are seen**.  
Using game metadata, engagement features, and large-scale review language, the project explains **why similarly tagged games can end up with very different outcomes**.

## Start here

- Main deliverable: **`main_notebook.ipynb`**
- Checkpoint notebooks: `checkpoints/checkpoint_1.ipynb`, `checkpoints/checkpoint_2.ipynb`
- Pitch video: https://youtu.be/_ceeB4O_iUM

---

## Table of contents

1. [What this project does](#what-this-project-does)  
2. [Motivation in one paragraph](#motivation-in-one-paragraph)  
3. [Repository layout](#repository-layout)  
4. [Dataset](#dataset)  
5. [Final notebook (`main_notebook`) at a glance](#final-notebook-main_notebook-at-a-glance)  
6. [Research questions → methods → outputs](#research-questions--methods--outputs)  
7. [Key quantitative results (documented run)](#key-quantitative-results-documented-run)  
8. [Algorithms and libraries](#algorithms-and-libraries)  
9. [Environment, installation, and reproduction](#environment-installation-and-reproduction)  
10. [Preprocessing summary](#preprocessing-summary)  
11. [Limitations and future work](#limitations-and-future-work)  
12. [Deliverables and links](#deliverables-and-links)  
13. [Citation](#citation)  
14. [License and acknowledgements](#license-and-acknowledgements)

---

## Why this matters

On the merged sample, recommendation quality and visibility diverge sharply: a game can be well-reviewed and still nearly invisible.  
SteaMine turns that gap into measurable outputs that can be inspected by players, developers, and marketplace stakeholders.

### Long-tail problem (core motivation)

The key question behind this project is: **if many games are liked, why do so few capture attention?**  
That is the long-tail visibility problem this notebook quantifies and explains.

> In our documented run, the top 10% of games capture roughly 97% of peak-CCU visibility.

![Steam store home share view](./images/store_home_share.jpg)

---

## Visual highlights

Below are supporting visuals for the discovery context and recommendation ecosystem that this analysis investigates.

| Marketplace context | Recommendation context |
|---|---|
| ![Popular Steam games panel](./images/popular_steam_games.jpeg) | ![Steam recommendation panel](./images/steam_rec.jpeg) |
| ![Players like you love panel](./images/players_like_you_love.jpeg) | ![Recommendation algorithm panel](./images/steam_rec_algo_based.png) |

For quantitative project outputs (long-tail histogram, segment map, and tag-vs-reality analysis plots), see `main_notebook.ipynb`.

---

## What this project does

SteaMine is a single end-to-end notebook narrative that:

- Loads **Steam game metadata** (`games.json`) and **per-game review CSVs** from the Mendeley dataset.  
- **Merges** them on `app_id` so every downstream analysis uses the **same game universe**.  
- Runs **three analysis blocks** (genre association mining, engagement clustering, review topics + sentiment).  
- Produces **three user-facing interpretations**: **Hidden Gems Finder**, **Tag vs. Reality Checker**, and **Market Position View** (with fixed segment colors across plots).

The main notebook is reproducible (`RANDOM_STATE = 42` where randomness applies) and documents concrete metrics from a full run.

---

## Motivation in one paragraph

On the merged sample in `main_notebook.ipynb`, the **median game-level recommendation rate is about 0.80**, yet **peak concurrent users (CCU)** are extremely concentrated: roughly **the top 10% of games account for about 97% of total peak-CCU "visibility"** in that sample. So "mostly positive" does **not** mean fairly distributed attention. SteaMine turns that inequality into **measurable segments**, **association patterns**, and **review-language themes**, then packages them into outputs a reader or stakeholder can **inspect** (rules and charts), not just a single aggregate score.

---

## Repository layout

| Path | Role |
|------|------|
| **`main_notebook.ipynb`** | **Final curated narrative** — primary artifact this README describes. |
| `checkpoints/checkpoint_1.ipynb` | Checkpoint 1 — EDA, dataset choice, feasibility. |
| `checkpoints/checkpoint_2.ipynb` | Checkpoint 2 — research questions and method mapping. |
| `requirements.txt` | Python dependencies for local or Colab-style runs. |
| `README.md` | This file. |

Final notebook lives at the repository root; checkpoint notebooks are in `checkpoints/`.

---

## Dataset

**Primary source:** *Steam Games Metadata and Player Reviews (2020–2024)*, **Mendeley Data**, DOI **[10.17632/jxy85cr3th.2](https://data.mendeley.com/datasets/jxy85cr3th/2)** (Abdelqader, 2025).

| Component | Contents |
|-----------|-----------|
| **`games.json`** | Per-game metadata: `app_id`, name, **genres**, price, playtime fields, **peak_ccu**, review counts, etc. On the order of **~65k** titles in the public metadata file. |
| **Review CSVs** | One file per game (typical naming: includes `app_id` in filename). Rows include **review text**, **recommend** flag, playtime at review, dates, helpfulness, etc. |

**Important:** numbers quoted in `main_notebook.ipynb` refer to that notebook's documented merge: after loading and cleaning, it documents ~6.64M review rows and an inner merge leaving 1,318 games that appear in both loaded reviews and metadata. If you load more or fewer review files, counts change - always cite the run you executed.

A **Google Drive mirror** for the dataset is linked inside the notebook’s opening markdown (same link as in the deliverable index).

---

## Final notebook (`main_notebook`) at a glance

`main_notebook.ipynb` is structured roughly as follows:

1. **Data and reproducible setup** — paths (`GAMES_PATH`, `REVIEWS_GLOB`), load `games.json`, glob and concatenate review CSVs, clean types, parse genres, normalize `recommend`, build `analysis_df` (inner merge + per-game `rec_rate` / `review_count`).  
2. **Analysis A — Genre pattern signals (RQ1)** — genre baskets → **Apriori** and **FP-Growth** (mlxtend), rule tables and lift/confidence visuals.  
3. **Analysis B — Engagement segments (RQ2)** — scale features → **K-Means** with **k = 4**, silhouette sweep for k = 2…6, segment labels (**Hidden / Niche / Mid / Blockbuster-like**), segment-colored scatter plots.  
4. **Analysis C — Tag vs. reality (RQ3)** — English-oriented text filters, **LDA** (scikit-learn) on bag-of-words, **VADER** sentiment by recommend label and by segment; per-game / case-study style comparisons (e.g. **Evergate vs. Factorio** in the narrative).  
5. **System outputs** — **Hidden Gems Finder** (rule-based shortlist), **Tag vs. Reality** cards, **Market Position** figure with hidden-gem overlay.  
6. **Conclusion, limitations, future work** — consolidated bullets and roadmap.

The notebook may assume **Google Colab** for `drive.mount` and optional `pip` installs; see [Reproduction](#environment-installation-and-reproduction) for running locally.

---

## Research questions → methods → outputs

| RQ | Question (short) | Lens | Algorithms | Primary outputs |
|----|------------------|------|--------------|-----------------|
| **RQ1** | Which **genre combinations** associate with stronger **recommendation** context? | Store **presentation** | **Apriori**, **FP-Growth** (frequent itemsets / association rules) | Supports **Tag vs. Reality** (**tag / storefront** side) |
| **RQ2** | How do games split by **visibility** when ratings look similar? | **Attention / engagement** | **K-Means** (k = 4), **StandardScaler**, silhouette diagnostics | **Market Position View**, **Hidden Gems Finder** |
| **RQ3** | How does **review language** differ from **store labels**, especially for overlooked titles? | Player **experience** | **LDA**, **VADER**, **langdetect** (optional) | **Tag vs. Reality** (**“reality”** side from reviews) |

**Design choice (cluster count):** silhouette is **higher** for **k = 2**, but **k = 4** is kept for **interpretability** — four segments map to the product story (Hidden / Niche / Mid / Blockbuster-like) instead of collapsing to “high vs. low engagement” only.

---

## Key quantitative results (documented run)

Figures below match the documented run inside `main_notebook.ipynb` (your merge may differ if file coverage differs).

| Topic | Approximate value (from `main_notebook.ipynb`) |
|-------|-------------------------------|
| Games after inner merge | **1,318** |
| Review rows loaded & cleaned | **~6.64M** |
| Median game-level `rec_rate` | **~0.802** |
| Top 10% of games’ share of total peak CCU | **~97.**% (visibility concentration) |
| Spearman: `rec_rate` vs `peak_ccu` | **~+0.22** |
| Spearman: `rec_rate` vs `average_playtime_forever` | **~+0.08** |
| K-Means k | **4**; silhouette (this run) | **~0.313** |
| RQ1: Apriori vs FP-Growth | **Identical** frequent itemsets at `min_support = 0.10`; **58** rules with lift ≥ 1.0 |
| Strongest rule (example) | `{Action, RPG} → {Adventure}` — **lift ~1.65**, **confidence ~0.75** |
| Hidden segment size | **564 / 1,318** games (~**43%**); median `rec_rate` **~0.86** with near-zero visibility |
| Hidden Gems shortlist (this run) | **154** candidates (transparent percentile rules in notebook) |

**LDA:** four topics are used as a **readable snapshot** (reactions/friction, product state, social positivity, design pillars — see notebook interpretation). **VADER:** recommended vs not-recommended distributions separate clearly in the documented plots; segment-level means are reported in the closing section.

---

## Algorithms and libraries

- **Core:** Python 3.x, **pandas**, **NumPy**, **SciPy**  
- **Plots:** **Matplotlib**, **Seaborn**  
- **Mining / ML:** **scikit-learn** (K-Means, scaling, `CountVectorizer`, `LatentDirichletAllocation`), **mlxtend** (Apriori / FP-Growth, `TransactionEncoder`)  
- **NLP:** **VADER** (`vaderSentiment`), **langdetect**, **NLTK** stopword lists where used  

See `requirements.txt` for minimum package versions.

---

## Environment, installation, and reproduction

### 1. Clone and install

```bash
git clone https://github.com/Nikithanatarajan1312/steam-steamine.git
cd steam-steamine
pip install -r requirements.txt
```

For **Colab**, the notebook’s second code cell installs `langdetect`, `vaderSentiment`, and `mlxtend` if the Colab runtime is detected.

### 2. Obtain data

Download **`games.json`** and the **review CSV collection** from [Mendeley](https://data.mendeley.com/datasets/jxy85cr3th/2) (or use the Drive mirror linked in the notebook).

### 3. Configure paths

In **`main_notebook.ipynb`**, set:

- `GAMES_PATH` — path to `games.json`  
- `REVIEWS_GLOB` — glob that matches all review CSVs (e.g. `/path/to/reviews/*.csv`)

If `app_id` is missing inside a CSV, the notebook can recover it from the **filename** (see loading cell).

### 4. Run

- **Colab:** mount Drive if needed, then **Run all**.  
- **Jupyter:** skip or adapt the `drive.mount` cell; ensure the same packages are installed.

**Reproducibility:** `RANDOM_STATE = 42` is used for clustering, LDA, and random subsampling where applicable.

**Full vs. partial text pipeline:** the imports cell defines **`USE_FULL_TEXT_PIPELINE`**. When **`False`**, language filtering / LDA / VADER use **documented row caps** for faster iteration. When **`True`**, the notebook is intended to process **all eligible review rows** for those steps (expect **longer wall time** and higher memory use).

**Hardware:** no GPU or paid API is required for the **documented** pipeline; a machine with **enough RAM** for ~6M+ rows in pandas is recommended for a **full** text pass.

---

## Preprocessing summary

- **Metadata:** normalize columns, parse **genres** into sorted unique lists, coerce numeric fields, `dropna` / dedupe on `app_id`.  
- **Reviews:** lowercase column names, enforce required columns, normalize **`recommend`** to {0, 1}, drop rows missing `app_id` or `recommend`, strip review text.  
- **Merge:** aggregate **`rec_rate`** and **`review_count`** per `app_id`, **inner-merge** onto `games` → **`analysis_df`**.  
- **RQ1:** each game’s genre list encoded as a **transaction** (`TransactionEncoder`) for itemset mining.  
- **RQ2:** features typically include **log-scaled** engagement fields plus price and `rec_rate`; **StandardScaler** before K-Means.  
- **RQ3:** length thresholds, optional English filter, **CountVectorizer** + **LDA**; **VADER** on review strings (truncated per scorer’s usual practice in code).

---

## Limitations and future work

Summarized from Section 8 of `main_notebook.ipynb` (not exhaustive):

- **Coverage:** results generalize to the **merged subset** (games with both metadata and loaded review files), not the entire Steam catalog.  
- **Association, not causation:** correlations and segments; not a causal identification of why a title is “Hidden.”  
- **LDA / lexicon:** topics are **qualitative**; some tokens can be noisy; VADER is **not** gaming-slang-tuned.  
- **Hidden Gems rules:** **transparent heuristics** (e.g. high `rec_rate` vs low `peak_ccu` by percentiles), not a learned ranker.  
- **Static snapshot:** not a time-series model of launch, updates, or seasonality.

**Future work** (from the same section) includes scaling to the full metadata catalog, stratified or transformer-based sentiment, temporal analysis on review dates, causal-style comparisons, recommender integration, and a small **Streamlit / Gradio** demo.

---

## Deliverables and links

| Item | URL |
|------|-----|
| **GitHub** | https://github.com/Nikithanatarajan1312/steam-steamine |
| **Pitch video (~2 min)** | https://youtu.be/_ceeB4O_iUM |
| **Dataset (Mendeley)** | https://data.mendeley.com/datasets/jxy85cr3th/2 |
| **Main notebook** | https://github.com/Nikithanatarajan1312/steam-steamine/blob/main/main_notebook.ipynb |
| **Checkpoint 1** | https://github.com/Nikithanatarajan1312/steam-steamine/blob/main/checkpoints/checkpoint_1.ipynb |
| **Checkpoint 2** | https://github.com/Nikithanatarajan1312/steam-steamine/blob/main/checkpoints/checkpoint_2.ipynb |

---

## Citation

When referencing the dataset:

**Abdelqader, Hisham (2025).** *Steam Games Metadata and Player Reviews (2020–2024).* Mendeley Data, V2. DOI: **10.17632/jxy85cr3th.2**.  
https://data.mendeley.com/datasets/jxy85cr3th/2

---

## License and acknowledgements

Add a **LICENSE** file to this repository if you intend open redistribution; the notebook's **Collaboration Declaration** lists documentation sources (mlxtend, scikit-learn, VADER, langdetect, Mendeley) and discloses use of AI tools for brainstorming, debugging, and narrative polish - see the end of `main_notebook.ipynb` for the exact wording.

---

*This README is written to match `main_notebook.ipynb` as the authoritative final narrative. If major outputs or paths change after a new run, update the key quantitative results and path sections accordingly.*
