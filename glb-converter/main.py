import trimesh
import os

# Path to your GLB file
input_path = "/storage/emulated/0/Models/input.glb"
output_path = "/storage/emulated/0/Models/output.mesh"

# Load mesh from GLB
mesh = trimesh.load(input_path, force='mesh')

# Ensure it is a Trimesh object (not Scene)
if not isinstance(mesh, trimesh.Trimesh):
    raise Exception("Model must contain a single mesh. Use Blender or gltfpack to flatten multiple meshes.")

vertices = mesh.vertices
normals = mesh.vertex_normals
uvs = mesh.visual.uv

if uvs is None:
    raise Exception("UV coordinates not found in this model.")

# Write the mesh in Roblox format v1
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

print("✅ Export complete:", output_path)
