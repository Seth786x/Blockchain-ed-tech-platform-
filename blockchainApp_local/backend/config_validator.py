"""
Configuration validation and environment setup
"""
import os
import sys
from typing import List, Dict, Any
from web3 import Web3
import secrets

class ConfigValidator:
    """Validates and sets up application configuration"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_env_file(self, env_path: str = ".env") -> bool:
        """Validate environment configuration"""
        if not os.path.exists(env_path):
            self.errors.append(f"Environment file {env_path} not found")
            return False
        
        # Check required environment variables
        required_vars = [
            "MONGODB_URL",
            "DATABASE_NAME", 
            "SECRET_KEY",
            "ETHEREUM_RPC_URL",
            "CONTRACT_ADDRESS"
        ]
        
        missing_vars = []
        weak_configs = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
            elif var == "SECRET_KEY" and len(value) < 32:
                weak_configs.append(f"{var} is too short (minimum 32 characters)")
            elif var == "SECRET_KEY" and value in ["your-secret-key", "your-super-secret-key-change-this-in-production"]:
                weak_configs.append(f"{var} is using default value - SECURITY RISK!")
        
        if missing_vars:
            self.errors.extend([f"Missing environment variable: {var}" for var in missing_vars])
        
        if weak_configs:
            self.errors.extend(weak_configs)
        
        return len(self.errors) == 0
    
    def validate_blockchain_config(self) -> bool:
        """Validate blockchain configuration"""
        rpc_url = os.getenv("ETHEREUM_RPC_URL")
        contract_address = os.getenv("CONTRACT_ADDRESS")
        
        if not rpc_url:
            self.errors.append("ETHEREUM_RPC_URL not configured")
            return False
        
        if not contract_address:
            self.errors.append("CONTRACT_ADDRESS not configured")
            return False
        
        # Try to connect to blockchain
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if not w3.is_connected():
                self.errors.append("Cannot connect to Ethereum RPC")
                return False
        except Exception as e:
            self.errors.append(f"Blockchain connection error: {str(e)}")
            return False
        
        # Validate contract address format
        if not Web3.is_address(contract_address):
            self.errors.append("Invalid contract address format")
            return False
        
        return True
    
    def validate_database_config(self) -> bool:
        """Validate database configuration"""
        mongodb_url = os.getenv("MONGODB_URL")
        
        if not mongodb_url:
            self.errors.append("MONGODB_URL not configured")
            return False
        
        # Basic MongoDB URL validation
        if not mongodb_url.startswith("mongodb://") and not mongodb_url.startswith("mongodb+srv://"):
            self.errors.append("Invalid MongoDB URL format")
            return False
        
        return True
    
    def generate_secure_config(self) -> Dict[str, str]:
        """Generate secure configuration values"""
        return {
            "SECRET_KEY": secrets.token_urlsafe(64),
            "PRIVATE_KEY": "0x" + secrets.token_hex(32),
            "API_KEY": secrets.token_urlsafe(32)
        }
    
    def create_secure_env_template(self, output_path: str = ".env.template") -> None:
        """Create a secure environment template"""
        secure_config = self.generate_secure_config()
        
        template = f"""# EdTech Blockchain App Configuration
# Copy this file to .env and update the values

# Database Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=edtech_hardware

# Security Configuration (CHANGE THESE!)
SECRET_KEY={secure_config['SECRET_KEY']}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Blockchain Configuration
ETHEREUM_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
CONTRACT_ADDRESS=YOUR_DEPLOYED_CONTRACT_ADDRESS
PRIVATE_KEY=YOUR_DEPLOYMENT_PRIVATE_KEY

# Server Configuration
HOST=127.0.0.1
PORT=8000
DEBUG=False

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:5173","http://localhost:3000"]
"""
        
        with open(output_path, 'w') as f:
            f.write(template)
        
        print(f"✅ Secure environment template created: {output_path}")
    
    def validate_all(self) -> bool:
        """Run all validation checks"""
        print("🔍 Validating application configuration...")
        
        env_valid = self.validate_env_file()
        db_valid = self.validate_database_config()
        blockchain_valid = self.validate_blockchain_config()
        
        if self.errors:
            print("❌ Configuration errors found:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print("⚠️  Configuration warnings:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        all_valid = env_valid and db_valid and blockchain_valid
        
        if all_valid:
            print("✅ All configuration checks passed!")
        else:
            print("❌ Configuration validation failed!")
            print("💡 Run create_secure_env_template() to generate a secure template")
        
        return all_valid

def main():
    """Run configuration validation"""
    validator = ConfigValidator()
    
    if len(sys.argv) > 1 and sys.argv[1] == "template":
        validator.create_secure_env_template()
    else:
        validator.validate_all()

if __name__ == "__main__":
    main()
