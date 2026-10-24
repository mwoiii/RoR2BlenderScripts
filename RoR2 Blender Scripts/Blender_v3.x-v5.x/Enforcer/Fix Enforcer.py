#Original Creator: KingEnderBrine
#Modified by: RuneFox237, Miyowi
#Version 1.1.0

import bpy
import re
from math import radians
from mathutils import Vector
from enum import Enum

bonesOrder = ['ROOT', 'base', 'pelvis', 'thighL', 'calfL', 'footL', 'toeL', 'calfTwistL1', 'calfTwistL2', 'calfTwistL3', 'thighTwistL1', 'thighTwistL2', 'thighTwistL3', 'thighR', 'calfR', 'footR', 'toeR', 'calfTwistR1', 'calfTwistR2', 'calfTwistR3', 'thighTwistR1', 'thighTwistR2', 'thighTwistR3', 'stomach', 'spine', 'chest', 'clavicleL', 'upper_armL', 'lower_armL', 'handL', 'thumb_L', 'thumb_L_1', 'thumb_L_2', 'mid_L', 'mid_L1', 'mid_L2', 'point_L1', 'point_L2', 'point_L3', 'fingerL3', 'fingerL3_1', 'fingerL3_2', 'fingerL3_end', 'shotgun_prop', 'shotgun_prop1', 'shotgun_prop_end', 'fingerL4', 'fingerL4_1', 'fingerL4_2', 'fingerL4_end', 'elbowL_twist1', 'elbowL_twist2', 'elbowL_twist3', 'armL_twist1', 'armL_twist2', 'armL_twist3', 'neck', 'head', 'clavicleR', 'upper_armR', 'lower_armR', 'handR', 'fingerR2', 'fingerR2_1', 'fingerR2_end', 'thumbR', 'thumbR_1', 'thumbR_end', 'shield_M_00_jnt', 'shield_M_01_jnt', 'shield_M_02_jnt', 'fingerR3', 'fingerR3_1', 'fingerR3_2', 'fingerR3_end', 'fingerR1', 'fingerR1_1', 'fingerR1_end', 'fingerR4', 'fingerR4_1', 'fingerR4_2', 'fingerR4_end', 'elbowR_twist1', 'elbowR_twist2', 'elbowR_twist3', 'armR_twist1', 'armR_twist2', 'armR_twist3', 'booster']
    
srcArmName = 'Armature'
targetArmName = 'Armature'
srcMeshName = 'Enforcer_geo'

meshOffset = None # Vector((1, 1, 1))
meshSpecificOffset = None # {'TestMesh'=Vector((1, 1, 1))}

meshesScale = None # (1, 1, 1)
meshSpecificScale = None # {'TesMesh'=(1, 1, 1)}

excessiveMeshes = [] # ['TestMesh']

applyRestToPose = False


"""
additional utilities for adjusting the tail position of bones to make maya models easier to work with

if you're only here to run this fix script, ignore this stuff. the generated apply/revert scripts should already be in the repo

remember that if you don't revert the visualisation changes before exporting, your model will be super twisted ingame
"""
generateVisualisationScripts = False

GENERATEDSCRIPTSTART = f"""
import bpy
from mathutils import Vector

srcArmName = '{srcArmName}'

boneTailPositions = {{
"""

GENERATEDSCRIPTEND = """
}

def SetBoneTailPositions(srcArmName):
    srcArm = bpy.data.objects[srcArmName]
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='EDIT')
    
    for bone in srcArm.data.edit_bones:
        if bone.name in boneTailPositions:
            bone.tail = boneTailPositions[bone.name]

SetBoneTailPositions(srcArmName)
"""

boneOldPositionsString = ""
boneNewPositionsString = ""

class TailType(Enum):
    FIRSTCHILD = 1 # ignore childName, set this bone's tail to the first child's head
    NAMEDCHILD = 2 # set this bone's tail to the named child's head
    ALLTONAMEDCHILD = 3 # set this bone's tail, and all other children's tails that aren't the named child, to the named child's head. overwrites settings of any children
    NAMEDSIBLING = 4 # set this bone's tail to the named sibling's head. no workie if at the root but think this doesn't really matter at this scope
    TOPOSITION = 5 # ignore childName, set this bone's tail to the position in the TailInfo instead

