# Notice
This is an active work in progress and not complete.

# Setup

```
conda create -n ground-station python=3.9
conda activate ground-station
```

## Install Needed Packages
`pip install -r requirements.txt`

## Export Needed Packages
If any new packages are added then you will need to update the requirements.txt file.

`pip list --format=freeze > requirements.txt`

# Resource Links
- https://www.instructables.com/Raspberry-Pi-NOAA-Weather-Satellite-Receiver/
- https://w6aer.com/setting-up-noaa-weather-satellite-receiver-raspberry-pi/

# TODO
- .env file setup
- SDR config LINUX
- Image processing
- Local storage
- DB modeling
- Remote storage (S3)
