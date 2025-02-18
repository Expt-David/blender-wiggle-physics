bl_info = {
    "name": "Wiggle 2",
    "author": "Steve Miller & David Zhang",
    "version": (2, 2, 6),
    "blender": (3, 0, 0),
    "location": "3D Viewport > Animation Panel",
    "description": "Simulate spring-like physics on Bone transforms",
    "warning": "",
    "wiki_url": "https://github.com/shteeve3d/blender-wiggle-2",
    "category": "Animation",
}

from . import wiggle_2
from . import wiggle_io

def register():
    wiggle_2.register()
    wiggle_io.register()

def unregister():
    wiggle_io.unregister()
    wiggle_2.unregister()
