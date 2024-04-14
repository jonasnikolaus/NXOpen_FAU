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

    # Further code will go here to handle other parts of the analysis

    lw.Close()

if __name__ == '__main__':
    list_geometries()
