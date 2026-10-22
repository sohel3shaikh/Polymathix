import math
import os
import json

def generate_perovskite_srtio3():
    """
    Generates cubic Perovskite SrTiO3 (Strontium Titanate) unit cell.
    Space group: Pm-3m (No. 221), a = 3.905 Angstroms
    Sr at corners (0,0,0), Ti at body center (0.5, 0.5, 0.5), O at face centers.
    """
    a = 3.905
    atoms = []
    
    # 8 Sr corners (scaled to 1 corner representation or full 2x2x2 cluster)
    # Generating 2x2x2 supercell for stunning visual representation
    for i in [0, 1]:
        for j in [0, 1]:
            for k in [0, 1]:
                atoms.append({
                    "x": (i - 0.5) * a,
                    "y": (j - 0.5) * a,
                    "z": (k - 0.5) * a,
                    "elem": "Sr",
                    "name": f"Sr_{i}{j}{k}"
                })
    
    # 1 Ti body center
    atoms.append({"x": 0.0, "y": 0.0, "z": 0.0, "elem": "Ti", "name": "Ti_center"})

    # 6 O face centers (coordinating to Ti)
    half = a / 2.0
    face_centers = [
        (half, 0, 0), (-half, 0, 0),
        (0, half, 0), (0, -half, 0),
        (0, 0, half), (0, 0, -half)
    ]
    for idx, (ox, oy, oz) in enumerate(face_centers):
        atoms.append({"x": ox, "y": oy, "z": oz, "elem": "O", "name": f"O_{idx+1}"})

    # Ti-O Octahedral bonds and Sr-O coordination bonds
    bonds = []
    ti_idx = 8 # Ti_center is index 8
    for o_idx in range(9, 15):
        bonds.append({"from": ti_idx, "to": o_idx, "order": 2})

    # Corner Sr connections to nearest Oxygen
    for sr_idx in range(8):
        sr = atoms[sr_idx]
        for o_idx in range(9, 15):
            o = atoms[o_idx]
            d = math.hypot(sr["x"] - o["x"], sr["y"] - o["y"], sr["z"] - o["z"])
            if d < a * 0.8:
                bonds.append({"from": sr_idx, "to": o_idx, "order": 1})

    return {
        "pdb_name": "Strontium Titanate (SrTiO3 Perovskite)",
        "atom_count": len(atoms),
        "residue_count": 1,
        "resolution": "Cubic Unit Cell (Pm-3m, a=3.905 Å)",
        "is_small_molecule": True,
        "is_material": True,
        "ca_coords": [],
        "atoms": atoms,
        "bonds": bonds,
        "sequence": [{"id": 1, "name": "SrTiO3"}],
        "helices": [],
        "sheets": [],
        "ssbonds": [],
        "hydration_waters": [],
        "binding_residues": [],
        "ligand": {
            "name": "SrTiO3 Perovskite",
            "formula": "SrTiO3",
            "mw": "183.49 g/mol",
            "cutoff": "Unit Cell Lattice",
            "show": True
        },
        "properties": {
            "Material Class": "Perovskite Oxide (Cubic)",
            "Chemical Formula": "SrTiO3",
            "Space Group": "Pm-3m (No. 221)",
            "Lattice Parameter (a)": "3.905 Å (α=β=γ=90°)",
            "Bandgap (Optical)": "3.25 eV (Direct/Indirect)",
            "Dielectric Constant (εr)": "~300 (Room Temp)",
            "Coordination": "Ti: Octahedral (CN=6), Sr: Cuboctahedral (CN=12)",
            "Total Lattice Atoms": f"{len(atoms)} atoms ({len(bonds)} coordination bonds)",
            "Applications": "Dielectrics, Superconducting Substrates, Photocatalysis"
        }
    }

