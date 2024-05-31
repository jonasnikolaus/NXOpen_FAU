import NXOpen

def list_geometries():
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    lw = theSession.ListingWindow

    lw.Open()

    # Manually count the bodies
    body_count = 0
    for body in workPart.Bodies:
        body_count += 1

    lw.WriteLine("Total bodies in the part: " + str(body_count))

    # Loop through each body and inspect properties
    for body in workPart.Bodies:
        lw.WriteLine("Inspecting body: " + body.Name)
        lw.WriteLine("Journal Identifier: " + body.JournalIdentifier)

        # Inspect each face of the body
        for face in body.GetFaces():
            lw.WriteLine("Face type: " + str(face.FaceType).split('.')[-1])  # Improved face type display
            # Check for edges and their details
            edges = face.GetEdges()
            lw.WriteLine("Number of edges: " + str(len(edges)))
            for edge in edges:
                lw.WriteLine("Edge type: " + str(edge.SolidEdgeType).split('.')[-1])  # Convert enum to string properly
                lw.WriteLine("Edge Length: " + str(edge.GetLength()))
                # Check if the edge is circular and attempt to access arc details
                if edge.SolidEdgeType == NXOpen.Edge.EdgeType.Circular:
                    curve = edge.GetCurve()
                    if curve:
                        arc = curve
                        lw.WriteLine("Arc Center: ({0}, {1}, {2})".format(arc.Center.X, arc.Center.Y, arc.Center.Z))
                        lw.WriteLine("Arc Radius: {0}".format(arc.Radius))

    lw.Close()

if __name__ == '__main__':
    list_geometries()
