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
        x_ee = self.l1 * math.cos(math.radians(theta1)) + self.l2 * math.cos(math.radians(theta1) + math.radians(theta2))
        y_ee = self.l1 * math.sin(math.radians(theta1)) + self.l2 * math.sin(math.radians(theta1) + math.radians(theta2))
        self.ee_pos = (x_ee, y_ee)

    def robot_to_points(self, joint_angles):
        '''Returns the three points that are used to plot the robot'''
        x = []
        y = []
        theta1 = joint_angles[0]
        theta2 = joint_angles[1]
        x.append(self.base_pos[0])
        y.append(self.base_pos[1])

        x.append(self.l1 * math.cos(math.radians(theta1)))
        y.append(self.l1 * math.sin(math.radians(theta1)))

        self.fwd_kin(joint_angles)
        x.append(self.ee_pos[0])
        y.append(self.ee_pos[1])

        return (x, y)

    def draw_robot(self, joint_angles, sub_plot_figure):

        x, y = self.robot_to_points(joint_angles)
        sub_plot_figure.plot(x, y)
                
    def robot_to_lines(self, joint_angles):
        '''finds the separate line equations defining the robot'''
        x, y = self.robot_to_points(joint_angles)
        line1 = utils.get_line_eq(x[0:2], y[0:2])
        line2 = utils.get_line_eq(x[1:3], y[1:3])

        return (line1, line2)

class RectangleObstacle(Rectangle):
    
    def __init__(self, xy, w, h, angle=0):
        '''origin specifies the coordinates of the lower left corner in the 2D space'''
        super().__init__(xy, w, h, angle)
        self.obs_lines = self.obstacle_to_lines()
    
    def obstacle_to_lines(self):
        '''finds the separate line equations defining the obstacle'''
        x, y = self.xy
        line1_v = [1, 0, x]
        line2_v = [1, 0, x+self._width]
        line1_h = [0, 1, y]
        line2_h = [0, 1, y+self._height]

        return (line1_v, line2_v, line1_h, line2_h)

class ConfigSpaceCreator(object):

    def __init__(self, robot, obstacles, figure):
        self.robot = robot
        self.obstacles = obstacles
        self.fig = figure
        self.first_plot = True
        self.task_space_plot = None
        self.config_space_plot = None

    def plot_space(self, joint_angles):

        if self.first_plot:
            # initiailizing the axes    
            self.task_space_plot = self.fig.add_subplot(121)
            self.config_space_plot = self.fig.add_subplot(122)

            # drawing the obstacle
            for obs in self.obstacles:
                self.task_space_plot.add_patch(obs)
            self.first_plot = False
        # drawing the robot
        self.robot.draw_robot(joint_angles, self.task_space_plot)

        # drawing the config space 
        if self.collision_check(joint_angles) == True:
            self.config_space_plot.plot(joint_angles[0], joint_angles[1], marker='x')


    def collision_check(self, joint_angles):
        for obs in self.obstacles:
            for line1 in self.robot.robot_to_lines(joint_angles):
                for line2 in obs.obstacle_to_lines():
                    if utils.find_intersection(line1, line2)[0]:
                        collision = True
                        return collision
        collision = False
        return collision


if __name__ == '__main__':
    
    my_robot = Robot2D(l1=1, l2=1, base_pos=(0, 0))
    rect1 = RectangleObstacle(xy=(-2,1), w=2, h=1)
    rect2 = RectangleObstacle(xy=(2,2), w=2, h=1)
    obstacles = [rect1, rect2]
    figure = plt.figure()

    config_space = ConfigSpaceCreator(my_robot, obstacles, figure)

    for theta1 in range(181):
        print(theta1)
        for theta2 in range(361):
            joint_angles = (theta1, theta2)
            config_space.plot_space(joint_angles)
