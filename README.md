# heatzy-home-assistant

**🚨 NOTICE: heatzy-home-assistant is no longer maintained and stopped working with versions 2021 of Home Assistant ([Learn more](https://github.com/Devotics/heatzy-home-hassistant/issues/20)). As an alternative, you can try [hass-heatzy](https://github.com/Cyr-ius/hass-heatzy) that is actively maintained and is kept up to date with Home Assistant.**

Home Assistant integration for the [Heatzy Pilot](https://heatzy.com/pilote) electric heater controller.

> You can find some extra information on how to integrate this component in your Home Assistant installation [here](https://community.home-assistant.io/t/heatzy-compoment/54863).

## Installation

To register the heatzy component to Home Assistant, copy the `heatzy` folder from this repository to your Home Assistant `custom_components` folder.

You can find installation instructions for specific Home Assistant versions below.

| Home Assistant version | Heatzy component version                                   |
| ---------------------- | ---------------------------------------------------------- |
| 0.110 and higher       | [master](#installation-for-home-assistant-0110-and-higher) |
| 0.96 to 0.109          | [3.1.0](#installation-for-home-assistant-096-to-0109)      |
| 0.89 to 0.95           | [2.0.1](#installation-for-home-assistant-089-to-095)       |
| 0.88 and lower         | [1.1.1](#installation-for-home-assistant-088-and-lower)    |

### Installation for Home Assistant 0.110 and higher

The following commands assume that your Home Assistant folder is located in `~/.homeassistant/custom_components`:

```bash
# Create custom_components folder
mkdir -p ~/.homeassistant/custom_components
# Move to the custom_components folder
cd ~/.homeassistant/custom_components
# Fetch this repo and extract it
curl -L https://api.github.com/repos/Devotics/heatzy-home-hassistant/tarball/master | tar -xz
# Copy heatzy folder
cp -rl Devotics-heatzy-home-hassistant-*/heatzy .
# Clean up
rm -rf Devotics-heatzy-home-hassistant-*
```

### Installation for Home Assistant 0.96 to 0.109

<details>
  <summary>Instructions</summary>

Version 4.0.0 of this component removes some deprecation notices introduced by [this pull request](https://github.com/home-assistant/core/pull/34591). You can still install a compatible version for Home Assistant versions 0.96 to 0.109 with the following instructions:

```bash
# Create custom_components folder
mkdir -p ~/.homeassistant/custom_components
# Move to the custom_components folder
cd ~/.homeassistant/custom_components
# Fetch this repo and extract it
curl -L https://api.github.com/repos/Devotics/heatzy-home-hassistant/tarball/3.1.0 | tar -xz
# Copy heatzy folder
cp -rl Devotics-heatzy-home-hassistant-*/heatzy .
# Clean up
rm -rf Devotics-heatzy-home-hassistant-*
```

</details>

### Installation for Home Assistant 0.89 to 0.95

<details>
  <summary>Instructions</summary>

Version 3.0.0 of this component introduces breaking changes related to [the Climate Cleanup](https://developers.home-assistant.io/blog/2019/07/03/climate-cleanup.html). You can still install a compatible version for Home Assistant versions 0.89 to 0.95 with the following instructions:

```bash
# Create custom_components folder
mkdir -p ~/.homeassistant/custom_components
# Move to the custom_components folder
cd ~/.homeassistant/custom_components
# Fetch this repo and extract it
curl -L https://api.github.com/repos/Devotics/heatzy-home-hassistant/tarball/2.0.1 | tar -xz
# Copy heatzy folder
cp -rl Devotics-heatzy-home-hassistant-*/heatzy .
# Clean up
rm -rf Devotics-heatzy-home-hassistant-*
```

</details>

### Installation for Home Assistant 0.88 and lower

<details>
  <summary>Instructions</summary>

Version 2.0.0 of this component introduces breaking changes related to [The Great Migration ™](https://developers.home-assistant.io/blog/2019/02/19/the-great-migration.html). You can still install a compatible version on Home Assistant 0.88 and lower with the following instructions:

```bash
# Create custom_components folder
mkdir -p ~/.homeassistant/custom_components
# Move to the custom_components folder
cd ~/.homeassistant/custom_components
# Fetch this repo and extract it
curl -L https://api.github.com/repos/Devotics/heatzy-home-hassistant/tarball/1.1.1 | tar -xz
# Copy climate folder
cp -rl Devotics-heatzy-home-hassistant-*/climate .
# Clean up
rm -rf Devotics-heatzy-home-hassistant-*
```

</details>

## Usage

Once installed, add the following lines to your `configuration.yaml`:

```yaml
climate:
  - platform: heatzy
    username: "<your heatzy email>"
    password: "<your heatzy password>"
```

This configuration will allow the component to query the Heatzy API to retrieve and control your devices status.

## License

[MIT](https://oss.ninja/mit/devotics)
