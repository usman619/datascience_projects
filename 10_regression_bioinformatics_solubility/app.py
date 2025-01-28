import streamlit as st
import pandas as pd
import numpy as np
import pickle
from rdkit import Chem
from rdkit.Chem import Descriptors

# Creates a list of boolean values indicating whether each atom in the molecule is aromatic.
# Counts the number of aromatic atoms.
# Calculates the total number of heavy atoms in the molecule.
# Computes the ratio of aromatic atoms to heavy atoms.
# Returns this ratio.

def AromaticProportion(m):

    aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
    aa_count = []

    for i in aromatic_atoms:
        if i == True:
            aa_count.append(1)
    
    AromaticAtom = sum(aa_count)
    HeavyAtom = Descriptors.HeavyAtomCount(m)

    AR = AromaticAtom/HeavyAtom

    return AR

# Input: Takes a list of SMILES strings.
# Initialization: Initializes an empty list moldata to store molecule objects.
# Molecule Conversion: Converts each SMILES string into a molecule object (mol) using Chem.MolFromSmiles and appends it to moldata.
# Descriptor Calculation: For each molecule, calculates four molecular descriptors: MolLogP, MolWt, NumRotatableBonds, and AromaticProportion.
# Data Aggregation: Stores the descriptors in a NumPy array and then in a Pandas DataFrame with appropriate column names, which is returned as the result.

def generate(smiles, verbose=False):
    moldata = []
    for elem in smiles:
        mol = Chem.MolFromSmiles(elem)
        moldata.append(mol)
    
    baseData = np.arange(1,1)

    i = 0
    for mol in moldata:
        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_MolWt = Descriptors.MolWt(mol)
        desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
        desc_AromaticProportion = AromaticProportion(mol)

        row = np.array([
            desc_MolLogP,
            desc_MolWt,
            desc_NumRotatableBonds,
            desc_AromaticProportion
        ])

        if i == 0:
            baseData = row
        else:
            baseData = np.vstack([baseData,row])
        i = i + 1
    
    columnNames=['MolLogP', 'MolWt', 'NumRotatableBonds', 'AromaticProportion']
    descriptors = pd.DataFrame(data = baseData, columns = columnNames)

    return descriptors

st.title('Bioinformatics Solubility Prediction App')

st.sidebar.header('User Input Parameter')

SMILES_input = "NCCCC\nCCC\nCN"

SMILES = st.sidebar.text_area("SMILES Input", SMILES_input)
SMILES = "C\n" + SMILES
SMILES = SMILES.split('\n')

st.header('Input SMILES')
SMILES[1:]

st.header('Computed Molecular Descriptors')
X = generate(SMILES)
X[1:]

# Importing the Model
load_model = pickle.load(open('solubility_model.pkl', 'rb'))

predication = load_model.predict(X)

st.header('Predicted LogS values')
predication[1:]