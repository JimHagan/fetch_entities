# `fetch_entities.py` - New Relic Entity Fetcher

This Python script fetches entities from New Relic accounts using the NerdGraph API. It supports fetching entities from multiple accounts, filtering by entity types, and outputting the results to text and CSV files. It also includes progress bars for a better user experience.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Building the Virtual Environment](#building-the-virtual-environment)
4. [Configuration](#configuration)
5. [Running the Script](#running-the-script)
6. [Output Files](#output-files)
7. [Example Screen Output](#example-screen-output)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before using this script, ensure you have the following:

1. **Python 3.6 or higher**: The script is written in Python and requires a compatible version.
2. **New Relic API Key**: You need a New Relic API key with permissions to query entities.
3. **Account IDs**: The New Relic account IDs from which you want to fetch entities.

---

## Setup

1. Clone or download the script to your local machine.
2. Build the Python virtual environment using the provided `dependencies.txt` file (see below).

---

## Building the Virtual Environment

To ensure you have all the required dependencies, you can build a Python virtual environment using the `dependencies.txt` file included in the project.

### Steps:
1. Navigate to the project directory:

   ```bash
   cd path/to/project

2. Create a virtual environment

```
python -m venv venv
```

3. Activate the virtual environment

```
source venv/bin/activate
```

4. Install the required dependencies

```
pip install -r dependencies.txt
```

## Configuration

1. 

The `config.py` file is used to configure the accounts and entity types to fetch. Here's an example:

```
# config.py
ACCOUNTS = [
    {
        'API_KEY': 'YOUR_API_KEY_1',  # Replace with your actual API key
        'ACCOUNT_ID': 'YOUR_ACCOUNT_ID_1',  # Replace with your actual account ID
        'ENTITY_DOMAINS': ['APM', 'BROWSER']  # Optional: List of entity types to fetch
    },
    {
        'API_KEY': 'YOUR_API_KEY_2',  # Replace with your actual API key
        'ACCOUNT_ID': 'YOUR_ACCOUNT_ID_2',  # Replace with your actual account ID
        # No ENTITY_DOMAINS specified: Fetch all entities in the account
    }
]
```

Fields:

- API_KEY: Your New Relic API key.
- ACCOUNT_ID: The New Relic account ID.
- ENTITY_DOMAINS: (Optional) A list of entity types to fetch (e.g., ['APM', 'BROWSER']). If not provided, the script fetches all entities in the account.

## Running the script

To run the script, use the following command:


```
python fetch_entities.py
```

What Happens:

1. The script reads the configuration from config.py.
2. It fetches entities from each account, using pagination to handle large datasets.
4. Progress bars show the fetching and writing progress.
5. Output files are created in the same directory.

*TIP*  It is possible to optimize the run by setting the `max_threads` parameter.

By default this is set to `1` however the following example would set it to `2` so if you are running it against 2 accounts it will process both simultaneously.

```
python fetch_entities.py --max_threads 2
```

Be aware that the API may subject the client to some rate limiting so don't overuse this.


### Output Files

The script generates the following output files:

`entities.txt`:

Contains all entities from all accounts in a human-readable format.

Example:

```
GUID: ABC123
Name: My Application
Type: APM
Domain: APM
Tags:
  environment: [production]
  team: [devops]
----------------------------------------
```

`entities_[account_id].txt`:

Contains entities in the same format of `entities.txt` but broken out by account.



`entities.csv`:

Contains all entities in CSV format, with columns for GUID, Name, Type, Domain, and tags.

Example Screen Output

When you run the script, you'll see progress bars and summaries like this:

```
Fetching entities for account 12345 (Total: 25): 100%|████████████████████| 5/5 [00:10<00:00,  2.00s/page]
Writing to entities_12345.txt: 100%|████████████████████| 25/25 [00:02<00:00, 10.00entity/s]
Fetching entities for account 67890 (Total: 10): 100%|████████████████████| 3/3 [00:06<00:00,  2.00s/page]
Writing to entities_67890.txt: 100%|████████████████████| 10/10 [00:01<00:00, 10.00entity/s]
Writing to entities.txt: 100%|████████████████████| 35/35 [00:03<00:00, 10.00entity/s]
Writing to entities.csv: 100%|████████████████████| 35/35 [00:03<00:00, 10.00entity/s]

Entity Counts by Type for account 12345:
APM: 12
BROWSER: 5
INFRA: 8
Total entities fetched for account 12345: 25

Entity Counts by Type for account 67890:
MOBILE: 3
SYNTH: 7
Total entities fetched for account 67890: 10

All entities have been written to 'entities.txt' and 'entities.csv'.

Global Entity Counts by Type (All Accounts):
APM: 12
BROWSER: 5
INFRA: 8
MOBILE: 3
SYNTH: 7
```


### Troubleshooting
Common Issues:

#### API Key Errors:

Ensure your API key has the necessary permissions.

Double-check the API key in config.py.

#### Account ID Errors:

Verify that the account IDs in config.py are correct.

##### No Entities Found:

Check if the ENTITY_DOMAINS filter in config.py is too restrictive.

If no ENTITY_DOMAINS are specified, ensure the account has entities.

#### Pagination Issues:

If the script stops prematurely, check the API response for errors.

### License
This script is provided under the MIT License. Feel free to modify and distribute it as needed.

For questions or issues, please open an issue on GitHub or contact the author. Happy fetching! 😊

### List of some known domain/entityType pairs

```
domain,entityType
IAST,GENERIC_ENTITY
INFRA,INFRASTRUCTURE_AWS_LAMBDA_FUNCTION_ENTITY
EXT,THIRD_PARTY_SERVICE_ENTITY
INFRA,INFRASTRUCTURE_HOST_ENTITY
EXT,EXTERNAL_ENTITY
NR1,WORKLOAD_ENTITY
REF,GENERIC_ENTITY
BROWSER,BROWSER_APPLICATION_ENTITY
APM,APM_APPLICATION_ENTITY
SYNTH,SYNTHETIC_MONITOR_ENTITY
AIOPS,GENERIC_ENTITY
VIZ,DASHBOARD_ENTITY
INFRA,GENERIC_INFRASTRUCTURE_ENTITY
SYNTH,SECURE_CREDENTIAL_ENTITY
UNINSTRUMENTED,GENERIC_ENTITY
EXT,KEY_TRANSACTION_ENTITY

```