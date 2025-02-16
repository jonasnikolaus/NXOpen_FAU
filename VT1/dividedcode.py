import NXOpen # type: ignore
import NXOpen.Features # type: ignore
import math
from itertools import combinations

# Globale Variable zur Festlegung der Übung
EXERCISE_NUMBER = 1  # Setzen Sie dies auf 1 oder 2 je nach Übung

# 1= Übung 1, 2= Vertiefungsübung 1
# 3= Übung 2, 4= Vertiefungsübung 2

# Musterlösungsdaten (alle 147 Kanten)
REFERENCE_EDGES_UE1 = [
    {'length': 1.573, 'start': (-21.685, 6.000, 16.000), 'end': (-21.213, 7.500, 16.000)},
    {'length': 6.502, 'start': (-19.900, 10.500, 16.000), 'end': (-19.820, 10.650, 9.500)},
    {'length': 6.502, 'start': (22.319, -2.850, 9.500), 'end': (22.299, -3.000, 16.000)},
    {'length': 42.426, 'start': (21.213, 7.500, 16.000), 'end': (-21.213, 7.500, 16.000)},
    {'length': 42.426, 'start': (21.213, -7.500, 16.000), 'end': (-21.213, -7.500, 16.000)},
    {'length': 75.398, 'start': (0.000, 12.000, 0.000), 'end': (0.000, 12.000, 0.000)},
    {'length': 39.640, 'start': (19.820, 10.650, 9.500), 'end': (-19.820, 10.650, 9.500)},
    {'length': 43.452, 'start': (21.726, 5.850, 9.500), 'end': (-21.726, 5.850, 9.500)},
    {'length': 41.373, 'start': (20.686, 8.850, 9.500), 'end': (-20.686, 8.850, 9.500)},
    {'length': 44.900, 'start': (22.450, 1.500, 16.000), 'end': (-22.450, 1.500, 16.000)},
    {'length': 1.290, 'start': (-20.686, -8.850, 9.500), 'end': (-21.160, -7.650, 9.500)},
    {'length': 1.552, 'start': (16.903, 14.850, 9.500), 'end': (17.887, 13.650, 9.500)},
    {'length': 1.552, 'start': (-16.903, -14.850, 9.500), 'end': (-17.887, -13.650, 9.500)},
    {'length': 2.103, 'start': (-16.771, 15.000, 16.000), 'end': (-15.297, 16.500, 16.000)},
    {'length': 44.091, 'start': (22.045, 4.500, 16.000), 'end': (-22.045, 4.500, 16.000)},
    {'length': 6.502, 'start': (22.319, 2.850, 9.500), 'end': (22.299, 3.000, 16.000)},
    {'length': 1.872, 'start': (-13.698, -17.850, 9.500), 'end': (-15.134, -16.650, 9.500)},
    {'length': 6.503, 'start': (-16.903, 14.850, 9.500), 'end': (-16.771, 15.000, 16.000)},
    {'length': 1.522, 'start': (22.299, -3.000, 16.000), 'end': (22.045, -4.500, 16.000)},
    {'length': 6.502, 'start': (22.450, -1.500, 16.000), 'end': (22.439, -1.650, 9.500)},
    {'length': 6.502, 'start': (-20.686, 8.850, 9.500), 'end': (-20.622, 9.000, 16.000)},
    {'length': 44.598, 'start': (22.299, -3.000, 16.000), 'end': (-22.299, -3.000, 16.000)},
    {'length': 41.243, 'start': (20.622, 9.000, 16.000), 'end': (-20.622, 9.000, 16.000)},
    {'length': 33.807, 'start': (16.903, -14.850, 9.500), 'end': (-16.903, -14.850, 9.500)},
    {'length': 1.290, 'start': (-21.160, 7.650, 9.500), 'end': (-20.686, 8.850, 9.500)},
    {'length': 6.502, 'start': (-22.014, -4.650, 9.500), 'end': (-22.045, -4.500, 16.000)},
    {'length': 6.504, 'start': (15.297, -16.500, 16.000), 'end': (15.134, -16.650, 9.500)},
    {'length': 6.502, 'start': (21.685, 6.000, 16.000), 'end': (21.726, 5.850, 9.500)},
    {'length': 30.267, 'start': (15.134, -16.650, 9.500), 'end': (-15.134, -16.650, 9.500)},
    {'length': 1.386, 'start': (19.820, -10.650, 9.500), 'end': (19.127, -11.850, 9.500)},
    {'length': 6.502, 'start': (-19.820, -10.650, 9.500), 'end': (-19.900, -10.500, 16.000)},
    {'length': 33.541, 'start': (16.771, 15.000, 16.000), 'end': (-16.771, 15.000, 16.000)},
    {'length': 44.638, 'start': (-22.319, 2.850, 9.500), 'end': (22.319, 2.850, 9.500)},
    {'length': 6.502, 'start': (22.045, -4.500, 16.000), 'end': (22.014, -4.650, 9.500)},
    {'length': 1.573, 'start': (21.213, 7.500, 16.000), 'end': (21.685, 6.000, 16.000)},
    {'length': 41.243, 'start': (20.622, -9.000, 16.000), 'end': (-20.622, -9.000, 16.000)},
    {'length': 43.370, 'start': (21.685, 6.000, 16.000), 'end': (-21.685, 6.000, 16.000)},
    {'length': 1.234, 'start': (-21.726, -5.850, 9.500), 'end': (-22.014, -4.650, 9.500)},
    {'length': 6.504, 'start': (-15.297, 16.500, 16.000), 'end': (-15.134, 16.650, 9.500)},
    {'length': 6.502, 'start': (21.160, 7.650, 9.500), 'end': (21.213, 7.500, 16.000)},
    {'length': 1.552, 'start': (17.887, -13.650, 9.500), 'end': (16.903, -14.850, 9.500)},
    {'length': 6.504, 'start': (15.134, 16.650, 9.500), 'end': (15.297, 16.500, 16.000)},
    {'length': 6.505, 'start': (13.698, -17.850, 9.500), 'end': (13.500, -18.000, 16.000)},
    {'length': 1.522, 'start': (-22.045, -4.500, 16.000), 'end': (-22.299, -3.000, 16.000)},
    {'length': 1.386, 'start': (19.127, 11.850, 9.500), 'end': (19.820, 10.650, 9.500)},
    {'length': 6.502, 'start': (-20.622, -9.000, 16.000), 'end': (-20.686, -8.850, 9.500)},
    {'length': 1.872, 'start': (13.698, 17.850, 9.500), 'end': (15.134, 16.650, 9.500)},
    {'length': 1.573, 'start': (-21.213, -7.500, 16.000), 'end': (-21.685, -6.000, 16.000)},
    {'length': 1.552, 'start': (-17.887, 13.650, 9.500), 'end': (-16.903, 14.850, 9.500)},
    {'length': 6.502, 'start': (-22.299, 3.000, 16.000), 'end': (-22.319, 2.850, 9.500)},
    {'length': 6.503, 'start': (-16.771, -15.000, 16.000), 'end': (-16.903, -14.850, 9.500)},
    {'length': 1.290, 'start': (20.686, 8.850, 9.500), 'end': (21.160, 7.650, 9.500)},
    {'length': 1.665, 'start': (-19.900, -10.500, 16.000), 'end': (-20.622, -9.000, 16.000)},
    {'length': 1.290, 'start': (21.160, -7.650, 9.500), 'end': (20.686, -8.850, 9.500)},
    {'length': 39.799, 'start': (19.900, -10.500, 16.000), 'end': (-19.900, -10.500, 16.000)},
    {'length': 1.665, 'start': (-20.622, 9.000, 16.000), 'end': (-19.900, 10.500, 16.000)},
    {'length': 3.002, 'start': (22.450, 1.500, 16.000), 'end': (22.450, -1.500, 16.000)},
    {'length': 28.958, 'start': (13.500, -18.000, 16.000), 'end': (-13.500, -18.000, 16.000)},
    {'length': 1.872, 'start': (-15.134, 16.650, 9.500), 'end': (-13.698, 17.850, 9.500)},
    {'length': 1.822, 'start': (19.033, -12.000, 16.000), 'end': (18.000, -13.500, 16.000)},
    {'length': 1.206, 'start': (-22.319, -2.850, 9.500), 'end': (-22.439, -1.650, 9.500)},
    {'length': 39.640, 'start': (19.820, -10.650, 9.500), 'end': (-19.820, -10.650, 9.500)},
    {'length': 44.638, 'start': (-22.319, -2.850, 9.500), 'end': (22.319, -2.850, 9.500)},
    {'length': 6.502, 'start': (20.622, 9.000, 16.000), 'end': (20.686, 8.850, 9.500)},
    {'length': 6.502, 'start': (19.820, 10.650, 9.500), 'end': (19.900, 10.500, 16.000)},
    {'length': 1.234, 'start': (-22.014, 4.650, 9.500), 'end': (-21.726, 5.850, 9.500)},
    {'length': 6.502, 'start': (21.213, -7.500, 16.000), 'end': (21.160, -7.650, 9.500)},
    {'length': 6.502, 'start': (19.033, 12.000, 16.000), 'end': (19.127, 11.850, 9.500)},
    {'length': 38.066, 'start': (19.033, -12.000, 16.000), 'end': (-19.033, -12.000, 16.000)},
    {'length': 6.502, 'start': (22.450, 1.500, 16.000), 'end': (22.439, 1.650, 9.500)},
    {'length': 1.234, 'start': (22.014, -4.650, 9.500), 'end': (21.726, -5.850, 9.500)},
    {'length': 6.503, 'start': (16.771, 15.000, 16.000), 'end': (16.903, 14.850, 9.500)},
    {'length': 2.103, 'start': (15.297, 16.500, 16.000), 'end': (16.771, 15.000, 16.000)},
    {'length': 44.029, 'start': (22.014, -4.650, 9.500), 'end': (-22.014, -4.650, 9.500)},
    {'length': 44.029, 'start': (22.014, 4.650, 9.500), 'end': (-22.014, 4.650, 9.500)},
    {'length': 1.206, 'start': (22.439, 1.650, 9.500), 'end': (22.319, 2.850, 9.500)},
    {'length': 44.091, 'start': (22.045, -4.500, 16.000), 'end': (-22.045, -4.500, 16.000)},
    {'length': 35.773, 'start': (17.887, 13.650, 9.500), 'end': (-17.887, 13.650, 9.500)},
    {'length': 27.000, 'start': (13.500, 18.000, 16.000), 'end': (-13.500, 18.000, 16.000)},
    {'length': 6.505, 'start': (-13.698, 17.850, 9.500), 'end': (-13.500, 18.000, 16.000)},
    {'length': 3.002, 'start': (-22.450, -1.500, 16.000), 'end': (-22.450, 1.500, 16.000)},
    {'length': 44.879, 'start': (-22.439, -1.650, 9.500), 'end': (22.439, -1.650, 9.500)},
    {'length': 6.505, 'start': (13.500, 18.000, 16.000), 'end': (13.698, 17.850, 9.500)},
    {'length': 6.502, 'start': (19.900, -10.500, 16.000), 'end': (19.820, -10.650, 9.500)},
    {'length': 27.000, 'start': (13.500, -18.000, 16.000), 'end': (-13.500, -18.000, 16.000)},
    {'length': 38.253, 'start': (19.127, 11.850, 9.500), 'end': (-19.127, 11.850, 9.500)},
    {'length': 1.386, 'start': (-19.127, -11.850, 9.500), 'end': (-19.820, -10.650, 9.500)},
    {'length': 6.502, 'start': (-22.299, -3.000, 16.000), 'end': (-22.319, -2.850, 9.500)},
    {'length': 1.665, 'start': (19.900, 10.500, 16.000), 'end': (20.622, 9.000, 16.000)},
    {'length': 1.872, 'start': (15.134, -16.650, 9.500), 'end': (13.698, -17.850, 9.500)},
    {'length': 75.398, 'start': (0.000, 12.000, 5.000), 'end': (0.000, 12.000, 5.000)},
    {'length': 1.522, 'start': (22.045, 4.500, 16.000), 'end': (22.299, 3.000, 16.000)},
    {'length': 43.370, 'start': (21.685, -6.000, 16.000), 'end': (-21.685, -6.000, 16.000)},
    {'length': 28.958, 'start': (-13.500, 18.000, 16.000), 'end': (13.500, 18.000, 16.000)},
    {'length': 44.879, 'start': (-22.439, 1.650, 9.500), 'end': (22.439, 1.650, 9.500)},
    {'length': 6.502, 'start': (-19.033, -12.000, 16.000), 'end': (-19.127, -11.850, 9.500)},
    {'length': 30.594, 'start': (15.297, 16.500, 16.000), 'end': (-15.297, 16.500, 16.000)},
    {'length': 33.541, 'start': (16.771, -15.000, 16.000), 'end': (-16.771, -15.000, 16.000)},
    {'length': 1.665, 'start': (20.622, -9.000, 16.000), 'end': (19.900, -10.500, 16.000)},
    {'length': 1.822, 'start': (-19.033, 12.000, 16.000), 'end': (-18.000, 13.500, 16.000)},
    {'length': 1.822, 'start': (-18.000, -13.500, 16.000), 'end': (-19.033, -12.000, 16.000)},
    {'length': 1.386, 'start': (-19.820, 10.650, 9.500), 'end': (-19.127, 11.850, 9.500)},
    {'length': 6.503, 'start': (17.887, 13.650, 9.500), 'end': (18.000, 13.500, 16.000)},
    {'length': 41.373, 'start': (20.686, -8.850, 9.500), 'end': (-20.686, -8.850, 9.500)},
    {'length': 6.502, 'start': (-19.127, 11.850, 9.500), 'end': (-19.033, 12.000, 16.000)},
    {'length': 1.206, 'start': (22.439, -1.650, 9.500), 'end': (22.319, -2.850, 9.500)},
    {'length': 36.000, 'start': (18.000, 13.500, 16.000), 'end': (-18.000, 13.500, 16.000)},
    {'length': 27.395, 'start': (13.698, -17.850, 9.500), 'end': (-13.698, -17.850, 9.500)},
    {'length': 141.372, 'start': (0.000, 22.500, 5.000), 'end': (0.000, 22.500, 5.000)},
    {'length': 1.822, 'start': (18.000, 13.500, 16.000), 'end': (19.033, 12.000, 16.000)},
    {'length': 6.502, 'start': (21.726, -5.850, 9.500), 'end': (21.685, -6.000, 16.000)},
    {'length': 2.103, 'start': (-15.297, -16.500, 16.000), 'end': (-16.771, -15.000, 16.000)},
    {'length': 6.502, 'start': (-22.439, 1.650, 9.500), 'end': (-22.450, 1.500, 16.000)},
    {'length': 2.103, 'start': (16.771, -15.000, 16.000), 'end': (15.297, -16.500, 16.000)},
    {'length': 6.503, 'start': (-18.000, 13.500, 16.000), 'end': (-17.887, 13.650, 9.500)},
    {'length': 6.502, 'start': (19.127, -11.850, 9.500), 'end': (19.033, -12.000, 16.000)},
    {'length': 1.573, 'start': (21.685, -6.000, 16.000), 'end': (21.213, -7.500, 16.000)},
    {'length': 6.502, 'start': (-21.726, 5.850, 9.500), 'end': (-21.685, 6.000, 16.000)},
    {'length': 42.319, 'start': (21.160, 7.650, 9.500), 'end': (-21.160, 7.650, 9.500)},
    {'length': 6.503, 'start': (16.903, -14.850, 9.500), 'end': (16.771, -15.000, 16.000)},
    {'length': 38.066, 'start': (19.033, 12.000, 16.000), 'end': (-19.033, 12.000, 16.000)},
    {'length': 38.253, 'start': (19.127, -11.850, 9.500), 'end': (-19.127, -11.850, 9.500)},
    {'length': 1.206, 'start': (-22.319, 2.850, 9.500), 'end': (-22.439, 1.650, 9.500)},
    {'length': 6.503, 'start': (18.000, -13.500, 16.000), 'end': (17.887, -13.650, 9.500)},
    {'length': 6.502, 'start': (-21.160, -7.650, 9.500), 'end': (-21.213, -7.500, 16.000)},
    {'length': 6.505, 'start': (-13.500, -18.000, 16.000), 'end': (-13.698, -17.850, 9.500)},
    {'length': 6.502, 'start': (-22.439, -1.650, 9.500), 'end': (-22.450, -1.500, 16.000)},
    {'length': 6.502, 'start': (-21.213, 7.500, 16.000), 'end': (-21.160, 7.650, 9.500)},
    {'length': 43.452, 'start': (21.726, -5.850, 9.500), 'end': (-21.726, -5.850, 9.500)},
    {'length': 44.900, 'start': (22.450, -1.500, 16.000), 'end': (-22.450, -1.500, 16.000)},
    {'length': 6.502, 'start': (-21.685, -6.000, 16.000), 'end': (-21.726, -5.850, 9.500)},
    {'length': 6.504, 'start': (-15.134, -16.650, 9.500), 'end': (-15.297, -16.500, 16.000)},
    {'length': 39.799, 'start': (19.900, 10.500, 16.000), 'end': (-19.900, 10.500, 16.000)},
    {'length': 6.502, 'start': (-22.045, 4.500, 16.000), 'end': (-22.014, 4.650, 9.500)},
    {'length': 30.594, 'start': (15.297, -16.500, 16.000), 'end': (-15.297, -16.500, 16.000)},
    {'length': 33.807, 'start': (16.903, 14.850, 9.500), 'end': (-16.903, 14.850, 9.500)},
    {'length': 6.502, 'start': (20.686, -8.850, 9.500), 'end': (20.622, -9.000, 16.000)},
    {'length': 44.598, 'start': (22.299, 3.000, 16.000), 'end': (-22.299, 3.000, 16.000)},
    {'length': 35.773, 'start': (17.887, -13.650, 9.500), 'end': (-17.887, -13.650, 9.500)},
    {'length': 42.319, 'start': (21.160, -7.650, 9.500), 'end': (-21.160, -7.650, 9.500)},
    {'length': 1.234, 'start': (21.726, 5.850, 9.500), 'end': (22.014, 4.650, 9.500)},
    {'length': 27.395, 'start': (13.698, 17.850, 9.500), 'end': (-13.698, 17.850, 9.500)},
    {'length': 36.000, 'start': (18.000, -13.500, 16.000), 'end': (-18.000, -13.500, 16.000)},
    {'length': 6.502, 'start': (22.014, 4.650, 9.500), 'end': (22.045, 4.500, 16.000)},
    {'length': 1.522, 'start': (-22.299, 3.000, 16.000), 'end': (-22.045, 4.500, 16.000)},
    {'length': 6.503, 'start': (-17.887, -13.650, 9.500), 'end': (-18.000, -13.500, 16.000)},
    {'length': 30.267, 'start': (15.134, 16.650, 9.500), 'end': (-15.134, 16.650, 9.500)},
]

