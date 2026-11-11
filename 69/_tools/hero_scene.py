#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
СЦЕНА ГЕРОЯ: СЕТЬ ИНТЕЛЛЕКТА
=============================
Задача визуала (слова владельца, 11.11.2026):
  «нет визуала который вызывает уважение... Doctor Ragimoff — Школа Психологии —
   вот что пиарится — вход в новое пространство интеллекта и развития —
   достичь своих жизненных целей пользуясь своим интеллектом».

Значит визуал обязан передавать три вещи БЕЗ СЛОВ:
  1. интеллект        — узлы и связи, как в нейронной сети
  2. развитие         — сеть растёт и упорядочивается по ходу движения
  3. достижение цели   — свет идёт от периферии к центру и там собирается

Почему именно сеть, а не абстрактные частицы:
  частицы — это «красиво», но бессмысленно. Сеть читается как МЫШЛЕНИЕ:
  связи, узлы, рост. Это предмет школы, а не украшение.

Запуск:
  blender --background --python hero_scene.py -- --test     (1 кадр, проверка)
  blender --background --python hero_scene.py -- --render   (все кадры)
"""
import bpy, bmesh, math, random, sys, os
from mathutils import Vector

# ── параметры ───────────────────────────────────────────────────────
FRAMES      = 120          # кадров в скрабе
W, H        = 1920, 1080
NODES       = 260          # узлов сети
LINK_DIST   = 1.9          # предел длины связи
SEED        = 20261111     # фиксированный: результат воспроизводим
OUT         = r"D:\Projects\Ragimoff\site\test\69\_tools\hero_frames"

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
TEST = "--test" in argv

random.seed(SEED)


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def build_nodes():
    """Узлы сети: точки в объёме, плотнее к центру.
       Плотность к центру — это и есть «собирается к цели»."""
    pts = []
    for i in range(NODES):
        # сферическое распределение с притяжением к центру
        while True:
            v = Vector((random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1)))
            if v.length > 0.05:
                break
        r = random.random() ** 0.65 * 3.4      # ближе к центру — плотнее
        pts.append(v.normalized() * r)
    return pts


def make_mesh(name, verts_faces, material):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts_faces[0], [], verts_faces[1])
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(material)
    return ob


def sphere_mesh(name, points, radius, material):
    """Все узлы одним мешем — быстро и без тысяч объектов в сцене."""
    bm = bmesh.new()
    for p in points:
        tmp = bmesh.new()
        bmesh.ops.create_icosphere(tmp, subdivisions=1, radius=radius)
        bmesh.ops.translate(tmp, verts=tmp.verts, vec=p)
        me = bpy.data.meshes.new("t")
        tmp.to_mesh(me)
        tmp.free()
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(material)
    return ob


def links_mesh(name, points, maxd, material):
    """Связи — тонкие отрезки между близкими узлами.
       Это то, что превращает точки в СЕТЬ, то есть в мышление.

       ПРИЧИНА ПЕРЕПИСИ: первая версия делала отдельный bmesh на каждую связь
       через bmesh.ops.create_cone. При 260 узлах это тысячи операций — Blender
       падал с EXCEPTION_ACCESS_VIOLATION ещё до рендера.
       РЕШЕНИЕ: строим четырёхгранную трубу вручную — 8 вершин и 4 грани
       на связь, всё в один меш. Быстро и без падений."""
    from mathutils import Matrix
    verts = []
    faces = []
    n = len(points)
    count = 0
    R = 0.013

    def basis(axis):
        """Два перпендикуляра к оси — для четырёхугольного сечения."""
        up = Vector((0, 0, 1))
        if abs(axis.dot(up)) > 0.95:
            up = Vector((0, 1, 0))
        u = axis.cross(up).normalized()
        v = axis.cross(u).normalized()
        return u, v

    for i in range(n):
        for j in range(i + 1, n):
            a, b = points[i], points[j]
            d = b - a
            if d.length > maxd or d.length < 1e-6:
                continue
            axis = d.normalized()
            u, v = basis(axis)
            base = len(verts)
            for p in (a, b):
                for k in range(4):
                    ang = k * math.pi / 2
                    verts.append(p + u * (math.cos(ang) * R) + v * (math.sin(ang) * R))
            # боковые грани: 0-3 у начала, 4-7 у конца
            for k in range(4):
                k2 = (k + 1) % 4
                faces.append((base + k, base + k2, base + 4 + k2, base + 4 + k))
            count += 1

    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(material)
    print("связей:", count, "| вершин:", len(verts))
    return ob


def mat_gold_emissive(name, strength=6.0, color=(1.0, 0.78, 0.34)):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*color, 1)
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return m


def mat_link(name, color=(0.78, 0.62, 0.28)):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = 0.42
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m


def setup_scene():
    sc = bpy.context.scene
    sc.render.resolution_x = W
    sc.render.resolution_y = H
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGB'

    # фон — почти чёрный с холодным оттенком, как «Ноктюрн»
    wd = bpy.data.worlds.new("W")
    sc.world = wd
    wd.use_nodes = True
    bg = wd.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.012, 0.016, 0.026, 1)
    bg.inputs["Strength"].default_value = 0.35

    # движок: EEVEE — в разы быстрее Cycles, для светящихся узлов достаточно
    try:
        sc.render.engine = 'BLENDER_EEVEE_NEXT'
    except Exception:
        try:
            sc.render.engine = 'BLENDER_EEVEE'
        except Exception:
            sc.render.engine = 'CYCLES'
    print("ДВИЖОК:", sc.render.engine)


def main():
    clear()
    setup_scene()

    pts = build_nodes()
    gold = mat_gold_emissive("gold", 9.0)
    link = mat_link("link")

    nodes_ob = sphere_mesh("nodes", pts, 0.052, gold)
    links_ob = links_mesh("links", pts, LINK_DIST, link)
    print("узлов:", len(pts), "| связей в меше:", len(links_ob.data.vertices) // 2)

    # ── камера: смотрит на сеть и медленно подходит ближе.
    #    Медленное приближение = «вход в новое пространство».
    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = 46
    cam = bpy.data.objects.new("cam", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam

    # ── свет: узкий прожектор, обходит сеть и подсвечивает связи металлом
    lamp = bpy.data.lights.new("lamp", type='AREA')
    lamp.energy = 900
    lamp.size = 3.2
    lamp.color = (1.0, 0.88, 0.62)
    lo = bpy.data.objects.new("lamp", lamp)
    bpy.context.collection.objects.link(lo)

    def place(frame):
        t = frame / FRAMES
        # камера: плавный вход по дуге
        ang = -0.55 + t * 0.75
        rad = 8.4 - t * 2.3
        cam.location = (math.sin(ang) * rad, -rad * 0.72, 1.5 + t * 0.9)
        cam.rotation_euler = (math.radians(80) - t * 0.06, 0, math.radians(38) + t * 0.14)
        # свет обходит сеть по кругу, второй оборот медленнее
        la = t * math.pi * 2.1
        lo.location = (math.cos(la) * 4.2, math.sin(la) * 4.2, 2.6 - t * 1.2)
        lo.rotation_euler = (math.radians(52), 0, la + math.pi / 2)

    # проба: первый кадр
    if TEST:
        place(0)
        sc = bpy.context.scene
        sc.frame_set(1)
        os.makedirs(OUT, exist_ok=True)
        sc.render.filepath = os.path.join(OUT, "test_0000.png")
        bpy.ops.render.render(write_still=True)
        print("ТЕСТОВЫЙ КАДР:", sc.render.filepath)
        return

    # ── полный рендер ──
    os.makedirs(OUT, exist_ok=True)
    sc = bpy.context.scene
    sc.frame_start = 1
    sc.frame_end = FRAMES
    for f in range(1, FRAMES + 1):
        sc.frame_set(f)
        place(f)
        sc.render.filepath = os.path.join(OUT, "f%03d" % (f - 1))
        bpy.ops.render.render(write_still=True)
        if f % 10 == 0:
            print("отрендерено", f, "из", FRAMES)
    print("ГОТОВО:", FRAMES, "кадров в", OUT)


main()