class TailInfo:
    def __init__(self, tailType=TailType.FIRSTCHILD, boneName="", position=Vector((0.0, 0.0, 0.0))):
        self.tailType = tailType
        self.boneName = boneName
        self.position = position
        
boneTailPositions = {"chest": TailInfo(TailType.NAMEDCHILD, "neck"),
    "stomach": TailInfo(TailType.FIRSTCHILD),
    "spine": TailInfo(TailType.FIRSTCHILD),
    "chest": TailInfo(TailType.NAMEDCHILD, "neck"),
    "neck": TailInfo(TailType.FIRSTCHILD),
    "head" : TailInfo(TailType.TOPOSITION, position=Vector((0, 0.003073, 1.94265))),
    
    "clavicleL" : TailInfo(TailType.FIRSTCHILD),
    "upper_armL" : TailInfo(TailType.ALLTONAMEDCHILD, "lower_armL"),
    "lower_armL" : TailInfo(TailType.ALLTONAMEDCHILD, "handL"),
    "handL" : TailInfo(TailType.TOPOSITION, position=Vector((0.490222, 0.165189, 1.06546))),
    "thumb_L": TailInfo(TailType.FIRSTCHILD),
    "thumb_L_1": TailInfo(TailType.FIRSTCHILD),
    "thumb_L_2": TailInfo(TailType.TOPOSITION, position=Vector((0.409268, 0.000325, 0.940004))),
    "point_L1": TailInfo(TailType.FIRSTCHILD),
    "point_L2": TailInfo(TailType.FIRSTCHILD),
    "point_L3": TailInfo(TailType.TOPOSITION, position=Vector((0.522802, 0.06852, 0.87629))),
    "mid_L": TailInfo(TailType.FIRSTCHILD),
    "mid_L1": TailInfo(TailType.FIRSTCHILD),
    "mid_L2": TailInfo(TailType.TOPOSITION, position=Vector((0.494715, 0.126018, 0.875531))),
    "fingerL3": TailInfo(TailType.FIRSTCHILD),
    "fingerL3_1": TailInfo(TailType.FIRSTCHILD),
    "fingerL3_2": TailInfo(TailType.FIRSTCHILD),
    "fingerL3_end": TailInfo(TailType.TOPOSITION, position=Vector((0.499088, 0.192261, 0.89384))),
    "fingerL4": TailInfo(TailType.FIRSTCHILD),
    "fingerL4_1": TailInfo(TailType.FIRSTCHILD),
    "fingerL4_2": TailInfo(TailType.FIRSTCHILD),
    "fingerL4_end": TailInfo(TailType.TOPOSITION, position=Vector((0.49507, 0.25232, 0.928514))),
    
    "clavicleR" : TailInfo(TailType.FIRSTCHILD),
    "upper_armR" : TailInfo(TailType.ALLTONAMEDCHILD, "lower_armR"),
    "lower_armR" : TailInfo(TailType.ALLTONAMEDCHILD, "handR"),
    "handR" : TailInfo(TailType.TOPOSITION, position=Vector((-0.490222, 0.165189, 1.06546))),
    "thumbR": TailInfo(TailType.FIRSTCHILD),
    "thumbR_1": TailInfo(TailType.FIRSTCHILD),
    "thumbR_end": TailInfo(TailType.TOPOSITION, position=Vector((-0.409268, 0.000325, 0.940004))),
    "fingerR1": TailInfo(TailType.FIRSTCHILD),
    "fingerR1_1": TailInfo(TailType.FIRSTCHILD),
    "fingerR1_end": TailInfo(TailType.TOPOSITION, position=Vector((-0.522802, 0.06852, 0.87629))),
    "fingerR2": TailInfo(TailType.FIRSTCHILD),
    "fingerR2_1": TailInfo(TailType.FIRSTCHILD),
    "fingerR2_end": TailInfo(TailType.TOPOSITION, position=Vector((-0.494715, 0.126018, 0.875531))),
    "fingerR3": TailInfo(TailType.FIRSTCHILD),
    "fingerR3_1": TailInfo(TailType.FIRSTCHILD),
    "fingerR3_2": TailInfo(TailType.FIRSTCHILD),
    "fingerR3_end": TailInfo(TailType.TOPOSITION, position=Vector((-0.499088, 0.192261, 0.89384))),
    "fingerR4": TailInfo(TailType.FIRSTCHILD),
    "fingerR4_1": TailInfo(TailType.FIRSTCHILD),
    "fingerR4_2": TailInfo(TailType.FIRSTCHILD),
    "fingerR4_end": TailInfo(TailType.TOPOSITION, position=Vector((-0.49507, 0.25232, 0.928514))),
    
    "thighL" : TailInfo(TailType.ALLTONAMEDCHILD, "calfL"),
    "calfL" : TailInfo(TailType.ALLTONAMEDCHILD, "footL"),
    "footL" : TailInfo(TailType.FIRSTCHILD),
    "toeL" : TailInfo(TailType.TOPOSITION, position=Vector((0.261753, -0.138072, 0.071211))),
    
    "thighR" : TailInfo(TailType.ALLTONAMEDCHILD, "calfR"),
    "calfR" : TailInfo(TailType.ALLTONAMEDCHILD, "footR"),
    "footR" : TailInfo(TailType.FIRSTCHILD),
    "toeR" : TailInfo(TailType.TOPOSITION, position=Vector((-0.257043, -0.138072, 0.071211))),
    
    "shotgun_prop" : TailInfo(TailType.FIRSTCHILD),
    "shotgun_prop1" : TailInfo(TailType.TOPOSITION, position=Vector((0.538953, -0.213577, 0.049665))),
    "shotgun_prop_end" : TailInfo(TailType.TOPOSITION, position=Vector((0.538953, -0.50903, -0.141149))),
    
    "shield_M_00_jnt" : TailInfo(TailType.TOPOSITION, position=Vector((-0.517523, -0.346363, 1.37849))),
    "shield_M_01_jnt" : TailInfo(TailType.FIRSTCHILD),
}
        