def generate_graphene_sheet():
    """
    Generates 2D Graphene hexagonal honeycomb lattice (4x4 rings, 32 Carbon atoms).
    C-C bond distance = 1.42 Angstroms.
    """
    a_cc = 1.42
    atoms = []
    bonds = []
    
    # Generate hexagonal honeycomb coordinates
    rows = 4
    cols = 4
    dx = a_cc * math.sqrt(3)
    dy = a_cc * 1.5

    pts = []
    for r in range(rows):
        for c in range(cols):
            x0 = c * dx + (r % 2) * (dx / 2.0)
            y0 = r * dy
            pts.append((x0, y0))
            pts.append((x0, y0 + a_cc))

    # Remove duplicates and center
    unique_pts = []
    for p in pts:
        if not any(math.hypot(p[0] - u[0], p[1] - u[1]) < 0.2 for u in unique_pts):
            unique_pts.append(p)

    avg_x = sum(p[0] for p in unique_pts) / len(unique_pts)
    avg_y = sum(p[1] for p in unique_pts) / len(unique_pts)

    for idx, (px, py) in enumerate(unique_pts):
        atoms.append({
            "x": round(px - avg_x, 3),
            "y": round(py - avg_y, 3),
            "z": 0.0,
            "elem": "C",
            "name": f"C_{idx+1}"
        })

    # Covalent sp2 bonds (distance ~ 1.42 A)
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            d = math.hypot(atoms[i]["x"] - atoms[j]["x"], atoms[i]["y"] - atoms[j]["y"])
            if 1.2 <= d <= 1.6:
                bonds.append({"from": i, "to": j, "order": 1})

    return {
        "pdb_name": "Graphene Monolayer (sp2 2D Carbon Lattice)",
        "atom_count": len(atoms),
        "residue_count": 1,
        "resolution": "Honeycomb 2D Lattice (C-C = 1.42 Å)",
        "is_small_molecule": True,
        "is_material": True,
        "ca_coords": [],
        "atoms": atoms,
        "bonds": bonds,
        "sequence": [{"id": 1, "name": "GRAPH"}],
        "helices": [],
        "sheets": [],
        "ssbonds": [],
        "hydration_waters": [],
        "binding_residues": [],
        "ligand": {
            "name": "Graphene Sheet",
            "formula": f"C{len(atoms)}",
            "mw": f"{len(atoms) * 12.011:.1f} g/mol",
            "cutoff": "2D Monolayer",
            "show": True
        },
        "properties": {
            "Material Class": "2D Dirac Semimetal",
            "Chemical Formula": f"C{len(atoms)} (sp² Carbon)",
            "Lattice Symmetry": "Hexagonal Honeycomb (P6/mmm)",
            "C-C Bond Length": "1.42 Å",
            "Thermal Conductivity": "~5,000 W/m·K",
            "Carrier Mobility": ">200,000 cm²/V·s",
            "Young's Modulus": "1.0 TPa",
            "Total Lattice Atoms": f"{len(atoms)} atoms ({len(bonds)} sp² bonds)",
            "Applications": "Quantum Electronics, Nanofiltration Membranes, Energy Storage"
        }
    }

def generate_carbon_nanotube_swcnt():
    """
    Generates (5,5) Armchair Single-Walled Carbon Nanotube (SWCNT).
    Radius ~ 3.39 Angstroms.
    """
    n = 5
    a_cc = 1.42
    r_cnt = (a_cc * math.sqrt(3) * n) / (2.0 * math.pi) # ~ 3.39 A
    length_layers = 6
    atoms = []
    bonds = []

    for layer in range(length_layers):
        z = (layer - length_layers / 2.0) * (a_cc * 1.5)
        phase = (math.pi / n) if (layer % 2 == 1) else 0.0
        for i in range(2 * n):
            theta = (i * math.pi / n) + phase
            x = r_cnt * math.cos(theta)
            y = r_cnt * math.sin(theta)
            atoms.append({
                "x": round(x, 3),
                "y": round(y, 3),
                "z": round(z, 3),
                "elem": "C",
                "name": f"C{len(atoms)+1}"
            })

    # Bonds
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            d = math.hypot(
                atoms[i]["x"] - atoms[j]["x"],
                atoms[i]["y"] - atoms[j]["y"],
                atoms[i]["z"] - atoms[j]["z"]
            )
            if 1.2 <= d <= 1.65:
                bonds.append({"from": i, "to": j, "order": 1})

    return {
        "pdb_name": "Carbon Nanotube (5,5 Armchair SWCNT)",
        "atom_count": len(atoms),
        "residue_count": 1,
        "resolution": "Chiral (5,5) Cylinder (Radius=3.39 Å)",
        "is_small_molecule": True,
        "is_material": True,
        "ca_coords": [],
        "atoms": atoms,
        "bonds": bonds,
        "sequence": [{"id": 1, "name": "SWCNT"}],
        "helices": [],
        "sheets": [],
        "ssbonds": [],
        "hydration_waters": [],
        "binding_residues": [],
        "ligand": {
            "name": "(5,5) Armchair SWCNT",
            "formula": f"C{len(atoms)}",
            "mw": f"{len(atoms) * 12.011:.1f} g/mol",
            "cutoff": "Nanotube Hollow Cavity",
            "show": True
        },
        "properties": {
            "Material Class": "1D Cylindrical Carbon Allotrope",
            "Chirality Indices": "(n=5, m=5) Armchair (Metallic)",
            "Tube Diameter": "6.78 Å (0.68 nm)",
            "Electronic State": "Ballistic Metallic Conductor",
            "Tensile Strength": "~100 GPa",
            "Total Lattice Atoms": f"{len(atoms)} atoms ({len(bonds)} covalent bonds)",
            "Applications": "Nanoelectronics, Targeted Drug Delivery, Composite Reinforcement"
        }
    }

