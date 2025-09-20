const hre = require("hardhat");

async function main() {
  console.log("🚀 Deploying EdTechDonation smart contract...");

  // Get the contract factory
  const EdTechDonation = await hre.ethers.getContractFactory("EdTechDonation");
  
  // Deploy the contract
  const edTechDonation = await EdTechDonation.deploy();
  
  // Wait for deployment to finish
  await edTechDonation.waitForDeployment();
  
  const contractAddress = await edTechDonation.getAddress();
  
  console.log("✅ EdTechDonation deployed to:", contractAddress);
  console.log("📋 Contract Address:", contractAddress);
  console.log("🌐 Network:", hre.network.name);
  
  // Save contract address to a file for frontend use
  const fs = require('fs');
  const contractInfo = {
    address: contractAddress,
    network: hre.network.name,
    deployedAt: new Date().toISOString(),
    deployer: await edTechDonation.signer.getAddress()
  };
  
  fs.writeFileSync(
    './contract-address.json', 
    JSON.stringify(contractInfo, null, 2)
  );
  
  console.log("💾 Contract address saved to contract-address.json");
  
  // Verify contract on Etherscan (if not local network)
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    console.log("🔍 Verifying contract on Etherscan...");
    try {
      await hre.run("verify:verify", {
        address: contractAddress,
        constructorArguments: [],
      });
      console.log("✅ Contract verified on Etherscan");
    } catch (error) {
      console.log("⚠️  Contract verification failed:", error.message);
    }
  }
  
  return contractAddress;
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });
