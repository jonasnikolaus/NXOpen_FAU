import NXOpen
import NXOpen.Features
import math

def list_features_and_geometries():
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    lw = theSession.ListingWindow

    lw.Open()

    # Manuell die Anzahl der Körper zählen
    body_count = 0
    for body in workPart.Bodies:
        body_count += 1

    lw.WriteLine("Gesamtanzahl der Körper im Teil: " + str(body_count))

    processed_edges = set()  # Ein Set, um bereits verarbeitete Kanten zu speichern

    for body in workPart.Bodies:
        lw.WriteLine("Körper wird inspiziert: " + body.Name)
        lw.WriteLine("Journal Identifier: " + body.JournalIdentifier)

        for face in body.GetFaces():
            lw.WriteLine("Flächentyp: " + str(face.FaceType).split('.')[-1])
            edges = face.GetEdges()
            lw.WriteLine("Anzahl der Kanten: " + str(len(edges)))

            for edge in edges:
                if edge not in processed_edges:
                    processed_edges.add(edge)
                    lw.WriteLine("Kantentyp: " + str(edge.SolidEdgeType).split('.')[-1])
                    lw.WriteLine("Kantenlänge (Umfang): " + str(edge.GetLength()))

                    if edge.SolidEdgeType == NXOpen.Edge.EdgeType.Circular:
                        circumference = edge.GetLength()
                        radius = circumference / (2 * math.pi)
                        diameter = 2 * radius
                        lw.WriteLine("Radius des Kreises: {0:.3f}".format(radius))
                        lw.WriteLine("Durchmesser des Kreises: {0:.3f}".format(diameter))

    # Extrusionsfeatures inspizieren
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

if __name__ == '__main__':
    list_features_and_geometries()
