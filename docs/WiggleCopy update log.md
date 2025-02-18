The problem turned out to be in the “copy settings” operator. In the operator, you can see that it simply takes the active bone’s properties and “assigns” them back to itself:

```python
def execute(self, context):
    b = context.active_pose_bone
    b.wiggle_mute = b.wiggle_mute
    b.wiggle_head = b.wiggle_head
    b.wiggle_tail = b.wiggle_tail
    b.wiggle_head_mute = b.wiggle_head_mute
    b.wiggle_tail_mute = b.wiggle_tail_mute
    ...
    return {'FINISHED'}
```

There are two issues here:

1. **No Iteration Over Selected Bones:**  
   The operator is meant to “copy active wiggle settings to selected bones”, but it never loops over the list of selected bones. Instead, it only works with the active bone (assigning its property to itself).

2. **Self‐assignment Doesn’t Trigger Updates:**  
   The add-on relies on the update callbacks defined on the properties (via `update=lambda s, c: update_prop(s, c, 'prop_name')`) to propagate the changes to all selected bones. In previous versions of Blender an assignment—even one that sets a property to its current value—might have triggered the update callback. However, in Blender 4.2 the update callback is not fired if the property is assigned the same value. In effect, the code

   ```python
   b.wiggle_mute = b.wiggle_mute
   ```
   
   does nothing, so no update is triggered and no copying occurs.

### What’s the fix?

The operator should instead iterate over all the selected pose bones (skipping the active one if necessary) and copy each property from the active bone to the other bones. For example:

```python
def execute(self, context):
    active = context.active_pose_bone
    for bone in context.selected_pose_bones:
        if bone != active:
            bone.wiggle_mute = active.wiggle_mute
            bone.wiggle_head = active.wiggle_head
            bone.wiggle_tail = active.wiggle_tail
            bone.wiggle_head_mute = active.wiggle_head_mute
            bone.wiggle_tail_mute = active.wiggle_tail_mute
            # ... and so on for all the properties ...
    return {'FINISHED'}
```

This way, the active bone’s settings are explicitly copied over to all selected bones, and you won’t be relying on an update callback firing on a “self‐assignment” that in Blender 4.2 no longer does so.

### In summary

The “copy settings to selected” function fails in Blender 4.2 because it only “copies” properties from the active bone to itself (by assigning each property its own value), and due to API changes in Blender 4.2, setting a property to its current value does not trigger the update callback. The operator should instead iterate over the selected bones and assign the active bone’s values to them explicitly.