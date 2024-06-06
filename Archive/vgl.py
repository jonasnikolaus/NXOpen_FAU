def print_revolve_details(lw, feature, workPart):
    lw.WriteLine(f"Analyzing Revolved Feature: {feature.JournalIdentifier}")
    revolve = feature
    try:
        revolve_builder = workPart.Features.CreateRevolveBuilder(revolve)
        
        # Access and print details from the Axis property
        axis = revolve_builder.Axis
        if axis:
            direction_vector = axis.Direction.Vector  # Accessing the vector
            point_coordinates = axis.Point.Coordinates  # Correctly accessing the coordinates of the point
            lw.WriteLine(f"  Axis: Direction - X: {direction_vector.X}, Y: {direction_vector.Y}, Z: {direction_vector.Z}, Point - X: {point_coordinates.X}, Y: {point_coordinates.Y}, Z: {point_coordinates.Z}")
        else:
            lw.WriteLine("  Axis: Not available")

        # Handle StartExtend and EndExtend properties
        limits = revolve_builder.Limits
        if limits:
            start_extend = limits.StartExtend
            end_extend = limits.EndExtend
            start_value = start_extend.Value.RightHandSide if start_extend.Value else "Undefined"
            end_value = end_extend.Value.RightHandSide if end_extend.Value else "Undefined"
            lw.WriteLine(f"  Start Extend Value: {start_value}")
            lw.WriteLine(f"  End Extend Value: {end_value}")
        else:
            lw.WriteLine("  Limits: Not available")
        
        # Access and print tolerance
        tolerance = revolve_builder.Tolerance
        lw.WriteLine(f"  Tolerance: {tolerance}")
        
    except Exception as e:
        lw.WriteLine(f"  Error analyzing revolve details: {str(e)}")
    finally:
        revolve_builder.Destroy()
