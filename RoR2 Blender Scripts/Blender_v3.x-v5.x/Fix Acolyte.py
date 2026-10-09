#Original Creator: KingEnderBrine
#Modified by: RuneFox237, Miyowi, acanthi
#Version 1.0.0

import bpy
import re
from math import radians
from mathutils import Vector


bonesOrder = ['ROOT','root_av','spine_av_M_cog_jnt','spine_av_M_01_jnt','spine_av_M_02_jnt','spine_av_M_03_jnt','clavicle_av_L_00_jnt','sh_spikes_root_L_00_jnt','sh_spike2_L_00_jnt','sh_spike4_L_00_jnt','arm_av_L_shldr_jnt','arm_av_L_elbow_jnt','arm_av_L_wrist_jnt','finger_ring_av_L_00_jnt','finger_ring_av_L_01_jnt','finger_ring_av_L_02_jnt','finger_middle_av_L_00_jnt','finger_middle_av_L_01_jnt','finger_middle_av_L_02_jnt','finger_thumb_av_L_00_jnt','finger_thumb_av_L_01_jnt','finger_thumb_av_L_02_jnt','finger_thumb_av_L_03_jnt','finger_pointer_av_L_00_jnt','finger_pointer_av_L_01_jnt','finger_pointer_av_L_02_jnt','arm_av_L_lwrTwist00_jnt','arm_av_L_lwrTwist01_jnt','arm_av_L_lwrTwist02_jnt','arm_av_L_uprTwist00_jnt','arm_av_L_uprTwist01_jnt','arm_av_L_uprTwist02_jnt','clavicle_av_R_00_jnt','sh_spikes_root_R_00_jnt','sh_spike4_R_00_jnt','sh_spike2_R_00_jnt','arm_av_R_shldr_jnt','arm_av_R_elbow_jnt','arm_av_R_wrist_jnt','finger_ring_av_R_00_jnt','finger_ring_av_R_01_jnt','finger_ring_av_R_02_jnt','finger_pointer_av_R_00_jnt','finger_pointer_av_R_01_jnt','finger_pointer_av_R_02_jnt','finger_middle_av_R_00_jnt','finger_middle_av_R_01_jnt','finger_middle_av_R_02_jnt','weapon_gimbal_av_R_00_jnt','weapon_av_R_00_jnt','weapon_staff_av_R_00_jnt','weapon_staff_av_R_01_jnt','weapon_staff_av_R_02_jnt','weapon_staff_av_R_03_jnt','weapon_staff_av_R_04_jnt','weapon_staff_av_R_05_jnt','finger_thumb_av_R_00_jnt','finger_thumb_av_R_01_jnt','finger_thumb_av_R_02_jnt','finger_thumb_av_R_03_jnt','arm_av_R_lwrTwist00_jnt','arm_av_R_lwrTwist01_jnt','arm_av_R_lwrTwist02_jnt','arm_av_R_uprTwist00_jnt','arm_av_R_uprTwist01_jnt','arm_av_R_uprTwist02_jnt','base','pelvis','thighR','calfR','footR','toeR','leg_R_lwrTwist','leg_R_lwrTwist01','leg_R_lwrTwist02','leg_R_uprTwist','leg_R_uprTwist01','leg_R_uprTwist02','tail_M','tail_M_01','tail_M_02','tail_M_03','tail_M_04','tail_M_05','thighL','calfL','footL','toeL','leg_L_lwrTwist','leg_L_lwrTwist01','leg_L_lwrTwist02','leg_L_uprTwist','leg_L_uprTwist01','leg_L_uprTwist02','stomach','spine','chest','clavicleL','upper_armL','lower_armL','handL','finger_middle_L','finger_middle_L_01','finger_middle_L_02','finger_middle_L_03','finger_pointer_L','finger_pointer_L_01','finger_pointer_L_02','finger_pointer_L_03','finger_ring_L','finger_ring_L_01','finger_ring_L_02','finger_ring_L_03','finger_thumb_L','finger_thumb_L_01','finger_thumb_L_02','spear_M_00','weapon_top_M','weapon_top_M_01','weapon_top_M_02','weapon_top_M_03','weapon_top_M_04','weapon_top_M_05','weapon_top_M_06','weapon_top_M_07','weapon_top_M_08','weapon_top_M_09','weapon_bot_M','weapon_bot_M_01','weapon_bot_M_02','weapon_bot_M_03','weapon_bot_M_04','weapon_bot_M_05','weapon_bot_M_06','weapon_bot_M_07','arm_L_lwrTwist','arm_L_lwrTwist01','arm_L_lwrTwist02','arm_L_uprTwist','arm_L_uprTwist01','arm_L_uprTwist02','necklace_M','necklace_M_01','necklace_M_02','necklace_M_03','clavicleR','upper_armR','lower_armR','handR','finger_thumb_R','finger_thumb_R_01','finger_thumb_R_02','finger_middle_R','finger_middle_R_01','finger_middle_R_02','finger_middle_R_03','finger_ring_R','finger_ring_R_01','finger_ring_R_02','finger_ring_R_03','finger_pointer_R','finger_pointer_R_01','finger_pointer_R_02','finger_pointer_R_03','arm_R_lwrTwist','arm_R_lwrTwist01','arm_R_lwrTwist02','arm_R_uprTwist','arm_R_uprTwist01','arm_R_uprTwist02','chestrope_M','chestrope_M_01','chestrope_M_02','chestrope_M_03','neck','head','hair_R','hair_R_01','hair_R_02','hair_R_03','hair_L','hair_L_01','hair_L_02','hair_L_03','ponytail_M','ponytail_M_01','ponytail_M_02','ponytail_M_03','ponytail_M_04','ponytail_M_05']


srcArmName = 'Armature'
srcMeshName = 'acolyte_geo'

meshOffset = None # Vector((1, 1, 1))
meshSpecificOffset = None # {'TestMesh'=Vector((1, 1, 1))}

meshesScale = None # (1, 1, 1)
meshSpecificScale = None # {'TesMesh'=(1, 1, 1)}

excessiveMeshes = [] # ['TestMesh']

applyRestToPose = False


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
            print(vertexGroup.name)
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

def Finalize():
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
Finalize()