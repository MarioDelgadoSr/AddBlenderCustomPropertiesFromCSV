<!-- Markdown reference: https://guides.github.com/features/mastering-markdown/ -->
# Add Blender Custom Properties From CSV File

A Blender Python script to read a formatted csv (comma seperated value) file an use its contents to set [Custom Properties](https://docs.blender.org/manual/en/latest/data_system/custom_properties.html?highlight=custom%20properties).

* The file loaded must be in a [*csv.DictReader*](https://docs.python.org/3/library/csv.html) class format.
* This script can be used to 'enrich' a Blender file, that will be exported to a glTF file, with embedded data.
	* When a Blender file is exported to a glTF file, the Custom Properties are placed in the [*extras* properties](https://docs.blender.org/manual/en/dev/addons/io_gltf2.html) associated with the mesh.

#3 Usage

[Run script from in Blender](https://docs.blender.org/api/2.79/info_quickstart.html#running-scripts) and respond to the input prompt with filename (format: [folder]/filename.csv ) that contains the data to update the Custom Properies. 

* Assuming a Blender object (.type = 'MESH'); 
* With a name = 'object1';
* The following file contents will assign the Blender object a Custom Property value of 'prop1' to property 'propName1':
* sanitize = True option will sanitize a mesh's name to be consitent wth [Three.js naming requirements for nodes](https://discourse.threejs.org/t/issue-with-gltfloader-and-objects-with-dots-in-their-name-attribute/6726 ).

````
# Python script to set Blender Custom Properties for a mesh (.type == 'MESH')
# Author: Mario Delgado, LinkedIn: https://www.linkedin.com/in/mario-delgado-5b6195155/
# Source: http://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV
# 
# Custom Properties: https://docs.blender.org/manual/en/latest/data_system/custom_properties.html?highlight=custom%20properties

import bpy, csv

# santize = True will convert Blender's duplicate object name to a Three.js sanitized name
# This is only a concern when exporting Blender to glTF files with the intent of importing
# them into Three.js.  Any names with mesh glTF nodes with '.' in the name will have the '.' removed.
# So sanitizing the names before exporting to glTF (and eventually Three.js) will provide for consitency
# in any processes that depend on a consitent and accurate node name. 
# See Three.js sanitizing:  https://discourse.threejs.org/t/issue-with-gltfloader-and-objects-with-dots-in-their-name-attribute/6726 	

sanitize = True   #True or False

# input: https://docs.python.org/3/library/functions.html#input
# Note: input awaits a response from the system console, not the Blender Python Interactive console
# System Console: https://docs.blender.org/manual/en/dev/advanced/command_line/launch/windows.html?highlight=toggle%20system%20console
# Python Interactive Console: https://docs.blender.org/manual/en/dev/editors/python_console.html

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
            # List Comprehension: https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
            mesh = [obj for obj in bpy.data.objects if obj.name == meshName and obj.type == 'MESH'][0]
			
            if sanitize:
                mesh.name = mesh.name.replace(".","")
                print (" Mesh's name sanitized from: ",meshName, " to: ", mesh.name)
                meshName = mesh.name
            
            mesh.data[propName] = propValue    
            print(" Updated meshName: ", meshName, ", propName: ", propName, ", propValue:", mesh.data[propName])
        
        print(" properties after assignment(s): ", bpy.data.objects[meshName].data.items()) 
        print("")
````

### Running the Test

* Open [test.blend](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/test/test.blend) file in test folder.
* Run [AddBlenderCustomPropertiesFromCSV.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/tree/master/py) Python script.
* Reference [test.csv](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/test/test.csv) in test folder when prompted by [input](https://docs.python.org/3/library/functions.html#input) prompt.

#### Test Output

````

******************************** meshName: Cube.000 ********************************************
 properties before assignment(s):  []
Mesh's name sanitized from:  Cube.000  to:  Cube000
Updated meshName:  Cube000 , propName:  visualKey , propValue: Cube.000
 properties after assignment(s):  [('visualKey', 'Cube.000')]

******************************** meshName: Cube.001 ********************************************
 properties before assignment(s):  []
Mesh's name sanitized from:  Cube.001  to:  Cube001
Updated meshName:  Cube001 , propName:  visualKey , propValue: Cube.001
 properties after assignment(s):  [('visualKey', 'Cube.001')]

````


## Author

* **Mario Delgado**  Github: [MarioDelgadoSr](https://github.com/MarioDelgadoSr)
* LinkedIn: [Mario Delgado](https://www.linkedin.com/in/mario-delgado-5b6195155/)
* [My Data Visualizer](http://MyDataVisualizer.com/demo/): A data visualization application using the [*DataVisual*](https://github.com/MarioDelgadoSr/DataVisual) design pattern.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

