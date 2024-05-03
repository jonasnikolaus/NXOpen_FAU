import NXOpen
import NXOpen.Features
import math
from itertools import combinations

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


def print_sketch_details(lw, sketch, sketch_idx):
    lw.WriteLine(f"Skizze {sketch_idx}: {sketch.Name}")
    #all_edges = []
    #circles = []

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

# Überprüft, ob ein Musterfeature vorhanden ist
def check_pattern_feature(all_edges):
    required_pattern_lengths = [1.5, 6.502, 6.502, 1.2]
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

# Analysiert Geometrien in Skizzen
def analyze_sketch_geometry(lw, all_edges, circles, sketch):
    found_rectangles = []
    found_circles = []
    found_lengths = []

    # Check for rectangles
    if len(all_edges) >= 4:
        found_rectangles = analyze_edges_for_rectangle(lw, all_edges, sketch)

    # Process circles
    for circle in circles:
        print_circle_details(lw, circle, sketch)
        found_circles.append(circle)

    # Speichern der Kantenlängen
    for edge in all_edges:
        length = edge.GetLength()
        found_lengths.append(length)
        if edge not in found_rectangles:
            print_edge_details(lw, edge, all_edges.index(edge) + 1)

    # Prüfung für Grundkörper
    check_specific_edge_lengths(lw, found_lengths)
    # Prüfung für Musterfeature
    check_pattern_feature(lw, found_lengths)

# Analysiert Kanten für Rechtecke
def analyze_edges_for_rectangle(lw, all_edges, sketch):
    found_edges = []
    for combo in combinations(all_edges, 4):
        if is_rectangle(combo):
            print_rectangle_details(lw, combo, sketch)
            found_edges.extend(combo)
    return found_edges

# Gibt Details eines Kreises aus
def print_circle_details(lw, circle, sketch):
    lw.WriteLine(f"Kreis gefunden in Skizze: {sketch.Name}")
    lw.WriteLine(f"Radius: {circle.Radius:.3f}")
    lw.WriteLine(f"Mittelpunkt: ({circle.CenterPoint.X:.3f}, {circle.CenterPoint.Y:.3f}, {circle.CenterPoint.Z:.3f})")
    return circle

# Gibt Details eines Rechtecks aus
def print_rectangle_details(lw, rectangle_edges, sketch):
    lengths = sorted([edge.GetLength() for edge in rectangle_edges])
    lw.WriteLine(f"Rechteck gefunden in Skizze: {sketch.Name}")
    lw.WriteLine(f"Seitenlängen: {lengths[0]:.3f}, {lengths[2]:.3f} (Länge, Breite)")
    return rectangle_edges

# Überprüft, ob die gegebenen Kanten ein Rechteck bilden
def is_rectangle(edges):
    # Sort the edges by length
    sorted_edges = sorted(edges, key=lambda e: e.GetLength())
    # Check if two pairs of edges are each of equal length
    if math.isclose(sorted_edges[0].GetLength(), sorted_edges[1].GetLength()) and math.isclose(sorted_edges[2].GetLength(), sorted_edges[3].GetLength()):
        return True
    return False

# Listet Merkmale und Geometrien auf
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

    lw.Close()

# Listet Geometrieeigenschaften in Skizzen auf
def list_geometry_properties_in_sketches(theSession, workPart):
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

    # Gesamtprüfung für alle Skizzen ausgeben
    lw.WriteLine("=" * 50)
    lw.WriteLine("Grundlagenprüfung:")
    lw.WriteLine("=" * 50)
    lw.WriteLine(f"Erzeugung Grundkörper:\nRotationsfeature: {'JA' if rotations_feature_found else 'NEIN'} Erzeugung Muster:\nMusterfeature: {'JA' if pattern_feature_found else 'NEIN'}")
    lw.WriteLine("\n")
    lw.Close()

if __name__ == '__main__':
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work

    list_geometry_properties_in_sketches(theSession, workPart)
    list_features_and_geometries(theSession, workPart)
