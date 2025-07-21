"""
Script documentation

- Tool parameters are accessed using arcpy.GetParameter() or 
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""
import arcpy
import os


def ClipExport(cities_fc, snow_shps, out_folder):
    """Script code goes below"""
    # Load the current ArcGIS Pro project
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    # Get the default geodatabase path
    default_gdb = aprx.defaultGeodatabase
    
    arcpy.env.overwriteOutput = True
    
    
    #======================CLIP SNOW TO CITIES===============================
        #arcpy.analysis.Clip(in_features, clip_features, out_feature_class, {cluster_tolerance})
    try:
        where_clause = "NAME20 IN ('Fort Collins') OR NAME20 IN ('Boulder') OR NAME20 IN ('Longmont') OR NAME20 IN ('Loveland') OR NAME20 IN ('Lyons') OR NAME20 IN ('Superior')"
        cities_sel = arcpy.management.SelectLayerByAttribute(cities_fc, "NEW_SELECTION", where_clause)
    #Rename output on: day, forcast, and probability
        for fc in snow_shps:
            folder = os.path.basename(os.path.dirname(fc))  # day1_psnow_gt_04_2022031612
            parts = folder.split("_")
            day = parts[0]       # day1
            amount = parts[-2]   # 04
            cycle = parts[-1][-2:]  # 12 from 2022031612
    
            out_fc = os.path.join(default_gdb, f"{day}_{amount}_{cycle}")
            arcpy.analysis.Clip(fc, cities_sel, out_fc)
    #======================EXPORT TO SHAPEFILE AND KMZ===============================
            # Export to shapefile
            arcpy.conversion.FeatureClassToFeatureClass(out_fc, out_folder, f"{day}_{amount}_{cycle}.shp")
    
            # Export to KMZ — requires a layer
            layer = arcpy.MakeFeatureLayer_management(out_fc, "temp_layer")
            kmz_out = os.path.join(out_folder, f"{day}_{amount}_{cycle}.kmz")
            arcpy.conversion.LayerToKML(layer, kmz_out)

    except Exception as e:
        arcpy.AddError(f"Error occurred: {e}")
        print(f"Error occurred: {e}")



if __name__ == "__main__":

    cities_fc = arcpy.GetParameterAsText(0)
    snow_shps_raw = arcpy.GetParameterAsText(1)
    snow_shps = snow_shps_raw.split(";")  # if MultiValue is enabled
    out_folder = arcpy.GetParameterAsText(2)

    ClipExport(cities_fc, snow_shps, out_folder)
    arcpy.SetParameterAsText(3, "Done")  # Optional derived param (not required)