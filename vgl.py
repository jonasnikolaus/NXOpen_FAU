def print_revolve_details(lw, feature):
    lw.WriteLine(f"Analyzing Revolved Feature: {feature.JournalIdentifier}")
    revolve=feature
    try:
        revolve_builder = workPart.CreateRevolveBuilder(revolve)
        
        # Access the Axis property correctly
        try:
            revolve_builder.Axis
            axis = revolve_builder.Axis()
            if axis:
                lw.WriteLine(f"  Axis: Direction - {axis}")
         
                lw.WriteLine("  Axis: Not available")
  

        # Access limits correctly
        if revolve_builder.Limits:
            limits = revolve_builder.Limits()
            lw.WriteLine(f"  Start Limit: {limits}")
            lw.WriteLine(f"  End Limit: {limits.End}")
        
        # Access tolerance correctly
        tolerance = revolve_builder.Tolerance
        lw.WriteLine(f"  Tolerance: {tolerance}")
        
    except Exception as e:
        lw.WriteLine(f"  Error analyzing revolve details: {str(e)}")
    finally:
        revolve_builder.Destroy()

def print_extrude_details(lw, feature):
    lw.WriteLine(f"  {feature.JournalIdentifier}:")
    extrude = feature
    builder = workPart.Features.CreateExtrudeBuilder(extrude)
    try:
        start_value = float(builder.Limits.StartExtend.Value.RightHandSide)
        end_value = float(builder.Limits.EndExtend.Value.RightHandSide)
        lw.WriteLine(f"    Startdistanz der Extrusion: {start_value}")
        lw.WriteLine(f"    Enddistanz der Extrusion: {end_value}")
        lw.WriteLine(f"    Extrusionshöhe: {abs(end_value - start_value)}")
    except Exception as e:
        lw.WriteLine(f"    Fehler beim Auswerten der Extrusionsgrenzen: {e}")
    finally:
        builder.Destroy()