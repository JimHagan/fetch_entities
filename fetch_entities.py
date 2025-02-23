import requests
import csv
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import ACCOUNTS

# NerdGraph API endpoint
NERDGRAPH_URL = 'https://api.newrelic.com/graphql'

# GraphQL query to fetch entities with pagination
def get_entities_query(account_id, entity_domains=None, cursor=None):
    if entity_domains:
        entity_domains_str = ', '.join([f"'{ed}'" for ed in entity_domains])
        query_filter = f"domain IN ({entity_domains_str}) AND accountId = {account_id}"
    else:
        query_filter = f"accountId = {account_id}"
    
    query = f"""
    {{
      actor {{
        entitySearch(query: "{query_filter}") {{
          results(cursor: {"null" if cursor is None else f'"{cursor}"'}) {{
            nextCursor
            entities {{
              guid
              name
              entityType
              domain
              tags {{
                key
                values
              }}
            }}
          }}
        }}
      }}
    }}
    """
    return query

# Function to fetch all entities for a given account
def fetch_all_entities(api_key, account_id, entity_domains=None):
    cursor = None
    all_entities = []
    total_entities = 0
    account_name = None  # Initialize account name as None

    with tqdm(desc=f"Fetching entities for account {account_id} (Unknown Name)", unit="page") as pbar:
        while True:
            response = requests.post(NERDGRAPH_URL, json={'query': get_entities_query(account_id, entity_domains, cursor)}, headers={'Content-Type': 'application/json', 'API-Key': api_key})
            
            if response.status_code == 200:
                data = response.json()
                if 'errors' in data:
                    print(f"Errors returned from the API for account {account_id}:")
                    for error in data['errors']:
                        print(error['message'])
                    break
                else:
                    results = data['data']['actor']['entitySearch']['results']
                    entities = results['entities']
                    all_entities.extend(entities)
                    total_entities += len(entities)

                    # Try to find the account name from the tags if not already found
                    if account_name is None:
                        for entity in entities:
                            for tag in entity['tags']:
                                if tag['key'] == 'account' and tag['values']:
                                    account_name = tag['values'][0]  # Use the first value as the account name
                                    break
                            if account_name:
                                break
                        # Update the progress bar description with the account name
                        pbar.set_description(f"Fetching entities for account {account_id} ({account_name if account_name else 'Unknown Name'})")

                    pbar.set_description(f"Fetching entities for account {account_id} ({account_name if account_name else 'Unknown Name'}) (Total: {total_entities})")
                    pbar.update(1)
                    cursor = results.get('nextCursor')
                    if not cursor:
                        break
                    time.sleep(1)  # Add a delay to avoid rate limits
            else:
                print(f"Failed to retrieve entities for account {account_id}. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                break
    
    return account_id, all_entities

# Function to write entities to a text file
def write_entities_to_txt(entities, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for entity in tqdm(entities, desc=f"Writing to {filename}", unit="entity"):
            file.write(f"GUID: {entity['guid']}\n")
            file.write(f"Name: {entity['name']}\n")
            file.write(f"Type: {entity['entityType']}\n")
            file.write(f"Domain: {entity['domain']}\n")
            file.write("Tags:\n")
            for tag in entity['tags']:
                file.write(f"  {tag['key']}: {tag['values']}\n")
            file.write("-" * 40 + "\n")

# Function to write entities to a CSV file
def write_entities_to_csv(entities, filename='entities.csv'):
    fieldnames = ['accountId', 'guid', 'name', 'entityType', 'domain']
    tag_keys = set()
    for entity in entities:
        for tag in entity['tags']:
            tag_keys.add(tag['key'])
    fieldnames.extend(sorted(tag_keys))
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entity in tqdm(entities, desc=f"Writing to {filename}", unit="entity"):
            row = {
                'accountId': entity['accountId'],
                'guid': entity['guid'],
                'name': entity['name'],
                'entityType': entity['entityType'],
                'domain': entity['domain']
            }
            for tag in entity['tags']:
                row[tag['key']] = ', '.join(tag['values'])
            writer.writerow(row)

# Function to write domain and entity type pairs to a CSV file
def write_entity_types_to_csv(entity_types, filename='entity_types.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['domain', 'entityType'])
        writer.writeheader()
        for domain, entity_type in entity_types:
            writer.writerow({'domain': domain, 'entityType': entity_type})

# Main function to process all accounts
def main(max_threads=1):  # Default to 1 threads if not specified
    all_entities = []
    entity_types_set = set()
    global_entity_type_counts = {}  # Dictionary to store global entity counts by type
    
    # Fetch entities for all accounts in parallel
    with ThreadPoolExecutor(max_workers=max_threads) as executor:  # Use max_threads here
        futures = [executor.submit(fetch_all_entities, account['API_KEY'], account['ACCOUNT_ID'], account.get('ENTITY_DOMAINS')) for account in ACCOUNTS]
        for future in as_completed(futures):
            account_id, entities = future.result()
            
            # Add account ID to each entity
            for entity in entities:
                entity['accountId'] = account_id
                entity_types_set.add((entity['domain'], entity['entityType']))
            
            # Write entities for this account to a separate text file
            write_entities_to_txt(entities, f'entities_{account_id}.txt')
            
            # Calculate entity counts by type for this account
            entity_type_counts = {}
            for entity in entities:
                entity_type = entity['entityType']
                if entity_type in entity_type_counts:
                    entity_type_counts[entity_type] += 1
                else:
                    entity_type_counts[entity_type] = 1
            
            # Print summary for this account
            print(f"\nEntity Counts by Type for account {account_id}:")
            for entity_type, count in entity_type_counts.items():
                print(f"{entity_type}: {count}")
            print(f"Total entities fetched for account {account_id}: {len(entities)}\n")
            
            # Update global entity counts
            for entity_type, count in entity_type_counts.items():
                if entity_type in global_entity_type_counts:
                    global_entity_type_counts[entity_type] += count
                else:
                    global_entity_type_counts[entity_type] = count
            
            # Add entities to the global list
            all_entities.extend(entities)
    
    # Write all entities to a CSV file
    write_entities_to_csv(all_entities)
    print(f"All entities have been written to 'entities.csv'.")
    
    # Write domain and entity type pairs to a CSV file
    with open('entity_types.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['domain', 'entityType'])
        writer.writeheader()
        for domain, entity_type in entity_types_set:
            writer.writerow({'domain': domain, 'entityType': entity_type})
    print(f"Domain and entity type pairs have been written to 'entity_types.csv'.")
    
    # Write all entities to a single text file
    write_entities_to_txt(all_entities, 'entities.txt')
    print(f"All entities have been written to 'entities.txt'.")
    
    # Print global summary of entity counts by type across all accounts
    print("\nGlobal Entity Counts by Type (All Accounts):")
    for entity_type, count in global_entity_type_counts.items():
        print(f"{entity_type}: {count}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch entities from New Relic NerdGraph API.")
    parser.add_argument('--max_threads', type=int, default=1, help='Maximum number of threads to use (default: 5)')
    args = parser.parse_args()
    main(max_threads=args.max_threads)