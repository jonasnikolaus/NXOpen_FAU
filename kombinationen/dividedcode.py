import NXOpen
import NXOpen.Features
import math
from itertools import combinations

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

def print_body_details(lw, body, body_idx, body_count):
    lw.WriteLine("-" * 50)
    lw.WriteLine(f"Körper {body_idx}/{body_count} wird inspiziert: {body.Name}")
    lw.WriteLine(f"Journal Identifier: {body.JournalIdentifier}")
    for face_idx, face in enumerate(body.GetFaces(), start=1):
        print_face_details(lw, face, face_idx)

def print_face_details(lw, face, face_idx):
    lw.WriteLine(f"  Fläche {face_idx}: Typ - {face_type_to_string(face.SolidFaceType)}")
    edges = face.GetEdges()
    lw.WriteLine(f"  Anzahl der Kanten: {len(edges)}")
    for edge_idx, edge in enumerate(edges, start=1):
        print_edge_details(lw, edge, edge_idx)
    lw.WriteLine("\n")

def print_edge_details(lw, edge, edge_idx):
    edge_type_name = edge_type_to_string(edge.SolidEdgeType)
    lw.WriteLine(f"    Kante {edge_idx}: Typ - {edge_type_name}, Länge (Umfang) - {edge.GetLength():.3f}")
    if edge.SolidEdgeType == NXOpen.Edge.EdgeType.Circular:
        print_circular_edge_details(lw, edge)

def print_circular_edge_details(lw, edge):
    circumference = edge.GetLength()
    radius = circumference / (2 * math.pi)
    diameter = 2 * radius
    lw.WriteLine(f"    Radius des Kreises: {radius:.3f}")
    lw.WriteLine(f"    Durchmesser des Kreises: {diameter:.3f}")

def print_extrude_details(lw, feature):
    lw.WriteLine(f"  {feature.JournalIdentifier}:")
    extrude = feature
    builder = workPart.Features.CreateExtrudeBuilder(extrude)
    try:
        start_value = float(builder.Limits.StartExtend.Value.RightHandSide)
        end_value = float(builder.Limits.EndExtend.Value.RightHandSide)
        lw.WriteLine(f"    Startdistanz der Extrusion: {start_value}")
        lw.WriteLine(f"    Enddistanz der Extrusion: {end_value}")
        lw.WriteLine(f"    Extrusionshöhe: {abs(end_value - start_value)}")
    except Exception as e:
        lw.WriteLine(f"    Fehler beim Auswerten der Extrusionsgrenzen: {e}")
    finally:
        builder.Destroy()

def print_sketch_details(lw, sketch, sketch_idx):
    lw.WriteLine(f"Skizze {sketch_idx}: {sketch.Name}")
    all_edges = []
    circles = []

def process_geometry(curve, all_edges, circles):
    if isinstance(curve, NXOpen.Arc):
        circles.append(curve)
    elif isinstance(curve, NXOpen.Line):
        all_edges.append(curve)

def analyze_sketch_geometry(lw, all_edges, circles, sketch):
    # Check for rectangles
    if len(all_edges) >= 4:
        analyze_edges_for_rectangle(lw, all_edges, sketch)
    # Process circles
    for circle in circles:
        print_circle_details(lw, circle, sketch)

def analyze_edges_for_rectangle(lw, all_edges, sketch):
    from itertools import combinations
    for combo in combinations(all_edges, 4):
        if is_rectangle(combo):
            print_rectangle_details(lw, combo, sketch)

def print_circle_details(lw, circle, sketch):
    lw.WriteLine(f"Kreis gefunden in Skizze: {sketch.Name}")
    lw.WriteLine(f"Radius: {circle.Radius:.3f}")
    lw.WriteLine(f"Mittelpunkt: ({circle.CenterPoint.X:.3f}, {circle.CenterPoint.Y:.3f}, {circle.CenterPoint.Z:.3f})")

def print_rectangle_details(lw, rectangle_edges, sketch):
    lengths = sorted([edge.GetLength() for edge in rectangle_edges])
    lw.WriteLine(f"Rechteck gefunden in Skizze: {sketch.Name}")
    lw.WriteLine(f"Seitenlängen: {lengths[0]:.3f}, {lengths[2]:.3f} (Länge, Breite)")

def is_rectangle(edges):
    # Sort the edges by length
    sorted_edges = sorted(edges, key=lambda e: e.GetLength())
    # Check if two pairs of edges are each of equal length
    if math.isclose(sorted_edges[0].GetLength(), sorted_edges[1].GetLength()) and math.isclose(sorted_edges[2].GetLength(), sorted_edges[3].GetLength()):
        return True
    return False

def list_features_and_geometries(theSession, workPart):
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
        lw.WriteLine("\nExtrude Features:")
        for feature in workPart.Features:
            if isinstance(feature, NXOpen.Features.Extrude):
                print_extrude_details(lw, feature)

    lw.Close()

def list_geometry_properties_in_sketches(theSession, workPart):
    lw = theSession.ListingWindow
    lw.Open()

    lw.WriteLine("=" * 50)
    lw.WriteLine("Analyse der Skizzen")
    lw.WriteLine("=" * 50)

    for sketch_idx, sketch in enumerate(workPart.Sketches, start=1):
        lw.WriteLine(f"Skizze {sketch_idx}: {sketch.Name}")
        all_edges = []
        circles = []

        for curve in sketch.GetAllGeometry():
            process_geometry(curve, all_edges, circles)

        lw.WriteLine("\n")
        analyze_sketch_geometry(lw, all_edges, circles, sketch)

    lw.Close()

if __name__ == '__main__':
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work

    list_features_and_geometries(theSession, workPart)
    list_geometry_properties_in_sketches(theSession, workPart)