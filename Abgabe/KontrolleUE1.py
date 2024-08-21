import NXOpen # type: ignore
import NXOpen.Features # type: ignore
import math

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


# Berechnet, ob spezifische Kantenlängen vorhanden sind (für  Grundkörper mit Rotationsfeature)
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
    lw.WriteLine(f"Grundlagenprüfung: 1")
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
        lw.WriteLine("")
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
        lw.WriteLine("")
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
        lw.WriteLine("")
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
        lw.WriteLine("")
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
    lw.Close()

def main():
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work

    list_geometry_properties_in_sketches_ue1(theSession, workPart)

if __name__ == '__main__':
    main()