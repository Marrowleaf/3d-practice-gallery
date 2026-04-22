import math
from pathlib import Path

import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial

OUT = Path('/root/hermes/3d-practice-gallery')
MODELS = OUT / 'models'
MODELS.mkdir(parents=True, exist_ok=True)


def rgba(hexstr, alpha=255):
    hexstr = hexstr.lstrip('#')
    return [int(hexstr[i:i+2], 16) for i in (0, 2, 4)] + [alpha]


def set_color(mesh, color_hex, emissive=None, metallic=0.2, roughness=0.7):
    color = rgba(color_hex)
    mesh.visual = trimesh.visual.TextureVisuals(
        material=PBRMaterial(
            baseColorFactor=color,
            metallicFactor=metallic,
            roughnessFactor=roughness,
            emissiveFactor=emissive or [0.0, 0.0, 0.0],
        )
    )
    return mesh


def export_scene(name, items):
    scene = trimesh.Scene()
    for item_name, mesh in items:
        scene.add_geometry(mesh, node_name=item_name)
    with open(MODELS / f'{name}.glb', 'wb') as f:
        f.write(scene.export(file_type='glb'))
    print('wrote', name)


# 1) Crystal shard
crystal_parts = []
core = trimesh.creation.icosphere(subdivisions=2, radius=0.72)
core.apply_scale([0.7, 1.8, 0.7])
set_color(core, '#67e8f9', emissive=[0.08, 0.18, 0.22], metallic=0.05, roughness=0.18)
crystal_parts.append(('core', core))
for i, ang in enumerate(np.linspace(0, 2 * math.pi, 6, endpoint=False)):
    shard = trimesh.creation.box(extents=[0.18, 1.3, 0.18])
    shard.apply_transform(trimesh.transformations.rotation_matrix(0.45, [1, 0, 0]))
    shard.apply_transform(trimesh.transformations.rotation_matrix(ang, [0, 1, 0]))
    shard.apply_translation([math.cos(ang) * 0.5, 0.15, math.sin(ang) * 0.5])
    set_color(shard, '#a5f3fc', emissive=[0.04, 0.08, 0.12], metallic=0.02, roughness=0.22)
    crystal_parts.append((f'shard_{i}', shard))
base = trimesh.creation.cylinder(radius=1.1, height=0.32, sections=6)
base.apply_translation([0, -1.65, 0])
set_color(base, '#374151', metallic=0.1, roughness=0.95)
crystal_parts.append(('base', base))
export_scene('arcane_crystal', crystal_parts)


# 2) Sci-fi drone
parts = []
body = trimesh.creation.icosphere(subdivisions=3, radius=0.9)
body.apply_scale([1.45, 0.45, 1.0])
set_color(body, '#94a3b8', metallic=0.75, roughness=0.28)
parts.append(('body', body))
canopy = trimesh.creation.icosphere(subdivisions=2, radius=0.46)
canopy.apply_scale([1.0, 0.55, 0.8])
canopy.apply_translation([0.12, 0.18, 0])
set_color(canopy, '#38bdf8', emissive=[0.02, 0.05, 0.08], metallic=0.1, roughness=0.08)
parts.append(('canopy', canopy))
for side in (-1, 1):
    arm = trimesh.creation.box(extents=[1.8, 0.12, 0.14])
    arm.apply_translation([0, 0.03, side * 1.05])
    set_color(arm, '#64748b', metallic=0.6, roughness=0.35)
    parts.append((f'arm_{side}', arm))
    ring = trimesh.creation.torus(major_radius=0.32, minor_radius=0.05, major_sections=32, minor_sections=18)
    ring.apply_translation([0.72, 0.03, side * 1.05])
    set_color(ring, '#22d3ee', emissive=[0.0, 0.15, 0.17], metallic=0.25, roughness=0.3)
    parts.append((f'ring_f_{side}', ring))
    ring2 = ring.copy()
    ring2.apply_translation([-1.44, 0, 0])
    parts.append((f'ring_b_{side}', ring2))
engine = trimesh.creation.cylinder(radius=0.12, height=0.85, sections=24)
engine.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 0, 1]))
for side in (-1, 1):
    for x, name in ((0.72, 'f'), (-0.72, 'b')):
        e = engine.copy()
        e.apply_translation([x, 0.03, side * 1.05])
        set_color(e, '#e2e8f0', emissive=[0.05, 0.08, 0.12], metallic=0.9, roughness=0.2)
        parts.append((f'engine_{name}_{side}', e))
export_scene('sky_drone', parts)


# 3) Fantasy sword
parts = []
blade = trimesh.creation.box(extents=[0.16, 3.0, 0.05])
blade.apply_translation([0, 1.6, 0])
set_color(blade, '#e5e7eb', metallic=0.98, roughness=0.18)
parts.append(('blade', blade))
fuller = trimesh.creation.box(extents=[0.035, 1.7, 0.01])
fuller.apply_translation([0, 1.55, 0.03])
set_color(fuller, '#94a3b8', metallic=0.9, roughness=0.18)
parts.append(('fuller', fuller))
point = trimesh.creation.cone(radius=0.09, height=0.42, sections=4)
point.apply_transform(trimesh.transformations.rotation_matrix(math.pi, [1, 0, 0]))
point.apply_translation([0, 3.1, 0])
set_color(point, '#f8fafc', metallic=0.98, roughness=0.15)
parts.append(('point', point))
guard = trimesh.creation.box(extents=[1.15, 0.12, 0.16])
guard.apply_translation([0, 0.12, 0])
set_color(guard, '#f59e0b', emissive=[0.08, 0.04, 0.0], metallic=0.8, roughness=0.3)
parts.append(('guard', guard))
grip = trimesh.creation.cylinder(radius=0.09, height=0.92, sections=20)
grip.apply_translation([0, -0.46, 0])
set_color(grip, '#7c2d12', metallic=0.1, roughness=0.85)
parts.append(('grip', grip))
pommel = trimesh.creation.icosphere(subdivisions=2, radius=0.16)
pommel.apply_translation([0, -0.98, 0])
set_color(pommel, '#fbbf24', emissive=[0.1, 0.06, 0.0], metallic=0.85, roughness=0.22)
parts.append(('pommel', pommel))
for side in (-1, 1):
    wing = trimesh.creation.box(extents=[0.42, 0.08, 0.09])
    wing.apply_transform(trimesh.transformations.rotation_matrix(side * 0.55, [0, 0, 1]))
    wing.apply_translation([side * 0.42, 0.18, 0])
    set_color(wing, '#fcd34d', emissive=[0.08, 0.04, 0.0], metallic=0.82, roughness=0.24)
    parts.append((f'wing_{side}', wing))
export_scene('emberblade', parts)

print('done')
