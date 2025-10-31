import pytest


def test_get_camera_prediction_success(
    camera_service_mock, camera_prediction_success_mock
):
    """
    Tests get_centroid_and_object_label returns a successful camera prediction.
    """
    result = camera_service_mock.get_centroid_and_object_label()
    assert result == camera_prediction_success_mock


def test_get_camera_prediction_default(
    camera_service_mock, camera_prediction_default_mock
):
    """
    Tests get_centroid_and_object_label returns default values when Mapper returns default.
    """
    result = camera_service_mock.get_centroid_and_object_label()
    assert result == camera_prediction_default_mock


def test_get_camera_prediction_error(camera_service_mock, requests_get_error):
    """
    Tests get_centroid_and_object_label raises exception when requests.get fails.
    """

    with pytest.raises(Exception, match="Connection error"):
        camera_service_mock.get_centroid_and_object_label()


def test_release_camera_prediction_success(
    camera_service_mock, camera_prediction_success_mock
):
    """
    Tests release_video_capture returns a successful camera prediction.
    """
    result = camera_service_mock.release_video_capture()
    assert result == camera_prediction_success_mock


def test_release_camera_prediction_error(camera_service_mock, requests_put_error):
    """
    Tests release_video_capture raises exception when requests.put fails.
    """

    with pytest.raises(Exception, match="Connection error"):
        camera_service_mock.release_video_capture()
