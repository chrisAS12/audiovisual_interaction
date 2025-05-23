import colour

bcp_xyY_colours = {
    "red-saturated": [0.549, 0.313, 22.93],
    "red-light": [0.407, 0.326, 49.95],
    "red-muted": [0.441, 0.324, 22.93],
    "red-dark": [0.506, 0.311, 7.6],
    "orange-saturated": [0.513, 0.412, 49.95],
    "orange-light": [0.399, 0.366, 68.56],
    "orange-muted": [0.423, 0.375, 34.86],
    "orange-dark": [0.481, 0.388, 10.76],
    "yellow-saturated": [0.446, 0.472, 91.25],
    "yellow-light": [0.391, 0.413, 91.25],
    "yellow-muted": [0.407, 0.426, 49.95],
    "yellow-dark": [0.437, 0.45, 18.43],
    "chartreuse-saturated": [0.387, 0.504, 68.56],
    "chartreuse-light": [0.357, 0.42, 79.9],
    "chartreuse-muted": [0.36, 0.436, 42.4],
    "chartreuse-dark": [0.369, 0.473, 18.43],
    "green-saturated": [0.254, 0.449, 42.4],
    "green-light": [0.288, 0.381, 63.9],
    "green-muted": [0.281, 0.392, 34.86],
    "green-dark": [0.261, 0.419, 12.34],
    "cyan-saturated": [0.226, 0.335, 49.95],
    "cyan-light": [0.267, 0.33, 68.56],
    "cyan-muted": [0.254, 0.328, 34.86],
    "cyan-dark": [0.233, 0.324, 13.92],
    "blue-saturated": [0.2, 0.23, 34.86],
    "blue-light": [0.255, 0.278, 59.25],
    "blue-muted": [0.241, 0.265, 28.9],
    "blue-dark": [0.212, 0.236, 10.76],
    "purple-saturated": [0.272, 0.156, 18.43],
    "purple-light": [0.29, 0.242, 49.95],
    "purple-muted": [0.287, 0.222, 22.93],
    "purple-dark": [0.28, 0.181, 7.6],
    "black": [0.31, 0.316, 0.3],
    "gray-dark": [0.31, 0.316, 12.34],
    "gray-medium": [0.31, 0.316, 31.88],
    "gray-light": [0.31, 0.316, 63.9],
    "white": [0.31, 0.316, 116.0],
}

def xyY_to_hex(xyY):
    XYZ = colour.xyY_to_XYZ(xyY)
    RGB = colour.XYZ_to_sRGB(XYZ)
    max_val = max(RGB)
    if max_val > 1:
        RGB = [c / max_val for c in RGB]
    RGB_255 = [int(max(0, min(1, c)) * 255) for c in RGB]
    return '#{:02x}{:02x}{:02x}'.format(*RGB_255)

for name, xyY in bcp_xyY_colours.items():
    hex_code = xyY_to_hex(xyY)
    print(f".colour-{name} {{ background-color: {hex_code}; }}\n")

# rēķinam krāsu koeficinetus pēc RGB vērtībām un brightness jeb luminance un noteiktā standarta


def xyY_to_linear_rgb(xyY):
    XYZ = colour.xyY_to_XYZ(xyY)
    RGB = colour.XYZ_to_sRGB(XYZ)
    return [max(0, min(1, c)) for c in RGB]

def luminance(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

luminance_dict = {}
for name, xyY in bcp_xyY_colours.items():
    rgb = xyY_to_linear_rgb(xyY)
    y = luminance(rgb)
    luminance_dict[name] = y

sorted_items = sorted(luminance_dict.items(), key=lambda x: x[1])
value_map_colour = {name: i + 1 for i, (name, _) in enumerate(sorted_items)}

print("value_map_colour = {")
for name, val in value_map_colour.items():
    print(f"    '{name}': {val},")
print("}")