# Konvertiert Edge-Typen in lesbare Strings
def edge_type_to_string(edge_type):
    edge_type_mapping = {
        NXOpen.EdgeEdgeType.Rubber: "Rubber",
        NXOpen.EdgeEdgeType.Linear: "Linear",
        NXOpen.EdgeEdgeType.Circular: "Circular",
        NXOpen.EdgeEdgeType.Elliptical: "Elliptical",
        NXOpen.EdgeEdgeType.Intersection: "Intersection",
        NXOpen.EdgeEdgeType.Spline: "Spline",
        NXOpen.EdgeEdgeType.SpCurve: "SP Curve",
        NXOpen.EdgeEdgeType.Foreign: "Foreign",
        NXOpen.EdgeEdgeType.ConstantParameter: "Constant Parameter",
        NXOpen.EdgeEdgeType.TrimmedCurve: "Trimmed Curve",
        NXOpen.EdgeEdgeType.Convergent: "Convergent",
        NXOpen.EdgeEdgeType.Undefined: "Undefined"
    }
    return edge_type_mapping.get(edge_type, f"Unknown Type: {edge_type}")

# Konvertiert Face-Typen in lesbare Strings
def face_type_to_string(face_type):
    face_type_mapping = {
        NXOpen.Face.FaceType.Rubber: "Rubber",
        NXOpen.Face.FaceType.Planar: "Planar",
        NXOpen.Face.FaceType.Cylindrical: "Cylindrical",
        NXOpen.Face.FaceType.Conical: "Conical",
        NXOpen.Face.FaceType.Spherical: "Spherical",
        NXOpen.Face.FaceType.SurfaceOfRevolution: "Surface of Revolution",
        NXOpen.Face.FaceType.Parametric: "Parametric",
        NXOpen.Face.FaceType.Blending: "Blending",
        NXOpen.Face.FaceType.Offset: "Offset",
        NXOpen.Face.FaceType.Swept: "Swept",
        NXOpen.Face.FaceType.Convergent: "Convergent",
        NXOpen.Face.FaceType.Undefined: "Undefined"
    }
    return face_type_mapping.get(face_type, f"Unknown Type: {face_type}")

# Gibt Details eines Körpers aus
def print_body_details(lw, body, body_idx, body_count):
    lw.WriteLine("-" * 50)
    lw.WriteLine(f"Körper {body_idx}/{body_count} wird inspiziert: {body.Name}")
    lw.WriteLine(f"Journal Identifier: {body.JournalIdentifier}")
    for face_idx, face in enumerate(body.GetFaces(), start=1):
        print_face_details(lw, face, face_idx)

# Gibt Details einer Fläche aus
def print_face_details(lw, face, face_idx):
    lw.WriteLine(f"  Fläche {face_idx}: Typ - {face_type_to_string(face.SolidFaceType)}")
    edges = face.GetEdges()
    lw.WriteLine(f"  Anzahl der Kanten: {len(edges)}")
    for edge_idx, edge in enumerate(edges, start=1):
        print_edge_details(lw, edge, edge_idx)
    lw.WriteLine("\n")

# Gibt Details einer Kante aus
def print_edge_details(lw, edge, edge_idx):
    # Bestimme den Typ der Kante basierend auf der Instanzklasse
    if isinstance(edge, NXOpen.Line):
        edge_type_name = "Linear"
        lw.WriteLine(f"    Kante {edge_idx}: Typ - {edge_type_name}, Länge - {edge.GetLength():.3f}")
    elif isinstance(edge, NXOpen.Arc):
        edge_type_name = "Circular"
        lw.WriteLine(f"    Kante {edge_idx}: Typ - {edge_type_name}, Länge (Umfang) - {edge.GetLength():.3f}")
        print_circular_edge_details(lw, edge)
    else:
        edge_type_name = "Unbekannter Typ"
        lw.WriteLine(f"    Kante {edge_idx}: Typ - {edge_type_name}, Länge - {edge.GetLength():.3f}")

# Gibt Details einer kreisförmigen Kante aus
def print_circular_edge_details(lw, edge):
    circumference = edge.GetLength()
    radius = circumference / (2 * math.pi)
    diameter = 2 * radius
    lw.WriteLine(f"    Radius des Kreises: {radius:.3f}")
    lw.WriteLine(f"    Durchmesser des Kreises: {diameter:.3f}")

