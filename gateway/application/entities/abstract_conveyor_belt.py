from abc import ABC, abstractmethod


class AbstractConveyorBelt(ABC):

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError

    @abstractmethod
    def is_connected(self):
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @abstractmethod
    def change_speed(self, speed: int):
        raise NotImplementedError

    @abstractmethod
    def change_direction(self, direction: bool):
        raise NotImplementedError

    @abstractmethod
    def get_actual_speed(self):
        raise NotImplementedError

    @abstractmethod
    def get_actual_direction(self):
        raise NotImplementedError
