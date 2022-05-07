import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from numpy.linalg import LinAlgError
import utils

class Robot2D(object):

    '''Class representing a 2D robot'''
    def __init__(self, l1, l2, base_pos):
        self.l1 = l1
        self.l2 = l2
        self.base_pos = base_pos
        self.ee_pos = None

    def fwd_kin(self, joint_angles):
        '''Calculates the fwd kinematics of the robot
        Inputs:
        theta1, theta2: degrees'''
        theta1 = joint_angles[0]
        theta2 = joint_angles[1]
        x_ee = self.l1 * math.cos((theta1/180) * math.pi) + math.cos((theta2/180) * math.pi)
        y_ee = self.l1 * math.sin((theta1/180) * math.pi) + math.sin((theta2/180) * math.pi)
        self.ee_pos = (x_ee, y_ee)

    def robot_to_lines(self, joint_angles):
        pass

    def draw_robot(self, figure):
        pass

class RectangleObstacle(Rectangle):
    
    def __init__(self, xy, w, h, angle):
        '''origin specifies the coordinates of the lower left corner in the 2D space'''
        super().init(xy, w, h, angle)
    
    def obstacle_to_lines(self):
        '''finds the separate line equations defining the obstacle'''
        pass


class ConfigSpaceCreator(object):

    def __init__(self, robot, obstacles, figure):
        self.robot = robot
        self.obstacles = obstacles
        self.fig = figure

    def plot_space(self, joint_angles):
        self.fig = plt.figure()
        task_space_plot = self.fig.add_subplot(121)
        config_space_plot = self.fig.add_subplot(122)
        for obs in self.obstacles:
            task_space_plot.add_patch(obs)
        if self.collision_check(joint_angles) == True:
            config_space_plot.plot(joint_angles[0], joint_angles[1], marker='x')


    def collision_check(self, joint_angles):
        for obs in self.obstacles:
            for line in self.robot.robot_to_lines(joint_angles):
                for line in obs.obstacle_to_lines():
                    if utils.find_intersection()[0]:
                        collision = True
                        return collision
        collision = False
        return collision