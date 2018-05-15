import eyepwm
import time


x = eyepwm.eyepwm(0,0)

y = eyepwm.eyepwm(0,0, 2, 3)

y.recentre_angle()

#x.vert_test()
#x.horiz_test()

#x.vert_angle_test()
#x.horiz_angle_test()

#x.vert_test_increasing_steps()

step_angle = 1
sleep = 0.01
repititions = 3
num_steps = 60
num_diag_steps = 40



while(True):
    x.recentre_angle()

    print("Horizontal")
    for i in range(0 , repititions):
        x.multistep_horiz(num_steps, step_angle, sleep)
        x.multistep_horiz(num_steps, -step_angle, sleep)
        time.sleep(1)
        x.multistep_horiz(num_steps, -step_angle, sleep)
        x.multistep_horiz(num_steps, step_angle, sleep)
        time.sleep(1)
        
    for i in range(0 , repititions):
        y.multistep_horiz(num_steps, step_angle, sleep)
        y.multistep_horiz(num_steps, -step_angle, sleep)
        time.sleep(1)
        y.multistep_horiz(num_steps, -step_angle, sleep)
        y.multistep_horiz(num_steps, step_angle, sleep)
        time.sleep(1)
       
    print("Vertical") 
    for i in range(0 , repititions):
        x.multistep_vert(num_steps, step_angle, sleep)
        x.multistep_vert(2*num_steps, -step_angle, sleep)
        x.multistep_vert(num_steps, step_angle, sleep)
        
    print("Diagonal Pos")
    for i in range(0 , repititions):
        x.multistep_both(num_diag_steps, step_angle, step_angle, sleep)
        x.multistep_both(2*num_diag_steps, -step_angle, -step_angle, sleep)
        x.multistep_both(num_diag_steps, step_angle, step_angle, sleep)
        
    print("Diagonal Neg")
    for i in range(0 , repititions):
        x.multistep_both(num_diag_steps, step_angle, -step_angle, sleep)
        x.multistep_both(2*num_diag_steps, -step_angle, step_angle, sleep)
        x.multistep_both(num_diag_steps, step_angle, -step_angle, sleep)



