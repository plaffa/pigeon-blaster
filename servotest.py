from pynput.mouse import Listener as MouseListener
from pynput.mouse import Button
from misc import fxy
import cv2
from threading import Thread
import pigpio
import time
import random


class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(1280,720),framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])

        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

	# Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
	# Return the most recent frame
        return self.frame

    def stop(self):
	# Indicate that the camera and thread should be stopped
        self.stopped = True


class BlasterAssembly(object):
    def __init__(self,
                 pan_pin, tilt_pin,
                 pump_pin,
                 imh, imw):
    
        self.video_stream = VideoStream(resolution=(self.imh, self.imw),framerate=10)
        self.gun = Gun(pump_pin)
        self.pan_tilt = PanTilt(pan_pin, tilt_pin, pump_pin)
    
    def start(self):
        self.gun.start()
        self.pan_tilt.start()
    
    def eliminate_target(self, y, x, coordinate_system='image'):
        self.aim_gun_at(y, x, coordinate_system)
        self.fire()
        
    def aim_gun_at(self, y, x, coordinate_system):
        self.pan_tilt.aim_at(y, x, coordinate_system)
        
    def fire(self):
        self.gun.fire()
        

class Gun(object):
    def __init__(self, gun_pin, fire_duration=1):
        
        self.firing = False
        self.fire_duration = fire_duration
        
        self.gun_pin = gun_pin
        self.gun = pigpio.pi()
    
    def start(self):
        Thread(target=self.fire_control, args=()).start()
    
    def fire_control(self):
        while True:
            if self.firing:
                self.gun.write(self.gun_pin, 1)
                time.sleep(self.fire_duration/2)
                self.gun.write(self.gun_pin, 0)
                time.sleep(self.fire_duration/2)
                self.firing = False
        
    def fire(self):
        self.firing = True
                 

