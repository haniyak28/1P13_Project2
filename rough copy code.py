ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

def Random_spawn (boxID, last_ID):
    while True:
        cage = random.randint(1,6)
        for i in last_ID:
            if cage == last_ID[i]:
                check = "yes"
                break
            else:
                check = "no"
        if check == "yes":
            cage = random.randint(1,6)
        elif check == "no":
            last_ID.append(cage)
            boxID = cage
            arm.spawn_cage(cage)
            break
    return boxID


def pickup(x_coordinate,y_coordinate,z_coordinate, boxID):
    arm.move_arm(x_coordinate, y_coordinate, z_coordinate)
    time.sleep(1.5)
    if boxID <=3:
        arm.control_gripper(35)
    elif boxID >3:
        arm.control_gripper(25)
    time.sleep(1.5)
    arm.move_arm(0.406, 0.0, 0.483)
    #time.sleep(2)
    #arm.rotate_shoulder(10)
    #arm.rotate_elbow(5)

        
def rotate_qarm_base(boxID):
    colour = 0
    if boxID == 1 or boxID == 4:
        colour = "red"
    elif boxID == 2 or boxID == 5:
        colour = "green"
    elif boxID == 3 or boxID == 6:
        colour = "blue"

    old_position = potentiometer.right()
    while arm.check_autoclave(colour) == False:
        new_position = potentiometer.right()
        position_change = new_position - old_position
        difference = (position_change)*100
        arm.rotate_base(3.5*difference)
        time.sleep(.3)
        old_position = new_position
        #print(colour)
        #print(arm.check_autoclave(colour))
                
           	
def transfer(boxID):
    if boxID == 1 or boxID == 2 or boxID == 3:
        arm.rotate_shoulder(10)
        time.sleep(0.1)
        arm.rotate_elbow(5)
    elif boxID == 4 or boxID == 5 or boxID == 6:
        arm.rotate_shoulder(24)

    while arm.effector_position() != correct_final_position:
        if potentiometer.left() > 0.5 and potentiometer.left() < 1:
            if containerID == 1 :
                arm.move_arm(0.0, 0.596, 0.314)
                time.sleep(1)
                arm.control_gripper(-35)
                time.sleep(1)
                arm.control_gripper(-30)
       
            if containerID == 2 :
                arm.move_arm(-0.61, 0.222, 0.295)
                time.sleep(2)
                arm.control_gripper(-30)
            if containerID == 3 :
                arm.move_arm(0.0, -0.61, 0.261)
                time.sleep(2)
                arm.control_gripper(-30)
            elif potentiometer.left() == 1:
                arm.activate_autoclaves()
            if containerID == 4:
                arm.open_autoclave("red")
                time.sleep(1)
                arm.move_arm(0.0, 0.389, 0.194)
                time.sleep(2)
                arm.control_gripper(-30)
                time.sleep(2)
                arm.open_autoclave("red", False)
                time.sleep(2)
                                
            if containerID == 5:
                arm.open_autoclave("green")
                time.sleep(2)
                arm.move_arm(-0.407, 0.148, 0.2)
                time.sleep(2)
                arm.control_gripper(-30)
                time.sleep(2)
                arm.open_autoclave("green", False)
                time.sleep(2)
                                
            if containerID == 6:
                arm.open_autoclave("blue")
                time.sleep(2)
                arm.move_arm(0.0, -0.399, 0.164)
                time.sleep(2)
                arm.control_gripper(-30)
                time.sleep(2)
                arm.open_autoclave("blue", False)
                time.sleep(2)
      
def main ():
    import random
    previous_ID = [0]
    container_ID = 0
    container_ID = Random_spawn(container_ID, previous_ID)
    pickup(0.579,0.051,0.06,container_ID)
    rotate_qarm_base(container_ID)
    #transfer(container_ID)
    #arm.home()









main()
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

