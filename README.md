# Coke-Reward-Codes-Automation
Redeems coke reward codes using web automation.

## Getting Started
Clone or download the repository and use the script `redeem_codes.py` as a command-line/terminal program.

### Usage
There are two ways of redeeming codes: submitting them to rewards or to a school.

#### Submit Codes to Rewards
`python redeem_codes_rewards.py twitter_user_name twitter_password desired_rewards reward_codes_file_path log_file_path element_load_timeout`

where `twitter_user_name` and `twitter_password` are your Twitter credentials linked to your Coca-Cola account,

`desired_rewards` is a comma-separated list of any of the following rewards:

`OliveGarden`
`Dominos`
`AMCTheaters`
`Magazines`
`iTunes`
`Nordstrom`
`Drink`
`Groceries`
`Coffee`
`VendingMachine`
`UHDTV`,

`reward_codes_file_path` is a file path to a CSV file with its first column containing all coke reward codes

`log_file_path` is a file path to a log file where all the codes and their status (`invalid`, `already_redeemed`, `success`, or `other`) are stored

and `element_load_timeout` is the maximum time required for an HTML element to load.

#### Submit Codes to a School
`Usage: python redeem_codes_school.py twitter_user_name twitter_password school_name reward_codes_file_path log_file_path element_load_timeout`

where `twitter_user_name` and `twitter_password` are your Twitter credentials linked to your Coca-Cola account,

`school_name` is the name of the school you wish to donate to,

`reward_codes_file_path` is a file path to a CSV file with its first column containing all coke reward codes

`log_file_path` is a file path to a log file where all the codes and their status (`invalid`, `already_redeemed`, `success`, or another error code) are stored

and `element_load_timeout` is the maximum time required for an HTML element to load.

### Example Usage
`python redeem_codes.py test hello123 Dominos,AMCTheaters example_data/reward_codes.csv example_data/log.csv 10`

`python redeem_codes_school.py test hello123 "Walton High School, 30062" example_data/reward_codes.csv example_data/log.csv 10`

## Prerequisites
selenium==3.5.0
