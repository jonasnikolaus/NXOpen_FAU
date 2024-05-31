import NXOpen
import math

def list_geometries():
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    lw = theSession.ListingWindow

    lw.Open()

    # Manuell die Anzahl der Körper zählen
    body_count = 0
    for body in workPart.Bodies:
        body_count += 1

    lw.WriteLine("Gesamtanzahl der Körper im Teil: " + str(body_count))

    # Jeden Körper durchgehen und Eigenschaften inspizieren
    for body in workPart.Bodies:
        lw.WriteLine("Körper wird inspiziert: " + body.Name)
        lw.WriteLine("Journal Identifier: " + body.JournalIdentifier)

        # Jede Fläche des Körpers inspizieren
        for face in body.GetFaces():
            lw.WriteLine("Flächentyp: " + str(face.FaceType).split('.')[-1])
            # Kanten und deren Details überprüfen
            edges = face.GetEdges()
            lw.WriteLine("Anzahl der Kanten: " + str(len(edges)))
            for edge in edges:
                lw.WriteLine("Kantentyp: " + str(edge.SolidEdgeType).split('.')[-1])
                lw.WriteLine("Kantenlänge (Umfang): " + str(edge.GetLength()))
                # Berechnung des Radius, wenn die Kante kreisförmig ist
                if edge.SolidEdgeType == NXOpen.Edge.EdgeType.Circular:
                    circumference = edge.GetLength()
                    radius = circumference / (2 * math.pi)
                    diameter = 2 * radius
                    lw.WriteLine("Radius des Kreises: {0:.3f}".format(radius))
                    lw.WriteLine("Durchmesser des Kreises: {0:.3f}".format(diameter))

    lw.Close()

if __name__ == '__main__':
    list_geometries()