# Analyse und Ausgabe der Details einer Extrusionsfunktion
def print_extrude_details(lw, feature, workPart):
    lw.WriteLine(f"Analyzing Extrude Feature: {feature.JournalIdentifier}")
    extrude = feature
    builder = workPart.Features.CreateExtrudeBuilder(extrude)
    try:
        # Basic properties of the extrude
        start_value = float(builder.Limits.StartExtend.Value.RightHandSide)
        end_value = float(builder.Limits.EndExtend.Value.RightHandSide)
        lw.WriteLine(f"  Start Distance of Extrusion: {start_value}")
        lw.WriteLine(f"  End Distance of Extrusion: {end_value}")
        lw.WriteLine(f"  Extrusion Height: {abs(end_value - start_value)}")

        # Accessing the section and its geometry
        section = builder.Section
        if section:
            curves = section.GetOutputCurves()
            lw.WriteLine("  Section Curves:")
            for curve in curves:
                curve_type = type(curve).__name__  # Using __name__ to get the type as a string
                lw.WriteLine(f"    Curve Type: {curve_type}")
                if isinstance(curve, NXOpen.Line):
                    start_point = curve.StartPoint
                    end_point = curve.EndPoint
                    line_length = math.sqrt((end_point.X - start_point.X)**2 + (end_point.Y - start_point.Y)**2 + (end_point.Z - start_point.Z)**2)
                    lw.WriteLine(f"    Line Start Point: {start_point.X}, {start_point.Y}, {start_point.Z}")
                    lw.WriteLine(f"    Line End Point: {end_point.X}, {end_point.Y}, {end_point.Z}")
                    lw.WriteLine(f"    Line Length: {line_length:.3f}")
                elif isinstance(curve, NXOpen.Arc):
                    center = curve.CenterPoint
                    lw.WriteLine(f"    Arc Center: {center.X}, {center.Y}, {center.Z}")
                    lw.WriteLine(f"    Radius: {curve.Radius}")
        else:
            lw.WriteLine("  No Section available for this extrude")

    except Exception as e:
        lw.WriteLine(f"  Error analyzing extrude details: {str(e)}")
    finally:
        builder.Destroy()

# Analyse und Ausgabe der Details einer Bohrfunktion
def print_hole_details(lw, feature, workPart):
    lw.WriteLine(f"Analyzing Hole Feature: {feature.JournalIdentifier}")
    try:
        # Create the HolePackageBuilder
        hole_builder = workPart.Features.CreateHolePackageBuilder(feature)

        # Fetch and display various properties
        hole_depth_expr = hole_builder.GeneralSimpleHoleDepth
        hole_depth = hole_depth_expr.RightHandSide if hole_depth_expr else "Undefined"

        hole_diameter_expr = hole_builder.GeneralSimpleHoleDiameter
        hole_diameter = hole_diameter_expr.RightHandSide if hole_diameter_expr else "Undefined"

        # Fetch type, boolean operation, general hole form, and counterbore details
        hole_type = hole_builder.Type.value
        boolean_operation = hole_builder.BooleanOperation
        general_hole_form = hole_builder.GeneralHoleForm.value

        # Enum mapping
        hole_type_descriptions = {
            0: "General Hole",
            1: "Drill Size Hole",
            2: "Screw Clearance Hole",
            3: "Threaded Hole",
            4: "Hole Series"
        }
        
        hole_form_descriptions = {
            0: "Simple",
            1: "Counterbored",
            2: "Countersink",
            3: "Tapered"
        }

        lw.WriteLine(f"  Hole Depth: {hole_depth}")
        lw.WriteLine(f"  Hole Diameter: {hole_diameter}")
        lw.WriteLine(f"  Type: {hole_type_descriptions.get(hole_type, 'Unknown Type')}")
        lw.WriteLine(f"  Boolean Operation: {boolean_operation}")
        lw.WriteLine(f"  General Hole Form: {hole_form_descriptions.get((general_hole_form), 'Unknown Form')}")

        # Counterbore details
        if hole_builder.GeneralCounterboreDiameter:
            counterbore_diameter_expr = hole_builder.GeneralCounterboreDiameter
            counterbore_diameter = counterbore_diameter_expr.RightHandSide
            lw.WriteLine(f"  Counterbore Diameter: {counterbore_diameter}")

        if hole_builder.GeneralCounterboreDepth:
            counterbore_depth_expr = hole_builder.GeneralCounterboreDepth
            counterbore_depth = counterbore_depth_expr.RightHandSide
            lw.WriteLine(f"  Counterbore Depth: {counterbore_depth}")

    except Exception as e:
        lw.WriteLine(f"Error analyzing hole feature details: {str(e)}")
    finally:
        # Always destroy the builder to release resources
        hole_builder.Destroy()

# Analyse und Ausgabe der Details einer Rotationsfunktion
def print_revolve_details(lw, feature, workPart):
    lw.WriteLine(f"Analyzing Revolved Feature: {feature.JournalIdentifier}")
    revolve = feature
    try:
        revolve_builder = workPart.Features.CreateRevolveBuilder(revolve)

        # Zugriff auf die Achse und ihre Details
        axis = revolve_builder.Axis
        if axis:
            direction_vector = axis.Direction.Vector
            point_coordinates = axis.Point.Coordinates
            lw.WriteLine(f"  Axis: Direction - X: {direction_vector.X}, Y: {direction_vector.Y}, Z: {direction_vector.Z}, Point - X: {point_coordinates.X}, Y: {point_coordinates.Y}, Z: {point_coordinates.Z}")

        # Start und Ende der Begrenzungen
        limits = revolve_builder.Limits
        if limits:
            start_value = limits.StartExtend.Value.RightHandSide if limits.StartExtend.Value else "Undefined"
            end_value = limits.EndExtend.Value.RightHandSide if limits.EndExtend.Value else "Undefined"
            lw.WriteLine(f"  Start Extend Value: {start_value}")
            lw.WriteLine(f"  End Extend Value: {end_value}")

        # Zugriff auf die Toleranz
        tolerance = revolve_builder.Tolerance
        lw.WriteLine(f"  Tolerance: {tolerance}")

        # Zugriff auf die Section und deren Geometrie
        section = revolve_builder.Section
        if section:
            curves = section.GetOutputCurves()
            lw.WriteLine("  Section Curves:")
            for curve in curves:
                curve_type = type(curve).Name
                lw.WriteLine(f"    Curve Type: {curve_type}")
                if isinstance(curve, NXOpen.Arc):
                    lw.WriteLine(f"    Arc Center: {curve.CenterPoint.X}, {curve.CenterPoint.Y}, {curve.CenterPoint.Z}")
                    lw.WriteLine(f"    Radius: {curve.Radius}")
                elif isinstance(curve, NXOpen.Line):
                    start_point = curve.StartPoint
                    end_point = curve.EndPoint
                    line_length = math.sqrt((end_point.X - start_point.X) ** 2 + (end_point.Y - start_point.Y) ** 2 + (end_point.Z - start_point.Z) ** 2)
                    lw.WriteLine(f"    Line Start Point: {start_point.X}, {start_point.Y}, {start_point.Z}")
                    lw.WriteLine(f"    Line End Point: {end_point.X}, {end_point.Y}, {end_point.Z}")
                    lw.WriteLine(f"    Line Length: {line_length:.3f}")
        else:
            lw.WriteLine("  No Section available for this revolve")

    except Exception as e:
        lw.WriteLine(f"  Error analyzing revolve details: {str(e)}")
    finally:
        revolve_builder.Destroy()

def process_geometry(curve, all_edges, circles):
    if isinstance(curve, NXOpen.Arc):
        circles.append(curve)
    elif isinstance(curve, NXOpen.Line):
        all_edges.append(curve)

# Berechnet, ob spezifische Kantenlängen vorhanden sind
def check_specific_edge_lengths(all_edges):
    required_lengths = [22.5, 11.0, 10.5, 5.0, 12.0, 16.0]
    found_lengths = [edge.GetLength() for edge in all_edges]
    return all(any(math.isclose(length, required, rel_tol=1e-5) for length in found_lengths) for required in required_lengths)

# Funktion zur Überprüfung der spezifischen Kreiseigenschaften (für die Alternativlösung)
def check_circular_features(circles):
    # Definierte Radien für die Alternative Lösung
    required_radii = [12.0, 22.5]

    found_radii = [circle.Radius for circle in circles]

    # Prüfen, ob alle benötigten Radien vorhanden sind, Reihenfolge ist egal
    return all(any(math.isclose(found, required, rel_tol=1e-5) for found in found_radii) for required in required_radii)

def check_specific_edge_lengths2(all_edges):
    required_lengths = [444.000, 17.000, 126.000, 0.500, 10.000, 2.000, 21.000, 0.500, 18.000, 5.000, 170.000, 2.500, 12.000, 5.000, 0.500, 5.000, 19.500, 65.000, 2.500, 17.000]
    found_lengths = [edge.GetLength() for edge in all_edges]
    return all(any(math.isclose(length, required, rel_tol=1e-5) for length in found_lengths) for required in required_lengths)


# Überprüft, ob ein Musterfeature vorhanden ist
def check_pattern_feature(all_edges):
    # required_pattern_lengths = [1.5, 6.502, 6.502, 1.2]
    # Erstellen eines Dictionarys zur Überwachung der erforderlichen Häufigkeiten
    required_counts = {1.5: 1, 6.502: 2, 1.2: 1}
    found_lengths = [round(edge.GetLength(), 3) for edge in all_edges]

    # Erstellen eines Counts Dictionary aus den gefundenen Längen
    found_counts = {}
    for length in found_lengths:
        if length in found_counts:
            found_counts[length] += 1
        else:
            found_counts[length] = 1

    # Überprüfen, ob alle benötigten Längen in der erforderlichen Häufigkeit gefunden wurden
    for length, count in required_counts.items():
        if found_counts.get(length, 0) < count:
            return False
    return True

# Überprüft, ob ein Musterfeature vorhanden ist
def check_passfeder_feature(all_edges):
    # required_pattern_lengths = [1.5, 6.502, 6.502, 1.2]
    # Erstellen eines Dictionarys zur Überwachung der erforderlichen Häufigkeiten
    required_counts = {31.0: 2, 55: 1}
    found_lengths = [round(edge.GetLength(), 3) for edge in all_edges]

    # Erstellen eines Counts Dictionary aus den gefundenen Längen
    found_counts = {}
    for length in found_lengths:
        if length in found_counts:
            found_counts[length] += 1
        else:
            found_counts[length] = 1

    # Überprüfen, ob alle benötigten Längen in der erforderlichen Häufigkeit gefunden wurden
    for length, count in required_counts.items():
        if found_counts.get(length, 0) < count:
            return False
    return True


# Überprüft, ob ein Musterfeature vorhanden ist
def check_keilwelle_feature(all_edges):
    # required_pattern_lengths = [1.5, 6.502, 6.502, 1.2]
    # Erstellen eines Dictionarys zur Überwachung der erforderlichen Häufigkeiten
    required_counts = {3.106: 2}
    found_lengths = [round(edge.GetLength(), 3) for edge in all_edges]

    # Erstellen eines Counts Dictionary aus den gefundenen Längen
    found_counts = {}
    for length in found_lengths:
        if length in found_counts:
            found_counts[length] += 1
        else:
            found_counts[length] = 1

    # Überprüfen, ob alle benötigten Längen in der erforderlichen Häufigkeit gefunden wurden
    for length, count in required_counts.items():
        if found_counts.get(length, 0) < count:
            return False
    return True

