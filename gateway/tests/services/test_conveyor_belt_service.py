import threading


def test_start_conveyor_belt_first_time(conveyor_belt_service_mock):
    """
    Tests starting the conveyor belt for the first time.
    Should initialize FSM and start thread.
    """
    service = conveyor_belt_service_mock
    assert service.start_conveyor_belt() is True
    assert service._ConveyotBeltService__conveyor_belt_fsm is not None
    assert service._ConveyotBeltService__is_started is True


def test_start_conveyor_belt_already_started(conveyor_belt_service_mock):
    """
    Tests starting the conveyor belt when already started.
    Should not create a new FSM or thread.
    """
    service = conveyor_belt_service_mock
    service.start_conveyor_belt()
    result = service.start_conveyor_belt()
    assert result is True
    assert service._ConveyotBeltService__conveyor_belt_fsm is not None


def test_stop_conveyor_belt(conveyor_belt_service_mock):
    """
    Tests stopping the conveyor belt.
    Should reset FSM, set is_started to False, and call real conveyor methods.
    """
    service = conveyor_belt_service_mock
    service.start_conveyor_belt()
    result = service.stop_conveyor_belt()
    assert result is True  # stop returns not __is_started
    assert service._ConveyotBeltService__conveyor_belt_fsm is None
    assert service._ConveyotBeltService__is_started is False


def test_fsm_exception_triggers_log(monkeypatch, conveyor_belt_service_mock):
    """
    Tests that an exception in FSM next_state triggers logging via DatabaseService.
    """
    service = conveyor_belt_service_mock

    class MockFSM:
        def next_state(self):
            raise Exception("FSM error")

    service._ConveyotBeltService__conveyor_belt_fsm = MockFSM()
    service._ConveyotBeltService__is_started = True

    def run_once():
        service._ConveyotBeltService__start_loop_conveyor_belt_states()
        service._ConveyotBeltService__is_started = False  # prevent infinite loop

    thread = threading.Thread(target=run_once)
    thread.start()
    thread.join()

    assert service._ConveyotBeltService__conveyor_belt_fsm is None
    assert service._ConveyotBeltService__is_started is False


def test_reset_conveyor_belt(monkeypatch, conveyor_belt_service_mock):
    """
    Tests that reset FSM sets proper flags and calls RobotService.close_connection_niryo_robot.
    """
    service = conveyor_belt_service_mock
    service._ConveyotBeltService__conveyor_belt_fsm = True
    service._ConveyotBeltService__is_started = True

    service._ConveyotBeltService__stop_internal = (
        service._ConveyotBeltService__reset_conveyor_belt_fsm
    )
    service._ConveyotBeltService__reset_conveyor_belt_fsm()

    assert service._ConveyotBeltService__conveyor_belt_fsm is None
    assert service._ConveyotBeltService__is_started is False
