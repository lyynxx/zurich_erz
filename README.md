# zurich_erz

This sensor custom component for HomeAssistant shows the next waste/recycling goods collection dates for Zürich, Switzerland. 
The data is provided by the open data portal of City of Zurich: https://data.stadt-zuerich.ch/
For details about the API, refer to: http://openerz.metaodi.ch/documentation

Thanks to @metaodi for providing the API: https://github.com/metaodi/openerz

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE.md)

![Project Maintenance][maintenance-shield]
[![GitHub Activity][commits-shield]][commits]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

## Options

| Name | Type | Requirement | Description
| ---- | ---- | ------- | -----------
| platform | string | **Required** | zurich_erz
| scan_interval | number | **Optional** | Scan interval to update the sensor
| zip | integer | **Required** | The zip code for the collection
| tour | string | **Optional** | Label for the tour if there's more than one waste collection tour for that zip code
| cardboard | boolean | **Optional** | Shows the next cardboard collection date (default: false)
| cargotram | boolean | **Optional** | Shows the next cargotram date (default: false)
| etram | boolean | **Optional** | Shows the next etram date (default: false)
| metal | boolean | **Optional** | Show the next metal collection date (default: false)
| organic | boolean | **Optional** | Show the next organic waste collection date (default: false)
| paper | boolean | **Optional** | Show the next paper collection date (default: false)
| special | boolean | **Optional** | Show the next special waste collection date (default: false)
| textile | boolean | **Optional** | Show the next textile collection date (default: false)
| waste | boolean | **Optional** | Show the next general waste collection date (default: false)


## Installation

### Step 1

Save sensor.py to `<config directory>/custom_components/zurich_erz/sensor.py`

### Step 2

Add to the configuration yaml file:

```yaml
sensor:
  - platform: zurich_erz
    zip: 8000
    scan_interval: 86400
    cardboard: true
    cargotram: true
    etram: true
    metal: true
    organic: true
    paper: true
    special: true
    textile: true
    waste: true
```

### Step 3

Restart HomeAssistant