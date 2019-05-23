# Coke-Reward-Codes-Automation
Redeems coke reward codes using web automation.

## Getting Started
Clone or download the repository and use the script `redeem_codes.py` as a command-line/terminal program.

### Usage
`python redeem_codes.py twitter_user_name twitter_password desired_rewards reward_codes_file_path element_load_timeout`

where `twitter_user_name` and `twitter_password` are your Twitter credentials linked to your Coca-Cola account,

`desired_rewards` is a comma-separated list of any of the following rewards:

`OliveGarden`
`Dominos`
`AMCTheaters`
`Magazines`
`iTunes`
`Nordstrom`
`Chilis`
`Shutterfly`
`Drink`
`Groceries`
`Coffee`
`VendingMachine`
`UHDTV`,

`reward_codes_file_path` is a file path to a CSV file with a column titled `codes` containing all coke reward codes

and `element_load_timeout` is the maximum time required for an HTML element to load.

## Prerequisites
selenium==3.5.0

pandas==0.23.4
