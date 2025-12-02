import streamlit as st
import pandas as pd
import requests
import random
import os

st.title("Boxer Profile:")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.normpath(os.path.join(BASE_DIR, "../../../data/processed/final_processed_data/boxing-match-fighters.csv"))

df = pd.read_csv(CSV_PATH)

def get_wikipedia_image(name):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{name.replace(' ', '_')}"
    
    headers = {
        "User-Agent": "BoxingETL/1.0 (mailto:gurvirsingdhillon@outlook.com)"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data for {name}")
        return None

    data = response.json()

    if "thumbnail" in data:
        return data["thumbnail"]["source"]
    else:
        return None


fighters_reunite = pd.concat([df['Boxer_A'], df['Boxer_B']], axis=0)
fighters_reunite = fighters_reunite.dropna().drop_duplicates().sort_values().tolist()

selected_fighter = st.selectbox("Select a Fighter", fighters_reunite)

if selected_fighter:
    st.subheader(f"{selected_fighter}")

    image_url = get_wikipedia_image(selected_fighter)

    if image_url:
        st.image(image_url, width=300)
    else:
        st.warning("Image not found on Wikipedia :(")

fighter_data = df[(df['Boxer_A'] == selected_fighter) | (df['Boxer_A'] == selected_fighter)]

# Filter fights involving selected fighter
fighter_df = df[(df['Boxer_A'] == selected_fighter) | (df['Boxer_B'] == selected_fighter)].copy()

# Identify which side the fighter was on for EACH row
fighter_df['is_A'] = fighter_df['Boxer_A'] == selected_fighter

# Wins
fighter_df['wins'] = fighter_df.apply(
    lambda row: row['won_A'] if row['is_A'] else row['won_B'],
    axis=1
)

# Losses
fighter_df['losses'] = fighter_df.apply(
    lambda row: row['lost_A'] if row['is_A'] else row['lost_B'],
    axis=1
)

# Draws
fighter_df['draws'] = fighter_df.apply(
    lambda row: row['drawn_A'] if row['is_A'] else row['drawn_B'],
    axis=1
)

# KOs
fighter_df['kos'] = fighter_df.apply(
    lambda row: row['kos_A'] if row['is_A'] else row['kos_B'],
    axis=1
)

# Physical attributes (height, reach, age, stance, weight_class)
fighter_df['height'] = fighter_df.apply(
    lambda row: row['height_A'] if row['is_A'] else row['height_B'],
    axis=1
)
fighter_df['reach'] = fighter_df.apply(
    lambda row: row['reach_A'] if row['is_A'] else row['reach_B'],
    axis=1
)
fighter_df['age'] = fighter_df.apply(
    lambda row: row['age_A'] if row['is_A'] else row['age_B'],
    axis=1
)
fighter_df['stance'] = fighter_df.apply(
    lambda row: row['stance_A'] if row['is_A'] else row['stance_B'],
    axis=1
)
fighter_df['weight_class'] = fighter_df.apply(
    lambda row: row['class_A'] if row['is_A'] else row['class_B'],
    axis=1
)

# Convert fight_date
fighter_df['fight_date'] = pd.to_datetime(fighter_df['Fight_Date'], errors='coerce')

# Sort by date ascending → last row = latest fight
fighter_df = fighter_df.sort_values('fight_date')

# Grab last fight row
last_fight = fighter_df.iloc[-1]


st.subheader(f"Fighter Profile: {selected_fighter}")

col1, col2, col3 = st.columns(3)
col1.metric("Wins", int(last_fight['wins']))
col2.metric("Losses", int(last_fight['losses']))
col3.metric("Draws", int(last_fight['draws']))

col4, col5, col6 = st.columns(3)
col4.metric("KOs", int(last_fight['kos']))
col5.metric("Age", int(last_fight['age']))
col6.metric("Stance", last_fight['stance'])

st.write(f"**Weight Class:** {last_fight['weight_class']}")
st.write(f"**Fight Date:** {last_fight['fight_date'].date()}")
