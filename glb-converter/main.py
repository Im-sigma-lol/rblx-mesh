from pygltflib import GLTF2
import struct

def read_accessor_data(gltf, accessor_index, buffer_data):
    accessor = gltf.accessors[accessor_index]
    bufferView = gltf.bufferViews[accessor.bufferView]
    byteOffset = bufferView.byteOffset or 0
    componentType = accessor.componentType
    count = accessor.count
    dtype = {
        5126: 'f',  # float32
    }[componentType]

    num_components = {
        'SCALAR': 1,
        'VEC2': 2,
        'VEC3': 3,
        'VEC4': 4,
    }[accessor.type]

    start = byteOffset + (accessor.byteOffset or 0)
    stride = bufferView.byteStride or num_components * struct.calcsize(dtype)
    values = []

    for i in range(count):
        offset = start + i * stride
        chunk = buffer_data[offset: offset + num_components * 4]
        values.append(struct.unpack('<' + dtype * num_components, chunk))

    return values

# Load GLB

# Load GLB
gltf = GLTF2().load("input.glb")
buffer_data = gltf.binary_blob()  # ← correctly gets embedded .glb data

# Assume first mesh, primitive
primitive = gltf.meshes[0].primitives[0]

positions = read_accessor_data(gltf, primitive.attributes.POSITION, buffer_data)
normals   = read_accessor_data(gltf, primitive.attributes.NORMAL, buffer_data)
uvs       = read_accessor_data(gltf, primitive.attributes.TEXCOORD_0, buffer_data) if 'TEXCOORD_0' in primitive.attributes else [(0.0, 0.0)] * len(positions)

# Write to .mesh
with open("output.mesh", "w") as f:
    f.write("version 1.00\n")
    f.write("2100\n")
    for pos, norm, uv in zip(positions, normals, uvs):
        f.write(f"[{pos[0]},{pos[1]},{pos[2]}][{norm[0]},{norm[1]},{norm[2]}][{uv[0]},{uv[1]},0]\n")