def check_passfeder_feature_with_lengths(workPart, lw):
    """
    Überprüft, ob ein Extrusionsfeature (EXTRUDE(7)) mit bestimmten Linienlängen vorhanden ist.
    """
    required_lengths = [31, 31, 7, 7]
    for feature in workPart.Features:
        if isinstance(feature, NXOpen.Features.Extrude):
            builder = workPart.Features.CreateExtrudeBuilder(feature)
            try:
                section = builder.Section
                if section:
                    curves = section.GetOutputCurves()
                    lengths = []
                    for curve in curves:
                        if isinstance(curve, NXOpen.Line):
                            start_point = curve.StartPoint
                            end_point = curve.EndPoint
                            line_length = math.sqrt((end_point.X - start_point.X)**2 + (end_point.Y - start_point.Y)**2 + (end_point.Z - start_point.Z)**2)
                            lengths.append(round(line_length, 3))
                        elif isinstance(curve, NXOpen.Arc):
                            lengths.append(round(curve.Radius, 3))  # Hier Radius verwenden

                    if all(length in lengths for length in required_lengths):
                        lw.WriteLine("Extrude Feature für Passfeder mit den erforderlichen Längen vorhanden.")
                        return True
            except Exception as e:
                lw.WriteLine(f"Fehler bei der Analyse des Features {feature.JournalIdentifier}: {str(e)}")
            finally:
                builder.Destroy()
    lw.WriteLine("Extrude Feature für Passfeder ohne die erforderlichen Längen gefunden.")
    return False

def check_keilwelle_feature_with_lengths(workPart, lw):
    """
    Überprüft, ob ein Extrusionsfeature (EXTRUDE(7)) mit bestimmten Linienlängen vorhanden ist.
    """
    required_lengths = [3.106, 3.106, 14.000, 17.000]
    for feature in workPart.Features:
        if isinstance(feature, NXOpen.Features.Extrude):
            builder = workPart.Features.CreateExtrudeBuilder(feature)
            try:
                section = builder.Section
                if section:
                    curves = section.GetOutputCurves()
                    lengths = []
                    for curve in curves:
                        if isinstance(curve, NXOpen.Line):
                            start_point = curve.StartPoint
                            end_point = curve.EndPoint
                            line_length = math.sqrt((end_point.X - start_point.X)**2 + (end_point.Y - start_point.Y)**2 + (end_point.Z - start_point.Z)**2)
                            lengths.append(round(line_length, 3))
                        elif isinstance(curve, NXOpen.Arc):
                            lengths.append(round(curve.Radius, 3))  # Hier Radius verwenden

                    if all(length in lengths for length in required_lengths):
                        lw.WriteLine("Extrude Feature für Keilwelle mit den erforderlichen Längen vorhanden.")
                        return True
            except Exception as e:
                lw.WriteLine(f"Fehler bei der Analyse des Features {feature.JournalIdentifier}: {str(e)}")
            finally:
                builder.Destroy()
    lw.WriteLine("Extrude Feature für Keilwelle ohne die erforderlichen Längen gefunden.")

    return False

def check_faces_against_reference_ue1(workPart, lw):
    """
    Überprüft das Vorhandensein von Flächen im vorliegenden Körper gegen eine Musterlösung.
    """
    lw.WriteLine("==================================================")
    lw.WriteLine("Analyse der vorhandenen Flächen gegen die Musterlösung")
    lw.WriteLine("==================================================")


    lw.WriteLine("Starte Überprüfung der Flächen gegen die Musterlösung...")

    # Definition der Musterlösung
    reference_faces = [
        ("Planar", [38.253, 39.640, 1.386, 1.386]),
        ("Planar", [27.395, 1.872, 1.872, 30.267]),
        ("Planar", [44.900, 44.879, 6.502, 6.502]),
        ("Planar", [39.799, 1.665, 1.665, 41.243]),
        ("Planar", [1.552, 35.773, 33.807, 1.552]),
        ("Planar", [41.243, 1.665, 39.799, 1.665]),
        ("Planar", [6.502, 6.502, 41.243, 41.373]),
        ("Planar", [1.522, 44.598, 1.522, 44.091]),
        ("Cylindrical", [3.002, 141.372, 6.502, 6.502, 1.206, 1.206, 6.502, 1.522, 6.502, 6.502, 6.504, 1.234, 2.103, 1.290, 6.503, 6.502, 6.502, 6.503, 1.872, 28.958, 6.503, 1.552, 6.502, 2.103, 1.290, 1.573, 6.502, 6.502, 6.503, 1.573, 1.822, 6.502, 1.234, 6.502, 6.502, 6.502, 1.872, 1.386, 1.665, 6.502, 1.552, 1.665, 6.504, 6.505, 1.522, 1.822, 6.505, 1.386, 6.502, 6.502, 6.502, 6.502, 1.522, 1.206, 1.206, 6.502, 3.002, 1.573, 6.502, 6.505, 6.502, 1.822, 1.872, 1.522, 2.103, 6.502, 6.502, 2.103, 6.503, 1.822, 6.502, 6.502, 6.502, 6.502, 1.386, 1.665, 6.502, 6.502, 6.503, 1.552, 1.290, 1.234, 1.573, 6.503, 1.872, 6.503, 6.502, 6.504, 1.290, 6.502, 6.505, 1.552, 28.958, 1.234, 1.665, 1.386, 6.504]),
        ("Cylindrical", [75.398, 75.398]),
        ("Planar", [1.822, 36.000, 1.822, 38.066]),
        ("Planar", [75.398]),
        ("Planar", [6.504, 30.594, 6.504, 30.267]),
        ("Planar", [27.000, 27.395, 6.505, 6.505]),
        ("Planar", [1.573, 43.370, 42.426, 1.573]),
        ("Planar", [6.502, 38.253, 6.502, 38.066]),
        ("Planar", [44.638, 44.879, 1.206, 1.206]),
        ("Planar", [6.503, 6.503, 35.773, 36.000]),
        ("Planar", [6.505, 27.395, 27.000, 6.505]),
        ("Planar", [28.958, 27.000]),
        ("Planar", [6.502, 6.502, 44.029, 44.091]),
        ("Planar", [27.000, 28.958]),
        ("Planar", [33.807, 1.552, 35.773, 1.552]),
        ("Planar", [44.879, 44.638, 1.206, 1.206]),
        ("Planar", [6.502, 6.502, 44.900, 44.879]),
        ("Planar", [6.502, 44.091, 44.029, 6.502]),
        ("Planar", [43.452, 1.234, 1.234, 44.029]),
        ("Planar", [1.386, 39.640, 38.253, 1.386]),
        ("Planar", [6.502, 39.640, 6.502, 39.799]),
        ("Planar", [1.234, 44.029, 1.234, 43.452]),
        ("Planar", [30.594, 6.504, 30.267, 6.504]),
        ("Planar", [1.290, 42.319, 1.290, 41.373]),
        ("Planar", [6.502, 43.370, 6.502, 43.452]),
        ("Planar", [6.502, 38.253, 6.502, 38.066]),
        ("Planar", [1.822, 1.822, 36.000, 38.066]),
        ("Planar", [2.103, 2.103, 30.594, 33.541]),
        ("Planar", [6.503, 33.807, 6.503, 33.541]),
        ("Planar", [44.598, 44.638, 6.502, 6.502]),
        ("Planar", [6.502, 44.638, 6.502, 44.598]),
        ("Planar", [44.598, 1.522, 44.091, 1.522]),
        ("Planar", [42.319, 6.502, 6.502, 42.426]),
        ("Planar", [41.243, 6.502, 6.502, 41.373]),
        ("Planar", [6.502, 39.799, 6.502, 39.640]),
        ("Planar", [33.807, 6.503, 6.503, 33.541]),
        ("Planar", [36.000, 6.503, 35.773, 6.503]),
        ("Planar", [2.103, 2.103, 30.594, 33.541]),
        ("Planar", [3.002, 44.900, 44.900, 3.002]),
        ("Planar", [141.372, 75.398]),
        ("Planar", [1.872, 27.395, 1.872, 30.267]),
        ("Planar", [1.573, 43.370, 1.573, 42.426]),
        ("Planar", [6.502, 6.502, 42.426, 42.319]),
        ("Planar", [43.452, 6.502, 43.370, 6.502]),
        ("Planar", [1.290, 42.319, 1.290, 41.373])
    ]

    # Extrahieren der Flächen aus dem aktuellen Werkstück
    current_faces = []
    for body in workPart.Bodies:
        for face in body.GetFaces():
            face_type = face_type_to_string(face.SolidFaceType)
            face_edges = face.GetEdges()
            face_edge_lengths = [round(edge.GetLength(), 3) for edge in face_edges]
            current_faces.append((face_type, sorted(face_edge_lengths)))

# Überprüfung, ob die Musterflächen im aktuellen Werkstück vorhanden sind
    total_reference_faces = len(reference_faces)
    found_reference_faces = 0

    for ref_face in reference_faces:
        ref_type, ref_edges = ref_face
        found = any(ref_type == cur_type and sorted(ref_edges) == sorted(cur_edges) for cur_type, cur_edges in current_faces)
        if found:
            # Kann verwendet werden, um anzugeben welche flächen vorhanden sind 
            #lw.WriteLine(f"Fläche vom Typ '{ref_type}' mit Kantenlängen {ref_edges} ist vorhanden.")
            found_reference_faces += 1
        else:
            lw.WriteLine(f"Fläche vom Typ '{ref_type}' mit Kantenlängen {ref_edges} ist nicht vorhanden.")

    lw.WriteLine(f"Es sind {found_reference_faces} von {total_reference_faces} erwarteten Flächen vorhanden.")
    lw.WriteLine("Überprüfung abgeschlossen.")

    return found_reference_faces

def check_faces_against_reference_vt1(workPart, lw):
    """
    Überprüft das Vorhandensein von Flächen im vorliegenden Körper gegen eine Musterlösung.
    """
    lw.WriteLine("==================================================")
    lw.WriteLine("Analyse der vorhandenen Flächen gegen die Musterlösung")
    lw.WriteLine("==================================================")


    lw.WriteLine("Starte Überprüfung der Flächen gegen die Musterlösung...")

    # Definition der Musterlösung
    reference_faces = [
    ("Planar", [109.956, 106.814]),
    ("Planar", [122.522]),
    ("Cylindrical", [125.664, 125.664]),
    ("Planar", [87.000, 3.106, 87.000, 3.106]),
    ("Planar", [9.727, 8.113, 3.106, 3.106, 9.727, 3.106, 3.106, 8.113, 3.106, 3.106, 9.727, 3.106, 3.106, 9.727, 3.106, 8.113, 8.113, 8.113, 3.106, 8.113, 3.106, 3.106, 9.727, 9.727]),
    ("Cylindrical", [109.956, 109.956]),
    ("Planar", [157.080, 125.664]),
    ("Cylindrical", [87.000, 8.113, 87.000, 8.113]),
    ("Planar", [157.080, 172.788]),
    ("Planar", [21.991, 31.000, 31.000, 21.991]),
    ("Planar", [3.106, 87.000, 87.000, 3.106]),
    ("Cylindrical", [8.113, 87.000, 8.113, 87.000]),
    ("Cylindrical", [122.522, 122.522]),
    ("Planar", [3.106, 3.106, 8.113, 8.076]),
    ("Cylindrical", [157.080, 157.080]),
    ("Planar", [87.000, 3.106, 3.106, 87.000]),
    ("Cylindrical", [172.788, 172.788]),
    ("Planar", [87.000, 3.106, 3.106, 87.000]),
    ("Planar", [141.372, 125.664]),
    ("Planar", [87.000, 3.106, 87.000, 3.106]),
    ("Cylindrical", [9.727, 106.814, 87.000, 87.000, 8.076, 9.727, 87.000, 87.000, 8.076, 87.000, 87.000, 9.727, 87.000, 9.727, 87.000, 87.000, 87.000, 8.076, 87.000, 8.076, 8.076, 8.076, 87.000, 9.727, 9.727]),
    ("Cylindrical", [8.113, 8.113, 87.000, 87.000]),
    ("Planar", [125.664, 122.522]),
    ("Planar", [4.383, 4.383, 31.000, 31.000]),
    ("Planar", [3.106, 8.076, 8.113, 3.106]),
    ("Cylindrical", [8.113, 87.000, 8.113, 87.000]),
    ("Planar", [8.113, 3.106, 3.106, 8.076]),
    ("Planar", [4.383, 31.000, 31.000, 4.383]),
    ("Cylindrical", [8.113, 87.000, 8.113, 87.000]),
    ("Planar", [87.000, 3.106, 3.106, 87.000]),
    ("Planar", [87.000, 87.000, 3.106, 3.106]),
    ("Cylindrical", [141.372, 141.372, 22.128, 31.000, 31.000, 22.128]),
    ("Planar", [3.106, 3.106, 87.000, 87.000]),
    ("Cylindrical", [122.522, 122.522]),
    ("Cylindrical", [22.128, 4.383, 4.383, 21.991]),
    ("Planar", [122.522, 109.956]),
    ("Planar", [141.372, 172.788]),
    ("Planar", [3.106, 87.000, 3.106, 87.000]),
    ("Planar", [8.113, 3.106, 8.076, 3.106]),
    ("Planar", [125.664, 122.522]),
    ("Planar", [3.106, 87.000, 87.000, 3.106]),
    ("Planar", [3.106, 87.000, 87.000, 3.106]),
    ("Cylindrical", [8.113, 8.113, 87.000, 87.000]),
    ("Planar", [87.000, 3.106, 3.106, 87.000]),
    ("Planar", [8.076, 8.113, 3.106, 3.106]),
    ("Cylindrical", [21.991, 4.383, 4.383, 22.128]),
    ("Cylindrical", [125.664, 125.664]),
    ("Planar", [8.113, 3.106, 3.106, 8.076])
]

    # Extrahieren der Flächen aus dem aktuellen Werkstück
    current_faces = []
    for body in workPart.Bodies:
        for face in body.GetFaces():
            face_type = face_type_to_string(face.SolidFaceType)
            face_edges = face.GetEdges()
            face_edge_lengths = [round(edge.GetLength(), 3) for edge in face_edges]
            current_faces.append((face_type, sorted(face_edge_lengths)))

