import streamlit as st
import pandas as pd
import os

st.title("Top 5 Fighters per Division")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.normpath(os.path.join(BASE_DIR, "../../../data/processed/final_processed_data/boxing-match-fighters.csv"))

df = pd.read_csv(CSV_PATH)


required_cols = ["Boxer_A", "Boxer_B", "class_A", "class_B", "won_A", "won_B", "Fight_Date", "result"]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Dataset is missing required columns: {missing}")
    st.stop()


fighters_A = df.rename(columns={
    "Boxer_A": "Boxer",
    "class_A": "Division",
    "won_A": "Wins"
})[["Boxer", "Division", "Wins", "Fight_Date", "result"]]

fighters_B = df.rename(columns={
    "Boxer_B": "Boxer",
    "class_B": "Division",
    "won_B": "Wins"
})[["Boxer", "Division", "Wins", "Fight_Date", "result"]]

fighters = pd.concat([fighters_A, fighters_B], ignore_index=True)

fighters["Fight_Date"] = pd.to_datetime(fighters["Fight_Date"])

# gets the fighters latest record by date
latest = (
    fighters
    .sort_values("Fight_Date")
    .groupby("Boxer")
    .tail(1)
    .reset_index(drop=True)
)


def get_draw(x):
    return 1 if x == "draw" else 0


def get_loss(x):
    return 1 if x in ["win_A", "win_B"] else 0  # This is placeholder logic; you can refine it if needed.


latest["Draws"] = latest["result"].apply(get_draw)
latest["Losses"] = latest["result"].apply(get_loss)


latest["Score"] = latest["Wins"] * 3 + latest["Draws"] - latest["Losses"] * 2

# so for every win the fighters get 3 points (based loosely on the premier league scoring system),
# for draws they get one point and for losses they get reduction of two points 

all_divisions = sorted(latest["Division"].dropna().unique())

selected_division = st.selectbox("Select a Weight Division:", all_divisions)


division_fighters = (
    latest[latest["Division"] == selected_division]
    .sort_values(["Score", "Wins"], ascending=False)
    .head(5)
    .reset_index(drop=True)
)

st.subheader(f"Top 5 Fighters in {selected_division}")

st.dataframe(
    division_fighters[["Boxer", "Wins", "Losses", "Draws", "Score", "Fight_Date"]]
)



