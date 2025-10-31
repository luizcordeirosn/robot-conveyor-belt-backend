from http import HTTPStatus


def test_put_start_conveyor_belt_success(client, conveyor_belt_route_mock):
    """
    Tests the PUT /conveyor-belt/start endpoint when the service returns True.
    """
    conveyor_belt_route_mock.start_conveyor_belt.return_value = True

    response = client.put("/conveyor-belt/start")

    assert response.status_code == HTTPStatus.OK
    assert response.json() is True


def test_put_start_conveyor_belt_already_running(client, conveyor_belt_route_mock):
    """
    Tests the PUT /conveyor-belt/start endpoint when the service indicates it is already running.
    """
    conveyor_belt_route_mock.start_conveyor_belt.return_value = False

    response = client.put("/conveyor-belt/start")

    assert response.status_code == HTTPStatus.OK
    assert response.json() is False


def test_put_stop_conveyor_belt_success(client, conveyor_belt_route_mock):
    """
    Tests the PUT /conveyor-belt/stop endpoint when the service successfully stops the conveyor.
    """
    conveyor_belt_route_mock.stop_conveyor_belt.return_value = True

    response = client.put("/conveyor-belt/stop")

    assert response.status_code == HTTPStatus.OK
    assert response.json() is True


def test_put_stop_conveyor_belt_failure(client, conveyor_belt_route_mock):
    """
    Tests the PUT /conveyor-belt/stop endpoint when the service fails to stop the conveyor.
    """
    conveyor_belt_route_mock.stop_conveyor_belt.return_value = False

    response = client.put("/conveyor-belt/stop")

    assert response.status_code == HTTPStatus.OK
    assert response.json() is False