def ResolveTailPosition(bone):
    global boneOldPositionsString
    global boneNewPositionsString
    if bone.name in boneTailPositions:
        tailInfo = boneTailPositions[bone.name]
        if isinstance(tailInfo, TailInfo):
                    
            if generateVisualisationScripts:
                boneOldPositionsString += f"    \"{bone.name}\":Vector(({bone.tail[0]},{bone.tail[1]},{bone.tail[2]})),\n"
            
            match tailInfo.tailType:
                
                case TailType.FIRSTCHILD:                    
                    if bone.children is not None:
                        tailChild = bone.children[0]
                        if tailChild is not None:
                            bone.tail = tailChild.head
                            
                case TailType.NAMEDCHILD:
                    if bone.children is not None:
                        tailChild = None
                        for c in bone.children:
                            if c.name == tailInfo.boneName:
                                tailChild = c
                                break
                        if tailChild is not None:
                            bone.tail = tailChild.head
                        
                case TailType.ALLTONAMEDCHILD:
                    if bone.children is not None:
                        tailChild = None
                        for c in bone.children:
                            if c.name == tailInfo.boneName:
                                tailChild = c
                                break
                        if tailChild is not None:   
                            bone.tail = tailChild.head                         
                            for c in bone.children:
                                if c.name != tailInfo.boneName:
                                    boneTailPositions[c.name] = TailInfo(TailType.NAMEDSIBLING, tailInfo.boneName)
                            
                case TailType.NAMEDSIBLING:
                    if bone.parent is not None:
                        tailSibling = None
                        for c in bone.parent.children:
                            if c.name == tailInfo.boneName:
                                tailSibling = c
                                break
                        if tailSibling is not None:
                            bone.tail = tailSibling.head
                            
                case TailType.TOPOSITION:
                    bone.tail = tailInfo.position
            
            if generateVisualisationScripts:
                boneNewPositionsString += f"    \"{bone.name}\":Vector(({bone.tail[0]},{bone.tail[1]},{bone.tail[2]})),\n"
        else:
            print(f"{bone.name} does not direct to a TailInfo instance! {type(boneTailPositions[bone.name])}")
        
def ApplyVisualFixes(srcArmName):
    srcArm = bpy.data.objects[srcArmName]
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='EDIT')
    for bone in srcArm.data.edit_bones:
        ResolveTailPosition(bone)  
    print(f"REVERT POSITIONS SCRIPT:\n{'#'*30}{GENERATEDSCRIPTSTART + boneOldPositionsString + GENERATEDSCRIPTEND}{'#'*30}{'\n'*10}")
    print(f"APPLY POSITIONS SCRIPT:\n{'#'*30}{GENERATEDSCRIPTSTART + boneNewPositionsString + GENERATEDSCRIPTEND}{'#'*30}")
