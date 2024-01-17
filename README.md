# Ethereum Validator Controller
This GUI validator controller makes operating a validator simple and accessible to all.

## Features:

- **Multi-client Support**: Controll all major clients including Geth, Besu, Nethermind, Teku, Nimbus, Lighthouse, Prysm, and Mevboost.
- **Standard Configuration**: Get the same results as manually entering terminal commands
- **Simple Operation**: Easy to operate, no technical skills required

### Validator Controller (GUI):
![image](https://github.com/accidental-green/validator-controller/assets/72235883/cf384644-c48d-4295-af3d-23010c9fff28)

## Prerequisites:

**Update system and install packages:**

`sudo apt update && sudo apt install git curl python3-pip python3-tk -y && sudo pip install requests`

**Clone the repository:**

`git clone https://github.com/accidental-green/validator-controller.git`

## Controller Instructions:
**Launch Controller:**

`python3 validator-controller/validator_controller.py`

### Validator Controller (GUI):

Select clients then operate everything with single click (start, stop, journals etc)

![image](https://github.com/accidental-green/validator-controller/assets/72235883/cf384644-c48d-4295-af3d-23010c9fff28)

### Validator Controller Options:
- **Select Execution Client**: (Besu, Geth, Nethermind)
- **Select Consensus Client**: (Lighthouse, Nimbus, Prysm, Teku)
- **Mevboost On/Off**: Toggle MEV on/off
- **Start All**: Start selected services
- **Stop All**: Stop all services
- **Journals**: Open journals in new windows
- **Service Files**: Open service files to view/edit

<br>

**Note**: The controller is meant to control validators already installed and configured. If you don't have a validator installed, you can visit my other Ethereum repos to get started:

[Validator Install](https://github.com/accidental-green/validator-install): Fresh Ubunutu to syncing validator in 52 seconds

[Validator Updater](https://github.com/accidental-green/validator-updater): Instantly update clients (Execution, Consensus, and Mevboost)

[Client-Switcher](https://github.com/accidental-green/client-switcher): Instantly switch to a new Execution client


## Important Note:

This project is open source but has not been audited. It is still relatively untested, so use with caution.

## Credits:

Many thanks to [Somer Esat](https://github.com/SomerEsat/ethereum-staking-guides) for creating the staking guides which served as the basis for this project.
