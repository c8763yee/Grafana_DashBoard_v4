from pydantic import BaseModel, computed_field


def convert_current_to_Kwatt(current: float) -> float:
    return (current / 1.732) * 220 / 1000


class FrontDoorFanModel(BaseModel):
    Temperature: float
    Humidity: float
    CO2: float
    TVOC: float
    fan_0: str
    fan_1: str


class BackDoorFanModel(BaseModel):
    Temperature: float
    Humidity: float
    CO2: float
    TVOC: float
    fan_0: str
    fan_1: str


class FirstMeetingRoomFanModel(BaseModel):
    fan_0: str


class FirstMeetingRoomModel(BaseModel):
    Temperature: float
    Humidity: float
    CO2: float
    TVOC: float


class SecondMeetingRoomModel(BaseModel):
    Temperature: float
    Humidity: float
    CO2: float
    TVOC: float


class PowerBoxModel(BaseModel):
    IN_A: float
    IN_B: float
    IN_C: float
    IN_Avg: float

    @computed_field
    @property
    def kW_A(self) -> float:
        return convert_current_to_Kwatt(self.IN_A)

    @computed_field
    @property
    def kW_B(self) -> float:
        return convert_current_to_Kwatt(self.IN_B)

    @computed_field
    @property
    def kW_C(self) -> float:
        return convert_current_to_Kwatt(self.IN_C)

    @computed_field
    @property
    def kW_tot(self) -> float:
        return self.kW_A + self.kW_B + self.kW_C


class ServerRoomModel(BaseModel):
    Temperature: float
    Humidity: float


class AirConditionerModel(BaseModel):
    Status: bool


class DL303Model(BaseModel):
    TemperatureC: float
    Humidity: float
    DewPointC: float
    CO2: float
