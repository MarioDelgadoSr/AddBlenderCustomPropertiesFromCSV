# Tutorial: https://youtu.be/OEkrQGFqM10
# Folder/File Dialog: https://blender.stackexchange.com/questions/26898/how-to-create-a-folder-dialog/26906#26906

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


class MySettings(PropertyGroup):

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
    
    properties = bpy.props.StringProperty() # defining the property  
    
    def execute(self, context):
        parmList = self.properties.split(",")
        filePath = parmList[0]			  #The file selected by the user		
        sanitize = parmList[1] == "True"  #Boolean test of check box selection	

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
        # objectName,propName1,propName2,...
        # object1,prop1,prop2,...
        # object2,prop1,prop2,...
        #
        # Script will assign bpy.data.objects[objectName].data[propNameN] = propN

        print("********************************Add Blender Custom Properties ********************************************")
        print(" ")
        print("Adding Custom Properties with the following options:")
        print(" ")
        print("filePath: ", filePath)
        print("sanitize: ", str(sanitize))
        print(" ")

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
        
        parameter = scn.csv_to_custom_props.path + "," + str(scn.csv_to_custom_props.sanitize_bool) #comma seperated parms	
        
        #Icons: https://blenderartists.org/t/icon-enumeration-script-blender-2-5/491147/3
        #Passing property: https://blenderartists.org/t/how-to-pass-two-arguments-to-a-button-operator/497013/8
        col.operator("object.process_Custom", text="Add Custom Props").properties= parameter
            
        
# ------------------------------------------------------------------------
#    register and unregister functions
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.csv_to_custom_props = PointerProperty(type=MySettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.csv_to_custom_props

if __name__ == "__main__":
    register()



