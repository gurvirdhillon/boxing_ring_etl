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

total_fights = len(fighter_data)

random_row = fighter_data.sample(1).iloc[0]

if random_row['Boxer_A'] == selected_fighter:
    wins = random_row['won_A']
    losses = random_row['lost_A']
    draws = random_row['drawn_A']
    kos = random_row['kos_A']
    height = random_row['height_A']
    reach = random_row['reach_A']
    age = random_row['age_A']
    stance = random_row['stance_A']
    weight_class = random_row['class_A']
else:
    wins = random_row['won_B']
    losses = random_row['lost_B']
    draws = random_row['drawn_B']
    kos = random_row['kos_B']
    height = random_row['height_B']
    reach = random_row['reach_B']
    age = random_row['age_B']
    stance = random_row['stance_B']
    weight_class = random_row['class_B']

st.subheader(f"Fighter Profile: {selected_fighter}")

col1, col2, col3 = st.columns(3)
col1.metric("Wins", wins)
col2.metric("Losses", losses)
col3.metric("Draws", draws)

col4, col5, col6 = st.columns(3)
col4.metric("KOs", kos)
col5.metric("Height", f"{height} cm")
col6.metric("Age", f"{age}")
# col6.metric("Reach", f"{reach} cm")

st.write(f"**Weight Class:** {weight_class}")
st.write(f"**Stance:** {stance}")