def generate_tio2_anatase():
    """
    Generates Anatase TiO2 photocatalyst unit cluster.
    """
    a = 3.784
    c = 9.515
    atoms = [
        {"x": 0.0, "y": 0.0, "z": 0.0, "elem": "Ti", "name": "Ti1"},
        {"x": a/2, "y": a/2, "z": c/4, "elem": "Ti", "name": "Ti2"},
        {"x": 0.0, "y": a/2, "z": c/8, "elem": "O", "name": "O1"},
        {"x": a/2, "y": 0.0, "z": -c/8, "elem": "O", "name": "O2"},
        {"x": 0.0, "y": -a/2, "z": c/8, "elem": "O", "name": "O3"},
        {"x": -a/2, "y": 0.0, "z": -c/8, "elem": "O", "name": "O4"},
        {"x": 0.0, "y": 0.0, "z": c/2, "elem": "Ti", "name": "Ti3"},
        {"x": a/2, "y": a/2, "z": 3*c/4, "elem": "Ti", "name": "Ti4"},
        {"x": 0.0, "y": a/2, "z": 5*c/8, "elem": "O", "name": "O5"},
        {"x": a/2, "y": 0.0, "z": 3*c/8, "elem": "O", "name": "O6"}
    ]
    avg_x = sum(a["x"] for a in atoms) / len(atoms)
    avg_y = sum(a["y"] for a in atoms) / len(atoms)
    avg_z = sum(a["z"] for a in atoms) / len(atoms)
    for a in atoms:
        a["x"] = round(a["x"] - avg_x, 3)
        a["y"] = round(a["y"] - avg_y, 3)
        a["z"] = round(a["z"] - avg_z, 3)

    bonds = []
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            d = math.hypot(atoms[i]["x"] - atoms[j]["x"], atoms[i]["y"] - atoms[j]["y"], atoms[i]["z"] - atoms[j]["z"])
            if 1.7 <= d <= 2.35 and atoms[i]["elem"] != atoms[j]["elem"]:
                bonds.append({"from": i, "to": j, "order": 1})

    return {
        "pdb_name": "Titanium Dioxide (Anatase TiO2 Photocatalyst)",
        "atom_count": len(atoms),
        "residue_count": 1,
        "resolution": "Tetragonal (I4_1/amd, a=3.78 Å, c=9.51 Å)",
        "is_small_molecule": True,
        "is_material": True,
        "ca_coords": [],
        "atoms": atoms,
        "bonds": bonds,
        "sequence": [{"id": 1, "name": "TiO2"}],
        "helices": [],
        "sheets": [],
        "ssbonds": [],
        "hydration_waters": [],
        "binding_residues": [],
        "ligand": {
            "name": "Anatase TiO2",
            "formula": "TiO2",
            "mw": "79.87 g/mol",
            "cutoff": "Tetragonal Octahedral Network",
            "show": True
        },
        "properties": {
            "Material Class": "Transition Metal Oxide Photocatalyst",
            "Crystal System": "Tetragonal (I4_1/amd)",
            "Lattice Parameters": "a=b=3.784 Å, c=9.515 Å",
            "Bandgap": "3.20 eV (Ultraviolet Absorber)",
            "Coordination": "Ti: 6 (Distorted Octahedron), O: 3 (Trigonal Planar)",
            "Total Lattice Atoms": f"{len(atoms)} atoms ({len(bonds)} Ti-O bonds)",
            "Applications": "Photocatalytic Water Splitting, Solar Cells, Self-Cleaning Surfaces"
        }
    }

