import maya.cmds as cmds
import sys

def fkIkSnapping():
    """
    Function for doing an FK/IK or IK/FK Snapping
    
    :return: None
    """
    #Grab the current selection that has the attribute
    swapCtrl = cmds.ls(sl=True)[0]
    
    if swapCtrl:       
        if cmds.attributeQuery("IK_FK_Switching", node=swapCtrl, exists=True):
            #Grab data
            getCurrentState = cmds.getAttr(swapCtrl+".IK_FK_Switching")
            
            #Add Namespace if needed
            findNameSpace   = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)[0]
            
            if findNameSpace in swapCtrl:
                addName = findNameSpace+":"
            else:
                addName = ""
            
            #Swap from IK to FK
            if getCurrentState == 0:
                #Grab all IK Rotations
                getIKJnts  = cmds.getAttr(swapCtrl+".IK_Joints").split()
                getFKCtrls = cmds.getAttr(swapCtrl+".FK_Controls").split()
                
                #Loop through the IK joints and apply data
                for num, jnt in enumerate(getIKJnts):
                    #get rotation value
                    getRot = cmds.getAttr(addName+jnt+".rotate")[0]
                    
                    #Set Value to FK controls
                    cmds.setAttr(addName+getFKCtrls[num]+".rotate", getRot[0], getRot[1], getRot[2], type="double3")
                    
                #Now Set it to FK
                cmds.setAttr(swapCtrl+".IK_FK_Switching", 10)
                
            #Swap from FK to IK
            else:
                #Get IK Control
                getIKControl     = cmds.getAttr(swapCtrl+".IK_Control")
                getIKPVControl   = cmds.getAttr(swapCtrl+".PV_Control")
                
                #Get rotation and position from loc space
                getAnkleLoc      = cmds.getAttr(swapCtrl+".Ankle_LOC")
                getPVLOC         = cmds.getAttr(swapCtrl+".Pole_LOC")
                
                cmds.delete(cmds.parentConstraint(addName+getAnkleLoc, addName+getIKControl, w=1, mo=0))
                cmds.delete(cmds.pointConstraint(addName+getPVLOC, addName+getIKPVControl, w=1, mo=0))
                
                #getAnklePosLOC   = cmds.getAttr(addName+getAnkleLoc+".translate")[0]
                #getAnkleRotLOC   = cmds.getAttr(addName+getAnkleLoc+".rotate")[0]
                
                #getPVPosLOC      = cmds.getAttr(addName+getPVLOC+".translate")[0]

                
                #Now set the values to the IK controls
                #cmds.setAttr(addName+getIKControl+".translate", getAnklePosLOC[0], getAnklePosLOC[1], getAnklePosLOC[2], type="double3")
                #cmds.setAttr(addName+getIKControl+".rotate", getAnkleRotLOC[0], getAnkleRotLOC[1], getAnkleRotLOC[2], type="double3")
                
                #cmds.setAttr(addName+getIKPVControl+".translate", getPVPosLOC[0], getPVPosLOC[1], getPVPosLOC[2], type="double3")
                
                #Switch back
                cmds.setAttr(swapCtrl+".IK_FK_Switching", 0)
        
        else:
            sys.stderr.write("Error! Please select the control with the switching attribute")
            
    else:
        sys.stderr.write("Error! Nothing was selected")
