import math


def generate_bowl_usda(filename: str = "bowl.usda", rings: int = 16, segments: int = 32) -> None:
    # Radius 1.0 Hemisphere (Bottom Half: y <= 0)
    # We generate vertices and faces.

    verts = []
    indices = []
    counts = []

    # Vertices
    # Ring 0 is the bottom pole (y=-1)
    # Ring N is the equator (y=0)
    # Logic: phi goes from pi (bottom) to pi/2 (equator)
    # But wait, standard spherical coords:
    # x = r sin(phi) cos(theta)
    # y = r cos(phi)  <-- y is up
    # z = r sin(phi) sin(theta)
    # y=1 is North Pole (phi=0), y=-1 is South Pole (phi=pi)
    # We want South Hemisphere: phi from pi (180) to pi/2 (90).

    # But let's build it layer by layer.
    # Bottom pole: single point (0, -1, 0)
    verts.append((0.0, -1.0, 0.0))

    # Rings
    for r in range(1, rings + 1):
        # fraction 0 (pole) to 1 (equator)
        frac = r / float(rings)
        # phi ranges from PI (180) -> PI/2 (90)
        phi = math.pi - (frac * (math.pi / 2.0))

        y = math.cos(phi)
        radius = math.sin(phi)

        for s in range(segments):
            theta = (s / float(segments)) * 2.0 * math.pi
            x = radius * math.cos(theta)
            z = radius * math.sin(theta)
            verts.append((x, y, z))

    # Faces
    # Bottom Cap (Triangle fan around pole)
    # Pole is index 0. First ring starts at 1.
    for s in range(segments):
        # Face: Pole, Ring1[s], Ring1[s+1]
        v1 = 1 + s
        v2 = 1 + ((s + 1) % segments)
        indices.extend([0, v2, v1])  # Order for outward normal?
        # Pole (0,-1,0). Normal down.
        # Check standard winding (CCW).
        # We look from outside bottom.
        # 0 -> v2 -> v1.
        counts.append(3)

    # Quads for rest of rings
    for r in range(
        rings - 1
    ):  # r is previous ring index (0-based relative to rings list, not verts)
        # Ring r verts start at: 1 + r*segments
        # Ring r+1 verts start at: 1 + (r+1)*segments
        start_current = 1 + r * segments
        start_next = 1 + (r + 1) * segments

        for s in range(segments):
            s_next = (s + 1) % segments

            # Quad: Current[s], Current[s+1], Next[s+1], Next[s]
            # But winding...
            # We want Normal OUT.
            # Verts are roughly ordered bottom to top.
            v_cur_s = start_current + s
            v_cur_sn = start_current + s_next
            v_next_s = start_next + s
            v_next_sn = start_next + s_next

            # To face OUT:
            # v_cur_s -> v_cur_sn -> v_next_sn -> v_next_s
            indices.extend([v_cur_s, v_cur_sn, v_next_sn, v_next_s])
            counts.append(4)

    # Format USDA
    usda = []
    usda.append("#usda 1.0")
    usda.append("(")
    usda.append('    defaultPrim = "Bowl"')
    usda.append('    upAxis = "Y"')
    usda.append(")")
    usda.append("")
    usda.append('def Mesh "Bowl"')
    usda.append("{")

    # Points
    usda.append("    point3f[] points = [")
    for v in verts:
        usda.append(f"        ({v[0]:.6f}, {v[1]:.6f}, {v[2]:.6f}),")
    usda.append("    ]")

    # Counts
    usda.append("    int[] faceVertexCounts = [")
    line = "        "
    for c in counts:
        line += f"{c}, "
        if len(line) > 80:
            usda.append(line)
            line = "        "
    usda.append(line)
    usda.append("    ]")

    # Indices
    usda.append("    int[] faceVertexIndices = [")
    line = "        "
    for i in indices:
        line += f"{i}, "
        if len(line) > 80:
            usda.append(line)
            line = "        "
    usda.append(line)
    usda.append("    ]")

    # Extent (approx)
    usda.append("    float3[] extent = [(-1, -1, -1), (1, 0, 1)]")
    usda.append("}")

    with open(filename, "w") as f:
        f.write("\n".join(usda))
    print(f"Generated {filename}")


if __name__ == "__main__":
    generate_bowl_usda("/home/lhzn/Projects/whoi-mpg/biologger-sim/omniverse/assets/bowl.usda")
