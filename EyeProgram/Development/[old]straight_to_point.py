def calculate_small_step_size(self, stepSize, bigDistance, smallDistance):
        """This function calculates a stepsize for the smaller distance to be travelled"""
        wlogger.log_info("calculating small step size")
        
        if (bigDistance != 0):
            smallStepSize = (abs(smallDistance) * stepSize)/abs(bigDistance)
        else:
            smallStepSize = 0
            
        print(smallStepSize)
        
        if (smallDistance < 0 and bigDistance < 0):
            return -smallStepSize
        else:
            return smallStepSize
    
    def calculate_individual_eye(self, XChange, YChange, stepSize):
                
        if (abs(YChange) == abs(XChange)):
            YStepSize = stepSize
            XStepSize = stepSize
            
        elif (abs(YChange) > abs(XChange)):
            XStepSize = self.calculate_small_step_size(stepSize, YChange, XChange)
            YStepSize = stepSize
        
        elif (abs(XChange) > abs(YChange)):
            YStepSize = self.calculate_small_step_size(stepSize, XChange, YChange)
            XStepSize = stepSize
            
        message = ("Y: " + str(YStepSize)+ " X: " + str(XStepSize))
        wlogger.log_info(message)
        print(message)
        return YStepSize, XStepSize
    
    def straight_to_point(self, stepSize, X, Y):
        """ This function moves each eye to the given point in a straight line"""
        wlogger.log_info("Performing Straight To Point movement")
        debug = True
                
        #calculate distance from given point of Left Eye
        leftVertChange = Y - self.LeftEye.eye_vert_angle
        leftHorizChange = X - self.LeftEye.eye_horiz_angle
        leftDistance = math.sqrt((leftVertChange**2)+(leftHorizChange**2))
        
        #calculate distance from given point of Right Eye
        rightVertChange = Y - self.RightEye.eye_vert_angle
        rightHorizChange = X - self.RightEye.eye_horiz_angle
        rightDistance = math.sqrt((rightVertChange**2)+(rightHorizChange**2))
        
        #Determine large distance,and calculate smaller step size accordingly
        if(leftDistance > rightDistance):
            if (abs(leftVertChange) > abs(leftHorizChange)):
                steps = math.floor(leftVertChange/stepSize)
            else:
                steps = math.floor(leftHorizChange/stepSize)
                
            rightStepSize = self.calculate_small_step_size(stepSize, leftDistance, rightDistance)
            leftStepSize = stepSize
            wlogger.log_info("Left is moving further")
            
        elif(rightDistance > leftDistance):
            if (abs(rightVertChange) > abs(rightHorizChange)):
                steps = math.floor(rightVertChange/stepSize)
            else:
                steps = math.floor(rightHorizChange/stepSize)
                
            leftStepSize = self.calculate_small_step_size(stepSize, rightDistance, leftDistance)
            rightStepSize = stepSize
            wlogger.log_info("Right is moving further")
        
        else:
            if (abs(leftVertChange) > abs(leftHorizChange)):
                steps = math.floor(leftVertChange/stepSize)
            else:
                steps = math.floor(leftHorizChange/stepSize)
            
            leftStepSize = stepSize
            rightStepSize = stepSize
            wlogger.log_info("Eyes moving same distance")
            if(debug):
                print("Eyes moving same distance")
                print(str(steps) + " number of steps")
        
        #determine which axis has a large distance for each eye, and calculate step sizes accordingly
        leftVertStepSize, leftHorizStepSize = self.calculate_individual_eye(leftHorizChange, leftVertChange, leftStepSize)
        rightVertStepSize, rightHorizStepSize = self.calculate_individual_eye(rightHorizChange, rightVertChange, rightStepSize)
        
        if (leftVertChange < 0):
            leftVertStepSize = -leftVertStepSize
        
        if (leftHorizChange < 0):
            leftHorizStepSize = -leftHorizStepSize
            
        if (rightVertChange < 0):
            rightVertStepSize = -rightVertStepSize
            
        if (rightHorizChange < 0):
            rightHorizStepSize = -rightHorizStepSize
        
        # take required number of steps to get as close to the area as possible    
        for i in range(abs(steps)):
            if(debug):
                print("Step " + str(i+1))
            message = "step " + str(i+1) + " of " + str(steps)
            wlogger.log_info(message)
            self.LeftEye.step_vert_angle(leftVertStepSize)
            self.LeftEye.step_horiz_angle(leftHorizStepSize)
            self.RightEye.step_vert_angle(rightVertStepSize)
            self.RightEye.step_horiz_angle(rightHorizStepSize)
        
        if (debug):
            print("LH:" +str(self.LeftEye.eye_horiz_angle))
            print("LV:" +str(self.LeftEye.eye_vert_angle))
            print("RH:" +str(self.RightEye.eye_horiz_angle))
            print("RV:" +str(self.RightEye.eye_vert_angle)) 