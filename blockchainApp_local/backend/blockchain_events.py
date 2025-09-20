import os
import time
import threading
from web3 import Web3
from dotenv import load_dotenv
from pymongo import MongoClient
import json
from typing import Any, Dict, Optional

load_dotenv()

# Load config
ETHEREUM_RPC_URL = os.getenv("ETHEREUM_RPC_URL", "https://sepolia.infura.io/v3/your-infura-project-id")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")  # Set this in your .env
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "edtech_hardware")

# Check if we have valid configuration
def is_valid_config():
    """Check if blockchain configuration is valid"""
    if not ETHEREUM_RPC_URL or "YOUR_INFURA_PROJECT_ID" in ETHEREUM_RPC_URL.upper():
        return False
    if not CONTRACT_ADDRESS or CONTRACT_ADDRESS == "YOUR_DEPLOYED_CONTRACT_ADDRESS":
        return False
    return True

# Only initialize blockchain connection if config is valid
w3: Optional[Web3] = None
contract = None

if is_valid_config():
    try:
        w3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))
        if w3.is_connected():
            print(f"[BlockchainEvents] ✅ Connected to Ethereum node")
        else:
            print(f"[BlockchainEvents] ❌ Failed to connect to Ethereum node")
            w3 = None
    except Exception as e:
        print(f"[BlockchainEvents] ❌ Blockchain connection error: {e}")
        w3 = None
else:
    print(f"[BlockchainEvents] ⚠️  Blockchain not configured - using placeholder values")
    print(f"[BlockchainEvents] 💡 Update ETHEREUM_RPC_URL and CONTRACT_ADDRESS in .env file")

# Load ABI safely
try:
    abi_path = os.path.join(os.path.dirname(__file__), '../smart-contracts/artifacts/contracts/EdTechDonation.sol/EdTechDonation.json')
    with open(abi_path, 'r') as f:
        contract_artifact = json.load(f)
        CONTRACT_ABI = contract_artifact['abi']
except FileNotFoundError:
    print("[BlockchainEvents] Warning: Contract ABI file not found")
    CONTRACT_ABI = []  # Empty ABI as fallback

# Initialize another w3 instance to ensure we have a clean connection
if w3 is None and is_valid_config():
    try:
        w3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))
    except Exception:
        w3 = None

# Initialize contract safely
contract = None
if CONTRACT_ABI and CONTRACT_ADDRESS and Web3.is_address(CONTRACT_ADDRESS) and w3 and w3.is_connected():
    try:
        contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
        print(f"[BlockchainEvents] ✅ Contract initialized at {CONTRACT_ADDRESS}")
    except Exception as e:
        print(f"[BlockchainEvents] ❌ Error initializing contract: {e}")
else:
    print(f"[BlockchainEvents] ⚠️  Contract not initialized - missing ABI or invalid address")

mongo = MongoClient(MONGODB_URL)
db = mongo[DATABASE_NAME]
donations_col = db['donations']

# Listen for DonationReceived events
def listen_donation_events():
    """Listen for blockchain donation events and sync to database"""
    if not contract or not w3 or not w3.is_connected():
        print("[BlockchainEvents] Contract or Web3 not initialized, skipping event listener")
        return
        
    print("[BlockchainEvents] Listening for DonationReceived events...")
    
    try:
        last_block = w3.eth.block_number
    except Exception as e:
        print(f"[BlockchainEvents] Error getting block number: {e}")
        return
    
    while True:
        try:
            event_filter = contract.events.DonationReceived.create_filter(from_block=last_block + 1)
            for event in event_filter.get_all_entries():
                donor = event['args']['donor']
                donationId = int(event['args']['donationId'])
                amount = int(event['args']['amount'])
                purpose = event['args']['purpose']
                txHash = event['transactionHash'].hex()
                blockNumber = event['blockNumber']
                
                # Safely get block timestamp
                try:
                    block_data = w3.eth.get_block(blockNumber)
                    timestamp = block_data.get('timestamp', int(time.time()))
                except Exception as e:
                    print(f"[BlockchainEvents] Error getting block timestamp: {e}")
                    timestamp = int(time.time())
                
                # Store donation event in database
                donations_col.update_one(
                    {"transaction_hash": txHash},
                    {"$set": {
                        "donor_address": donor,
                        "donation_id": donationId,
                        "amount": amount,
                        "purpose": purpose,
                        "transaction_hash": txHash,
                        "block_number": blockNumber,
                        "timestamp": timestamp,
                        "status": "confirmed"
                    }},
                    upsert=True
                )
                print(f"[BlockchainEvents] Synced donation: {donor} donated {amount} wei for {purpose}")
                last_block = max(last_block, blockNumber)
        except Exception as e:
            print(f"[BlockchainEvents] Error: {e}")
        time.sleep(10)  # Poll every 10 seconds

def start_listener():
    """Start the blockchain event listener in a background thread"""
    if contract and w3 and w3.is_connected():
        t = threading.Thread(target=listen_donation_events, daemon=True)
        t.start()
        print("[BlockchainEvents] ✅ Event listener started")
    else:
        print("[BlockchainEvents] ⚠️  Event listener not started - blockchain connection not available")
        print("[BlockchainEvents] 💡 App will work without blockchain events (using API only)")