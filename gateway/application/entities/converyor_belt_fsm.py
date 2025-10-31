from transitions import State
from transitions.extensions import GraphMachine


class ConveryorBeltFSM(GraphMachine):
    def __init__(self, model) -> None:
        """Constructor of the base `ConveryorBelt` class."""
        idle = State(
            name="idle",
        )
        detecting_object = State(
            name="detecting_object",
            on_enter=["camera_detects_object"],
        )
        grabbing_object = State(
            name="grabbing_object",
            on_enter=["activate_gripper"],
        )
        pre_moving_to_drop = State(
            name="pre_moving_to_drop",
            on_enter=["go_to_pre_drop_position"],
        )
        pre_moving_to_grasp = State(
            name="pre_moving_to_grasp",
            on_enter=["move_robot_to_pre_grasp_position"],
        )
        catching_object = State(
            name="catching_object",
        )
        moving_to_grasp = State(
            name="moving_to_grasp",
            on_enter=["move_robot_to_grasp_position"],
        )
        moving_to_drop = State(
            name="moving_to_drop",
            on_enter=["go_to_drop_position"],
        )
        droping_object = State(
            name="droping_object",
            on_enter=["deactivate_gripper"],
        )
        moving_to_safe_position = State(
            name="moving_to_safe_position",
            on_enter=["go_to_safe_position"],
            on_exit=["save_log"],
        )
        selecting_situation_gripper = State(
            name="selecting_situation_gripper",
            on_enter=["select_situation_gripper"],
        )
        orient_gripper_downward = State(
            name="orient_gripper_downward",
            on_enter=["orient_gripper_downward"],
        )

        states = [
            idle,
            detecting_object,
            grabbing_object,
            pre_moving_to_drop,
            pre_moving_to_grasp,
            catching_object,
            moving_to_grasp,
            moving_to_drop,
            droping_object,
            moving_to_safe_position,
            selecting_situation_gripper,
            orient_gripper_downward,
        ]

        transitions = [
            {
                "trigger": "orient_gripper_downward_to_pre_moving_to_grasp",
                "source": "orient_gripper_downward",
                "dest": "pre_moving_to_grasp",
            },
            {
                "trigger": "selecting_situation_gripper_to_orient_gripper_downward",
                "source": "selecting_situation_gripper",
                "dest": "orient_gripper_downward",
            },
            {
                "trigger": "moving_to_safe_position_to_catching_object",
                "source": "moving_to_safe_position",
                "dest": "catching_object",
                "after": ["reset_state_machine"],
            },
            {
                "trigger": "droping_object_to_moving_to_safe_position",
                "source": "droping_object",
                "dest": "moving_to_safe_position",
            },
            {
                "trigger": "moving_to_drop_to_droping_object",
                "source": "moving_to_drop",
                "dest": "droping_object",
            },
            {
                "trigger": "moving_to_grasp_to_grabbing_object",
                "source": "moving_to_grasp",
                "dest": "grabbing_object",
            },
            {
                "trigger": "idle_to_catching_object",
                "source": "idle",
                "dest": "catching_object",
                "after": ["start_conveyor_belt"],
            },
            {
                "trigger": "pre_moving_to_drop_to_moving_to_drop",
                "source": "pre_moving_to_drop",
                "dest": "moving_to_drop",
            },
            {
                "trigger": "grabbing_object_to_pre_moving_to_drop",
                "source": "grabbing_object",
                "dest": "pre_moving_to_drop",
            },
            {
                "trigger": "pre_moving_to_grasp_to_moving_to_grasp",
                "source": "pre_moving_to_grasp",
                "dest": "moving_to_grasp",
            },
            {
                "trigger": "detecting_object_to_selecting_situation_gripper",
                "source": "detecting_object",
                "dest": "selecting_situation_gripper",
            },
            {
                "trigger": "catching_object_to_detecting_object",
                "source": "catching_object",
                "dest": "detecting_object",
                "conditions": ["camera_detected_object"],
                "before": ["stop_conveyor_belt"],
            },
            {
                "trigger": "catching_object_to_catching_object",
                "source": "catching_object",
                "dest": "catching_object",
                "unless": ["camera_detected_object"],
            },
        ]

        super().__init__(
            model=model,
            states=states,
            transitions=transitions,
            initial=idle,
        )

    def __getattr__(self, item):
        """Method to get unlisted attributes of the class. If the attribute
        is not found, the method will return the class attribute.

        Args:
            item: The class attribute that should be retrieved.

        Returns:
            The class attribute.
        """
        return self.model.__getattribute__(item)

    def next_state(self):
        """Method for automatic execution of available transitions in each
        of the machine states.
        """
        available_transitions = self.get_triggers(self.state)
        available_transitions = available_transitions[len(self.states) :]

        for curr_transition in available_transitions:
            may_method_result = self.may_trigger(curr_transition)
            if may_method_result:
                self.trigger(curr_transition)
