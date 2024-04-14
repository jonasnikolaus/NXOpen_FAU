using System;
using NXOpen;
using NXOpen.Features;
using NXOpen.UF;

public class Program
{
    public static int Main(string[] args)
    {
        Session theSession = Session.GetSession();
        Part workPart = theSession.Parts.Work;

        // Iterate over all features in the work part
        foreach (Feature feature in workPart.Features)
        {
            Console.WriteLine("Feature: {0}, Name: {1}", feature.GetType().Name, feature.Name);

            // Check if the feature is an extrusion and handle accordingly
            if (feature.FeatureType == "EXTRUDE")
            {
                Extrude extrudeFeature = feature as Extrude;
                if (extrudeFeature != null)
                {
                    Console.WriteLine("Extrusion Feature: {0}", feature.JournalIdentifier);

                    // Access and log details about the bodies created by this extrusion
                    Body[] bodies = extrudeFeature.GetBodies();
                    foreach (Body body in bodies)
                    {
                        Console.WriteLine("Body created by extrusion: {0}", body.JournalIdentifier);
                    }
                }
            }

            // Correctly handle Sketch features
            if (feature.FeatureType == "SKETCH")
            {
                Sketch sketch = feature as Sketch;
                if (sketch != null)
                {
                    Console.WriteLine("Sketch Name: {0}", sketch.Name);
                    foreach (NXObject obj in sketch.GetAllGeometry())
                    {
                        if (obj is Arc arc)
                        {
                            Console.WriteLine("Arc with radius: {0} at center ({1}, {2})", arc.Radius, arc.CenterPoint.X, arc.CenterPoint.Y);
                        }
                        else if (obj is Line line)
                        {
                            Console.WriteLine("Line from ({0}, {1}) to ({2}, {3})", line.StartPoint.X, line.StartPoint.Y, line.EndPoint.X, line.EndPoint.Y);
                        }
                    }
                }
            }
        }

        return 0;
    }

    public static int GetUnloadOption(string dummy) { return (int)Session.LibraryUnloadOption.AtTermination; }
}
