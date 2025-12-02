import streamlit as st
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.normpath(os.path.join(BASE_DIR, "../../../data/processed/final_processed_data/boxing-match-fighters.csv"))

df = pd.read_csv(CSV_PATH)

st.title("KO Leaders by Division")

a = df[[
    "Boxer_A",
    "Weight_Class",
    "kos_A",
    "won_A",
    "lost_A",
]].rename(columns={
    "Boxer_A": "Boxer",
    "Weight_Class": "Weight_Class",
    "kos_A": "kos",
    "won_A": "won",
    "lost_A": "lost"
})

b = df[[
    "Boxer_B",
    "Weight_Class",
    "kos_B",
    "won_B",
    "lost_B",
]].rename(columns={
    "Boxer_B": "Boxer",
    "Weight_Class": "Weight_Class",
    "kos_B": "kos",
    "won_B": "won",
    "lost_B": "lost"
})


# renaming the columns so they all can be classed as one^

# combining the fighters
fighters = pd.concat([a, b], ignore_index=True)
fighters = fighters.dropna(subset=["Boxer"]) # remove no values even though this was done in transformation, just for safe keeping

# keeping the best ko count for each of the fighters
fighters_agg = (
    fighters.groupby(["Boxer", "Weight_Class"])
            .agg({
                "won": "max",
                "kos": "max",
            }).reset_index()
)


# get the fighter with the most knock outs for every weight class
ko_leaders = (
    fighters_agg.sort_values("kos", ascending=False)
                .groupby("Weight_Class")
                .head(1)
                .sort_values("kos", ascending=False)
                .reset_index(drop=True)
)

st.dataframe(ko_leaders)

