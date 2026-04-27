# SteaMine: Finding Hidden Gems in Steam's Long Tail

Author: Nikitha Natarajan  
Course: CSCE 676 - Data Mining, Spring 2026

![SteaMine banner](./assets/steam-logo-welcome-banner.jpg)

![Python](https://img.shields.io/badge/Python-3.12.13-blue)
![Notebook](https://img.shields.io/badge/Main%20Artifact-main_notebook.ipynb-success)
![Status](https://img.shields.io/badge/Project-Final%20Deliverable-brightgreen)

SteaMine studies a core discovery paradox in the Steam marketplace: **many games are liked, but only a small fraction are seen**.  
Using game metadata, engagement features, and large-scale review language, the project explains why similarly tagged games can end up with very different outcomes, helps surface hidden gems, and highlights **tag-vs-reality** mismatches between store labels and player experience.

This can help developers and platforms better understand visibility gaps and improve discovery.

## Start here

- 👉 **Start here:** [**`main_notebook.ipynb`**](./main_notebook.ipynb)
- Checkpoint notebooks: [`checkpoints/checkpoint_1.ipynb`](./checkpoints/checkpoint_1.ipynb), [`checkpoints/checkpoint_2.ipynb`](./checkpoints/checkpoint_2.ipynb)
- Pitch video: https://youtu.be/_ceeB4O_iUM
- Environment: Google Colab, Python 3.12.13

---

## Table of contents

1. [What this project does](#what-this-project-does)  
2. [Research Questions](#research-questions)  
3. [Key insights](#key-insights)  
4. [Repository layout](#repository-layout)  
5. [Dataset](#dataset)  
6. [Final notebook (`main_notebook`) at a glance](#final-notebook-main_notebook-at-a-glance)  
7. [Research questions → methods → outputs](#research-questions--methods--outputs)  
8. [Key quantitative results (documented run)](#key-quantitative-results-documented-run)  
9. [Algorithms and libraries](#algorithms-and-libraries)  
10. [Environment, installation, and reproduction](#environment-installation-and-reproduction)  
11. [Preprocessing summary](#preprocessing-summary)  
12. [Limitations and future work](#limitations-and-future-work)  
13. [Deliverables and links](#deliverables-and-links)  
14. [Citation](#citation)

---

## Why this matters

On the merged sample, recommendation quality and visibility diverge sharply: a game can be well-reviewed and still nearly invisible.  
SteaMine turns that gap into measurable outputs that can be inspected by players, developers, and marketplace stakeholders.

### Long-tail problem (core motivation)

The key question behind this project is: **if many games are liked, why do so few capture attention?**  
That is the long-tail visibility problem this notebook quantifies and explains.

> In our documented run, the top 10% of games capture 99.1% of peak-CCU visibility.

![Long-tail visibility concentration](./assets/long-tail.png)

---

## What this project does

SteaMine is a single end-to-end notebook narrative that:

- Loads **Steam game metadata** (`games.json`) and **per-game review CSVs** from the Mendeley dataset.  
- **Merges** them on `app_id` so every downstream analysis uses the **same game universe**.  
- Runs **three analysis blocks** (genre association mining, engagement clustering, review topics + sentiment).  
- Produces **three user-facing interpretations**: **Hidden Gems Finder**, **Tag vs. Reality Checker**, and **Market Position View** (with fixed segment colors across plots).

The main notebook is reproducible (`RANDOM_STATE = 42` where randomness applies) and documents concrete metrics from a full run.

---

## Research Questions

- **RQ1:** Which genre combinations are associated with stronger recommendation context?
- **RQ2:** How do games split by visibility when ratings are similar?
- **RQ3:** How does review language differ from store-facing labels, especially for overlooked titles?

---

## Key insights

- Strong ratings alone do not guarantee visibility.
- Hidden gems can be identified systematically from high-recommendation, low-attention patterns.
- Tag-vs-reality gaps are observable in review language and sentiment.
- Combining rule mining, segmentation, and NLP gives a fuller explanation than any one metric alone.

---

## Repository layout

| Path | Role |
|------|------|
| **`main_notebook.ipynb`** | **Final curated narrative** - primary artifact this README describes. |
| `checkpoints/checkpoint_1.ipynb` | Checkpoint 1 - EDA, dataset choice, feasibility. |
| `checkpoints/checkpoint_2.ipynb` | Checkpoint 2 - research questions and method mapping. |
| `scripts/build_full_reviews_cache.py` | Preprocessing utility to build full review parquet cache from raw CSV files. |
| `requirements.txt` | Python dependencies for local or Colab-style runs. |
| `README.md` | This file. |

Final notebook lives at the repository root; checkpoint notebooks are in `checkpoints/`.

```text
.
|-- README.md                          <- you are here
|-- main_notebook.ipynb               <- final curated deliverable (run this)
|-- requirements.txt                  <- pinned Python environment for reproducibility
|-- .gitignore                        <- ignores data/cache/system files
|-- checkpoints/
|   |-- checkpoint_1.ipynb            <- Project Checkpoint 1 (early EDA/feasibility)
|   `-- checkpoint_2.ipynb            <- Project Checkpoint 2 (RQ/method progress)
|-- scripts/
|   `-- build_full_reviews_cache.py   <- preprocessing: CSVs -> full_reviews_clean.parquet
`-- assets/                           <- README visual assets
```

---

## Dataset

**Primary source:** *Steam Games Metadata and Player Reviews (2020–2024)*, **Mendeley Data**, DOI **[10.17632/jxy85cr3th.2](https://data.mendeley.com/datasets/jxy85cr3th/2)** (Abdelqader, 2025).

| Component | Contents |
|-----------|-----------|
| **`games.json`** | Per-game metadata: `app_id`, name, **genres**, price, playtime fields, **peak_ccu**, review counts, etc. On the order of **~65k** titles in the public metadata file. |
| **Review CSVs** | One file per game (typical naming: includes `app_id` in filename). Rows include **review text**, **recommend** flag, playtime at review, dates, helpfulness, etc. |

**Preprocessing step used in this repo:** raw review CSV files are consolidated with `scripts/build_full_reviews_cache.py` into `full_reviews_clean.parquet`, then merged with metadata on `app_id` for the final notebook analysis.

A **Google Drive mirror** for the dataset is linked inside the notebook’s opening markdown (same link as in the deliverable index).

**Google Drive mirror (project data folder):** [steam_project drive folder](https://drive.google.com/drive/folders/1F5trj8KWjBqw4-Y8zJFdnCAFIJ2M8nVO?usp=share_link)

---

## Final notebook (`main_notebook`) at a glance

`main_notebook.ipynb` is structured roughly as follows:

1. **Data setup** - load metadata + reviews, clean key fields, and build `analysis_df`.
2. **Analysis A (RQ1)** - Apriori/FP-Growth genre pattern mining.
3. **Analysis B (RQ2)** - K-Means engagement segmentation with silhouette diagnostics.
4. **Analysis C (RQ3)** - LDA + VADER for review-language and sentiment signals.
5. **System outputs** - Hidden Gems Finder, Tag vs Reality cards, and Market Position view.
6. **Conclusion** - key findings, limitations, and future work.

The notebook may assume **Google Colab** for `drive.mount` and optional `pip` installs; see [Reproduction](#environment-installation-and-reproduction) for running locally.

---

## Research questions → methods → outputs

| RQ | Question (short) | Lens | Algorithms | Primary outputs |
|----|------------------|------|--------------|-----------------|
| **RQ1** | Which **genre combinations** associate with stronger **recommendation** context? | Store **presentation** | **Apriori**, **FP-Growth** (frequent itemsets / association rules) | Supports **Tag vs. Reality** (**tag / storefront** side) |
| **RQ2** | How do games split by **visibility** when ratings look similar? | **Attention / engagement** | **K-Means** (k = 4), **StandardScaler**, silhouette diagnostics | **Market Position View**, **Hidden Gems Finder** |
| **RQ3** | How does **review language** differ from **store labels**, especially for overlooked titles? | Player **experience** | **LDA**, **VADER**, **langdetect** (optional) | **Tag vs. Reality** (**“reality”** side from reviews) |

**Design choice (cluster count):** silhouette is **higher** for **k = 2**, but **k = 4** is kept for **interpretability** - four segments map to the product story (Hidden / Niche / Mid / Blockbuster-like) instead of collapsing to "high vs. low engagement" only.

---

## Key quantitative results (documented run)

**Key takeaway:** Visibility is far more skewed than player satisfaction.

- **23,107** games analyzed and **31,692,774** review rows processed.
- Median game-level recommendation rate is **0.8421**.
- The top **10%** of games capture **99.1%** of total peak-CCU visibility.
- Quality and visibility are only weakly aligned (Spearman `rec_rate` vs `peak_ccu` is about **+0.22**).
- The Hidden Gems shortlist identifies **3,421** candidates in this run.

Full metrics and diagnostics remain in `main_notebook.ipynb`.

### Headline figure

The main takeaway is visible concentration: despite high approval levels, visibility remains highly skewed toward a small slice of the catalog.

![Market Position headline figure](./assets/market_position.png)

---

## Algorithms and libraries

- **Core:** Python 3.12.13, pandas, NumPy, SciPy
- **Visualization:** Matplotlib, Seaborn
- **Modeling:** scikit-learn (K-Means, CountVectorizer, LDA), mlxtend (Apriori/FP-Growth)
- **Text:** vaderSentiment, langdetect, NLTK

### Key dependencies and versions

- Python `3.12.13`
- pandas `>=1.5.0`
- scikit-learn `>=1.2.0`
- mlxtend `>=0.22.0`
- vaderSentiment `==3.3.2`

See `requirements.txt` for the full dependency list.

---

## Environment, installation, and reproduction

### 1. Clone and install

```bash
git clone https://github.com/Nikithanatarajan1312/steam-steamine.git
cd steam-steamine
pip install -r requirements.txt
python --version
```

This project was developed using **Google Colab** and documented with **Python 3.12.13**.

For **Colab**, `pip install -r requirements.txt` is still the recommended starting point.
In a fresh notebook runtime, a package such as `vaderSentiment` may still need a manual install if the environment has been reset.

### 2. Obtain data

Download **`games.json`** and the **review CSV collection** from [Mendeley](https://data.mendeley.com/datasets/jxy85cr3th/2) (or use the Drive mirror linked in the notebook).

### 3. Configure paths

In **`main_notebook.ipynb`**, set:

- `GAMES_PATH` - path to `games.json`  
- `REVIEWS_GLOB` - glob that matches all review CSVs (e.g. `/path/to/reviews/*.csv`)
- `FULL_REVIEW_CACHE_PATH` - full parquet cache path if you built it with the preprocessing script

If `app_id` is missing inside a CSV, the notebook can recover it from the **filename** (see loading cell).

### 4. Run

- **Colab:** mount Drive if needed, then **Run all**.  
- **Jupyter:** skip or adapt the `drive.mount` cell; ensure the same packages are installed.

**Reproducibility:** `RANDOM_STATE = 42` is used for clustering, LDA, and random subsampling where applicable.

### 5. Full-dataset preprocessing script (recommended)

To support full-dataset runs without repeatedly re-reading thousands of CSV files, this repo includes:

- `scripts/build_full_reviews_cache.py`

Run it once to build a reusable parquet cache:

```bash
python "scripts/build_full_reviews_cache.py" \
  --reviews-glob "/absolute/path/to/Game Reviews/*.csv" \
  --output "/absolute/path/to/full_reviews_clean.parquet"
```

Then set `FULL_REVIEW_CACHE_PATH` in `main_notebook.ipynb` and keep `USE_REVIEW_CACHE = True`.

## Preprocessing summary

- Metadata is normalized (`app_id` cleaned, numeric fields coerced, genres parsed).
- Reviews are standardized (`recommend` normalized to 0/1, invalid rows removed, text cleaned).
- The final notebook builds `analysis_df` by inner-joining metadata with per-game review aggregates (`rec_rate`, `review_count`).
- Feature prep then feeds RQ1 (transactions for association rules), RQ2 (scaled engagement features for K-Means), and RQ3 (vectorized text for LDA + VADER sentiment).

---

## Limitations and future work

### Limitations

- Results apply to the merged subset, not the full Steam catalog.
- The analysis is correlational, not causal.
- LDA topics and VADER sentiment are approximate and can miss gaming-specific language.
- Hidden Gems detection uses transparent heuristics, not a learned ranking model.

### Future work

- Add temporal analysis of review and engagement trends.
- Improve sentiment modeling with transformer-based approaches.
- Build a recommender extension or interactive demo.

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
| **Preprocessing script** | https://github.com/Nikithanatarajan1312/steam-steamine/blob/main/scripts/build_full_reviews_cache.py |

---

## Citation

When referencing the dataset:

**Abdelqader, Hisham (2025).** *Steam Games Metadata and Player Reviews (2020–2024).* Mendeley Data, V2. DOI: **10.17632/jxy85cr3th.2**.  
https://data.mendeley.com/datasets/jxy85cr3th/2
