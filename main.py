from src.utils.noaa import fetch_local_pass_times
from src.services.scheduler import Scheduler
from src.services.process import process_pass
import time
import logging

logging.basicConfig(level=logging.INFO)

MINUTES_DELAY = 5


def daily_check():
    scheduler = Scheduler.instance()
    logging.info("Fetching todays pass times")
    local_pass_times = fetch_local_pass_times()
    for noaa_sat, passes in local_pass_times.items():
        for pass_details in passes:
            logging.info(
                f"Scheduling pass for {noaa_sat} from {pass_details.aos.dt} to {pass_details.los.dt}"
            )
            scheduler.add_job(
                lambda: process_pass(noaa_sat, pass_details), pass_details.aos.dt
            )


def main_loop():
    scheduler = Scheduler.instance()
    while True:
        time.sleep(MINUTES_DELAY * 60)
        logging.info(f"Current jobs: {scheduler.job_count()}")


if __name__ == "__main__":
    scheduler = Scheduler.instance()
    scheduler.add_cron(daily_check, 0, 0)
    main_loop()