"""
end of all maya utility stuff that you would need to worry about
"""


def RemoveExcessiveMeshes(excessiveMeshes):
    for meshName in excessiveMeshes:
        bpy.data.objects.remove(bpy.data.objects[meshName])    

def CopyEditBones(bones, editBones, offset = None):
    for bone in bones:
        boneCopy = editBones.new(bone.name)
    for bone in bones:
        boneCopy = editBones[bone.name]
        boneCopy.bbone_curveinx = bone.bbone_curveinx
        boneCopy.bbone_curveinz = bone.bbone_curveinz
        boneCopy.bbone_curveoutx = bone.bbone_curveoutx
        boneCopy.bbone_curveoutz = bone.bbone_curveoutz
        if bone.bbone_custom_handle_start is not None:
            boneCopy.bbone_custom_handle_start = editBones.get(bone.bbone_custom_handle_start.name, None)
        if bone.bbone_custom_handle_end is not None:
            boneCopy.bbone_custom_handle_end = editBones.get(bone.bbone_custom_handle_end.name, None)
        boneCopy.bbone_easein = bone.bbone_easein
        boneCopy.bbone_easeout = bone.bbone_easeout
        boneCopy.bbone_handle_type_end = bone.bbone_handle_type_end
        boneCopy.bbone_handle_type_start = bone.bbone_handle_type_start
        boneCopy.bbone_rollin = bone.bbone_rollin
        boneCopy.bbone_rollout = bone.bbone_rollout
        boneCopy.bbone_scalein = bone.bbone_scalein
        boneCopy.bbone_scaleout = bone.bbone_scaleout
        boneCopy.bbone_segments = bone.bbone_segments
        boneCopy.bbone_x = bone.bbone_x
        boneCopy.bbone_z = bone.bbone_z
        boneCopy.envelope_distance = bone.envelope_distance
        boneCopy.envelope_weight = bone.envelope_weight
        if offset is None or bone.use_connect:
            boneCopy.head = bone.head
        else:
            boneCopy.head = bone.head - offset
        if offset is None:
            boneCopy.tail = bone.tail
        else:
            boneCopy.tail = bone.tail - offset
            
        boneCopy.head_radius = bone.head_radius
        boneCopy.hide_select = bone.hide_select
        boneCopy.inherit_scale = bone.inherit_scale
        if bpy.app.version[0] <= 3:
            boneCopy.layers = bone.layers
        boneCopy.lock = bone.lock
        if bone.parent is not None:
            boneCopy.parent = editBones.get(bone.parent.name, None)
        
        boneCopy.roll = bone.roll
        boneCopy.select = bone.select
        boneCopy.select_head = bone.select_head
        boneCopy.select_tail = bone.select_tail
        boneCopy.show_wire = bone.show_wire
        boneCopy.tail_radius = bone.tail_radius
        boneCopy.use_connect = bone.use_connect
        boneCopy.use_cyclic_offset = bone.use_cyclic_offset
        boneCopy.use_deform = bone.use_deform
        boneCopy.use_endroll_as_inroll = bone.use_endroll_as_inroll
        boneCopy.use_envelope_multiply = bone.use_envelope_multiply
        boneCopy.use_inherit_rotation = bone.use_inherit_rotation
        boneCopy.use_local_location = bone.use_local_location
        boneCopy.use_relative_parent = bone.use_relative_parent

def Prepare(srcArmName):
    srcArm = bpy.data.objects[srcArmName]
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='EDIT')

    roll = srcArm.data.edit_bones[0].roll 
    
    bpy.ops.object.mode_set(mode='OBJECT')
    srcArm.rotation_euler = (radians(90), 0, -roll)
    srcArm.scale = (1,1,1)

def PrepareMeshes(srcMeshName, meshParentBones, scale = None, meshOffset = None, meshSpecificScale = None, meshSpecificOffset = None):
    srcMesh = bpy.data.objects[srcMeshName]
    bpy.context.view_layer.objects.active = srcMesh
    bpy.ops.object.mode_set(mode='OBJECT')
    
    offset = Vector(srcMesh.location)
    
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        
        if meshSpecificScale is not None and obj.name in meshSpecificScale:
            obj.scale = meshSpecificScale[obj.name]
        elif scale is not None:
            obj.scale = scale
                
        if not obj.parent_bone:
            obj.location -= offset
            if meshSpecificOffset is not None and obj.name in meshSpecificOffset:
                obj.location += meshSpecificOffset[obj.name]
            elif meshOffset is not None:
                obj.location += meshOffset
        else:
            meshParentBones[obj.name] = obj.parent_bone