class PanTilt(object):
    def __init__(self,
                 pan_pin,
                 tilt_pin,
                 pump_pin,
                 mouse_x_max=1920,
                 mouse_y_max=1200,
                 servo_min=500,
                 servo_max=2500,
                 pwm_frequency=50,
                 image_height=500,
                 image_width=500,
                 ):

        self.servo_min = servo_min
        self.servo_max = servo_max

        self.pump_pin = pump_pin
        self.pump = pigpio.pi()

        self.pan_pin = pan_pin
        self.tilt_pin = tilt_pin
        self.pan = pigpio.pi()
        self.tilt = pigpio.pi()
        self.pan.set_mode(self.pan_pin, pigpio.OUTPUT)
        self.tilt.set_mode(self.tilt_pin, pigpio.OUTPUT)
        self.pan.set_PWM_frequency(self.pan_pin, pwm_frequency)
        self.tilt.set_PWM_frequency(self.tilt_pin, pwm_frequency)

        self.mouse_x_max = mouse_x_max
        self.mouse_y_max = mouse_y_max

        self.imw = image_width
        self.imh = image_height

        # Initialise pan and tilt positions to center
        self.pan_position = (servo_max - servo_min) / 2
        self.tilt_position = (servo_max - servo_min) / 2

        self.calibrated = True
        self.video_stream = VideoStream(resolution=(self.imh, self.imw),framerate=10)
        self.mouse_listener = MouseListener(on_move=self.on_move, on_click=self.on_click)

        self.calibration_markers = [(0, 0), (0, self.imw//2), (0, self.imw),
                                    (self.imh//2, 0), (self.imh//2, self.imw//2), (self.imh//2, self.imw),
                                    (self.imh, 0), (self.imh, self.imw//2), (self.imh, self.imw)]

        self.calibration_points = [(), (), (),
                                   (), (), (),
                                   (), (), ()]

        self.conversion_matrix = None
        self.new_position = False
        
    def start(self):
        Thread(target=self.update_positions, args=()).start()
        return self
    
    def update_positions(self):
        while True:
            if self.new_position:
                self.tilt.set_servo_pulsewidth(self.tilt_pin, self.tilt_position)
                self.pan.set_servo_pulsewidth(self.pan_pin, self.pan_position)
                self.new_position = False            
    
    def aim_at(self, y, x, coordinate_system='image'):
        if coordinate_system == 'image':
            self.tilt_position = self.conversion_matrix[0, y, x]
            self.pan_position = self.conversion_matrix[1, y, x]
        else:
            self.tilt_position = y
            self.pan_position = x
            
        self.new_position = True
    

    def calibrate(self):
        self.calibrated = False

        self.video_stream.start()
        self.mouse_listener.start()

        self.cal_point_idx = 0
        while not self.calibrated:

            if cv2.waitKey(1) == ord('q'):
                break

            # Grab frame from video stream
            frame = self.video_stream.read()
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            cal_point_coordinates = (int(self.calibration_markers[self.cal_point_idx][1]),
                                     int(self.calibration_markers[self.cal_point_idx][0]))
            cv2.circle(frame, cal_point_coordinates, 15, (0, 0, 255), 2)
            cv2.imshow('Object detector', frame)

        print('\nCalibration finished!\n')
        self.mouse_listener.stop()
        self.video_stream.stop()
        cv2.destroyAllWindows()

        print('The following points are calibrated:')
        for cal_point in self.calibration_points:
            print(cal_point)

        self.conversion_matrix = fxy(self.calibration_points, self.imh, self.imw)

    def on_move(self, x, y):
        self.tilt_position = int(self.servo_min + ((y)/self.mouse_y_max) * (self.servo_max-self.servo_min))
        self.pan_position = int(self.servo_min + ((self.mouse_x_max-x)/self.mouse_x_max) * (self.servo_max-self.servo_min))
        self.tilt.set_servo_pulsewidth(self.tilt_pin, self.tilt_position)
        self.pan.set_servo_pulsewidth(self.pan_pin, self.pan_position)

    def on_click(self, x, y, button, pressed):
        if pressed:
            print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
            if button == Button.left:
                self.pump.write(self.pump_pin, 1)

            elif button == Button.right:
                self.calibrated = True

        else:
            if button == Button.left:
                print(f'Saving calibration idx [{self.cal_point_idx}] to ({self.pan_position, self.tilt_position})')
                self.pump.write(self.pump_pin, 0)

                self.calibration_points[self.cal_point_idx] = (self.tilt_position, self.pan_position)

                if self.cal_point_idx < len(self.calibration_points)-1:
                    self.cal_point_idx += 1
                else:
                    self.calibrated = True


servo_tilt_pin = 13
servo_pan_pin = 12
pump_pin = 16

try:
    pan_tilt = PanTilt(servo_pan_pin, servo_tilt_pin, pump_pin)
    pan_tilt.calibrate()
    
    pan_tilt.video_stream.start()
    pan_tilt.start()
    
    markers = (random.randint(0, pan_tilt.imw-1), random.randint(0, pan_tilt.imh-1))
    t = time.time()
    gun = Gun(pump_pin)
    gun.start()
    
    while(True):
        
        frame = pan_tilt.video_stream.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.circle(frame, markers, 15, (0, 0, 255), 2)
        cv2.imshow('Object detector', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
        
        if not gun.firing:
            markers = (random.randint(0, pan_tilt.imw-1), random.randint(0, pan_tilt.imh-1))
            pan_tilt.aim_at(markers[1], markers[0], coordinate_system='image')
            gun.fire()

            

            
        
    

except KeyboardInterrupt:
    servo_y.set_PWM_dutycycle(servo_tilt_pin, 0)
    servo_y.set_PWM_frequency(servo_tilt_pin, 0)
    servo_x.set_PWM_dutycycle(servo_pan_pin, 0)
    servo_x.set_PWM_frequency(servo_pan_pin, 0)
