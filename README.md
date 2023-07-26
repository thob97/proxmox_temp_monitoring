# Proxmox Temp Monitoring
Service that fetches the CPU temperature of your Proxmox server, sends it to InfluxDB, and then visualizes the data using Grafana

<p float="left">
    <img src="./keyboards/kprepublic/bm40hsrgb/rev2/_github_example_pictures//layer1.png"  width="45.5%" height="45.5%">
    <img src="./keyboards/kprepublic/bm40hsrgb/rev2/_github_example_pictures/1.jpeg"  width="40%" height="40%">
</p>

## Table Of Content

- [Pre Requirements](#pre-requirements)
- [Getting Started](#getting-started)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Compile and run](#compile-and-run)
- [Vizualise Keymap](#vizualise-keymap)
- [Example pictures](#example-pictures)
- [See also](#see-also)
- [Original readme of forked repo](#quantum-mechanical-keyboard-firmware)

## Pre Requirements
This section will handeln of how to install and configure grafana, influxdb on an lxc container on proxmox. Skip this section if you have already setup this.

1. Create a new debain 12 lxc container on your proxmox node. I choose the config:
Storage: 8GB
RAM: 2GB
SWAP: 0MB
CPU: 1
unprivileged: yes
nesting: yes

2. Install the influxDB the following commands:
```
# update
apt update
apt upgrade
apt install curl
# install & start influxdb 
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.0.9-amd64.deb
dpkg -i influxdb2-2.0.9-amd64.deb
service influxdb start
```
Afterwards visit the webgui (with standard port 8086), folow the initial setps and then create a new api token for proxmox & grafana.

3. Install the grafana the following commands:
```
# install grafana
apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_10.0.3_amd64.deb
dpkg -i grafana_10.0.3_amd64.deb
# start grafana
systemctl daemon-reload
systemctl enable grafana-server
systemctl start grafana-server
```
Afterwards visit the webgui (with standard port 3000 and user/pass: admin/admin), folow the initial setps and then a new connection to influxDB by moving to `connections` -> `add new connections` -> `select InfluxDB` and adding the following config:
- Query Language: Flux
- URL: http://localhost:8086
- Organization: <from influxDB setup>
- Token: <from influxDB setup>
- Default Bucket: <from influxDB setup>


4. Configure proxmox so that it sends its informations to the influxdb by heading to the proxmox website -> `datascenter` -> `metric server` -> `add influxdb` with e.g. the following values:
influxdb: monitoring
port 8086
server <ip of influxDB container>
influxdbproto http
bucket <from influxDB setup>
organization <from influxDB setup>
token <from influxDB setup>


## Getting Started

### Dependencies

In order for the scripts to work you will need the following dependencies:
 * python (tested with)
 * influxDB (tested with)
 * grafana (tested with)
 * proxmox (tested with)

### Installation
 - Ensure that your PC is set to use an English keyboard layout. However, for maximum compatibility, consider using [EurKey](https://eurkey.steffen.bruentjen.eu/layout.html).
 - `git clone https://github.com/thob97/qmk_firmware_bm40hsrgb_v2_Neo_Bone.git`
 - `cd qmk_firmware_bm40hsrgb_v2_Neo_Bone`

### Compile and run
 - `make git-submodule`
 - `make kprepublic/bm40hsrgb/rev2:default:flash`
 - `echo 'PATH="$HOME/.local/bin:$PATH"' >> $HOME/.bashrc && source $HOME/.bashrc`

### Add as service

### Load grafana dashboard

## Example pictures
<p float="left">
    <img src="./keyboards/kprepublic/bm40hsrgb/rev2/_github_example_pictures/preview1.jpeg"  width="48%" height="48%">
    <img src="./keyboards/kprepublic/bm40hsrgb/rev2/_github_example_pictures/2.JPG"  width="48%" height="48%">
</p>
<p float="left">
    <img src="./keyboards/kprepublic/bm40hsrgb/rev2/_github_example_pictures/layer1.png"  width="48%" height="48%">
    <img src="./keyboards/kprepublic/bm40hsrgb/rev2/_github_example_pictures/layer2.png"  width="48%" height="48%">
    <img src="./keyboards/kprepublic/bm40hsrgb/rev2/_github_example_pictures/layer3.png"  width="48%" height="48%">
    <img src="./keyboards/kprepublic/bm40hsrgb/rev2/_github_example_pictures/layer4.png"  width="48%" height="48%">
    <img src="./keyboards/kprepublic/bm40hsrgb/rev2/_github_example_pictures/layer5.png"  width="48%" height="48%">

</p>


## Acknowledgment
* influxDB: https://docs.influxdata.com/influxdb/v1.8/introduction/install/](https://docs.influxdata.com/influxdb/v2.7/install/?t=Linux#install-influxdb-as-a-service-with-systemd
* grafana: https://grafana.com/grafana/download?edition=enterprise&pg=get&plcmt=selfmanaged-box1-cta1
* many of the metrics were taken from the following dashboard: https://grafana.com/grafana/dashboards/16537-proxmox-flux/
