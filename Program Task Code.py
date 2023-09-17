def pickup(x_coordinate,y_coordinate,z_coordinate, boxID):
    arm.move_arm(x_coordinate, y_coordinate, z_coordinate)
    time.sleep(1.5)
    if boxID == 1 or boxID == 2 or boxID == 3:
        arm.control_gripper(35)
    elif boxID == 4 or boxID == 5 or boxID == 6:
        arm.control_gripper(25)
    time.sleep(1.5)
    arm.move_arm(0.406, 0.0, 0.483)
    #predetermined xyz pickup location is (0.588, 0.093, 0.017)
