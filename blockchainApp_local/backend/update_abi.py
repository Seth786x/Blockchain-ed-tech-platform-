"""
Extract contract ABI and update frontend Web3 store
"""
import json
import os

def extract_and_update_abi():
    # Path to contract artifact
    artifact_path = "../smart-contracts/artifacts/contracts/EdTechDonation.sol/EdTechDonation.json"
    web3_store_path = "../frontend/src/stores/web3.js"
    
    try:
        # Read contract artifact
        with open(artifact_path, 'r') as f:
            artifact = json.load(f)
        
        # Extract ABI
        abi = artifact['abi']
        
        # Convert ABI to JavaScript format
        abi_js = json.dumps(abi, indent=2)
        
        # Read current web3.js file
        with open(web3_store_path, 'r') as f:
            web3_content = f.read()
        
        # Replace the empty ABI array
        old_abi = """const DONATION_CONTRACT_ABI = [
  // Add your contract ABI here
]"""
        
        new_abi = f"""const DONATION_CONTRACT_ABI = {abi_js}"""
        
        # Update the file
        updated_content = web3_content.replace(old_abi, new_abi)
        
        with open(web3_store_path, 'w') as f:
            f.write(updated_content)
        
        print("✅ Successfully updated Web3 store with contract ABI")
        print(f"📝 ABI has {len(abi)} functions/events")
        
        # List the main functions
        functions = [item['name'] for item in abi if item['type'] == 'function']
        events = [item['name'] for item in abi if item['type'] == 'event']
        
        print(f"🔧 Functions: {', '.join(functions[:5])}...")
        print(f"📡 Events: {', '.join(events)}")
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("💡 Make sure you've compiled the smart contracts first:")
        print("   cd smart-contracts && npx hardhat compile")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    extract_and_update_abi()
