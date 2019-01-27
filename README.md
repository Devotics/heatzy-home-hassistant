# heatzy-home-assistant

Climate Home Assistant component for Heatzy Pilot

## Installation

To register the heatzy component to Home Assistant, copy the `climate` folder from this repository to your Home Assistant `custom_components` folder.

```bash
# Create `custom_components` folder
mkdir -p ~/.homeassistant/custom_components
cd ~/.homeassistant/custom_components
git clone https://github.com/Devotics/heatzy-home-hassistant
```

## Usage

Once installed, add the following lines to your `configuration.yaml`:
```yaml
climate:
  - platform: heatzy
    username: <your heatzy email>
    password: <your heatzy password>
```
This configuration will allow the component to query the Heatzy API to retrieve and contrôl your devices status.

## License

[MIT](https://oss.ninja/mit/dramloc)