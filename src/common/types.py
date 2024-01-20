from passpredict import PredictedPass
import collections.abc

SatInfo = tuple[str, str]  # Normal name and norad number
SatInfoList = list[SatInfo]

PassMap = dict[tuple[str, str], list[PredictedPass]]

Job = collections.abc.Callable[[], None]