def PrepareBones(bonesOrder, srcArmName):
    srcArm = bpy.data.objects[srcArmName]
    
    tmpArm = bpy.data.objects.new('TempArmature', bpy.data.armatures.new('TempArmature'))
    bpy.context.scene.collection.objects.link(tmpArm)
    
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.view_layer.objects.active = tmpArm
    bpy.ops.object.mode_set(mode='EDIT')
    
    srcEditBones = srcArm.data.edit_bones
    
    offset = Vector(srcEditBones.get('ROOT').parent.head) if srcEditBones.get('ROOT').parent is not None else None
    
    bones = []
    for key in bonesOrder:
        bones.append(srcEditBones[key])
        
    tmpEditBones = tmpArm.data.edit_bones
    
    for bone in tmpEditBones:
        tmpEditBones.remove(bone)
    CopyEditBones(bones, tmpEditBones, offset)
    
    for bone in srcEditBones:
        srcEditBones.remove(bone)
    
    CopyEditBones(tmpEditBones, srcEditBones)
    
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = tmpArm
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.context.scene.collection.objects.unlink(tmpArm)
    bpy.data.armatures.remove(tmpArm.data)
  
def FinalizeBones(bonesOrder, srcArmName):
    srcArm = bpy.data.objects[srcArmName]
    bones = srcArm.data.bones
    
    meshes = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH': 
            meshes.append(obj)
            
    vertexGroupNames = set()
    for vertexGroups in [ m.vertex_groups for m in meshes ]:
        for vertexGroup in vertexGroups:
            #print(vertexGroup.name)
            vertexGroupNames.add(vertexGroup.name)
        
    pattern = '\A.*IK.*\Z'
    for bone in bones:
        if bone.name not in vertexGroupNames:
            bone.use_deform = False
        if re.search(pattern, bone.name):
            bone.hide = True
        
def FinalizeMeshes(meshParentBones):
    for meshName in meshParentBones:
        bpy.data.objects[meshName].parent_bone = meshParentBones[meshName]

def FinalizePose(srcArmName, applyRestToPose = False):
    srcArm = bpy.data.objects[srcArmName]
    bpy.context.view_layer.objects.active = srcArm
    
    if not applyRestToPose:
        bpy.ops.object.mode_set(mode='POSE')
    
        if bpy.app.version[0] > 4:
            for pbone in srcArm.pose.bones:
                pbone.select = True
        else:
            for pbone in srcArm.pose.bones:
                pbone.bone.select = True
    
        bpy.ops.pose.rot_clear()
        bpy.ops.pose.scale_clear()
        bpy.ops.pose.transforms_clear()
    
        bpy.ops.object.mode_set(mode='OBJECT')
        return
    
    storedModifiersInfo = {}
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        if 'Armature' not in [m.name for m in obj.modifiers ]:
            continue
        
        modifier = obj.modifiers['Armature']
        
        storedModifiersInfo[obj.name] = modifier.object
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier='Armature')
    
    bpy.context.view_layer.objects.active = srcArm
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        if obj.name not in storedModifiersInfo:
            continue
        
        modifier = obj.modifiers.new('Armature', 'ARMATURE')
        modifier.object = storedModifiersInfo[obj.name]
        modifier.use_vertex_groups = True

def Finalize(srcArmName, targetArmName):
    srcArm = bpy.data.objects[srcArmName]
    srcArm.name = targetArmName
    srcArm.data.name = targetArmName
    for obj in bpy.data.objects:
        bpy.ops.object.transform_apply(location = True, scale = False, rotation = True)

meshParentBones = {}
RemoveExcessiveMeshes(excessiveMeshes)
Prepare(srcArmName)
PrepareMeshes(srcMeshName, meshParentBones, meshesScale, meshOffset, meshSpecificScale, meshSpecificOffset)
PrepareBones(bonesOrder, srcArmName)
FinalizeBones(bonesOrder, srcArmName)
FinalizeMeshes(meshParentBones)
FinalizePose(srcArmName, applyRestToPose)
Finalize(srcArmName, targetArmName)
if generateVisualisationScripts:
    ApplyVisualFixes(targetArmName)