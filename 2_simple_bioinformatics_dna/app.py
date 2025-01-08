import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

# Count nucleotide in DNA
def DNA_nucleotide_count(seq):
    d = dict([
        ('A',seq.count('A')),
        ('T',seq.count('T')),
        ('G',seq.count('G')),
        ('C',seq.count('C'))
    ])
    return d

image = Image.open('dna-logo.jpg')


st.image(image, use_container_width=True)
st.write("""
# DNA Nucleotide Count Web App
This app counts the nucleotide composition of a query DNA
""")

st.header("Enter DNA Squence")


sequence_input = "GAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

squence = st.text_area("Squence Input", sequence_input, height=250)

squence = squence.splitlines()
squence = ''.join(squence)

st.write("***")

st.header("Input (DNA Query)")
squence

st.header("Output (DNA Nucleotide Count)")
st.subheader("1. Print Dictionary")

X = DNA_nucleotide_count(squence)
X

st.subheader('2. Print Text')
st.write('There are ' + str(X['A']) + ' adenine (A)')
st.write('There are ' + str(X['T']) + ' thymine (T)')
st.write('There are ' + str(X['G']) + ' guanine (G)')
st.write('There are ' + str(X['C']) + ' cytosine (C)')

st.subheader('3. Display Dataframe')
df = pd.DataFrame.from_dict(X,orient='index')

df.reset_index(inplace=True)
df.rename(columns={'index':'nucleotide', 0:'count'}, inplace=True)

st.write(df)

st.subheader("4. Display Bar Chart")
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',y='count'
)
p = p.properties(
    width=alt.Step(80) # Set the width of the bars
)
st.write(p)