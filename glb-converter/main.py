import trimesh
import os

# Use the current directory
input_path = "input.glb"
output_path = "output.mesh"

# Load the mesh
mesh = trimesh.load(input_path, force='mesh')

# Check if it's a Trimesh object
if not isinstance(mesh, trimesh.Trimesh):
    raise Exception("Model must contain a single mesh.")

vertices = mesh.vertices
normals = mesh.vertex_normals
uvs = mesh.visual.uv

if uvs is None:
    raise Exception("UV coordinates not found.")

# Write in Roblox Mesh v1 format
with open(output_path, "w") as f:
    f.write("version 1.00\n")
    f.write(f"{len(vertices)}\n")
    for i in range(len(vertices)):
        pos = vertices[i]
        nor = normals[i]
        uv = uvs[i]
        f.write(f"[{pos[0]},{pos[1]},{pos[2]}]"
                f"[{nor[0]},{nor[1]},{nor[2]}]"
                f"[{uv[0]},{uv[1]},0]\n")

print("✅ Done! Mesh saved to:", output_path)
