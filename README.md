<!-- Markdown reference: https://guides.github.com/features/mastering-markdown/ -->
# Add Blender Custom Properties From CSV File

A Blender Python script to read a formatted csv (comma seperated value) file to set [Custom Properties](https://docs.blender.org/manual/en/latest/data_system/custom_properties.html?highlight=custom%20properties).

# Usage

[Run script from in Blender](https://docs.blender.org/api/2.79/info_quickstart.html#running-scripts) and respond to the input prompt with filename.csv that contains the data to update the Custom Properies. 

* Assuming a Blender object (.type = 'MESH') with a name = 'object1', the following file contents will assign the object the value of 'prop1' to property 'propName1'

objectName,propName1
object1,prop1

Script Syntax (source code includes comments)

''''

import bpy, csv

filePath = input("Enter file name path (folder/filename.csv):")        le


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


''''


## Author

* **Mario Delgado**  Github: [MarioDelgadoSr](https://github.com/MarioDelgadoSr)
* LinkedIn: [Mario Delgado](https://www.linkedin.com/in/mario-delgado-5b6195155/)
* [My Data Visualizer](https://qzfcxunzx7ydnpxm3djoqw-on.drv.tw/DataVisualizer/): A data visualization application using the *DataVisual* design pattern.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

