from src.common.types import PassMap, SatInfo
from passpredict import PredictedPass
import logging
import simplesoapy


def process_pass(sat: SatInfo, pass_details: PredictedPass):
    logging.info(
        "Pass running for {sat} from {pass_details.aos.dt} to {pass_details.los.dt}")
    duration = pass_details.duration
