# Python script to set Blender Custom Properties for a mesh (.type == 'MESH')
# Author: Mario Delgado, LinkeIn: https://www.linkedin.com/in/mario-delgado-5b6195155/
# Source: http://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV
# 
# Custom Properties: https://docs.blender.org/manual/en/latest/data_system/custom_properties.html?highlight=custom%20properties

import bpy, csv

# input: https://docs.python.org/3/library/functions.html#input
filePath = input("Enter file name path (folder/filename.csv):")         #Example: Type "c:/data/keys.csv" when prompted in the conole

# Example of content in .csv file, line 1 contains column heading (Object Name and Properties):
#
# objectName,propName1,propName2,...
# object1,prop1,prop2
# object2,prop1,prop2
#
# Script will assign bpy.data.objects[objectName].data[propNameN] = propN

with open( filePath ) as csvfile:
    rdr = csv.DictReader( csvfile )     # https://docs.python.org/3/library/csv.html
    for row in rdr:

        meshName = row[rdr.fieldnames[0]]
        
        print("******************************** meshName:", meshName ,"********************************************")
        print(" properties before assignment(s): ", bpy.data.objects[meshName].data.items()) 
        
        for x in range (1, len(rdr.fieldnames)):  
            propName =  rdr.fieldnames[x]
            propValue = row[propName]
            # List Comprehension: hhttps://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
            mesh = [obj for obj in bpy.data.objects if obj.name == meshName and obj.type == 'MESH'][0]
            mesh.data[propName] = propValue    
            print("Updated meshName: ", meshName, ", propName: ", propName, ", propValue:", mesh.data[propName])
        
        print(" properties after assignment(s): ", bpy.data.objects[meshName].data.items()) 
        print("******************************** meshName:", meshName ,"********************************************")