# Überprüfung, ob die Musterflächen im aktuellen Werkstück vorhanden sind
    total_reference_faces = len(reference_faces)
    found_reference_faces = 0

    for ref_face in reference_faces:
        ref_type, ref_edges = ref_face
        found = any(ref_type == cur_type and sorted(ref_edges) == sorted(cur_edges) for cur_type, cur_edges in current_faces)
        if found:
            # Kann verwendet werden, um anzugeben welche flächen vorhanden sind 
            #lw.WriteLine(f"Fläche vom Typ '{ref_type}' mit Kantenlängen {ref_edges} ist vorhanden.")
            found_reference_faces += 1
        else:
            lw.WriteLine(f"Fläche vom Typ '{ref_type}' mit Kantenlängen {ref_edges} ist nicht vorhanden.")

    lw.WriteLine(f"Es sind {found_reference_faces} von {total_reference_faces} erwarteten Flächen vorhanden.")
    lw.WriteLine("Überprüfung abgeschlossen.")

    return found_reference_faces

def check_faces_against_reference_ue2(workPart, lw):
    """
    Überprüft das Vorhandensein von Flächen im vorliegenden Körper gegen eine Musterlösung.
    """
    lw.WriteLine("==================================================")
    lw.WriteLine("Analyse der vorhandenen Flächen gegen die Musterlösung")
    lw.WriteLine("==================================================")


    lw.WriteLine("Starte Überprüfung der Flächen gegen die Musterlösung...")

    # Definition der Musterlösung
    reference_faces = [
    ("Cylindrical", [1.152, 38.000, 1.152, 38.000]),
    ("Planar", [38.000, 38.000, 7.000, 7.000]),
    ("Spherical", [94.248]),
    ("Planar", [38.000, 38.000, 7.000, 7.000]),
    ("Planar", [5.000, 6.000, 5.000, 9.425, 7.854]),
    ("Parametric", [21.104, 25.235, 9.000, 10.997]),
    ("Cylindrical", [94.248, 19.990, 38.000, 19.990, 38.000, 94.248]),
    ("Spherical", [84.823]),
    ("Cylindrical", [7.854, 7.854]),
    ("Cylindrical", [3.380, 3.380, 17.279, 17.540]),
    ("Planar", [6.000, 8.838, 8.838, 6.051]),
    ("Cylindrical", [7.854, 7.854]),
    ("Planar", [38.000, 3.380, 3.380, 38.000]),
    ("Conical", [41.539, 84.125]),
    ("Conical", [0.707, 9.425, 0.707, 10.996]),
    ("Planar", [38.000, 21.991, 38.000, 21.991, 38.000, 38.000, 10.996, 10.996]),
    ("Conical", [7.854]),
    ("Planar", [38.000, 0.707, 38.000, 0.707]),
    ("Cylindrical", [2.500, 2.500, 9.425, 9.425]),
    ("Parametric", [21.104, 25.235, 9.000, 10.997]),
    ("Surface of Revolution", [31.416, 41.539]),
    ("Cylindrical", [21.991, 10.997, 10.997]),
    ("Conical", [0.707, 9.425, 10.996, 0.707]),
    ("Planar", [38.000, 3.380, 3.380, 38.000]),
    ("Planar", [2.500, 2.500, 5.000, 8.838, 5.000, 8.838, 28.000, 38.000]),
    ("Conical", [21.991, 84.823]),
    ("Parametric", [14.998, 19.997, 26.343, 15.700]),
    ("Cylindrical", [15.700, 15.700, 31.416]),
    ("Cylindrical", [21.991, 21.991, 7.000, 7.000]),
    ("Cylindrical", [84.823, 84.823, 28.000, 6.051, 6.051, 28.000]),
    ("Blending", [19.990, 1.152, 17.540, 1.152]),
    ("Planar", [2.500, 2.500, 5.000, 5.000, 8.838, 8.838, 28.000, 38.000]),
    ("Parametric", [19.997, 14.998, 26.343, 15.700]),
    ("Blending", [1.152, 1.152, 19.990, 17.540]),
    ("Cylindrical", [2.500, 2.500, 9.425, 9.425]),
    ("Planar", [38.000, 0.707, 0.707, 38.000]),
    ("Planar", [38.000, 38.000, 17.279, 21.991, 38.000, 38.000, 17.279, 21.991]),
    ("Planar", [8.838, 6.000, 8.838, 6.051]),
    ("Planar", [5.000, 5.000, 6.000, 9.425, 7.854]),
    ("Planar", [14.998, 14.998, 9.000, 9.000]),
    ("Cylindrical", [1.152, 38.000, 38.000, 1.152]),
    ("Cylindrical", [17.279, 3.380, 3.380, 17.540]),
    ("Surface of Revolution", [94.248, 84.125]),
    ("Conical", [7.854]),
    ("Cylindrical", [7.000, 7.000, 21.991, 21.991])
    ]

    # Extrahieren der Flächen aus dem aktuellen Werkstück
    current_faces = []
    for body in workPart.Bodies:
        for face in body.GetFaces():
            face_type = face_type_to_string(face.SolidFaceType)
            face_edges = face.GetEdges()
            face_edge_lengths = [round(edge.GetLength(), 3) for edge in face_edges]
            current_faces.append((face_type, sorted(face_edge_lengths)))

# Überprüfung, ob die Musterflächen im aktuellen Werkstück vorhanden sind
    total_reference_faces = len(reference_faces)
    found_reference_faces = 0

    for ref_face in reference_faces:
        ref_type, ref_edges = ref_face
        found = any(ref_type == cur_type and sorted(ref_edges) == sorted(cur_edges) for cur_type, cur_edges in current_faces)
        if found:
            # Kann verwendet werden, um anzugeben welche flächen vorhanden sind 
            #lw.WriteLine(f"Fläche vom Typ '{ref_type}' mit Kantenlängen {ref_edges} ist vorhanden.")
            found_reference_faces += 1
        else:
            lw.WriteLine(f"Fläche vom Typ '{ref_type}' mit Kantenlängen {ref_edges} ist nicht vorhanden.")

    lw.WriteLine(f"Es sind {found_reference_faces} von {total_reference_faces} erwarteten Flächen vorhanden.")
    lw.WriteLine("Überprüfung abgeschlossen.")

def check_faces_against_reference_vt2(workPart, lw):
    """
    Überprüft das Vorhandensein von Flächen im vorliegenden Körper gegen eine Musterlösung.
    """
    lw.WriteLine("==================================================")
    lw.WriteLine("Analyse der vorhandenen Flächen gegen die Musterlösung")
    lw.WriteLine("==================================================")


    lw.WriteLine("Starte Überprüfung der Flächen gegen die Musterlösung...")

    # Definition der Musterlösung
    reference_faces = [
    ("Cylindrical", [56.549, 56.549]),
    ("Cylindrical", [28.274, 28.274]),
    ("Cylindrical", [56.549, 56.549]),
    ("Planar", [865.720, 827.500]),
    ("Planar", [444.885, 113.097, 28.274, 56.549, 28.274, 56.549, 56.549, 56.549]),
    ("Cylindrical", [28.274, 28.274]),
    ("Offset", [827.500, 439.402]),
    ("Cylindrical", [113.097, 113.097]),
    ("Cylindrical", [56.549, 56.549]),
    ("Parametric", [444.885, 865.720]),
    ("Planar", [439.402, 113.097, 28.274, 56.549, 28.274, 56.549, 56.549, 56.549]),
    ("Cylindrical", [56.549, 56.549])
]

    # Extrahieren der Flächen aus dem aktuellen Werkstück
    current_faces = []
    for body in workPart.Bodies:
        for face in body.GetFaces():
            face_type = face_type_to_string(face.SolidFaceType)
            face_edges = face.GetEdges()
            face_edge_lengths = [round(edge.GetLength(), 3) for edge in face_edges]
            current_faces.append((face_type, sorted(face_edge_lengths)))

# Überprüfung, ob die Musterflächen im aktuellen Werkstück vorhanden sind
    total_reference_faces = len(reference_faces)
    found_reference_faces = 0

    for ref_face in reference_faces:
        ref_type, ref_edges = ref_face
        found = any(ref_type == cur_type and sorted(ref_edges) == sorted(cur_edges) for cur_type, cur_edges in current_faces)
        if found:
            # Kann verwendet werden, um anzugeben welche flächen vorhanden sind 
            #lw.WriteLine(f"Fläche vom Typ '{ref_type}' mit Kantenlängen {ref_edges} ist vorhanden.")
            found_reference_faces += 1
        else:
            lw.WriteLine(f"Fläche vom Typ '{ref_type}' mit Kantenlängen {ref_edges} ist nicht vorhanden.")

    lw.WriteLine(f"Es sind {found_reference_faces} von {total_reference_faces} erwarteten Flächen vorhanden.")
    lw.WriteLine("Überprüfung abgeschlossen.")

def get_mass_properties(body, workPart):
    measure_manager = NXOpen.MeasureManager(workPart)
    mass_properties = measure_manager.MeasureBodiesMassProperties([body])
    mass = mass_properties.Mass
    surface_area = mass_properties.Area
    center_of_gravity = mass_properties.CenterOfGravity
    return mass, surface_area, center_of_gravity

def print_mass_properties(lw, body, workPart):
    mass, surface_area, center_of_gravity = get_mass_properties(body, workPart)
    lw.WriteLine(f"  Masse: {mass:.3f}")
    lw.WriteLine(f"  Oberfläche: {surface_area:.3f}")
    lw.WriteLine(f"  Schwerpunkt: X: {center_of_gravity.X:.3f}, Y: {center_of_gravity.Y:.3f}, Z: {center_of_gravity.Z:.3f}")

