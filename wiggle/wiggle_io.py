import bpy, json

# --- Export Operator ---
class WIGGLE_OT_ExportSettings(bpy.types.Operator):
    """Export all wiggle settings to a JSON file"""
    bl_idname = "wiggle.export_settings"
    bl_label = "Export Wiggle Settings"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    def execute(self, context):
        export_data = {}
        scene = context.scene
        export_data["scene"] = {
            "wiggle_enable": scene.wiggle_enable,
            "iterations": scene.wiggle.iterations,
            "loop": scene.wiggle.loop,
            "preroll": scene.wiggle.preroll,
            "bake_overwrite": scene.wiggle.bake_overwrite,
            "bake_nla": scene.wiggle.bake_nla,
        }
        export_data["armatures"] = {}
        for obj in scene.objects:
            if obj.type == 'ARMATURE' and getattr(obj, "wiggle_enable", False):
                armature_data = {
                    "wiggle_mute": obj.wiggle_mute,
                    "wiggle_freeze": obj.wiggle_freeze,
                    "bones": {}
                }
                for bone in obj.pose.bones:
                    if getattr(bone, "wiggle_enable", False):
                        bone_data = {
                            # Tail settings
                            "wiggle_head": bone.wiggle_head,
                            "wiggle_tail": bone.wiggle_tail,
                            "wiggle_mute": bone.wiggle_mute,
                            "wiggle_mass": bone.wiggle_mass,
                            "wiggle_stiff": bone.wiggle_stiff,
                            "wiggle_stretch": bone.wiggle_stretch,
                            "wiggle_damp": bone.wiggle_damp,
                            "wiggle_gravity": bone.wiggle_gravity,
                            "wiggle_wind": bone.wiggle_wind,
                            "wiggle_chain": bone.wiggle_chain,
                            # Export pointer properties (by name) for collision & wind:
                            "wiggle_collider": bone.wiggle_collider.name if bone.wiggle_collider else "",
                            "wiggle_collider_collection": bone.wiggle_collider_collection.name if bone.wiggle_collider_collection else "",
                            "wiggle_wind_ob": bone.wiggle_wind_ob.name if bone.wiggle_wind_ob else "",
                            # Head settings
                            "wiggle_mass_head": bone.wiggle_mass_head,
                            "wiggle_stiff_head": bone.wiggle_stiff_head,
                            "wiggle_stretch_head": bone.wiggle_stretch_head,
                            "wiggle_damp_head": bone.wiggle_damp_head,
                            "wiggle_gravity_head": bone.wiggle_gravity_head,
                            "wiggle_wind_head": bone.wiggle_wind_head,
                            "wiggle_chain_head": bone.wiggle_chain_head,
                            "wiggle_collider_head": bone.wiggle_collider_head.name if bone.wiggle_collider_head else "",
                            "wiggle_collider_collection_head": bone.wiggle_collider_collection_head.name if bone.wiggle_collider_collection_head else "",
                            "wiggle_wind_ob_head": bone.wiggle_wind_ob_head.name if bone.wiggle_wind_ob_head else "",
                            # Collision numeric settings remain unchanged…
                            "wiggle_collider_type": bone.wiggle_collider_type,
                            "wiggle_radius": bone.wiggle_radius,
                            "wiggle_friction": bone.wiggle_friction,
                            "wiggle_bounce": bone.wiggle_bounce,
                            "wiggle_sticky": bone.wiggle_sticky,
                            "wiggle_collider_type_head": bone.wiggle_collider_type_head,
                            "wiggle_radius_head": bone.wiggle_radius_head,
                            "wiggle_friction_head": bone.wiggle_friction_head,
                            "wiggle_bounce_head": bone.wiggle_bounce_head,
                            "wiggle_sticky_head": bone.wiggle_sticky_head
                        }
                        armature_data["bones"][bone.name] = bone_data
                export_data["armatures"][obj.name] = armature_data

        try:
            with open(self.filepath, 'w') as f:
                json.dump(export_data, f, indent=4)
            self.report({'INFO'}, f"Wiggle settings exported to {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Error exporting settings: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# --- Import Operator ---
class WIGGLE_OT_ImportSettings(bpy.types.Operator):
    """Import wiggle settings from a JSON file and apply them"""
    bl_idname = "wiggle.import_settings"
    bl_label = "Import Wiggle Settings"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    def execute(self, context):
        try:
            with open(self.filepath, 'r') as f:
                import_data = json.load(f)
        except Exception as e:
            self.report({'ERROR'}, f"Error loading file: {e}")
            return {'CANCELLED'}

        scene = context.scene
        scene.wiggle_enable = import_data.get("scene", {}).get("wiggle_enable", scene.wiggle_enable)
        scene.wiggle.iterations = import_data.get("scene", {}).get("iterations", scene.wiggle.iterations)
        scene.wiggle.loop = import_data.get("scene", {}).get("loop", scene.wiggle.loop)
        scene.wiggle.preroll = import_data.get("scene", {}).get("preroll", scene.wiggle.preroll)
        scene.wiggle.bake_overwrite = import_data.get("scene", {}).get("bake_overwrite", scene.wiggle.bake_overwrite)
        scene.wiggle.bake_nla = import_data.get("scene", {}).get("bake_nla", scene.wiggle.bake_nla)
        
        for obj in scene.objects:
            if obj.type == 'ARMATURE' and obj.name in import_data.get("armatures", {}):
                armature_data = import_data["armatures"][obj.name]
                obj.wiggle_mute = armature_data.get("wiggle_mute", obj.wiggle_mute)
                obj.wiggle_freeze = armature_data.get("wiggle_freeze", obj.wiggle_freeze)
                for bone in obj.pose.bones:
                    if bone.name in armature_data.get("bones", {}):
                        bone_data = armature_data["bones"][bone.name]
                        bone.wiggle_head = bone_data.get("wiggle_head", bone.wiggle_head)
                        bone.wiggle_tail = bone_data.get("wiggle_tail", bone.wiggle_tail)
                        bone.wiggle_mute = bone_data.get("wiggle_mute", bone.wiggle_mute)
                        # Tail settings
                        bone.wiggle_mass = bone_data.get("wiggle_mass", bone.wiggle_mass)
                        bone.wiggle_stiff = bone_data.get("wiggle_stiff", bone.wiggle_stiff)
                        bone.wiggle_stretch = bone_data.get("wiggle_stretch", bone.wiggle_stretch)
                        bone.wiggle_damp = bone_data.get("wiggle_damp", bone.wiggle_damp)
                        bone.wiggle_gravity = bone_data.get("wiggle_gravity", bone.wiggle_gravity)
                        bone.wiggle_wind = bone_data.get("wiggle_wind", bone.wiggle_wind)
                        bone.wiggle_chain = bone_data.get("wiggle_chain", bone.wiggle_chain)
                        # Reassign pointer properties (look up by name)
                        bone.wiggle_collider = bpy.data.objects.get(bone_data.get("wiggle_collider", "")) if bone_data.get("wiggle_collider", "") else None
                        bone.wiggle_collider_collection = bpy.data.collections.get(bone_data.get("wiggle_collider_collection", "")) if bone_data.get("wiggle_collider_collection", "") else None
                        bone.wiggle_wind_ob = bpy.data.objects.get(bone_data.get("wiggle_wind_ob", "")) if bone_data.get("wiggle_wind_ob", "") else None
                        # Head settings
                        bone.wiggle_mass_head = bone_data.get("wiggle_mass_head", bone.wiggle_mass_head)
                        bone.wiggle_stiff_head = bone_data.get("wiggle_stiff_head", bone.wiggle_stiff_head)
                        bone.wiggle_stretch_head = bone_data.get("wiggle_stretch_head", bone.wiggle_stretch_head)
                        bone.wiggle_damp_head = bone_data.get("wiggle_damp_head", bone.wiggle_damp_head)
                        bone.wiggle_gravity_head = bone_data.get("wiggle_gravity_head", bone.wiggle_gravity_head)
                        bone.wiggle_wind_head = bone_data.get("wiggle_wind_head", bone.wiggle_wind_head)
                        bone.wiggle_chain_head = bone_data.get("wiggle_chain_head", bone.wiggle_chain_head)
                        bone.wiggle_collider_head = bpy.data.objects.get(bone_data.get("wiggle_collider_head", "")) if bone_data.get("wiggle_collider_head", "") else None
                        bone.wiggle_collider_collection_head = bpy.data.collections.get(bone_data.get("wiggle_collider_collection_head", "")) if bone_data.get("wiggle_collider_collection_head", "") else None
                        bone.wiggle_wind_ob_head = bpy.data.objects.get(bone_data.get("wiggle_wind_ob_head", "")) if bone_data.get("wiggle_wind_ob_head", "") else None
                        # Collision numeric settings remain unchanged…
                        bone.wiggle_collider_type = bone_data.get("wiggle_collider_type", bone.wiggle_collider_type)
                        bone.wiggle_radius = bone_data.get("wiggle_radius", bone.wiggle_radius)
                        bone.wiggle_friction = bone_data.get("wiggle_friction", bone.wiggle_friction)
                        bone.wiggle_bounce = bone_data.get("wiggle_bounce", bone.wiggle_bounce)
                        bone.wiggle_sticky = bone_data.get("wiggle_sticky", bone.wiggle_sticky)
                        bone.wiggle_collider_type_head = bone_data.get("wiggle_collider_type_head", bone.wiggle_collider_type_head)
                        bone.wiggle_radius_head = bone_data.get("wiggle_radius_head", bone.wiggle_radius_head)
                        bone.wiggle_friction_head = bone_data.get("wiggle_friction_head", bone.wiggle_friction_head)
                        bone.wiggle_bounce_head = bone_data.get("wiggle_bounce_head", bone.wiggle_bounce_head)
                        bone.wiggle_sticky_head = bone_data.get("wiggle_sticky_head", bone.wiggle_sticky_head)
        self.report({'INFO'}, f"Wiggle settings imported from {self.filepath}")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# --- Import/Export Panel ---
class WIGGLE_PT_ImportExport(bpy.types.Panel):
    bl_label = "Import/Export Settings"
    bl_category = 'Animation'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'WIGGLE_PT_Settings'

    @classmethod
    def poll(cls, context):
        return context.scene and context.scene.wiggle_enable

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator("wiggle.export_settings", text="Export Settings", icon='EXPORT')
        row.operator("wiggle.import_settings", text="Import Settings", icon='IMPORT')

# --- Registration Helpers ---
def register():
    bpy.utils.register_class(WIGGLE_OT_ExportSettings)
    bpy.utils.register_class(WIGGLE_OT_ImportSettings)
    bpy.utils.register_class(WIGGLE_PT_ImportExport)

def unregister():
    bpy.utils.unregister_class(WIGGLE_PT_ImportExport)
    bpy.utils.unregister_class(WIGGLE_OT_ImportSettings)
    bpy.utils.unregister_class(WIGGLE_OT_ExportSettings)
