import os
import math

def generate_sphere(center, radius, resolution=2):
    # Generates a low-poly sphere (icosphere) at a given center
    t = (1.0 + math.sqrt(5.0)) / 2.0
    vertices = [
        [-1,  t,  0], [ 1,  t,  0], [-1, -t,  0], [ 1, -t,  0],
        [ 0, -1,  t], [ 0,  1,  t], [ 0, -1, -t], [ 0,  1, -t],
        [ t,  0, -1], [ t,  0,  1], [-t,  0, -1], [-t,  0,  1]
    ]
    
    faces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ]

    # Normalize and scale vertices, then translate
    scaled_verts = []
    for v in vertices:
        length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        scaled_verts.append((
            (v[0]/length) * radius + center[0],
            (v[1]/length) * radius + center[1],
            (v[2]/length) * radius + center[2]
        ))
    return scaled_verts, faces

def pdb_to_obj(pdb_file, obj_file):
    if not os.path.exists(pdb_file):
        return False, "PDB file not found."
        
    try:
        with open(pdb_file, 'r') as f:
            lines = f.readlines()
            
        atoms = []
        for line in lines:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                element = line[76:78].strip()
                atoms.append((x, y, z, element))
                
        if not atoms:
            return False, "No atoms found in PDB."

        with open(obj_file, 'w') as out:
            out.write("# Polymathix 3D Export (OBJ)\n")
            vertex_offset = 1
            for i, atom in enumerate(atoms):
                x, y, z, elem = atom
                radius = 1.5 if elem != 'H' else 1.0  # Basic VDW approximation
                verts, faces = generate_sphere((x, y, z), radius)
                
                for v in verts:
                    out.write(f"v {v[0]:.3f} {v[1]:.3f} {v[2]:.3f}\n")
                    
                for face in faces:
                    out.write(f"f {face[0]+vertex_offset} {face[1]+vertex_offset} {face[2]+vertex_offset}\n")
                    
                vertex_offset += len(verts)
                
        return True, f"Successfully exported {len(atoms)} atoms to {obj_file}"
    except Exception as e:
        return False, str(e)
