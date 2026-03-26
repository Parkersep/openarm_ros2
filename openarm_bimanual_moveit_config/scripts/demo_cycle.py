#!/usr/bin/env python3
from moveit_configs_utils import MoveItConfigsBuilder
from moveit.planning import MoveItPy
from moveit.planning import PlanningComponent
import rclpy
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("demo_cycle")


ROBOT_CONFIG = (
    MoveItConfigsBuilder(robot_name="openarm", package_name="openarm_bimanual_moveit_config")
    .robot_description_semantic(
        file_path="config/openarm_bimanual.srdf",
    )
    .to_dict()
)

ROBOT_CONFIG = {
    **ROBOT_CONFIG,
    "planning_scene_monitor": {
        "name": "planning_scene_monitor",
        "robot_description": "robot_description",
        "joint_state_topic": "/joint_states",
        "attached_collision_object_topic": "/moveit_cpp/planning_scene_monitor",
        "publish_planning_scene_topic": "/moveit_cpp/publish_planning_scene",
        "monitored_planning_scene_topic": "/moveit_cpp/monitored_planning_scene",
        "wait_for_initial_state_timeout": 10.0,
    },
    "planning_pipelines": {"pipeline_names": ["ompl"]},
    "plan_request_params": {
        "planning_attempts": 1,
        "planning_pipeline": "ompl",
        "max_velocity_scaling_factor": 1.0,
        "max_acceleration_scaling_factor": 1.0,
    },
    "ompl": {
        "planning_plugins": ["ompl_interface/OMPLPlanner"],
        "request_adapters": [
            "default_planning_request_adapters/ResolveConstraintFrames",
            "default_planning_request_adapters/ValidateWorkspaceBounds",
            "default_planning_request_adapters/CheckStartStateBounds",
            "default_planning_request_adapters/CheckStartStateCollision",
        ],
        "response_adapters": [
            "default_planning_response_adapters/AddTimeOptimalParameterization",
            "default_planning_response_adapters/ValidateSolution",
            "default_planning_response_adapters/DisplayMotionPath",
        ],
        "start_state_max_bounds_error": 0.5,
    },
    "trajectory_execution": {
        "allowed_execution_duration_scaling": 4.0,
        "allowed_goal_duration_margin": 2.0,
    },
}
def plan_and_execute_group(robot, moves):
    """Plan and execute multiple moves simultaneously.

    moves: list of (planner, goal_name) tuples that should run at the same time.
    """
    trajectories = []
    for planner, goal_name in moves:
        planner.set_start_state_to_current_state()
        planner.set_goal_state(configuration_name=goal_name)
        plan_result = planner.plan()
        if plan_result:
            logger.info(f"  Planned -> {goal_name}")
            trajectories.append(plan_result.trajectory)
        else:
            logger.warning(f"  Failed to plan -> {goal_name}")

    # Execute all trajectories (each goes to a different controller, so they run in parallel)
    for traj in trajectories:
        robot.execute(traj, controllers=[])


def main(args=None):
    rclpy.init(args=args)
    robot = MoveItPy(node_name="moveit_py", config_dict=ROBOT_CONFIG)

    left_arm = robot.get_planning_component("left_arm")
    right_arm = robot.get_planning_component("right_arm")
    left_gripper = robot.get_planning_component("left_gripper")
    right_gripper = robot.get_planning_component("right_gripper")

    # Each step is a list of simultaneous moves, followed by a wait time
    SEQUENCE = [
        # Both arms wave left + grippers open
        ([(left_arm, "wave_left"), (right_arm, "wave_left"),
          (left_gripper, "open"), (right_gripper, "open")], 3.0),
        # Both arms wave right + grippers close
        ([(left_arm, "wave_right"), (right_arm, "wave_right"),
          (left_gripper, "closed"), (right_gripper, "closed")], 3.0),
        # Both arms wave left + grippers open
        ([(left_arm, "wave_left"), (right_arm, "wave_left"),
          (left_gripper, "open"), (right_gripper, "open")], 3.0),
        # Both arms wave right + grippers close
        ([(left_arm, "wave_right"), (right_arm, "wave_right"),
          (left_gripper, "closed"), (right_gripper, "closed")], 3.0),
        # Return home
        ([(left_arm, "home"), (right_arm, "home"),
          (left_gripper, "open"), (right_gripper, "open")], 3.0),
    ]

    NUM_CYCLES = 10
    for cycle in range(NUM_CYCLES):
        logger.info(f"=== Cycle {cycle + 1}/{NUM_CYCLES} ===")
        for moves, pause in SEQUENCE:
            plan_and_execute_group(robot, moves)
            time.sleep(pause)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
