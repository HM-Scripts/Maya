import maya.cmds as cmds
import maya.mel

def timeSliderCutKey():
    mel('timeSliderCutKey;')

def timeSliderCopyKey():
    mel('timeSliderCopyKey;')

def timeSliderPasteKey():
    mel('timeSliderPasteKey false;')

def timeSliderDeleteKey():
    mel('timeSliderClearKey;')

def mel(mel_command):
    return maya.mel.eval(mel_command)