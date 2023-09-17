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

#this function spawns a random container
def Random_spawn (boxID, last_ID): 
    while True: #loop so that the code keeps running until it picks a container that hasn't been spawned before  
        container = random.randint(1,6) #picks a random number from 1-6 which will be the container ID number
        for i in range (len(last_ID)): #loop that goes through an array of ID's that have already been spawned
            #if the current ID picked matches any of the previous spawned IDs then break loop to pick new ID
            if container == last_ID[i]:
                check = "yes"
                break
            else:
                check = "no"
        if check == "yes":
            #if ID picked matches the previous IDs, it picks a new ID number and runs through while loop to check again
            container = random.randint(1,6)
        elif check == "no":
            #if the current ID picked does not matche any of the previous spawned IDs then it adds the ID to an array of all previously picked IDs
            last_ID.append(container)
            #saves the current ID into a variable to be used for other functions 
            boxID = container
            #spawns the container that correlates to the current ID
            arm.spawn_cage(container)
            break
    return boxID


#this function moves the arm to pick up the container
def pickup(x_coordinate,y_coordinate,z_coordinate, boxID):
    #moves to the coordinates where the container gets spawned 
    arm.move_arm(x_coordinate, y_coordinate, z_coordinate)
    time.sleep(1.5)
    if boxID <=3: #checks if container is small
        arm.control_gripper(35) #gripper closes more if it's a small container
    elif boxID >3: #checks if conatiner is big
        arm.control_gripper(25) #gripper closes a bit less if it's a big container
    time.sleep(1.5)
    arm.move_arm(0.406, 0.0, 0.483) #moves back to home coordinates without dropping the container


#this function rotates the base using the right potentiometer     
def rotate_qarm_base(boxID):
    colour = 0
    #defines which colour the current container is
    if boxID == 1 or boxID == 4:
        colour = "red"
    elif boxID == 2 or boxID == 5:
        colour = "green"
    elif boxID == 3 or boxID == 6:
        colour = "blue"

    old_position = 0.5 #starting position default is 0.5 for potentiometer values
    while arm.check_autoclave(colour) == False: #while loop runs until the arm doesn't reach the range of the autoclave so it keeps reading right potentiometer 
        if potentiometer.right() == 0.5: #arm goes back to home position if right potentiometer is at 50%
            arm.move_arm(0.406, 0.0, 0.483)
        #relating potentiometer values and scaling them for how many degrees the arm moves as the potentiometer increments 
        new_position = potentiometer.right() #reads current right potentiometer value and saves it into variable
        position_change = new_position - old_position #finds the difference of the potentiometer values from where it was before to where it is now as we move it
        percent = (position_change)*100 #takes the difference and turns it into a percent integer
        arm.rotate_base(3.5*percent) #scaling the potentiometer value to the amount of degrees needed to rotate (3.5 degrees) for every 1 percent the potentiometer moves
        time.sleep(.3)
        old_position = new_position #makes the old position the new position
                
#this function transfers the containers into the correct position of the correct autoclave        	
def transfer(boxID):
    colour = 0
    #defines which colour the current container is
    if boxID == 1 or boxID == 4:
        colour = "red"
    elif boxID == 2 or boxID == 5:
        colour = "green"
    elif boxID == 3 or boxID == 6:
        colour = "blue"

    #runs loop that keeps checking the left potentiometer values to transfer the container into right position
    while arm.check_autoclave(colour) == True: #while loop runs as long as the arm is within the range of the correct autoclave
        #checks left potentiometer values and if it is in between 50 and 100 percent and the container is small it goes to the top position of the autoclave and drops the container in
        if potentiometer.left() > 0.5 and potentiometer.left() < 1:
            if boxID == 1 or boxID == 2 or boxID == 3:
                #checks colour and moves it to right top position on autoclave based on its colour
                if colour == "red":
                    arm.move_arm(0.0, 0.596, 0.314)
                elif colour == "green":
                    arm.move_arm(-0.61, 0.222, 0.295)
                elif colour == "blue":
                    arm.move_arm(0.0, -0.61, 0.261)
                
                time.sleep(2)
                arm.control_gripper(-35) #drops the container
                time.sleep(2)
                break #while loop ends (no more need to check left potentiometer values)
        #checks left potentiometer values and if it is at a 100 percent and the container is big, it goes to the bottom drawer of the autoclave and drops the container in
        elif potentiometer.left() == 1:
            if boxID == 4 or boxID == 5 or boxID == 6:
                arm.activate_autoclaves() #activates autoclaves
                #checks colour and moves it to right bottom position on autoclave based on its colour
                if colour == "red":
                    arm.move_arm(0.0, 0.389, 0.194)
                elif colour == "green":
                    arm.move_arm(-0.407, 0.148, 0.2)
                elif colour == "blue":
                    arm.move_arm(0.0, -0.399, 0.164)

                arm.open_autoclave(colour) #opens the drawer of the right autoclave that correlates with the colour of the container
                time.sleep(1)
                arm.control_gripper(-25) #drops container into autoclave
                time.sleep(1)
                arm.open_autoclave(colour, False) #closes the correct autoclave's drawer that correlates with the colour of the container
                time.sleep(1)
                break #while loop ends (no more need to check left potentiometer values)
            
#this is the main function that makes everything run in one cycle 
def main ():
    import random #imported random for the random spawning function
    previous_ID = [0] #inital array that will store all previous spawned containers
    container_ID = 0 #initial variable that will hold the current container ID number
    count = 0 #variable that acts as a counter for when to stop the while loop
    while count < 6: #loop that runs 6 times for all 6 containers
        container_ID = Random_spawn(container_ID, previous_ID) #container ID variable becomes the current container ID and calls the random spawning function which spawns a container
        pickup(0.579,0.051,0.03,container_ID) #calls pick up function to pick up container
        rotate_qarm_base(container_ID) #calls rotate base function to rotate base to correct autoclave
        transfer(container_ID) #calls transfer function to put the container in right part of the container based on size of container
        arm.home() #once transfered, arm goes home
        time.sleep(2)
        count = count + 1 #counter counts one up since one cycle has been completed
    arm.deactivate_autoclaves() #autoclaves deactivated once all containers have been placed



main() #calls the main function which makes everything actually happen
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

    

