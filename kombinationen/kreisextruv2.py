import NXOpen
import NXOpen.Features
import math

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

def list_features_and_geometries():
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    lw = theSession.ListingWindow

    lw.Open()

    # Zählen der Körper
    body_count = 0
    for body in workPart.Bodies:
        body_count += 1
    lw.WriteLine("Gesamtanzahl der Körper im Teil: " + str(body_count))

    processed_edges = set()  # Ein Set, um bereits verarbeitete Kanten zu speichern

    for body in workPart.Bodies:
        lw.WriteLine("Körper wird inspiziert: " + body.Name)
        lw.WriteLine("Journal Identifier: " + body.JournalIdentifier)

        for face in body.GetFaces():
            lw.WriteLine("Flächentyp: " + face_type_to_string(face.SolidFaceType))
            edges = face.GetEdges()
            lw.WriteLine("Anzahl der Kanten: " + str(len(edges)))

            for edge in edges:
                if edge not in processed_edges:
                    processed_edges.add(edge)
                    edge_type_name = edge_type_to_string(edge.SolidEdgeType)
                    lw.WriteLine("Kantentyp: " + edge_type_name)
                    lw.WriteLine("Kantenlänge (Umfang): " + str(edge.GetLength()))

                    if edge.SolidEdgeType == NXOpen.Edge.EdgeType.Circular:
                        circumference = edge.GetLength()
                        radius = circumference / (2 * math.pi)
                        diameter = 2 * radius
                        lw.WriteLine("Radius des Kreises: {0:.3f}".format(radius))
                        lw.WriteLine("Durchmesser des Kreises: {0:.3f}".format(diameter))

    for feature in workPart.Features:
        if isinstance(feature, NXOpen.Features.Extrude):
            lw.WriteLine("Extrude Feature gefunden: " + feature.JournalIdentifier)
            extrude = feature
            builder = workPart.Features.CreateExtrudeBuilder(extrude)
            try:
                start_value = float(builder.Limits.StartExtend.Value.RightHandSide)
                end_value = float(builder.Limits.EndExtend.Value.RightHandSide)
                lw.WriteLine(f"Startdistanz der Extrusion: {start_value}")
                lw.WriteLine(f"Enddistanz der Extrusion: {end_value}")
                lw.WriteLine(f"Extrusionshöhe: {abs(end_value - start_value)}")
            except Exception as e:
                lw.WriteLine("Fehler beim Auswerten der Extrusionsgrenzen: " + str(e))
            finally:
                builder.Destroy()

    lw.Close()

def is_rectangle(edges):
    if len(edges) != 4:
        return False
    # Sortiere die Kanten nach Länge
    sorted_edges = sorted(edges, key=lambda e: e.GetLength())
    # Prüfe, ob zwei Paare von Kanten jeweils gleich lang sind
    if math.isclose(sorted_edges[0].GetLength(), sorted_edges[1].GetLength()) and math.isclose(sorted_edges[2].GetLength(), sorted_edges[3].GetLength()):
        return True
    return False

def list_geometry_properties_in_sketches():
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    lw = theSession.ListingWindow
    lw.Open()

    for sketch in workPart.Sketches:
        lw.WriteLine(f"Skizze: {sketch.Name}")
        all_edges = []
        circles = []

        for curve in sketch.GetAllGeometry():
            if isinstance(curve, NXOpen.Arc):
                circles.append(curve)
            elif isinstance(curve, NXOpen.Line):
                all_edges.append(curve)

        # Suche nach Rechtecken
        if len(all_edges) >= 4:
            # Prüfe jede mögliche Kombination von vier Kanten
            from itertools import combinations
            for combo in combinations(all_edges, 4):
                if is_rectangle(combo):
                    lengths = sorted([e.GetLength() for e in combo])
                    lw.WriteLine(f"Rechteck gefunden in Skizze: {sketch.Name}")
                    lw.WriteLine(f"Seitenlängen: {lengths[0]:.3f}, {lengths[2]:.3f} (Länge, Breite)")

        for circle in circles:
            lw.WriteLine(f"Kreis gefunden in Skizze: {sketch.Name}")
            lw.WriteLine(f"Radius: {circle.Radius:.3f}")
            lw.WriteLine(f"Mittelpunkt: ({circle.CenterPoint.X:.3f}, {circle.CenterPoint.Y:.3f}, {circle.CenterPoint.Z:.3f})")

    lw.Close()

if __name__ == '__main__':
    list_features_and_geometries()
    list_geometry_properties_in_sketches()