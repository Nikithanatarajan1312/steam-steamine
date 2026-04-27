#!/usr/bin/env python3
"""
Build a full-dataset review cache parquet from many Steam review CSV files.

Example:
python scripts/build_full_reviews_cache.py \
  --reviews-glob "/content/drive/MyDrive/steam_project/Game Reviews/*.csv" \
  --output "/content/drive/MyDrive/steam_project/full_reviews_clean.parquet"
"""

from __future__ import annotations

import argparse
import gc
import glob
import os
import re
import sys
import time
from typing import Optional

import pandas as pd


def normalize_recommend(value) -> Optional[int]:
    if pd.isna(value):
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)

    s = str(value).strip().lower()
    if s in {"true", "1", "yes", "recommended"}:
        return 1
    if s in {"false", "0", "no", "not recommended"}:
        return 0
    return None


def maybe_extract_app_id_from_filename(path: str) -> Optional[int]:
    stem = os.path.splitext(os.path.basename(path))[0]
    token = stem.split("_")[0].split(" ")[0]
    try:
        return int(token)
    except ValueError:
        m = re.match(r"^(\d+)", stem)
        return int(m.group(1)) if m else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build full reviews parquet cache.")
    parser.add_argument("--reviews-glob", required=True, help="Glob pattern for review CSV files.")
    parser.add_argument("--output", required=True, help="Output parquet path.")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=300,
        help="How many files to concatenate per in-memory batch.",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=500,
        help="Print progress every N files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    start = time.time()

    review_files = sorted(glob.glob(args.reviews_glob, recursive=True))
    if not review_files:
        print(f"No files found for glob: {args.reviews_glob}", file=sys.stderr)
        return 1

    print(f"Found {len(review_files):,} files. Building cache...")
    load_errors = 0
    buffer_parts = []
    review_batches = []

    for i, fp in enumerate(review_files, 1):
        try:
            part = pd.read_csv(
                fp,
                usecols=lambda c: c.strip().lower() in {"app_id", "review", "recommend"},
                low_memory=False,
            )
            part.columns = part.columns.str.strip().str.lower()

            if "app_id" not in part.columns:
                app_id = maybe_extract_app_id_from_filename(fp)
                if app_id is None:
                    continue
                part["app_id"] = app_id

            keep_cols = [c for c in ["app_id", "review", "recommend"] if c in part.columns]
            part = part[keep_cols]
            buffer_parts.append(part)
        except Exception:
            load_errors += 1
            continue

        if i % args.batch_size == 0:
            review_batches.append(pd.concat(buffer_parts, ignore_index=True))
            buffer_parts = []
            gc.collect()

        if i % args.progress_every == 0 or i == len(review_files):
            print(f"  Loaded {i:,}/{len(review_files):,} files")

    if buffer_parts:
        review_batches.append(pd.concat(buffer_parts, ignore_index=True))
        buffer_parts = []
        gc.collect()

    if not review_batches:
        print("No review rows were loaded.", file=sys.stderr)
        return 2

    df_reviews = pd.concat(review_batches, ignore_index=True)
    del review_batches
    gc.collect()

    for col in ["app_id", "review", "recommend"]:
        if col not in df_reviews.columns:
            print(f"Missing required column after load: {col}", file=sys.stderr)
            return 3

    df_reviews["recommend"] = df_reviews["recommend"].apply(normalize_recommend)
    df_reviews["app_id"] = pd.to_numeric(df_reviews["app_id"], errors="coerce")
    df_reviews_clean = df_reviews.dropna(subset=["app_id", "recommend"]).copy()
    df_reviews_clean["app_id"] = df_reviews_clean["app_id"].astype("int64")
    df_reviews_clean["recommend"] = df_reviews_clean["recommend"].astype("int8")
    df_reviews_clean["review"] = df_reviews_clean["review"].astype(str).str.strip()
    df_reviews_clean.loc[df_reviews_clean["review"].isin(["", "nan", "none"]), "review"] = pd.NA
    df_reviews_clean = df_reviews_clean.dropna(subset=["review"])

    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    df_reviews_clean.to_parquet(args.output, index=False)

    elapsed = (time.time() - start) / 60.0
    print(
        f"Saved {len(df_reviews_clean):,} rows to {args.output} "
        f"(errors skipped: {load_errors:,}, elapsed: {elapsed:.1f} min)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
