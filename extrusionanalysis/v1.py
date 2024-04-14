import NXOpen
import NXOpen.Features

def list_extrusions_and_heights():
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    lw = theSession.ListingWindow

    lw.Open()

    # Alle Features durchgehen und nach Extrusionsfeatures suchen
    for feature in workPart.Features:
        # Hier prüfen wir, ob das Feature vom Typ Extrude ist
        if isinstance(feature, NXOpen.Features.Extrude):
            lw.WriteLine("Extrude Feature gefunden: " + feature.JournalIdentifier)
            extrude = feature
            # Erstellen eines Builders, um die Extrusionsdetails zu erhalten
            builder = workPart.Features.CreateExtrudeBuilder(feature)
            try:
                # Versuch, die Extrusionshöhe zu bestimmen
                start_value = builder.Limits.StartExtend.Value
                end_value = builder.Limits.EndExtend.Value
                lw.WriteLine(f"Startdistanz der Extrusion: {start_value}")
                lw.WriteLine(f"Enddistanz der Extrusion: {end_value}")
                lw.WriteLine(f"Extrusionshöhe: {abs(end_value - start_value)}")
            finally:
                # Sicherstellen, dass der Builder zerstört wird
                builder.Destroy()
    lw.Close()

if __name__ == '__main__':
    list_extrusions_and_heights()
