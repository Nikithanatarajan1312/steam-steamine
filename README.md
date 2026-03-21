# 🎮 SteaMine  
## Multi-Modal Data Mining and Engagement Analysis of Steam Games

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

---

## 📌 Project Overview

**SteaMine** is a comprehensive data mining project that explores structural, behavioral, and textual patterns in the Steam gaming marketplace using multi-modal analysis techniques. The project integrates game metadata with large-scale user reviews to uncover:

- 🎯 **Genre co-occurrence patterns** and their relationship to recommendation success
- 📊 **Engagement-based game clusters** revealing market segments from blockbusters to niche titles
- 💬 **Latent topics in review text** and their association with recommendation behavior
- 💰 **Price-engagement dynamics** across different game types
- 📈 **Temporal trends** in game releases and review activity

---

## 📂 Dataset

### Primary Source: Steam Games Metadata and Player Reviews (2020–2024)

**Source:** [Mendeley Data](https://data.mendeley.com/datasets/jxy85cr3th/2)  
**Citation:** Abdelqader, M. (2025). *Steam Games Metadata and Player Reviews Dataset*. Mendeley Data.

### 📊 Dataset Composition

| Component | Description | Size |
|-----------|-------------|------|
| **games.json** | Game metadata (genres, price, playtime, CCU, reviews) | 65,686 games |
| **Review CSVs** | User reviews (text, recommendation, playtime, date) | ~12.8M reviews total |
| **Analysis Sample** | Randomly sampled games for computational feasibility | 400 games, ~1.84M reviews |

### 📈 Sample Statistics (400-Game Analysis Set)

| Metric | Value |
|--------|-------|
| Total Games (Metadata) | 65,686 |
| Games in Sample | 400 |
| Total Reviews in Sample | 1,840,146 |
| Unique Reviewers | 1,401,918 |
| Unique Genres | 20 (in sample) |
| Positive Recommendation Rate | 82.27% |
| English-Only Reviews | 774,574 (47%) |
| Median Review Length | 14 words |
| Avg Genres per Game | 3.30 |

---

## 🎯 Research Questions

### RQ1: Genre Co-occurrence and Recommendation Success
**Task:** Frequent itemset mining / Association rule mining  
**Algorithms:** Apriori, FP-Growth (course techniques)  
**Metrics:** Support, confidence, lift, leverage, interpretability  

**Goal:** Identify which genre combinations are most strongly associated with high recommendation rates and engagement metrics.

### RQ2: Engagement-Based Game Segmentation
**Task:** Clustering  
**Algorithms:** k-Means, Hierarchical Clustering (course techniques)  
**Metrics:** Silhouette score, Davies-Bouldin index, cluster interpretability  

**Goal:** Discover latent market segments based on engagement (CCU, playtime) and analyze how price and genre composition differ across clusters.

### RQ3: Review Sentiment and Topic Modeling
**Task:** Sentiment analysis + Topic modeling  
**Algorithms:** VADER, Latent Dirichlet Allocation / LDA (external techniques)  
**Metrics:** VADER compound scores, topic coherence (Cv), perplexity  

**Goal:** Extract latent themes from review text and examine their relationship to recommendation behavior beyond what metadata alone reveals.

---

## 🔬 Key Findings (Checkpoint 2)

### Genre Structure
- **Average basket size:** 3.30 genres per game
- **Co-occurrence sparsity:** 0.54 (dense itemset space suitable for mining)
- **Most frequent pair:** Casual + Indie (20,511 occurrences)
- **Genre-outcome correlation:** 21% range in recommendation rates across genres

### Engagement Distribution
- **Zero-engagement games:** 69% have peak CCU = 0
- **High-engagement cluster:** Median CCU = 99, Median playtime = 536 mins
- **Price-engagement correlation:** Weak (ρ ≈ 0.15)
- **Optimal k for clustering:** 4 (separates Invisible/Niche/Mid-Tier/Blockbuster)

### Review Text Characteristics
- **Non-English content:** 23% of reviews (filtered for topic modeling)
- **VADER sentiment range:** -0.95 to +0.98
- **Topic coherence (LDA):** Cv = 0.37–0.40 (GOOD range)
- **Processing time:** 15 seconds for 10K reviews (scalable)

### Feasibility Validation
- ✅ **Apriori vs FP-Growth:** Identical outputs (32 itemsets, 74 rules at support=0.10)
- ✅ **k-Means clustering:** Silhouette score ≈ 0.36 (acceptable structure)
- ✅ **LDA scalability:** Tested on 1K/5K/10K samples, coherence stable across sizes

---

## 🔄 Project Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    Data Acquisition                      │
│  • Download games.json + review CSVs from Mendeley      │
│  • Sample 400 games (seed=42) for analysis              │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│              Data Preprocessing & Cleaning               │
│  • Standardize column names                             │
│  • Convert types (price, playtime, recommend)           │
│  • Parse genres into lists                              │
│  • Filter non-ASCII text for topic modeling             │
│  • Remove duplicates                                     │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│                   Data Integration                       │
│  • Merge games.json + review CSVs on app_id             │
│  • Validate merge quality (0% data loss)                │
│  • Create game-level aggregates                         │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│            Exploratory Data Analysis (EDA)               │
│  • Distribution analysis (price, CCU, playtime)         │
│  • Genre co-occurrence patterns                          │
│  • Sentiment distribution (VADER)                        │
│  • Language detection                                    │
│  • Zero-engagement analysis                              │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│              Feasibility Testing (CP2)                   │
│  • RQ1: Apriori vs FP-Growth comparison                 │
│  • RQ2: k-Means clustering (k=3, k=4)                   │
│  • RQ3: LDA scalability test (1K/5K/10K samples)        │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│         Research Question Formation (CP2) ✅             │
│  • Define 3 research questions                           │
│  • Map to course/external techniques                     │
│  • Validate feasibility with code                        │
│  • Plan methodology for CP3                              │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│          Full Analysis & Modeling (CP3) 🔜               │
│  • Execute full RQ1 analysis (association rules)         │
│  • Execute full RQ2 analysis (clustering)                │
│  • Execute full RQ3 analysis (sentiment + topics)        │
│  • Cross-validate results                                │
│  • Generate insights and recommendations                 │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab
- 8GB+ RAM recommended (for full dataset processing)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/steammine.git
cd steammine
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn \
            mlxtend gensim nltk vaderSentiment langdetect \
            jupyter notebook
```

### 3. Download Dataset
1. Visit [Mendeley Data](https://data.mendeley.com/datasets/jxy85cr3th/2)
2. Download `games.json` and review CSVs
3. Place in `data/` directory:
   ```
   data/
   ├── games.json
   └── reviews/
       ├── 10_reviews.csv
       ├── 20_reviews.csv
       └── ...
   ```

### 4. (Optional) Download NLTK Data
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

---

## 🚀 Usage

### Run Checkpoint 2 Notebook (Current)
```bash
jupyter notebook notebooks/steammine_cp2.ipynb
```

### For Google Colab Users
1. Upload notebook to Google Drive
2. Mount Drive in Colab:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
3. Update `BASE_PATH` in notebook to your Drive location

### Quick Start (Minimal Example)
```python
import pandas as pd
import json

# Load game metadata
with open('data/games.json', 'r') as f:
    games = pd.DataFrame(json.load(f))

# Load sample reviews
reviews = pd.read_csv('data/reviews/10_reviews.csv')

# Check data
print(f"Games: {len(games):,}")
print(f"Reviews: {len(reviews):,}")
```

---

## 📊 Reproducibility

### Controlled Randomness
All random operations use fixed seeds for reproducibility:
- **Sample selection:** `seed=42`
- **k-Means clustering:** `random_state=42`
- **LDA topic modeling:** `random_state=42`
- **Train/test splits:** `random_state=42`

### Computational Environment
```
Python: 3.10+
Pandas: 1.5+
NumPy: 1.23+
Scikit-learn: 1.2+
Gensim: 4.3+
MLxtend: 0.22+
```

### Sample Size Justification
- **Full dataset:** 65,686 games with 12.8M+ reviews
- **Analysis sample:** 400 games (~0.6% of total)
- **Rationale:** Balances computational feasibility with statistical power
- **Validation:** Sample characteristics match population distributions

---

## 📈 Key Techniques & Algorithms

### Course Techniques
| Technique | Algorithm | Library | Use Case |
|-----------|-----------|---------|----------|
| **Frequent Itemsets** | Apriori, FP-Growth | mlxtend | RQ1: Genre patterns |
| **Clustering** | k-Means, Hierarchical | scikit-learn | RQ2: Game segments |

### External Techniques
| Technique | Algorithm | Library | Use Case |
|-----------|-----------|---------|----------|
| **Sentiment Analysis** | VADER | vaderSentiment | RQ3: Review polarity |
| **Topic Modeling** | LDA | gensim | RQ3: Review themes |
| **Language Detection** | langdetect | langdetect | RQ3: Text filtering |

### Evaluation Metrics
- **Association Rules:** Support, confidence, lift, leverage
- **Clustering:** Silhouette score, Davies-Bouldin index
- **Topic Modeling:** Coherence (Cv), perplexity
- **Sentiment:** VADER compound scores (-1 to +1)
  
---

## 📊 Sample Outputs

### Association Rules (RQ1 Preview)
```
{RPG, Indie, Action} → {Adventure}
  Support: 0.128
  Confidence: 0.878
  Lift: 1.956
```

### Cluster Profiles (RQ2 Preview)
```
Cluster 1 (Invisible): CCU=0, Playtime=0, Rec=57.9%
Cluster 2 (Niche):     CCU=0, Playtime=0, Rec=84.9%
Cluster 3 (Mid-Tier):  CCU=7, Playtime=89, Rec=75.8%
Cluster 4 (Blockbuster): CCU=212, Playtime=1050, Rec=80.5%
```

### Topic Example (RQ3 Preview)
```
Positive Review Topic 1:
  fun, great, amazing, love, story, hours, playing

Negative Review Topic 1:
  bad, dead, boring, waste, refund, broken, bugs
```

---
