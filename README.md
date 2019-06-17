<!-- Markdown reference: https://guides.github.com/features/mastering-markdown/ -->
# Python Script to Add Blender Custom Properties From CSV File

* The Python script, [AddBlenderCustomPropertiesFromCSV.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/py/AddBlenderCustomPropertiesFromCSV.py), will read a formatted csv (comma seperated value) file and use its contents to set [Custom Properties](https://docs.blender.org/manual/en/latest/data_system/custom_properties.html?highlight=custom%20properties).

* The Blender Add-on, [AddBlenderCustomPropertiesFromCSVAddOn.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/py/AddBlenderCustomPropertiesFromCSVAddOn.py), will perform the same task, but as an Add-on integrated into the 3D View Tool Panel.

* The file loaded must be in a [*csv.DictReader*](https://docs.python.org/3/library/csv.html) class format readable with *QUOTE_NONNUMERIC* quoting:
````
QUOTE_NONNUMERIC
    ... When used with the reader, input fields that are not quoted are converted to floats.
````
* Therefor, non-numeric components (including column headers) must be enclosed within double qutoes.
	
* This script or Add-on can be used to 'enrich' a Blender file, that will be exported to a glTF file, with embedded data.
	* When a Blender file is exported to a glTF file, the [Custom Properties](https://docs.blender.org/manual/en/latest/data_system/custom_properties.html?highlight=custom%20properties) are placed in the [*extras* properties](https://docs.blender.org/manual/en/dev/addons/io_gltf2.html) associated with the mesh.

## Usage


### Option 1

* [Run](https://docs.blender.org/api/2.79/info_quickstart.html#running-scripts) the [AddBlenderCustomPropertiesFromCSV.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/py/AddBlenderCustomPropertiesFromCSV.py) script from within Blender and respond to the input prompt with filename (format: [folder]/filename.csv ) that contains the data to update the Custom Properies. 

**Note:**
* The [*input*](https://docs.python.org/3/library/functions.html#input) method awaits a response from the [system console](https://docs.blender.org/manual/en/dev/advanced/command_line/launch/windows.html?highlight=toggle%20system%20console), not the [Blender Python Interactive console](https://docs.blender.org/manual/en/dev/editors/python_console.html).
 
### Option 2

* Alternatively [install](https://www.youtube.com/watch?v=DDt96E-xojg) [AddBlenderCustomPropertiesFromCSVAddOn.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/py/AddBlenderCustomPropertiesFromCSVAddOn.py) as a [Blender Add-on](https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html?highlight=addon)
	* Add-on name is '**CVS to Custom Properties**' under Object;	
	* Then select file with file selector; 
	* Select 'Add Custom Props' button to initiate the Python script that adds Customp Properties.
		* **Note**: The file [testWithAddOn.blend](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/test/testWithAddOn.blend) has the Blender add-on in a text editor window ready to be added directly for a quick-test scenario that doesn't involve [User Preferences](https://docs.blender.org/manual/en/dev/editors/preferences/addons.html?highlight=user%20preferences).
	
### Screen Shot of Installed Add-on:

![Screen Shot of Demonstration](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/test/AddOnScreenShot.png)	


#### Creating a Properly Formatted CSV Files

* All text value (including column headers) must be double quoted in the csv file.
* Excel does not add double quotes around text values automatically with its [Save As](https://support.office.com/en-us/article/Save-a-workbook-in-another-file-format-6A16C862-4A36-48F9-A300-C2CA0065286E) option. 
* One option is to use a [macro](https://stackoverflow.com/questions/846839/excel-how-to-add-double-quotes-to-strings-only-in-csv-file).
* Another option is to use [OpenOffice](http://www.openoffice.org/) as detailed in [this post](https://superuser.com/questions/130592/how-do-you-force-excel-to-quote-all-columns-of-a-csv-file).
* The Python Scripts will throw an exception error if they attempt to convert an un-quoted character string to a float numeric.

#### Script Workflow

* Assuming a Blender object (.type = 'MESH'); 
* With a name == 'object1';
* The following csv file contents will assign the Blender mesh a [Custom Properties](https://docs.blender.org/manual/en/latest/data_system/custom_properties.html?highlight=custom%20properties) numeric float value of *prop1* to property 'propName1' and a character value of "*prop2*" to 'propertyName2':

````
"objectName","propName1","propName2"
"object1",prop1,"prop2"
````

* The *sanitize = True* option will sanitize a mesh's name to be consitent wth [Three.js naming requirements for nodes](https://discourse.threejs.org/t/issue-with-gltfloader-and-objects-with-dots-in-their-name-attribute/6726 ).

##### Contents of [AddBlenderCustomPropertiesFromCSV.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/tree/master/py): 
	
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
# "objectName","propName1","propName2",...
# "object1","prop1",prop2,...
# "object2","prop1",prop2,...
#
# Script will assign bpy.data.objects[objectName].data[propNameN] = propN
#	* The quoted propNs will be treated as characters
#	* The un-quoted propNs will be converted to float.


print("********************************Add Blender Custom Properties ********************************************")
print(" ")
print("Adding Custom Properties with the following options:")
print(" ")
print("filePath: ", filePath)
print("sanitize: ", str(sanitize))
print(" ")
		
with open( filePath ) as csvfile:   # https://docs.python.org/3/library/csv.html
    rdr = csv.DictReader( csvfile, quoting = csv.QUOTE_NONNUMERIC )     
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

#### Blender Add-on Workflow

* Assuming a Blender object (.type = 'MESH'); 
* With a name == 'object1';
* The following csv file contents will assign the Blender mesh a [Custom Properties](https://docs.blender.org/manual/en/latest/data_system/custom_properties.html?highlight=custom%20properties) numeric float value of *prop1* to property 'propName1' and a character value of "*prop2*" to 'propertyName2':

````
"objectName","propName1","propName2"
"object1",prop1,"prop2"
````
* Once  [installed](https://www.youtube.com/watch?v=DDt96E-xojg) , the Blender Add-on will be registered in the Tools panel:

![Screen Shot of Demonstration](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/test/AddOnScreenShot.png)	

##### Contents of [AddBlenderCustomPropertiesFromCSVAddOn.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/py/AddBlenderCustomPropertiesFromCSVAddOn.py):
	
````
# Add-on Tutorial: https://youtu.be/OEkrQGFqM10
# Python script to set Blender Custom Properties for a mesh (.type == 'MESH')
# Author: Mario Delgado, LinkedIn: https://www.linkedin.com/in/mario-delgado-5b6195155/
# Source: http://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV
# 
# Custom Properties: https://docs.blender.org/manual/en/latest/data_system/custom_properties.html?highlight=custom%20properties
# Modified from: https://blender.stackexchange.com/questions/26898/how-to-create-a-folder-dialog/26906#26906

bl_info = {"name": "CVS to Custom Properties", "category": "Object"}

import bpy, csv

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )


class addPropsSettings(PropertyGroup):

    path = StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')
        
    sanitize_bool = BoolProperty(        #https://blender.stackexchange.com/questions/35007/how-can-i-add-a-checkbox-in-the-tools-ui
        name="Sanitize Mesh Name",
        description="Sanitize the Mesh Name",
        default = True
        )        
        
        
class processCustom(bpy.types.Operator):
  
    bl_idname = "object.process_custom"
    bl_label = ""
    
    filePath =  bpy.props.StringProperty() 
    sanitize =  bpy.props.BoolProperty() 
    
    def execute(self, context):

        filePath = self.filePath
        sanitize = self.sanitize

        # santize = True will convert Blender's duplicate object name to a Three.js sanitized name
        # This is only a concern when exporting Blender to glTF files with the intent of importing
        # them into Three.js.  Any names with mesh glTF nodes with '.' in the name will have the '.' removed.
        # So sanitizing the names before exporting to glTF (and eventually Three.js) will provide for consitency
        # in any processes that depend on a consitent and accurate node name. 
        # See Three.js sanitizing:  https://discourse.threejs.org/t/issue-with-gltfloader-and-objects-with-dots-in-their-name-attribute/6726 	
        #sanitize = True   #True or False
        

        # input: https://docs.python.org/3/library/functions.html#input
        # Note: input awaits a response from the system console, not the Blender Python Interactive console
        # System Console: https://docs.blender.org/manual/en/dev/advanced/command_line/launch/windows.html?highlight=toggle%20system%20console
        # Python Interactive Console: https://docs.blender.org/manual/en/dev/editors/python_console.html
        #filePath = input("Enter file name path (folder/filename.csv):")         #Example: Type "c:/data/keys.csv" when prompted in the conole

		# Example of content in .csv file, line 1 contains column heading (Object Name and Properties):
		#
		# "objectName","propName1","propName2",...
		# "object1","prop1",prop2,...
		# "object2","prop1",prop2,...
		#
		# Script will assign bpy.data.objects[objectName].data[propNameN] = propN
		#	* The quoted propNs will be treated as characters
		#	* The un-quoted propNs will be converted to float.

        print("********************************Add Blender Custom Properties ********************************************")
        print(" ")
        print("Adding Custom Properties with the following options:")
        print(" ")
        print("filePath: ", filePath)
        print("sanitize: ", str(sanitize))
        print(" ")

        with open( filePath ) as csvfile:   # https://docs.python.org/3/library/csv.html
			rdr = csv.DictReader( csvfile, quoting = csv.QUOTE_NONNUMERIC )  
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
		
        return {'FINISHED'}

# ---------------------------------------------------------------------------------
#  Customize Tool Panel and add file selector and check box for sanitize option
# ---------------------------------------------------------------------------------

class addCustomProperitesPanel(Panel):
    bl_idname = "addCustomProperitesPanel"
    bl_label = "CSV to Custom Props"  # scn.csv_to_custom_props
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        col = layout.column(align=True)
        col.prop(scn.csv_to_custom_props, "path", text="")      				#The file path selected by the user
        col.prop(scn.csv_to_custom_props, "sanitize_bool","Sanitize Mesh Name") #The sanitize option True/False 
        
        #Passing property: https://blenderartists.org/t/how-to-pass-two-arguments-to-a-button-operator/497013/8         
        processCustomButton =  col.operator("object.process_custom", text="Add Custom Props")
        processCustomButton.filePath =  scn.csv_to_custom_props.path 
        processCustomButton.sanitize =  scn.csv_to_custom_props.sanitize_bool
        
# ------------------------------------------------------------------------
#    register and unregister functions
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.csv_to_custom_props = PointerProperty(type=addPropsSettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.csv_to_custom_props

if __name__ == "__main__":
    register()

````

### Running the Test(s)

#### Option 1

* Open [test.blend](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/test/test.blend) file in test folder.
* Run [AddBlenderCustomPropertiesFromCSV.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/tree/master/py) Python script.
* Reference [test.csv](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/test/test.csv) in test folder when prompted by [input](https://docs.python.org/3/library/functions.html#input) prompt.

**Note:**
* The [*input*](https://docs.python.org/3/library/functions.html#input) method awaits a response from the [system console](https://docs.blender.org/manual/en/dev/advanced/command_line/launch/windows.html?highlight=toggle%20system%20console), not the [Blender Python Interactive console](https://docs.blender.org/manual/en/dev/editors/python_console.html).
 
 #### Option 2
 
* Alternatively [install](https://www.youtube.com/watch?v=DDt96E-xojg)  [AddBlenderCustomPropertiesFromCSVAddOn.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/py/AddBlenderCustomPropertiesFromCSVAddOn.py) as a [Blender Add-on](https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html?highlight=addon)
	* Add-on name is '**CVS to Custom Properties**' under Object;
	* Then select file with file selector;
    * Select 'Add Custom Props' button to initiate the Python script that adds Customp Properties.
		* Note: The file [testWithAddOn.blend](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/test/testWithAddOn.blend) has the Blender Add-on ready for a quick test, without having to install via [User Preferences](https://docs.blender.org/manual/en/dev/editors/preferences/addons.html?highlight=user%20preferences). 
		
**Screen Shot of Installed Add-on**
![Screen Shot of Demonstration](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/test/AddOnScreenShot.png)	
	
#### Contents of test.csv

````
"Mesh","value"
"Cube.000",10
"Cube.001",20
````	
	
	
#### Test Output 

The output is the same for either [AddBlenderCustomPropertiesFromCSV.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/tree/master/py) script or [AddBlenderCustomPropertiesFromCSVAddOn.py](https://github.com/MarioDelgadoSr/AddBlenderCustomPropertiesFromCSV/blob/master/py/AddBlenderCustomPropertiesFromCSVAddOn.py)  Add-on):

````

********************************Add Blender Custom Properties ********************************************

Adding Custom Properties with the following options:

filePath:  c:\temp\test.csv
sanitize:  True

******************************** meshName: Cube.000 ********************************************
 properties before assignment(s):  []
 Mesh's name sanitized from:  Cube.000  to:  Cube000
 Updated meshName:  Cube000 , propName:  value , propValue: 10.0
 properties after assignment(s):  [('value', 10.0)]

******************************** meshName: Cube.001 ********************************************
 properties before assignment(s):  []
 Mesh's name sanitized from:  Cube.001  to:  Cube001
 Updated meshName:  Cube001 , propName:  value , propValue: 20.0
 properties after assignment(s):  [('value', 20.0)]
````


## Author

* **Mario Delgado**  Github: [MarioDelgadoSr](https://github.com/MarioDelgadoSr)
* LinkedIn: [Mario Delgado](https://www.linkedin.com/in/mario-delgado-5b6195155/)
* [My Data Visualizer](http://MyDataVisualizer.com/demo/): A data visualization application using the [*DataVisual*](https://github.com/MarioDelgadoSr/DataVisual) design pattern.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

