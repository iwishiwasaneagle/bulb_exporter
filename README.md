# bulb_exporter
[![Build and publish](https://github.com/iwishiwasaneagle/bulb_exporter/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/iwishiwasaneagle/bulb_exporter/actions/workflows/docker-publish.yml)
[![Test and lint](https://github.com/iwishiwasaneagle/bulb_exporter/actions/workflows/test_and_lint.yml/badge.svg)](https://github.com/iwishiwasaneagle/bulb_exporter/actions/workflows/test_and_lint.yml)


## Usage

First set up SmartThings Energy Control [here](https://help.bulb.co.uk/hc/en-us/articles/360034651651-Setting-up-SmartThings-Energy-Control-STEC-), then get your API token [here](https://account.smartthings.com/login?redirect=https%3A%2F%2Faccount.smartthings.com%2Ftokens) (requires `list all devices` and `see all devices`)

### Variables
| Required | Environmental Variable | Description | Default | Possible values |
| - | - | - | - | - |
| Yes | `SMARTTHINGS_TOKEN` | [Smartthings API token](https://account.smartthings.com/login?redirect=https%3A%2F%2Faccount.smartthings.com%2Ftokens) | n/a | `str` | 
| No | `LOG_LEVEL` | Logger level | `'INFO'` | `['DEBUG','INFO','WARNING','ERROR']` |
| No | `PORT` | Connection port | `8023` | `int`
| No | `INTERVAL` | Smartthings scrape interval (seconds) | `20` | `int` |
| No | `ONCE` | Run loop once. Used for testing | `FALSE` | `TRUE`/`FALSE` |

### Docker

```bash
docker run --rm -p 8023:8023 -e SMARTTHINGS_TOKEN=[ REPLACE WITH YOUR TOKEN ] iwishiwasaneagle/bulb_exporter:latest
```

An example `docker-compose.yml` exists [here](docker-compose.yml)

### Manually

```bash
git clone https://github.com/iwishiwasaneagle/bulb_exporter
cd bulb_exporter
pip install -r requirements
SMARTTHINGS_TOKEN=[ REPLACE WITH YOUR TOKEN ] python3 src/
```