# Erweiterte Funktion zum Ausgeben der Körperdetails
def print_body_details(lw, body, body_idx, body_count, workPart):
    lw.WriteLine("-" * 50)
    lw.WriteLine(f"Körper {body_idx}/{body_count} wird inspiziert: {body.Name}")
    lw.WriteLine(f"Journal Identifier: {body.JournalIdentifier}")
    #print_mass_properties(lw, body, workPart)  # Druckt die Masseninformationen
    for face_idx, face in enumerate(body.GetFaces(), start=1):
        print_face_details(lw, face, face_idx)

def check_circular_pattern_feature(workPart, lw):
    # Find the pattern feature
    pattern_features = [feat for feat in workPart.Features if isinstance(feat, NXOpen.Features.PatternFeature)]
    for pattern_feature in pattern_features:
        try:
            pattern_builder = workPart.Features.CreatePatternFeatureBuilder(pattern_feature)
            lw.WriteLine(f"Pattern Feature {pattern_feature.JournalIdentifier} hat den Muster-Typ: {pattern_builder.PatternMethod}")
            lw.WriteLine(f"Output Option: {pattern_builder.OutputOption}")
            lw.WriteLine(f"Expression Option: {pattern_builder.ExpressionOption}")
            
            # Fetch more properties if available
            reference_point = pattern_builder.ReferencePoint
            lw.WriteLine(f"Reference Point: {reference_point}")

            pattern_service = pattern_builder.PatternService
            lw.WriteLine(f"Pattern Service: {pattern_service}")
            
            feature_list = pattern_builder.FeatureList
            lw.WriteLine(f"Number of Features: {feature_list.GetCount()}")
            
        except Exception as e:
            lw.WriteLine(f"Fehler bei der Analyse des Features {pattern_feature.JournalIdentifier}: {str(e)}")
        finally:
            pattern_builder.Destroy()

def is_pattern_feature(feature):
    return isinstance(feature, NXOpen.Features.PatternFeature)

def is_mirror_feature(feature):
    return isinstance(feature, NXOpen.Features.MirrorFeature)

def count_pattern_and_mirror_features(workPart, lw):
    pattern_count = 0
    mirror_count = 0

    for feature in workPart.Features:
        if is_pattern_feature(feature):
            lw.WriteLine(f"Pattern Feature gefunden: {feature.JournalIdentifier}")  # Debugging-Ausgabe
            pattern_count += 1
        if is_mirror_feature(feature):
            lw.WriteLine(f"Mirror Feature gefunden: {feature.JournalIdentifier}")  # Debugging-Ausgabe
            mirror_count += 1

    lw.WriteLine(f"Anzahl der Pattern Features: {pattern_count}")
    lw.WriteLine(f"Anzahl der Mirror Features: {mirror_count}")
    return pattern_count, mirror_count

def get_pattern_feature_count(workPart, lw):
    """
    Ermittelt, wie oft das Pattern Feature mit bestimmten Dimensionen im Werkstück vorkommt.
    """
    required_lengths = [1.5, 6.502, 6.502, 1.2]
    pattern_count = 0

    # Durchsuchen aller Features im Werkstück
    for feature in workPart.Features:
        if isinstance(feature, NXOpen.Features.Extrude):
            # Prüfen, ob das Feature ein Pattern Feature ist
            builder = workPart.Features.CreateExtrudeBuilder(feature)
            try:
                section = builder.Section
                if section:
                    curves = section.GetOutputCurves()
                    lengths = [
                        round(math.sqrt((curve.EndPoint.X - curve.StartPoint.X)**2 +
                                        (curve.EndPoint.Y - curve.StartPoint.Y)**2 +
                                        (curve.EndPoint.Z - curve.StartPoint.Z)**2), 3)
                        for curve in curves if isinstance(curve, NXOpen.Line)
                    ]
                    # Prüfen, ob alle erforderlichen Längen vorhanden sind
                    if sorted(lengths) == sorted(required_lengths):
                        pattern_count += 1
            except Exception as e:
                lw.WriteLine(f"Error processing feature {feature.JournalIdentifier}: {str(e)}")
            finally:
                builder.Destroy()

   # lw.WriteLine(f"Pattern Feature mit spezifischen Dimensionen kommt {pattern_count} mal vor.")
    return pattern_count

def extract_edge_positions(workPart, lw):
    """
    Extrahiert die Positionen aller Kanten aus dem Teil.
    """
    edge_positions = []  # Liste zur Speicherung der Positionen der Kanten

    for body in workPart.Bodies:
        for edge in body.GetEdges():
            vertices = edge.GetVertices()
            start_point = vertices[0]
            end_point = vertices[1]
            edge_length = edge.GetLength()
            edge_type = edge.SolidEdgeType
            
            edge_positions.append({
                'start': (start_point.X, start_point.Y, start_point.Z),
                'end': (end_point.X, end_point.Y, end_point.Z),
                'length': edge_length,
                'type': edge_type
            })
    
    return edge_positions

def calculate_relative_positions(edges):
    """
    Berechnet die relativen Positionen der Kanten zueinander.
    """
    relative_positions = []
    for (edge1_idx, edge1), (edge2_idx, edge2) in combinations(enumerate(edges), 2):
        start_distance = calculate_distance(edge1['start'], edge2['start'])
        end_distance = calculate_distance(edge1['end'], edge2['end'])
        relative_positions.append((start_distance, end_distance))
    return relative_positions


