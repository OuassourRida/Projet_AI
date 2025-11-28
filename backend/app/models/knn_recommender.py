"""Simple recommender utilities.

This module provides a lightweight recommendation function used by the
backend for prototyping. It computes average ratings per hotel and returns
the top-rated hotels excluding any provided by the user input.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from functools import lru_cache


def _data_path(name: str) -> Path:
   # project root is three levels above this file: /Projet_AI
   base = Path(__file__).resolve().parents[3]
   return base / 'data' / name


@lru_cache(maxsize=1)
def load_tables():
   hotels_path = _data_path('hotels.csv')
   ratings_path = _data_path('ratings.csv')
   hotels = pd.read_csv(hotels_path)
   ratings = pd.read_csv(ratings_path)
   return hotels, ratings


def _match_input_to_ids(inputs, hotels_df):
   """Return a set of hotel_id matched by either exact id or name substring."""
   matched = set()
   for item in inputs:
      if not item:
         continue
      s = str(item).strip()
      # If it looks like an id (starts with H and digits), match by hotel_id
      if s.upper().startswith('H') and any(ch.isdigit() for ch in s):
         rows = hotels_df[hotels_df['hotel_id'].str.upper() == s.upper()]
         for hid in rows['hotel_id'].tolist():
            matched.add(hid)
      else:
         # match by name (nom) case-insensitive substring
         rows = hotels_df[hotels_df['nom'].str.contains(s, case=False, na=False)]
         for hid in rows['hotel_id'].tolist():
            matched.add(hid)
   return matched


def recommend(inputs, top_k=10):
   """Return top_k recommended hotels as a list of dicts.

   - `inputs` can be an iterable of hotel ids or names supplied by the user.
   - The function excludes any hotels that match the input set.
   - Recommendations are the hotels with highest average rating.
   """
   hotels_df, ratings_df = load_tables()

   # compute average rating per hotel_id
   avg = ratings_df.groupby('hotel_id', as_index=False)['rating'].mean()
   avg.rename(columns={'rating': 'avg_rating'}, inplace=True)

   # merge with hotels to get names and metadata
   merged = pd.merge(hotels_df, avg, how='left', left_on='hotel_id', right_on='hotel_id')
   merged['avg_rating'] = merged['avg_rating'].fillna(0)

   # identify inputs to exclude
   exclude_ids = _match_input_to_ids(inputs or [], hotels_df)

   # filter out excluded ids
   candidates = merged[~merged['hotel_id'].isin(exclude_ids)].copy()

   # sort by average rating desc, then by hotel_id for determinism
   candidates.sort_values(['avg_rating', 'hotel_id'], ascending=[False, True], inplace=True)

   # build result list
   result = []
   for _, row in candidates.head(top_k).iterrows():
      result.append({
         'id': row.get('hotel_id'),
         'name': row.get('nom'),
         'category': row.get('categorie'),
         'location': row.get('localisation'),
         'price': row.get('prix'),
         'stars': row.get('etoiles'),
         'avg_rating': float(np.round(row.get('avg_rating', 0.0), 2)),
      })
   return result
