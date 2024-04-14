import NXOpen
import NXOpen.Features


def list_extrusions_and_heights():
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    lw = theSession.ListingWindow

    lw.Open()

    for feature in workPart.Features:
        if isinstance(feature, NXOpen.Features.Extrude):
            lw.WriteLine("Extrude Feature gefunden: " + feature.JournalIdentifier)
            extrude = feature
            builder = workPart.Features.CreateExtrudeBuilder(extrude)
            try:
                # Extrahiere die numerischen Werte der Expression Objekte für Start und Ende
                start_value = builder.Limits.StartExtend.Value
                end_value = builder.Limits.EndExtend.Value
                lw.WriteLine(f"Startdistanz der Extrusion: {start_value}")
                lw.WriteLine(f"Enddistanz der Extrusion: {end_value}")
                lw.WriteLine(f"Extrusionshöhe: {abs(end_value - start_value)}")
            except Exception as e:
                lw.WriteLine("Fehler beim Auswerten der Extrusionsgrenzen: " + str(e))
            finally:
                builder.Destroy()
    lw.Close()

if __name__ == '__main__':
    list_extrusions_and_heights()
