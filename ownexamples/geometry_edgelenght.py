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
                # Try logging some properties to see what's available
                lw.WriteLine("Attempting to log edge properties for inspection:")
                try:
                    # Assuming Edge object has properties we can log to understand its structure
                    lw.WriteLine("Edge properties: ")
                    lw.WriteLine("  Edge Length: " + str(edge.GetLength()))
                    lw.WriteLine("  Edge Arc Data (if circular): ")
                    if edge.SolidEdgeType == NXOpen.Edge.EdgeType.Circular:
                        arc_data = edge.GetArcData()
                        lw.WriteLine("    Center: ({0}, {1}, {2})".format(arc_data.Center.X, arc_data.Center.Y, arc_data.Center.Z))
                        lw.WriteLine("    Radius: {0}".format(arc_data.Radius))
                except Exception as e:
                    lw.WriteLine("Error accessing edge data: " + str(e))

    lw.Close()

if __name__ == '__main__':
    list_geometries()