def calculate_distance(point1, point2):
    """
    Berechnet die euklidische Distanz zwischen zwei Punkten.
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

def compare_relative_positions(reference_positions, test_positions, tolerance=1e-5):
    """
    Vergleicht die relativen Positionen der Referenzkanten mit den Testkanten.
    """
    if len(reference_positions) != len(test_positions):
        return False

    for (ref_start_dist, ref_end_dist), (test_start_dist, test_end_dist) in zip(reference_positions, test_positions):
        if not (math.isclose(ref_start_dist, test_start_dist, rel_tol=tolerance) and math.isclose(ref_end_dist, test_end_dist, rel_tol=tolerance)):
            return False

    return True

def check_relative_positions(reference_edges, test_edges, tolerance=1e-1):
    """
    Überprüft, ob die relativen Positionen der Kanten im Testkörper mit der Referenz übereinstimmen.
    """
    reference_positions = calculate_relative_positions(reference_edges)
    test_positions = calculate_relative_positions(test_edges)

    return compare_relative_positions(reference_positions, test_positions, tolerance)

def check_edges_against_reference(workPart, lw):
    """
    Überprüft die Kantenpositionen des aktuellen Teils gegen die Referenzkanten.
    """
    lw.WriteLine("==================================================")
    lw.WriteLine("Überprüfung der Kantenpositionen gegen Referenzkanten")
    lw.WriteLine("==================================================")

    # Extrahiert die aktuellen Kantenpositionen aus dem Teil
    edge_positions = extract_edge_positions(workPart, lw)
    
    # Prüft die relativen Positionen gegen die Referenzkanten
    is_matching = check_relative_positions(REFERENCE_EDGES_UE1, edge_positions)

    if is_matching:
        lw.WriteLine("Die Kantenpositionen stimmen mit den Referenzkanten überein.")
    else:
        lw.WriteLine("Die Kantenpositionen stimmen NICHT mit den Referenzkanten überein.")

def extract_line_positions(workPart, lw):
    """
    Extrahiert die Positionen aller Linien aus dem Teil.
    """
    lw.WriteLine("==================================================")
    lw.WriteLine("Extrahieren der Positionen aller Linien im Teil")
    lw.WriteLine("==================================================")

    edge_positions = []  # Liste zur Speicherung der Positionen der Kanten

    # Zählen der Körper
    body_count = sum(1 for _ in workPart.Bodies)
    lw.WriteLine(f"Anzahl der Körper: {body_count}")

    for body_idx, body in enumerate(workPart.Bodies, start=1):
        lw.WriteLine(f"Körper {body_idx} von {body_count}")
        for edge_idx, edge in enumerate(body.GetEdges(), start=1):
            vertices = edge.GetVertices()
            start_point = vertices[0]
            end_point = vertices[1]
            edge_length = edge.GetLength()
            edge_type = edge.SolidEdgeType
            
            edge_positions.append({
                'start': (start_point.X, start_point.Y, start_point.Z),
                'end': (end_point.X, end_point.Y, end_point.Z),
                'length': edge_length,
                'type': edge_type
            })
       #     lw.WriteLine(f"  Kante {edge_idx}: Typ - {edge_type}, Länge - {edge_length:.3f}")
        #    lw.WriteLine(f"    Startpunkt - ({start_point.X:.3f}, {start_point.Y:.3f}, {start_point.Z:.3f})")
         #   lw.WriteLine(f"    Endpunkt - ({end_point.X:.3f}, {end_point.Y:.3f}, {end_point.Z:.3f})")

    lw.WriteLine(f"Anzahl der Kanten gefunden: {len(edge_positions)}")
    
    return edge_positions

#Ausgabe Übung 1
# Listet Merkmale und Geometrien auf
def list_features_and_geometries_ue1(theSession, workPart):
    lw = theSession.ListingWindow
    lw.Open()
    
    lw.WriteLine("=" * 50)
    lw.WriteLine("Analyse der Körper und Geometrien")
    lw.WriteLine("=" * 50)

    body_count = 0
    for body in workPart.Bodies:
        body_count += 1
    lw.WriteLine("Gesamtanzahl der Körper im Teil: " + str(body_count))

    #for body_idx, body in enumerate(workPart.Bodies, start=1):
     #   print_body_details(lw, body, body_idx, body_count, workPart)
    
    lw.WriteLine("=" * 50)
    lw.WriteLine("Feature-Analyse:")
    lw.WriteLine("=" * 50)
    for feature in workPart.Features:
        lw.WriteLine(f"Analyse des Features: {feature.JournalIdentifier} vom Typ {type(feature)}")
        if isinstance(feature, NXOpen.Features.Extrude):
            print_extrude_details(lw, feature, workPart)
        elif isinstance(feature, NXOpen.Features.Revolve):
            print_revolve_details(lw, feature, workPart)
        elif isinstance(feature, NXOpen.Features.HolePackage):
            print_hole_details(lw, feature, workPart)

    # Überprüfen und Zählen der Pattern- und Mirror-Features
    total_patterns, total_mirrors = count_pattern_and_mirror_features(workPart, lw)
    lw.WriteLine(f"Anzahl der Pattern Features: {total_patterns}")
    lw.WriteLine(f"Anzahl der Mirror Features: {total_mirrors}")

    lw.Close()

# Funktion zur Verarbeitung der Geometrie
def process_geometry(curve, all_edges, circles):
    if isinstance(curve, NXOpen.Line):
        all_edges.append(curve)
    elif isinstance(curve, NXOpen.Arc):
        circles.append(curve)
    elif isinstance(curve, NXOpen.Circle):
        circles.append(curve)

# Listet Geometrieeigenschaften in Skizzen auf
def list_geometry_properties_in_sketches_ue1(theSession, workPart):
    lw = theSession.ListingWindow
    lw.Open()

    lw.WriteLine("=" * 50)
    lw.WriteLine("Analyse der Skizzen")
    lw.WriteLine("=" * 50)
    
    # Variablen zur Erfassung des Zustands der Features über alle Skizzen hinweg
    rotations_feature_found = False
    pattern_feature_found = False
    alternative_solution_found = False

    all_circles = []

    for sketch_idx, sketch in enumerate(workPart.Sketches, start=1):
        lw.WriteLine(f"Skizze {sketch_idx}: {sketch.Name}")
        all_edges = []
        circles = []

        for curve in sketch.GetAllGeometry():
            process_geometry(curve, all_edges, circles)

        all_circles.extend(circles)

        # Überprüfung der Kantenlängen für jedes Feature innerhalb jeder Skizze
        if check_specific_edge_lengths(all_edges):
            rotations_feature_found = True

        if check_pattern_feature(all_edges):
            pattern_feature_found = True

        # Ausgabe der Linien (Edges)
        for edge in all_edges:
            lw.WriteLine(f"    Kante {all_edges.index(edge) + 1}: Typ - Linear, Länge - {edge.GetLength():.3f}")
        
        # Ausgabe der Kreise (Circles)
        for circle in circles:
            lw.WriteLine(f"    Kreis {circles.index(circle) + 1}: Radius - {circle.Radius:.3f}, Durchmesser - {2 * circle.Radius:.3f}, Umfang - {2 * 3.141592653589793 * circle.Radius:.3f}")
        
        lw.WriteLine("\n")

    # Prüfung auf die Alternativlösung
    if not rotations_feature_found:
        alternative_solution_found = check_circular_features(all_circles)


    # Überprüfung der Flächen nur einmal durchführen
    faces_check_result = check_faces_against_reference_ue1(workPart, lw)
    
    # Gesamtprüfung für alle Skizzen ausgeben
    lw.WriteLine("=" * 50)
    lw.WriteLine(f"Grundlagenprüfung: {EXERCISE_NUMBER}")
    lw.WriteLine("=" * 50)
    lw.WriteLine(f"Erzeugung Grundkörper:\nRotationsfeature: {'Wie in der Musterlösung, Skizze korrekt.' if rotations_feature_found else 'NEIN'}")
    lw.WriteLine(f"Erzeugung Muster:\nMusterfeature: {'Wie in der Musterlösung, Skizze korrekt.' if pattern_feature_found else 'NEIN'}")
   # lw.WriteLine(f"Anzahl der Muster-Features: {get_pattern_feature_count(workPart, lw)}{' --> Anzahl korrekt.' if total_patterns==12 else 'NEIN'}")
    
    if not rotations_feature_found and alternative_solution_found:
        lw.WriteLine(f"Prüfung nach Alternativlösungen hat folgendes ergeben: Zwei Kreise Extrudiert")
    
    lw.WriteLine(f"Rotationsfeature gefunden: {rotations_feature_found}")
    lw.WriteLine(f"Anzahl der gefundenen Flächen: {faces_check_result}")

    # Qualitätsanalyse nur ausgeben, wenn die Bedingungen erfüllt sind
    if rotations_feature_found and faces_check_result == 53:
        lw.WriteLine("==================================================")
        lw.WriteLine("Qualitäts-Analyse:")
        lw.WriteLine("==================================================")
        lw.WriteLine("Modellierung entspricht genau den Anforderungen der Aufgabe.")
        lw.WriteLine("")
        lw.WriteLine("Es wurde das Rotations-Feature zur Erzeugung des Grundkörpers genutzt.")
        lw.WriteLine("Alle 53 von 53 erwarteten Flächen sind vorhanden.")
        lw.WriteLine("")
        lw.WriteLine("Daraus lässt sich schließen, dass alle Anforderungen an den Aufbau des Modells erfüllt werden.")
        lw.WriteLine("Insgesamt wird das Modell mit der vollen Punktzahl bewertet, da es genau den Prinzipien guter Konstruktionspraxis folgt.")
        lw.WriteLine("")
        lw.WriteLine("Bewertung: 10/10")

    if alternative_solution_found and faces_check_result == 3:
        lw.WriteLine("==================================================")
        lw.WriteLine("Qualitäts-Analyse:")
        lw.WriteLine("==================================================")
        lw.WriteLine("Modellierung entspricht nicht den Anforderungen der Aufgabe.")
        lw.WriteLine("")
        lw.WriteLine("Anstatt einer Rotation einer einzigen Skizze wurden zwei Kreise extrudiert.")
        lw.WriteLine("")
        lw.WriteLine("Nur 3 von 53 erwarteten Flächen sind vorhanden.")
        lw.WriteLine("Daraus lässt sich schließen, dass das Muster-Feature der Kühlrippen entweder gar nicht oder falsch verwendet wurde.")
        lw.WriteLine("")
        lw.WriteLine("Fehlende Flächen und geometrische Elemente weisen auf eine unzureichende Modellierung hin.")
        lw.WriteLine("")
        lw.WriteLine("Das Design durch zwei extrudierte Kreise führt zwar optisch zum gleichen Ergebnis, ist aber technisch weniger effizient.")
        lw.WriteLine("Der Einsatz von zwei Extrusionen anstelle einer Rotationsfunktion führt zu einer unnötigen Komplexität im Modell.")
        lw.WriteLine("")
        lw.WriteLine("Das Design ist weniger robust, da es schwieriger ist, nachträglich Änderungen vorzunehmen oder das Modell für andere Zwecke zu modifizieren.")
        lw.WriteLine("")
        lw.WriteLine("Insgesamt wird das Modell durch die Verwendung der zwei extrudierten Kreise als nicht ausreichend bewertet, da es nicht den Prinzipien guter Konstruktionspraxis folgt. Außerdem fehlen wesentliche Bestandteile des Modells.")
        lw.WriteLine("")
        lw.WriteLine("Bewertung: 03/10")

    if alternative_solution_found and faces_check_result == 53:
        lw.WriteLine("==================================================")
        lw.WriteLine("Qualitäts-Analyse:")
        lw.WriteLine("==================================================")
        lw.WriteLine("Modellierung entspricht nicht den Anforderungen der Aufgabe.")
        lw.WriteLine("")
        lw.WriteLine("Anstatt einer Rotation einer einzigen Skizze wurden zwei Kreise extrudiert.")
        lw.WriteLine("")
        lw.WriteLine("Alle 53 von 53 erwarteten Flächen sind vorhanden.")
        lw.WriteLine("Daraus lässt sich schließen, dass alle Anforderungen an den Aufbau des Modells erfüllt werden.")
        lw.WriteLine("")
        lw.WriteLine("Das Design durch zwei extrudierte Kreise führt zwar optisch zum gleichen Ergebnis, ist aber technisch weniger effizient.")
        lw.WriteLine("Der Einsatz von zwei Extrusionen anstelle einer Rotationsfunktion führt zu einer unnötigen Komplexität im Modell.")
        lw.WriteLine("")
        lw.WriteLine("Das Design ist weniger robust, da es schwieriger ist, nachträglich Änderungen vorzunehmen oder das Modell für andere Zwecke zu modifizieren.")
        lw.WriteLine("")
        lw.WriteLine("Insgesamt wird das Modell durch die Verwendung der zwei extrudierten Kreise als nicht ausreichend bewertet, da es nicht den Prinzipien guter Konstruktionspraxis folgt.")
        lw.WriteLine("")
        lw.WriteLine("Bewertung: 07/10")

    if faces_check_result == 0:
        lw.WriteLine("==================================================")
        lw.WriteLine("Qualitäts-Analyse:")
        lw.WriteLine("==================================================")
        lw.WriteLine("Modellierung entspricht nicht den Anforderungen der Aufgabe.")
        lw.WriteLine("")
        lw.WriteLine("Alle erwarteten Flächen fehlen oder sind falsch modelliert.")
        lw.WriteLine("Dies deutet darauf hin, dass grundlegende Fehler bei der Modellierung gemacht wurden.")
        lw.WriteLine("")
        lw.WriteLine("Weder die Rotationsfunktion noch die richtigen Muster-Features wurden verwendet.")
        lw.WriteLine("Die gesamte geometrische Struktur des Modells ist fehlerhaft.")
        lw.WriteLine("")
        lw.WriteLine("Das Design ist weit von den gestellten Anforderungen entfernt und kann nicht als funktional betrachtet werden.")
        lw.WriteLine("Jegliche Nachbearbeitung des Modells wäre äußerst komplex und ineffizient.")
        lw.WriteLine("")
        lw.WriteLine("Insgesamt wird das Modell als ungenügend bewertet, da es nicht den Prinzipien guter Konstruktionspraxis folgt.")
        lw.WriteLine("Es fehlen alle wesentlichen Bestandteile und die geometrische Integrität des Modells ist stark beeinträchtigt.")
        lw.WriteLine("")
        lw.WriteLine("Bewertung: 00/10")


    # Zählen von Pattern- und Mirror-Features
 #   total_patterns, total_mirrors = count_pattern_and_mirror_features(workPart, lw)

    lw.WriteLine("\n")

    #lw.WriteLine(f"Anzahl der Muster-Features: {total_patterns}")
    #lw.WriteLine(f"Anzahl der Mirror-Features: {total_mirrors}")
    lw.WriteLine("\n")

    # Extrahiere die Positionen der Linien aus der Musterlösung
    extract_line_positions(workPart, lw)
    check_edges_against_reference(workPart, lw)

    lw.Close()




#Ab hier: Vertiefungsübung 1
# Listet Merkmale und Geometrien auf
def list_features_and_geometries_vt1(theSession, workPart):
    lw = theSession.ListingWindow
    lw.Open()
    
    lw.WriteLine("=" * 50)
    lw.WriteLine("Analyse der Körper und Geometrien")
    lw.WriteLine("=" * 50)

    body_count = 0
    for body in workPart.Bodies:
        body_count += 1
    lw.WriteLine("Gesamtanzahl der Körper im Teil: " + str(body_count))

    for body_idx, body in enumerate(workPart.Bodies, start=1):
        print_body_details(lw, body, body_idx, body_count)
    
    lw.WriteLine("=" * 50)
    lw.WriteLine("Feature-Analyse:")
    lw.WriteLine("=" * 50)
    for feature in workPart.Features:
        lw.WriteLine(f"Analyse des Features: {feature.JournalIdentifier} vom Typ {type(feature)}")
        if isinstance(feature, NXOpen.Features.Extrude):
            print_extrude_details(lw, feature, workPart)
        elif isinstance(feature, NXOpen.Features.Revolve):
            print_revolve_details(lw, feature, workPart)
        elif isinstance(feature, NXOpen.Features.HolePackage):
            print_hole_details(lw, feature, workPart)

    # Überprüfen und Zählen der Pattern- und Mirror-Features
    #total_patterns, total_mirrors = count_pattern_and_mirror_features(workPart, lw)
    #lw.WriteLine(f"Anzahl der Pattern Features: {total_patterns}")
    #lw.WriteLine(f"Anzahl der Mirror Features: {total_mirrors}")

    lw.Close()


# Listet Geometrieeigenschaften in Skizzen auf
def list_geometry_properties_in_sketches_vt1(theSession, workPart):
    lw = theSession.ListingWindow
    lw.Open()

    lw.WriteLine("=" * 50)
    lw.WriteLine("Analyse der Skizzen")
    lw.WriteLine("=" * 50)

    # Variablen zur Erfassung des Zustands der Features über alle Skizzen hinweg
    rotations_feature_found = False
    passfeder_feature_found = False
    keilwelle_feature_found = False
    extrude_feature_found = False

    for sketch_idx, sketch in enumerate(workPart.Sketches, start=1):
        lw.WriteLine(f"Skizze {sketch_idx}: {sketch.Name}")
        all_edges = []
        circles = []

        for curve in sketch.GetAllGeometry():
            process_geometry(curve, all_edges, circles)

        # Überprüfung der Kantenlängen für jedes Feature innerhalb jeder Skizze
        if check_specific_edge_lengths2(all_edges):
            rotations_feature_found = True
        if check_passfeder_feature(all_edges):
            passfeder_feature_found = True
        if check_keilwelle_feature(all_edges):
            keilwelle_feature_found = True

        for edge in all_edges:
            edge_type = "Linear" if isinstance(edge, NXOpen.Line) else "Circular" if isinstance(edge, NXOpen.Arc) else "Unbekannt"
            lw.WriteLine(f"    Kante {all_edges.index(edge) + 1}: Typ - {edge_type}, Länge - {edge.GetLength():.3f}")
        lw.WriteLine("\n")

    
    check_circular_pattern_feature(workPart, lw)
    check_faces_against_reference_vt1(workPart, lw)
    # Gesamtprüfung für alle Skizzen ausgeben
    lw.WriteLine("=" * 50)
    lw.WriteLine(f"Grundlagenprüfung: Preset {EXERCISE_NUMBER}")
    lw.WriteLine("=" * 50)
    lw.WriteLine(f"Erzeugung Grundkörper:\nRotationsfeature: {'JA, Skizze korrekt.' if rotations_feature_found else 'NEIN'}")
    # Überprüfung, ob das Extrusionsfeature EXTRUDE(7) mit den erforderlichen Längen vorhanden ist
    extrude_feature_found = check_passfeder_feature_with_lengths(workPart, lw)

    lw.WriteLine(f"Erzeugung Features:\nPassfeder: {'JA, Skizze korrekt.' if passfeder_feature_found else 'NEIN'}")
    lw.WriteLine(f"Keilwelle: {'JA, Skizze korrekt.' if keilwelle_feature_found else 'NEIN'}")
    # Überprüfung, ob das Extrusionsfeature EXTRUDE(7) mit den erforderlichen Längen vorhanden ist
    extrude_feature_found = check_keilwelle_feature_with_lengths(workPart, lw)

    lw.WriteLine(f"Extrude Feature Keilwelle: {'JA, mit richtigen Maßen' if extrude_feature_found else 'NEIN'}")

    # Zählen von Pattern- und Mirror-Features
    total_patterns, total_mirrors = count_pattern_and_mirror_features(workPart, lw)

    lw.WriteLine(f"Anzahl der Muster-Features: {total_patterns}")
    lw.WriteLine(f"Anzahl der Mirror-Features: {total_mirrors}")
    lw.WriteLine("\n")
    lw.Close()

#Ab hier: Übung 2
# Listet Merkmale und Geometrien auf
def list_features_and_geometries_ue2(theSession, workPart):
    lw = theSession.ListingWindow
    lw.Open()
    
    lw.WriteLine("=" * 50)
    lw.WriteLine("Analyse der Körper und Geometrien")
    lw.WriteLine("=" * 50)

    body_count = 0
    for body in workPart.Bodies:
        body_count += 1
    lw.WriteLine("Gesamtanzahl der Körper im Teil: " + str(body_count))

    for body_idx, body in enumerate(workPart.Bodies, start=1):
        print_body_details(lw, body, body_idx, body_count)
    
    lw.WriteLine("=" * 50)
    lw.WriteLine("Feature-Analyse:")
    lw.WriteLine("=" * 50)
    for feature in workPart.Features:
        lw.WriteLine(f"Analyse des Features: {feature.JournalIdentifier} vom Typ {type(feature)}")
        if isinstance(feature, NXOpen.Features.Extrude):
            print_extrude_details(lw, feature, workPart)
        elif isinstance(feature, NXOpen.Features.Revolve):
            print_revolve_details(lw, feature, workPart)
        elif isinstance(feature, NXOpen.Features.HolePackage):
            print_hole_details(lw, feature, workPart)

    # Überprüfen und Zählen der Pattern- und Mirror-Features
    total_patterns, total_mirrors = count_pattern_and_mirror_features(workPart, lw)
    lw.WriteLine(f"Anzahl der Pattern Features: {total_patterns}")
    lw.WriteLine(f"Anzahl der Mirror Features: {total_mirrors}")

    lw.Close()


# Listet Geometrieeigenschaften in Skizzen auf
def list_geometry_properties_in_sketches_ue2(theSession, workPart):
    lw = theSession.ListingWindow
    lw.Open()

    lw.WriteLine("=" * 50)
    lw.WriteLine("Analyse der Skizzen")
    lw.WriteLine("=" * 50)

    # Variablen zur Erfassung des Zustands der Features über alle Skizzen hinweg
    rotations_feature_found = False
    pattern_feature_found = False

    for sketch_idx, sketch in enumerate(workPart.Sketches, start=1):
        lw.WriteLine(f"Skizze {sketch_idx}: {sketch.Name}")
        all_edges = []
        circles = []

        for curve in sketch.GetAllGeometry():
            process_geometry(curve, all_edges, circles)

        # Überprüfung der Kantenlängen für jedes Feature innerhalb jeder Skizze
        if check_specific_edge_lengths(all_edges):
            rotations_feature_found = True
        if check_pattern_feature(all_edges):
            pattern_feature_found = True

        for edge in all_edges:
            edge_type = "Linear" if isinstance(edge, NXOpen.Line) else "Circular" if isinstance(edge, NXOpen.Arc) else "Unbekannt"
            lw.WriteLine(f"    Kante {all_edges.index(edge) + 1}: Typ - {edge_type}, Länge - {edge.GetLength():.3f}")
        lw.WriteLine("\n")

    # Muster-Features zählen
    total_patterns = get_pattern_feature_count(workPart, lw)
    check_faces_against_reference_ue2(workPart, lw)
    # Gesamtprüfung für alle Skizzen ausgeben
    lw.WriteLine("=" * 50)
    lw.WriteLine(f"Grundlagenprüfung: {EXERCISE_NUMBER}")
    lw.WriteLine("=" * 50)
    lw.WriteLine(f"Erzeugung Grundkörper:\nRotationsfeature: {'JA, Skizze korrekt.' if rotations_feature_found else 'NEIN'}")
    lw.WriteLine(f"Erzeugung Muster:\nMusterfeature: {'JA, Skizze korrekt.' if pattern_feature_found else 'NEIN'}")
    lw.WriteLine(f"Anzahl der Muster-Features: {total_patterns}{' --> Anzahl korrekt.' if total_patterns==12 else 'NEIN'}")
    
    # Zählen von Pattern- und Mirror-Features
    total_patterns, total_mirrors = count_pattern_and_mirror_features(workPart, lw)

    lw.WriteLine(f"Anzahl der Muster-Features: {total_patterns}")
    lw.WriteLine(f"Anzahl der Mirror-Features: {total_mirrors}")
    lw.WriteLine("\n")
    lw.Close()

#Ab hier: Vertiefungsübung 2
# Listet Merkmale und Geometrien auf
def list_features_and_geometries_vt2(theSession, workPart):
    lw = theSession.ListingWindow
    lw.Open()
    
    lw.WriteLine("=" * 50)
    lw.WriteLine("Analyse der Körper und Geometrien")
    lw.WriteLine("=" * 50)

    body_count = 0
    for body in workPart.Bodies:
        body_count += 1
    lw.WriteLine("Gesamtanzahl der Körper im Teil: " + str(body_count))

    for body_idx, body in enumerate(workPart.Bodies, start=1):
        print_body_details(lw, body, body_idx, body_count)
    
    lw.WriteLine("=" * 50)
    lw.WriteLine("Feature-Analyse:")
    lw.WriteLine("=" * 50)
    for feature in workPart.Features:
        lw.WriteLine(f"Analyse des Features: {feature.JournalIdentifier} vom Typ {type(feature)}")
        if isinstance(feature, NXOpen.Features.Extrude):
            print_extrude_details(lw, feature, workPart)
        elif isinstance(feature, NXOpen.Features.Revolve):
            print_revolve_details(lw, feature, workPart)
        elif isinstance(feature, NXOpen.Features.HolePackage):
            print_hole_details(lw, feature, workPart)

    # Überprüfen und Zählen der Pattern- und Mirror-Features
    total_patterns, total_mirrors = count_pattern_and_mirror_features(workPart, lw)
    lw.WriteLine(f"Anzahl der Pattern Features: {total_patterns}")
    lw.WriteLine(f"Anzahl der Mirror Features: {total_mirrors}")

    lw.Close()


# Listet Geometrieeigenschaften in Skizzen auf
def list_geometry_properties_in_sketches_vt2(theSession, workPart):
    lw = theSession.ListingWindow
    lw.Open()

    lw.WriteLine("=" * 50)
    lw.WriteLine("Analyse der Skizzen")
    lw.WriteLine("=" * 50)

    # Variablen zur Erfassung des Zustands der Features über alle Skizzen hinweg
    rotations_feature_found = False
    pattern_feature_found = False

    for sketch_idx, sketch in enumerate(workPart.Sketches, start=1):
        lw.WriteLine(f"Skizze {sketch_idx}: {sketch.Name}")
        all_edges = []
        circles = []

        for curve in sketch.GetAllGeometry():
            process_geometry(curve, all_edges, circles)

        # Überprüfung der Kantenlängen für jedes Feature innerhalb jeder Skizze
        if check_specific_edge_lengths(all_edges):
            rotations_feature_found = True
        if check_pattern_feature(all_edges):
            pattern_feature_found = True

        for edge in all_edges:
            edge_type = "Linear" if isinstance(edge, NXOpen.Line) else "Circular" if isinstance(edge, NXOpen.Arc) else "Unbekannt"
            lw.WriteLine(f"    Kante {all_edges.index(edge) + 1}: Typ - {edge_type}, Länge - {edge.GetLength():.3f}")
        lw.WriteLine("\n")

    # Muster-Features zählen
    total_patterns = get_pattern_feature_count(workPart, lw)
    check_faces_against_reference_vt2(workPart, lw)
    # Gesamtprüfung für alle Skizzen ausgeben
    lw.WriteLine("=" * 50)
    lw.WriteLine(f"Grundlagenprüfung: {EXERCISE_NUMBER}")
    lw.WriteLine("=" * 50)
    lw.WriteLine(f"Erzeugung Grundkörper:\nRotationsfeature: {'JA, Skizze korrekt.' if rotations_feature_found else 'NEIN'}")
    lw.WriteLine(f"Erzeugung Muster:\nMusterfeature: {'JA, Skizze korrekt.' if pattern_feature_found else 'NEIN'}")
    lw.WriteLine(f"Anzahl der Muster-Features: {total_patterns}{' --> Anzahl korrekt.' if total_patterns==12 else 'NEIN'}")
    
    # Zählen von Pattern- und Mirror-Features
    total_patterns, total_mirrors = count_pattern_and_mirror_features(workPart, lw)

    lw.WriteLine(f"Anzahl der Muster-Features: {total_patterns}")
    lw.WriteLine(f"Anzahl der Mirror-Features: {total_mirrors}")
    lw.WriteLine("\n")
    lw.Close()


def main():
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work

    if EXERCISE_NUMBER == 1:
        # Führe Prüfungen für Übung 1 durch
        list_geometry_properties_in_sketches_ue1(theSession, workPart)
        list_features_and_geometries_ue1(theSession, workPart)
    elif EXERCISE_NUMBER == 2:
        # Führe Prüfungen für Vertiefung 1 durch
        list_geometry_properties_in_sketches_vt1(theSession, workPart)
        list_features_and_geometries_vt1(theSession, workPart)
    elif EXERCISE_NUMBER == 3:
        # Führe Prüfungen für Übung 2 durch
        list_geometry_properties_in_sketches_ue2(theSession, workPart)
        list_features_and_geometries_ue2(theSession, workPart)
    elif EXERCISE_NUMBER == 4:
        # Führe Prüfungen für Vertiefung 2 durch
        list_geometry_properties_in_sketches_vt2(theSession, workPart)
        list_features_and_geometries_vt2(theSession, workPart)

    else:
        print("Ungültige Übungsnummer. Bitte setzen Sie EXERCISE_NUMBER auf 1, 2, 3 oder 4.")

if __name__ == '__main__':
    main()