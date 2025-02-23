# `fetch_entities.py` - Multi-Threaded New Relic Entity Fetcher

This Python program fetches entities from New Relic accounts using the NerdGraph API. It supports fetching entities from multiple accounts, filtering by entity `domains`, and outputting the results to text and CSV files. It also includes progress bars for a better user experience for longer running jobs.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Building the Virtual Environment](#building-the-virtual-environment)
4. [Configuration](#configuration)
5. [Running the program](#running-the-program)
6. [Output Files](#output-files)
7. [Example Screen Output](#example-screen-output)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before using this program, ensure you have the following:

1. **Python 3.6 or higher**: The program is written in Python and requires a compatible version.
2. **New Relic API Key**: You need a New Relic API key with permissions to query entities.
3. **Account IDs**: The New Relic account IDs from which you want to fetch entities.

---

## Setup

1. Clone or download the repo to your local machine.
2. Build the Python virtual environment using the provided `dependencies.txt` file (see below).

---

## Building the Virtual Environment

To ensure you have all the required dependencies, you can build a Python virtual environment using the `dependencies.txt` file included in the project.

### Steps:
1. Navigate to the project directory:

   ```bash
   cd path/to/project

2. Create a virtual environment named venv

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

1. The `config.py` file is used to configure the accounts and entity `domains` to fetch. Here's an example:

```
# config.py
ACCOUNTS = [
    {
        'API_KEY': 'YOUR_API_KEY_1',  # Replace with your actual API key
        'ACCOUNT_ID': 'YOUR_ACCOUNT_ID_1',  # Replace with your actual account ID
        'ENTITY_DOMAINS': ['APM', 'BROWSER']  # Optional: List of domains
    },
    {
        'API_KEY': 'YOUR_API_KEY_2',  # Replace with your actual API key
        'ACCOUNT_ID': 'YOUR_ACCOUNT_ID_2',  # Replace with your actual account ID
        'ENTITY_DOMAINS': ['INFRA', 'SYNTH'] # Optional: List of domains
    },
    {
        'API_KEY': 'YOUR_API_KEY_3',  # Replace with your actual API key
        'ACCOUNT_ID': 'YOUR_ACCOUNT_ID_3',  # Replace with your actual account ID
        # No ENTITY_DOMAINS specified: Fetch all entities in the account
    }    
]
```

Fields:

- API_KEY: Your New Relic API key.
- ACCOUNT_ID: The New Relic account ID.
- ENTITY_DOMAINS: (Optional) A list of entity types to fetch (e.g., ['APM', 'BROWSER']). If not provided, the program fetches all entities in the account.
APM
## Running the program

To run the program make sure your virtualenv is activated and use the following command:


```
python fetch_entities.py
```

What Happens:

1. The program reads the configuration from config.py.
2. It fetches entities from each account, using `pagination` to handle large datasets.
3. The program will use as many threads as you specify (see below for details)
4. Progress bars show the fetching and writing progress.
5. Output files are created in the same directory.

### Optimizing with more threads
It is possible to optimize the run by setting the `max_threads` parameter.

By default this is set to `1` however the following example would set it to `2` so if you are running it against 2 accounts it will process both simultaneously.

```
python fetch_entities.py --max_threads 2
```

Be aware that the API may subject the client to some rate limiting so don't overuse this.


### Output Files

The program generates the following output files:

1. `entities.txt`:

Contains all entities from all accounts in a human-readable format.

Example:

```
GUID: f315487c9b0244f3879bdbb4eb9d5246
Name: Ad Service4120837
Type: APM_APPLICATION_ENTITY
Domain: APM
Tags:
  account: ['Advertising Account (PROD)']
  accountId: ['12345']
  agentVersion: ['8.16.0']
  built_by: ['terraform']
  feature: ['threads']
  instrumentation.name: ['apm']
  instrumentation.provider: ['newRelic']
  k8s.clusterName: ['Ad Cluster']
  k8s.deploymentName: ['microservicesdemo-adservice']
  k8s.namespaceName: ['microservicesdemo']
  language: ['java']
----------------------------------------
```

2. `entities_[account_id].txt`:

Contains fetched entities in the same format of `entities.txt` but broken out by account.


3. `entities.csv`:

Contains all entities in CSV format, with columns for GUID, Name, Type, Domain, and tags.

### Example Screen Output

When you run the program, you'll see progress bars and summaries like this:

```
Deleted entities.txt
Deleted entities_123.txt
Deleted entities_234.txt

Fetching entities for account 123 (ACME Prod) (Total: 915): [00:07,  1.44s/page]
Writing to entities_123.txt: 100%

Entity Counts by Type for account 123:
GENERIC_INFRASTRUCTURE_ENTITY: 796
SYNTHETIC_MONITOR_ENTITY: 10
SECURE_CREDENTIAL_ENTITY: 6
APM_APPLICATION_ENTITY: 19
WORKLOAD_ENTITY: 15
INFRASTRUCTURE_AWS_LAMBDA_FUNCTION_ENTITY: 3
INFRASTRUCTURE_HOST_ENTITY: 65
BROWSER_APPLICATION_ENTITY: 1
Total entities fetched for account 123: 915

Fetching entities for account 234 (ACME DEV) (Total: 1418): [00:11,  1.46s/page]
Writing to entities_234.txt: 100%

Entity Counts by Type for account 234:
WORKLOAD_ENTITY: 240
GENERIC_INFRASTRUCTURE_ENTITY: 943
SYNTHETIC_MONITOR_ENTITY: 65
SECURE_CREDENTIAL_ENTITY: 9
MOBILE_APPLICATION_ENTITY: 7
GENERIC_ENTITY: 21
APM_APPLICATION_ENTITY: 48
BROWSER_APPLICATION_ENTITY: 6
INFRASTRUCTURE_HOST_ENTITY: 71
INFRASTRUCTURE_AWS_LAMBDA_FUNCTION_ENTITY: 8
Total entities fetched for account 234: 1418

Writing to entities.csv: 100%
Domain and entity type pairs have been written to 'entity_types.csv'.
Writing to entities.txt: 100%

Global Entity Counts by Type (All Accounts):
GENERIC_INFRASTRUCTURE_ENTITY: 1739
SYNTHETIC_MONITOR_ENTITY: 75
SECURE_CREDENTIAL_ENTITY: 15
APM_APPLICATION_ENTITY: 67
WORKLOAD_ENTITY: 255
INFRASTRUCTURE_AWS_LAMBDA_FUNCTION_ENTITY: 11
INFRASTRUCTURE_HOST_ENTITY: 136
BROWSER_APPLICATION_ENTITY: 7
MOBILE_APPLICATION_ENTITY: 7
GENERIC_ENTITY: 21
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

If the program stops prematurely, check the API response for errors.

### License
This program is provided under the MIT License. Feel free to modify and distribute it as needed.

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