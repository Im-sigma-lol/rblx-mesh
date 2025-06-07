import trimesh

mesh = trimesh.load("input.glb")
mesh.export("final.gltf")
