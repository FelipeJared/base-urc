import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('teleop')

        self.speed_setting = 2 # default to medium speed

        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.on_joy,
            10)
        
        self.publisher_ = self.create_publisher(Twist, 'teleop/cmd_vel', 1)
        self.servo_pan_speed = 5
        self.servo_pan_max = 160
        self.servo_pan_min = 0
        self.servo_position = self.servo_pan_max/2
        # self.publisher_ = self.create_publisher(String, 'topic', 10)
        # timer_period = 0.5  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

    def on_joy(self, data):
        # Set speed ratio using d-pad
        if data.axes[7] == 1: # full speed (d-pad up)
            self.speed_setting = 1
        if data.axes[6] != 0: # medium speed (d-pad left or right)
            self.speed_setting = 2
        if data.axes[7] == -1: # low speed (d-pad down)
            self.speed_setting = 3

        # Drive sticks
        left_speed = -data.axes[1] / self.speed_setting # left stick
        right_speed = -data.axes[4] / self.speed_setting # right stick

        # Convert skid steering speeds to twist speeds
        linear_vel  = (left_speed + right_speed) / 2.0 # (m/s)
        angular_vel  = (right_speed - left_speed) / 2.0 # (rad/s)

        # Publish Twist
        twist = Twist()
        twist.linear.x = linear_vel
        twist.angular.z = angular_vel
        self.publisher_.publish(twist)

        # Camera servo panning control
        if data.buttons[5]: # pan rightward (right bumper)
            if self.servo_position > self.servo_pan_min:
                self.servo_position -= self.servo_pan_speed
        if data.buttons[4]: # pan leftward (left bumper)
            if self.servo_position < self.servo_pan_max:
                self.servo_position += self.servo_pan_speed
        if data.buttons[3]: # center servo position (Y button)
            self.servo_position = self.servo_pan_max/2
        #self.servo_pub.publish(self.servo_position)

        # Cancel move base goal
        if data.buttons[2]: # X button
            self.get_logger().info('Stopping Movement')
            # rospy.loginfo('Cancelling move_base goal')
            # cancel_msg = GoalID()
            # self.goal_cancel_pub.publish(cancel_msg)

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()