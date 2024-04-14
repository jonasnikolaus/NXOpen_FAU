import NXOpen

def list_geometries():
    # Access the current NX session and the work part
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    lw = theSession.ListingWindow

    # Start listing window
    lw.Open()

    # Access all bodies in the part and count them
    bodies = workPart.Bodies
    body_count = 0
    for body in bodies:
        body_count += 1
    
    lw.WriteLine("Total bodies in the part: " + str(body_count))
    
    # Loop through each body to access its geometries
    for body in bodies:
        lw.WriteLine("Body Name: " + body.Name)
        lw.WriteLine("Body Type: " + body.BodyType.ToString())

        # Access the facets of the body for detailed geometry data
        for face in body.GetFaces():
            lw.WriteLine("Face Type: " + face.SolidFaceType.ToString())
            edges = face.GetEdges()
            lw.WriteLine("Number of edges: " + str(len(edges)))

            # Detail each edge and its start and end points
            for edge in edges:
                start_point = edge.StartPoint
                end_point = edge.EndPoint
                lw.WriteLine("Edge Type: " + edge.SolidEdgeType.ToString())
                lw.WriteLine(f"Start Point: ({start_point.X}, {start_point.Y}, {start_point.Z})")
                lw.WriteLine(f"End Point: ({end_point.X}, {end_point.Y}, {end_point.Z})")

                # If the edge is an arc, additional details like radius
                if edge.SolidEdgeType == "Circular":
                    arc = edge.Arc
                    lw.WriteLine("Arc Radius: " + str(arc.Radius))
                    lw.WriteLine("Arc Center: (" + str(arc.Center.X) + ", " + str(arc.Center.Y) + ", " + str(arc.Center.Z) + ")")

    # Close the listing window
    lw.Close()

if __name__ == '__main__':
    list_geometries()
