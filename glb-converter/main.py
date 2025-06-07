from pygltflib import GLTF2
import struct
import base64

# === Utility Functions ===

def load_buffer(gltf, glb_path):
    uri = gltf.buffers[0].uri
    if uri is None:
        # Binary buffer is embedded in .glb
        return gltf.binary_blob()
    elif uri.startswith('data:'):
        # Embedded base64 buffer in .gltf
        header, data = uri.split(',', 1)
        return base64.b64decode(data)
    else:
        # External .bin file
        with open(uri, 'rb') as f:
            return f.read()

def read_accessor_data(gltf, accessor_index, buffer_bytes):
    accessor = gltf.accessors[accessor_index]
    buffer_view = gltf.bufferViews[accessor.bufferView]
    start = (buffer_view.byteOffset or 0) + (accessor.byteOffset or 0)
    length = accessor.count
    component_type = accessor.componentType
    type_str = accessor.type

    # Map GLTF type/component to Python struct format
    type_count = {
        "SCALAR": 1,
        "VEC2": 2,
        "VEC3": 3,
        "VEC4": 4
    }[type_str]

    fmt_map = {
        5126: 'f',  # FLOAT
        5123: 'H',  # UNSIGNED_SHORT
        5125: 'I'   # UNSIGNED_INT
    }

    stride = buffer_view.byteStride or (type_count * struct.calcsize(fmt_map[component_type]))
    fmt = fmt_map[component_type]

    results = []
    for i in range(length):
        offset = start + i * stride
        chunk = buffer_bytes[offset: offset + (type_count * struct.calcsize(fmt))]
        values = struct.unpack('<' + fmt * type_count, chunk)
        results.append(values)
    return results

# === Load GLB ===

glb_path = "input.glb"
gltf = GLTF2().load(glb_path)
buffer_data = load_buffer(gltf, glb_path)

# === Extract Data from First Mesh ===

primitive = gltf.meshes[0].primitives[0]

# Positions
positions = read_accessor_data(gltf, primitive.attributes.POSITION, buffer_data)

# Normals
normals = read_accessor_data(gltf, primitive.attributes.NORMAL, buffer_data) if hasattr(primitive.attributes, 'NORMAL') else [(0.0, 1.0, 0.0)] * len(positions)

# UVs
if hasattr(primitive.attributes, 'TEXCOORD_0'):
    uvs = read_accessor_data(gltf, primitive.attributes.TEXCOORD_0, buffer_data)
else:
    uvs = [(0.0, 0.0)] * len(positions)

# === Output as Roblox Mesh v1 Format ===

with open("output.mesh", "w") as f:
    f.write("version 1.00\n")
    f.write(f"{len(positions)}\n")
    for i in range(len(positions)):
        v = positions[i]
        n = normals[i]
        t = uvs[i]
        f.write("[{:.6f},{:.6f},{:.6f}]".format(*v))
        f.write("[{:.6f},{:.6f},{:.6f}]".format(*n))
        f.write("[{:.6f},{:.6f},0]".format(*t))

print("✅ Mesh exported to 'output.mesh'")
