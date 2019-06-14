<!-- Markdown reference: https://guides.github.com/features/mastering-markdown/ -->
# Add Blender Custom Properties From CSV File

A Blender Python script to read a formatted csv (comma seperated value) file to set [Custom Properties](https://docs.blender.org/manual/en/latest/data_system/custom_properties.html?highlight=custom%20properties).

The file loaded must be in a [*csv.DictReader*](https://docs.python.org/3/library/csv.html) class format.

#3 Usage

[Run script from in Blender](https://docs.blender.org/api/2.79/info_quickstart.html#running-scripts) and respond to the input prompt with filename (format: [folder]/filename.csv ) that contains the data to update the Custom Properies. 

* Assuming a Blender object (.type = 'MESH'); 
* With a name = 'object1';
* The following file contents will assign the Blender object a Custom Property value of 'prop1' to property 'propName1':

````
objectName,propName1
object1,prop1
````

* The objectName's property values for the indivdual mesh(es) must always be in column 1. 

### Script Syntax:

````
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
# object1,prop1,prop2,...
# object2,prop1,prop2,...
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
````

### Running Test

* Open [test.blend](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/test/test.blend) file in test folder.
* Run [AddBlenderCustomPropertiesFromCSV.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/tree/master/py) Python script.
* Reference [test.csv](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/test/test.csv) in test folder when prompted by [input](https://docs.python.org/3/library/functions.html#input) prompt.

#### Test Output

````

******************************** meshName: Cube.000 ********************************************
 properties before assignment(s):  []
Updated meshName:  Cube.000 , propName:  visualKey , propValue: Cube.000
 properties after assignment(s):  [('visualKey', 'Cube.000')]
******************************** meshName: Cube.000 ********************************************
******************************** meshName: Cube.001 ********************************************
 properties before assignment(s):  []
Updated meshName:  Cube.001 , propName:  visualKey , propValue: Cube.001
 properties after assignment(s):  [('visualKey', 'Cube.001')]
******************************** meshName: Cube.001 ********************************************

````


## Author

* **Mario Delgado**  Github: [MarioDelgadoSr](https://github.com/MarioDelgadoSr)
* LinkedIn: [Mario Delgado](https://www.linkedin.com/in/mario-delgado-5b6195155/)
* [My Data Visualizer](https://qzfcxunzx7ydnpxm3djoqw-on.drv.tw/DataVisualizer/): A data visualization application using the *DataVisual* design pattern.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

