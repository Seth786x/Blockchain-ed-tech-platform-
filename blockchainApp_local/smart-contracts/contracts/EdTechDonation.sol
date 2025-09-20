// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title EdTechDonation
 * @dev Smart contract for managing transparent donations and resource allocation for educational institutions
 */
contract EdTechDonation is Ownable, ReentrancyGuard {
    
    uint256 private _donationIds;
    uint256 private _schoolIds;
    uint256 private _allocationIds;
    
    // Events
    event DonationReceived(uint256 indexed donationId, address indexed donor, uint256 amount, string purpose);
    event SchoolRegistered(uint256 indexed schoolId, address indexed schoolWallet, string name);
    event SchoolVerified(uint256 indexed schoolId, address indexed verifier);
    event FundsAllocated(uint256 indexed allocationId, uint256 indexed schoolId, uint256 amount, string purpose);
    event FundsWithdrawn(uint256 indexed schoolId, uint256 amount, address indexed recipient);
    
    // Enums
    enum DonationStatus { Pending, Allocated, Withdrawn }
    enum SchoolStatus { Pending, Verified, Suspended }
    
    // Structs
    struct Donation {
        uint256 id;
        address donor;
        uint256 amount;
        string purpose;
        DonationStatus status;
        uint256 timestamp;
        uint256 allocatedToSchool; // 0 if not allocated
    }
    
    struct School {
        uint256 id;
        address walletAddress;
        string name;
        string contactInfo;
        SchoolStatus status;
        uint256 totalReceived;
        uint256 totalWithdrawn;
        uint256 registrationTimestamp;
    }
    
    struct Allocation {
        uint256 id;
        uint256 schoolId;
        uint256 donationId;
        uint256 amount;
        string purpose;
        uint256 timestamp;
        bool withdrawn;
    }
    
    // State variables
    mapping(uint256 => Donation) public donations;
    mapping(uint256 => School) public schools;
    mapping(uint256 => Allocation) public allocations;
    mapping(address => uint256) public schoolByWallet; // wallet => schoolId
    mapping(uint256 => uint256[]) public schoolAllocations; // schoolId => allocationIds[]
    
    uint256 public totalDonations;
    uint256 public totalAllocated;
    uint256 public totalWithdrawn;
    
    // Course purchase logic
    uint256 public coursePrice = 0.000005 ether;
    uint256 public totalCourseFunds; // Track course purchase funds separately

    // Mapping: courseId => buyer address => purchased
    mapping(uint256 => mapping(address => bool)) public coursePurchases;

    // Event for course purchase
    event CoursePurchased(address indexed buyer, uint256 indexed courseId, uint256 amount);
    
    // Modifiers
    modifier onlyVerifiedSchool() {
        uint256 schoolId = schoolByWallet[msg.sender];
        require(schoolId > 0, "Not a registered school");
        require(schools[schoolId].status == SchoolStatus.Verified, "School not verified");
        _;
    }
    
    modifier schoolExists(uint256 schoolId) {
        require(schoolId > 0 && schoolId <= _schoolIds, "School does not exist");
        _;
    }
    
    // Constructor
    constructor() Ownable(msg.sender) {}
    
    /**
     * @dev Receive donations - SIMPLIFIED VERSION FOR DEMO
     */
    function donate(string memory purpose) external payable {
        require(msg.value > 0, "Donation amount must be greater than 0");
        require(bytes(purpose).length > 0, "Purpose cannot be empty");
        
        _donationIds++;
        uint256 donationId = _donationIds;
        
        donations[donationId] = Donation({
            id: donationId,
            donor: msg.sender,
            amount: msg.value,
            purpose: purpose,
            status: DonationStatus.Pending,
            timestamp: block.timestamp,
            allocatedToSchool: 0
        });
        
        totalDonations += msg.value;
        
        emit DonationReceived(donationId, msg.sender, msg.value, purpose);
    }
    
    /**
     * @dev Get donation details
     */
    function getDonation(uint256 donationId) external view returns (
        uint256 id,
        address donor,
        uint256 amount,
        string memory purpose,
        DonationStatus status,
        uint256 timestamp
    ) {
        Donation memory donation = donations[donationId];
        require(donation.id > 0, "Donation does not exist");
        
        return (
            donation.id,
            donation.donor,
            donation.amount,
            donation.purpose,
            donation.status,
            donation.timestamp
        );
    }
    
    /**
     * @dev Get total donations count
     */
    function getDonationCount() external view returns (uint256) {
        return _donationIds;
    }
    
    /**
     * @dev Get contract balance
     */
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
    
    /**
     * @dev Get donation statistics
     */
    function getStats() external view returns (
        uint256 totalDonationsCount,
        uint256 totalDonationsAmount,
        uint256 totalAllocatedAmount,
        uint256 totalWithdrawnAmount,
        uint256 contractBalance
    ) {
        return (
            _donationIds,
            totalDonations,
            totalAllocated,
            totalWithdrawn,
            address(this).balance
        );
    }
    
    /**
     * @dev Register a new school
     */
    function registerSchool(
        address schoolWallet,
        string memory name,
        string memory contactInfo
    ) external onlyOwner {
        require(schoolWallet != address(0), "Invalid school wallet address");
        require(schoolByWallet[schoolWallet] == 0, "School already registered");
        require(bytes(name).length > 0, "Name cannot be empty");
        
        _schoolIds++;
        uint256 schoolId = _schoolIds;
        
        schools[schoolId] = School({
            id: schoolId,
            walletAddress: schoolWallet,
            name: name,
            contactInfo: contactInfo,
            status: SchoolStatus.Pending,
            totalReceived: 0,
            totalWithdrawn: 0,
            registrationTimestamp: block.timestamp
        });
        
        schoolByWallet[schoolWallet] = schoolId;
        
        emit SchoolRegistered(schoolId, schoolWallet, name);
    }
    
    /**
     * @dev Verify a school
     */
    function verifySchool(uint256 schoolId) external onlyOwner schoolExists(schoolId) {
        require(schools[schoolId].status == SchoolStatus.Pending, "School not in pending status");
        
        schools[schoolId].status = SchoolStatus.Verified;
        
        emit SchoolVerified(schoolId, msg.sender);
    }
    
    /**
     * @dev Allocate funds from a donation to a school
     */
    function allocateFunds(
        uint256 donationId,
        uint256 schoolId,
        string memory purpose
    ) external onlyOwner schoolExists(schoolId) {
        require(donationId > 0 && donationId <= _donationIds, "Invalid donation ID");
        require(donations[donationId].status == DonationStatus.Pending, "Donation already allocated");
        require(schools[schoolId].status == SchoolStatus.Verified, "School not verified");
        
        Donation storage donation = donations[donationId];
        School storage school = schools[schoolId];
        
        _allocationIds++;
        uint256 allocationId = _allocationIds;
        
        allocations[allocationId] = Allocation({
            id: allocationId,
            schoolId: schoolId,
            donationId: donationId,
            amount: donation.amount,
            purpose: purpose,
            timestamp: block.timestamp,
            withdrawn: false
        });
        
        schoolAllocations[schoolId].push(allocationId);
        
        donation.status = DonationStatus.Allocated;
        donation.allocatedToSchool = schoolId;
        
        school.totalReceived += donation.amount;
        totalAllocated += donation.amount;
        
        emit FundsAllocated(allocationId, schoolId, donation.amount, purpose);
    }
    
    /**
     * @dev Allow verified schools to withdraw allocated funds
     */
    function withdrawFunds(uint256 allocationId) external onlyVerifiedSchool nonReentrant {
        require(allocationId > 0 && allocationId <= _allocationIds, "Invalid allocation ID");
        
        Allocation storage allocation = allocations[allocationId];
        uint256 schoolId = schoolByWallet[msg.sender];
        
        require(allocation.schoolId == schoolId, "Not authorized for this allocation");
        require(!allocation.withdrawn, "Funds already withdrawn");
        
        allocation.withdrawn = true;
        schools[schoolId].totalWithdrawn += allocation.amount;
        totalWithdrawn += allocation.amount;
        
        // Transfer funds
        (bool success, ) = payable(msg.sender).call{value: allocation.amount}("");
        require(success, "Transfer failed");
        
        emit FundsWithdrawn(schoolId, allocation.amount, msg.sender);
    }
    
    /**
     * @dev Get school's available balance
     */
    function getSchoolBalance(uint256 schoolId) external view schoolExists(schoolId) returns (uint256) {
        return schools[schoolId].totalReceived - schools[schoolId].totalWithdrawn;
    }
    
    /**
     * @dev Get school allocations
     */
    function getSchoolAllocations(uint256 schoolId) external view schoolExists(schoolId) returns (uint256[] memory) {
        return schoolAllocations[schoolId];
    }
    
    /**
     * @dev Get total number of donations
     */
    function getTotalDonations() external view returns (uint256) {
        return _donationIds;
    }
    
    /**
     * @dev Get total number of schools
     */
    function getTotalSchools() external view returns (uint256) {
        return _schoolIds;
    }
    
    /**
     * @dev Get total number of allocations
     */
    function getTotalAllocations() external view returns (uint256) {
        return _allocationIds;
    }
    
    /**
     * @dev Emergency withdrawal with proper safeguards (only owner)
     * Only allows withdrawal of unallocated funds to prevent theft of donations
     */
    function emergencyWithdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        require(balance > 0, "No funds to withdraw");
        
        // Calculate allocated but not withdrawn funds
        uint256 allocatedFunds = totalAllocated - totalWithdrawn;
        uint256 availableForWithdraw = balance - allocatedFunds;
        
        require(availableForWithdraw > 0, "No unallocated funds available for withdrawal");
        
        (bool success, ) = payable(owner()).call{value: availableForWithdraw}("");
        require(success, "Transfer failed");
        
        emit EmergencyWithdraw(owner(), availableForWithdraw);
    }

    // Add emergency withdraw event
    event EmergencyWithdraw(address indexed owner, uint256 amount);

    // Purchase a course
    function purchaseCourse(uint256 courseId) external payable nonReentrant {
        require(msg.value == coursePrice, "Incorrect ETH amount");
        require(!coursePurchases[courseId][msg.sender], "Already purchased");
        require(courseId > 0, "Invalid course ID");

        coursePurchases[courseId][msg.sender] = true;
        totalCourseFunds += msg.value;

        emit CoursePurchased(msg.sender, courseId, msg.value);
    }

    // Check if a user has purchased a course
    function hasPurchased(uint256 courseId, address user) external view returns (bool) {
        return coursePurchases[courseId][user];
    }

    // Owner can update course price
    function setCoursePrice(uint256 newPriceWei) external onlyOwner {
        coursePrice = newPriceWei;
    }
}
