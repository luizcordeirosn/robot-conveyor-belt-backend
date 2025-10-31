def test_get_centroid_and_object_label_success(client, camera_service_mock):
    """
    Tests the GET /cameras/label endpoint when the service returns valid data.
    """
    camera_service_mock.get_centroid_and_label_from_capture_frame.return_value = {
        "x": 0.1,
        "y": 0.2,
        "label": 9,
        "class": "semisphere",
        "confidence": 0.95,
    }

    response = client.get("/cameras/label")
    assert response.status_code == 200
    assert response.json() == {
        "x": 0.1,
        "y": 0.2,
        "label": 9,
        "class": "semisphere",
        "confidence": 0.95,
    }


def test_get_centroid_and_object_label_empty_response(client, camera_service_mock):
    """
    Tests the GET /cameras/label endpoint when the service returns an empty dictionary.
    """
    camera_service_mock.get_centroid_and_label_from_capture_frame.return_value = {
        "x": 0,
        "y": 0,
        "label": None,
        "class": None,
        "confidence": None,
    }

    response = client.get("/cameras/label")
    assert response.status_code == 200
    assert response.json() == {
        "x": 0,
        "y": 0,
        "label": None,
        "class": None,
        "confidence": None,
    }


def test_put_release_video_capture_success(client, camera_service_mock):
    """
    Tests the PUT /cameras/release-video endpoint when the service returns True.
    """
    camera_service_mock.release_video_capture_from_camera.return_value = True

    response = client.put("/cameras/release-video")
    assert response.status_code == 200
    assert response.json() is True


def test_put_release_video_capture_failure(client, camera_service_mock):
    """
    Tests the PUT /cameras/release-video endpoint when the service returns False.
    """
    camera_service_mock.release_video_capture_from_camera.return_value = False

    response = client.put("/cameras/release-video")
    assert response.status_code == 200
    assert response.json() is False