def generate_mof_5_cluster():
    """
    Generates Metal-Organic Framework MOF-5 (IRMOF-1) secondary building unit (Zn4O tetrahedral core with terephthalate arms).
    """
    atoms = [
        {"x": 0.0, "y": 0.0, "z": 0.0, "elem": "O", "name": "O_core"},
        {"x": 1.65, "y": 0.95, "z": 0.0, "elem": "Zn", "name": "Zn1"},
        {"x": -1.65, "y": 0.95, "z": 0.0, "elem": "Zn", "name": "Zn2"},
        {"x": 0.0, "y": -1.90, "z": 0.0, "elem": "Zn", "name": "Zn3"},
        {"x": 0.0, "y": 0.0, "z": 1.95, "elem": "Zn", "name": "Zn4"},
        # Organic terephthalate carboxylate oxygens
        {"x": 3.10, "y": 1.70, "z": 0.5, "elem": "O", "name": "O_b1"},
        {"x": 3.10, "y": 1.70, "z": -0.5, "elem": "O", "name": "O_b2"},
        {"x": -3.10, "y": 1.70, "z": 0.5, "elem": "O", "name": "O_b3"},
        {"x": -3.10, "y": 1.70, "z": -0.5, "elem": "O", "name": "O_b4"},
        {"x": 0.0, "y": -3.40, "z": 0.7, "elem": "O", "name": "O_b5"},
        {"x": 0.0, "y": -3.40, "z": -0.7, "elem": "O", "name": "O_b6"},
        # BDC Carbon benzene ring skeleton
        {"x": 4.30, "y": 2.40, "z": 0.0, "elem": "C", "name": "C_carboxyl"},
        {"x": 5.40, "y": 3.00, "z": 0.0, "elem": "C", "name": "C_ar1"},
        {"x": 6.60, "y": 2.40, "z": 0.0, "elem": "C", "name": "C_ar2"},
        {"x": 7.70, "y": 3.00, "z": 0.0, "elem": "C", "name": "C_ar3"},
        {"x": 7.70, "y": 4.30, "z": 0.0, "elem": "C", "name": "C_ar4"}
    ]
    bonds = [
        {"from": 0, "to": 1, "order": 1},
        {"from": 0, "to": 2, "order": 1},
        {"from": 0, "to": 3, "order": 1},
        {"from": 0, "to": 4, "order": 1},
        {"from": 1, "to": 5, "order": 1},
        {"from": 1, "to": 6, "order": 1},
        {"from": 2, "to": 7, "order": 1},
        {"from": 2, "to": 8, "order": 1},
        {"from": 3, "to": 9, "order": 1},
        {"from": 3, "to": 10, "order": 1},
        {"from": 5, "to": 11, "order": 1},
        {"from": 6, "to": 11, "order": 2},
        {"from": 11, "to": 12, "order": 1},
        {"from": 12, "to": 13, "order": 2},
        {"from": 13, "to": 14, "order": 1},
        {"from": 14, "to": 15, "order": 2}
    ]

    return {
        "pdb_name": "MOF-5 (Metal-Organic Framework SBU)",
        "atom_count": len(atoms),
        "residue_count": 1,
        "resolution": "Zn4O(BDC)3 Porous Nanocage",
        "is_small_molecule": True,
        "is_material": True,
        "ca_coords": [],
        "atoms": atoms,
        "bonds": bonds,
        "sequence": [{"id": 1, "name": "MOF5"}],
        "helices": [],
        "sheets": [],
        "ssbonds": [],
        "hydration_waters": [],
        "binding_residues": [],
        "ligand": {
            "name": "MOF-5 SBU",
            "formula": "Zn4O(C8H4O4)3",
            "mw": "770.86 g/mol",
            "cutoff": "Nanoporous MOF Node",
            "show": True
        },
        "properties": {
            "Material Class": "Metal-Organic Framework (MOF)",
            "Secondary Building Unit": "Zn4O(CO2)6 Octahedral Cluster",
            "Linker": "1,4-Benzenedicarboxylate (BDC / Terephthalate)",
            "BET Surface Area": "2,900 - 3,500 m²/g",
            "Pore Diameter": "11.2 Å & 18.5 Å (Dual Micropores)",
            "Porosity": "79% Void Fraction",
            "Total SBU Atoms": f"{len(atoms)} atoms ({len(bonds)} coordination & covalent bonds)",
            "Applications": "Hydrogen & Methane Storage, Carbon Dioxide Capture, Catalysis"
        }
    }

MATERIALS_REGISTRY = {
    "perovskite": generate_perovskite_srtio3,
    "srtio3": generate_perovskite_srtio3,
    "strontium titanate": generate_perovskite_srtio3,
    "graphene": generate_graphene_sheet,
    "nanotube": generate_carbon_nanotube_swcnt,
    "cnt": generate_carbon_nanotube_swcnt,
    "swcnt": generate_carbon_nanotube_swcnt,
    "tio2": generate_tio2_anatase,
    "titanium dioxide": generate_tio2_anatase,
    "anatase": generate_tio2_anatase,
    "mof": generate_mof_5_cluster,
    "mof-5": generate_mof_5_cluster,
    "mof5": generate_mof_5_cluster
}

def resolve_material_3d(query):
    q_lower = query.lower()
    for key, generator in MATERIALS_REGISTRY.items():
        if key in q_lower:
            return generator()
    return None
