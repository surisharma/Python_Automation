import boto3

def delete_archives_and_vault(account_id, vault_name):
    # Create a Glacier client
    glacier = boto3.client('glacier')

    # List the archives in the vault
    response = glacier.list_vaults(accountId=account_id)
    archives = glacier.list_vaults(accountId=account_id, vaultName=vault_name)['ArchiveList']

    # Delete each archive in the vault
    for archive in archives:
        archive_id = archive['ArchiveId']
        glacier.delete_archive(accountId=account_id, vaultName=vault_name, archiveId=archive_id)
        print(f"Deleted archive: {archive_id}")

    print("Waiting for deletion of archives...")

    # Wait for the archives to be deleted
    waiter = glacier.get_waiter('archive_not_exists')
    waiter.wait(accountId=account_id, vaultName=vault_name, archiveId=archive_id)

    print("All archives deleted.")

    # Delete the vault
    glacier.delete_vault(accountId=account_id, vaultName=vault_name)
    print(f"Deleted vault: {vault_name}")

if __name__ == "__main__":
    # Replace with your AWS account ID and Glacier vault name
    aws_account_id = 'YOUR_AWS_ACCOUNT_ID'
    glacier_vault_name = 'YOUR_GLACIER_VAULT_NAME'

    # Call the function to delete archives and vault
    delete_archives_and_vault(aws_account_id, glacier_vault_name)
