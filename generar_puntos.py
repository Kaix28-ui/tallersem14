"""
Laboratorio semana 14 - Recorrido inmersivo interactivo
Lee puntos.csv (posiciones en píxeles sobre la foto 360°) y genera puntos.json
con los ángulos (yaw, pitch) y la posición (x, y, z) de cada punto en la escena.

Uso:  python generar_puntos.py
"""
import csv
import json
import math

# Tamaño de la foto 360° en píxeles (proporción 2:1). Cámbielo si usa su propia foto.
ANCHO = 4096
ALTO = 2048

R = 6.0             # distancia del visitante a cada punto, en metros
ALTURA_OJOS = 1.6   # altura de la cámara, en metros


def angulos(px, py):
    """Convierte un píxel de la foto equirectangular en yaw y pitch (grados)."""
    # TODO 1: calcule yaw y pitch con las fórmulas de la guía
    yaw = (px / ANCHO - 0.5) * 360
    pitch = (0.5 - py / ALTO) * 180
    return yaw, pitch


def posicion(yaw, pitch):
    """Convierte yaw y pitch en una posición (x, y, z) a la distancia R."""
    # TODO 2: convierta los ángulos a radianes (math.radians) y calcule x, y, z
    yaw_rad = math.radians(yaw)
    pitch_rad = math.radians(pitch)

    x = R * math.cos(pitch_rad) * math.sin(yaw_rad)
    y = ALTURA_OJOS + R * math.sin(pitch_rad)
    z = -R * math.cos(pitch_rad) * math.cos(yaw_rad)
    return round(x, 3), round(y, 3), round(z, 3)


def main():
    puntos = []
    with open("puntos.csv", encoding="utf-8-sig") as archivo:
        for fila in csv.DictReader(archivo):
            yaw, pitch = angulos(float(fila["px"]), float(fila["py"]))
            x, y, z = posicion(yaw, pitch)
            puntos.append({
                "id": fila["id"],
                "titulo": fila["titulo"],
                "descripcion": fila["descripcion"],
                "yaw": round(yaw, 1),
                "pitch": round(pitch, 1),
                "posicion": {"x": x, "y": y, "z": z},
            })

    print(f"{'id':<14}{'yaw':>8}{'pitch':>8}   posición (x, y, z)")
    for p in puntos:
        pos = p["posicion"]
        print(f"{p['id']:<14}{p['yaw']:>8}{p['pitch']:>8}   ({pos['x']}, {pos['y']}, {pos['z']})")

    with open("puntos.json", "w", encoding="utf-8") as archivo:
        json.dump(puntos, archivo, ensure_ascii=False, indent=2)
    print(f"\nSe generó puntos.json con {len(puntos)} puntos.")


if __name__ == "__main__":
    main()