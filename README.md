# SteaMine: Multi-Modal Data Mining and Engagement Analysis of Steam
# 🎮 SteaMine  
## Multi-Modal Data Mining and Engagement Analysis of Steam

---

## 📌 Overview

**SteaMine** explores structural, behavioral, and textual patterns in the Steam gaming marketplace using data mining techniques.  

Game metadata is integrated with large-scale user reviews to analyze:

- 📊 Popularity and engagement concentration  
- 🛒 Genre structure (market basket analysis)  
- 💰 Price vs engagement relationships  
- 📝 Review sentiment imbalance  
- 📅 Temporal growth trends  

All preprocessing and analytical decisions are documented and justified within the notebook.

---

## 📂 Dataset

### Primary Dataset: Steam (Metadata + Reviews)

🔗 Steam dataset (Mendeley Data):  
https://data.mendeley.com/datasets/jxy85cr3th/2  

### 📊 Local Run Scale

| Metric | Value |
|--------|-------|
| Total Games (Metadata) | 65,686 |
| Total Reviews | 1,840,146 |
| Games with Review Data | 399 |
| Unique Users | 1,401,918 |
| Unique Genres | 30 |
| Positive Recommendation Rate | 82.27% |

---

## 🔄 Project Workflow

```text
Data Loading
      ↓
Data Cleaning & Type Fixing
      ↓
Merge Metadata + Reviews
      ↓
Exploratory Data Analysis
      ↓
Market Basket & Genre Structure
      ↓
Correlation & Temporal Analysis
      ↓
Insights & Research Direction
```

## 🔁 Reproducibility

### Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Run Notebook

```bash
jupyter notebook steam_eda.ipynb
```
