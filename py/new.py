# Modified from: https://blender.stackexchange.com/questions/26898/how-to-create-a-folder-dialog/26906#26906
# https://blender.stackexchange.com/questions/26898/how-to-create-a-folder-dialog/26906#26906
import bpy
from bpy.props import (StringProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

# ------------------------------------------------------------------------
#    ui
# ------------------------------------------------------------------------

class MySettings(PropertyGroup):

    path = StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')

class addCustomProperitesPanel(Panel):
    bl_idname = "addCustomProperitesPanel"
    bl_label = "CSV to Custom Props"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        col = layout.column(align=True)
        col.prop(scn.csv_to_custom_props, "path", text="")

        # print the path to the console
        #print (scn.csv_to_custom_props.path)
        
        
    def addCustomPropsToMeshes(filePath,sanitize)
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