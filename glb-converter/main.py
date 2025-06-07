import json
import base64

def extract_accessor_data(gltf, accessor_index, buffers, bufferViews):
    accessor = gltf["accessors"][accessor_index]
    bufferView = bufferViews[accessor["bufferView"]]
    buffer = buffers[bufferView["buffer"]]
    byte_offset = bufferView.get("byteOffset", 0) + accessor.get("byteOffset", 0)
    byte_length = bufferView["byteLength"]
    count = accessor["count"]
    type_map = {"VEC3": 3, "VEC2": 2}
    components = type_map[accessor["type"]]
    component_type = accessor["componentType"]
    dtype = {
        5126: "f",  # float32
    }[component_type]

    import struct
    data = buffer[byte_offset:byte_offset + byte_length]
    step = struct.calcsize(dtype) * components
    result = []

    for i in range(count):
        values = struct.unpack_from(f"<{components}{dtype}", data, i * step)
        result.append(values)

    return result

with open("final.gltf") as f:
    gltf = json.load(f)

buffers = []
for b in gltf["buffers"]:
    uri = b["uri"]
    if uri.startswith("data:"):
        _, b64 = uri.split(",", 1)
        buffers.append(base64.b64decode(b64))
    else:
        with open(uri, "rb") as buf_file:
            buffers.append(buf_file.read())

meshes = gltf["meshes"]
bufferViews = gltf["bufferViews"]

output = ["version 1.00"]

for mesh in meshes:
    for prim in mesh["primitives"]:
        pos = extract_accessor_data(gltf, prim["attributes"]["POSITION"], buffers, bufferViews)
        nor = extract_accessor_data(gltf, prim["attributes"]["NORMAL"], buffers, bufferViews)
        uv = extract_accessor_data(gltf, prim["attributes"].get("TEXCOORD_0", 0), buffers, bufferViews)

        count = len(pos)
        output.append(str(count))
        for i in range(count):
            line = f"[{','.join(map(str, pos[i]))}][{','.join(map(str, nor[i]))}][{','.join(map(str, uv[i]))},0]"
            output.append(line)

with open("output.mesh", "w") as f:
    f.write("\n".join(output))
