from rdkit import Chem
from rdkit.Chem import Descriptors, Draw
import random
import os

def generate_novel_molecule(base_smiles="CC(=O)OC1=CC=CC=C1C(=O)O"):
    try:
        mol = Chem.MolFromSmiles(base_smiles)
        if mol is None:
            return None, None, None, None
            
        variations = [
            "CC(=O)OC1=CC=C(F)C=C1C(=O)O", # Fluoro-aspirin
            "CC(=O)OC1=CC=C(O)C=C1C(=O)O", # Hydroxy-aspirin
            "CC(=O)OC1=CC=C(N)C=C1C(=O)O", # Amino-aspirin
            "CC(=O)OC1=CC=C(Cl)C=C1C(=O)O",# Chloro-aspirin
            "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O" # Ibuprofen-like
        ]
        
        novel_smiles = random.choice(variations)
        novel_mol = Chem.MolFromSmiles(novel_smiles)
        
        mol_weight = round(Descriptors.MolWt(novel_mol), 2)
        logp = round(Descriptors.MolLogP(novel_mol), 2)
        
        # Safely resolve path to the root assets folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # current is drug_hunting -> modules -> polymathix -> Polymathix (root)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        assets_dir = os.path.join(root_dir, "assets")
        os.makedirs(assets_dir, exist_ok=True)
        
        img_path = os.path.join(assets_dir, "generated_mol.png")
        Draw.MolToFile(novel_mol, img_path, size=(350, 350))
        
        return novel_smiles, mol_weight, logp, img_path
    except Exception as e:
        print(f"RDKit Backend Error: {e}")
        return None, None, None, None
