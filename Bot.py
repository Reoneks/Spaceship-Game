import pyautogui
#_________________________________________________________
def MoveShip(XShipCoord,XMeteorCoord,ButtonPushed):
    if XShipCoord>(XMeteorCoord+10) and ButtonPushed==0:
        pyautogui.keyDown('A')
        pyautogui.keyUp('D')
        ButtonPushed=1
    elif XShipCoord<(XMeteorCoord-10) and ButtonPushed==0:
        pyautogui.keyDown('D')
        pyautogui.keyUp('A')
        ButtonPushed=1
    elif XShipCoord>(XMeteorCoord-10) and XShipCoord<(XMeteorCoord+10) and ButtonPushed==1:
        ButtonPushed=0
        pyautogui.keyUp('A')
        pyautogui.keyUp('D')
    return ButtonPushed
#_________________________________________________________
def StopBot():
    pyautogui.keyUp('A')
    pyautogui.keyUp('D')
#_________________________________________________________
