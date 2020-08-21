import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

st.title("Conditional Pitch Type Probabilities")
st.header("1. Select Team")
st.header("2. Select Pitcher")


trackman = pd.read_csv('cleanedTrackman.csv')  

def conditional_pitch_type_probabilities(df , team , pitcher):
    '''
    Using Trackman data, this displays the probabiility of pitch types for a given pitcher and team.
    
    RETURNS: Dataframe of pitch type distribution for all possible counts 
    '''
    team = df[df["PitcherTeam"] == team]
    df = team[df["Pitcher"] == pitcher]
    df = df.rename(columns={"TaggedPitchType":"PitchType"})
    x = df.groupby(["Count"]).count()["PitchType"]
    conditional = df.groupby('Count')['PitchType'].value_counts() / df.groupby('Count')['PitchType'].count()
    return conditional.unstack(level=1).fillna(0).transpose().round(2)

def highlight_max(s):
    '''
    highlight the maximum in a Series yellow.
    '''
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]

team = st.selectbox("Team", trackman.PitcherTeam.unique().tolist())

pitching_team = trackman[trackman["PitcherTeam"] == team]

player = st.selectbox("Pitcher", pitching_team.Pitcher.unique().tolist())


x = conditional_pitch_type_probabilities(trackman,team,player)
cm = sns.light_palette("red", as_cmap=True)
s = x.style.background_gradient(cmap=cm)

st.table(s)
st.write("Developed By: Tyler Nunez")