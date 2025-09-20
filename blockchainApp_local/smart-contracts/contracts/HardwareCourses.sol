// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract HardwareCourses is Ownable, ReentrancyGuard {
    struct Course {
        uint256 id;
        string title;
        string description;
        uint256 price; // in wei (1 eth = 10^18 wei)
        bool active;
    }

    // Storage
    mapping(uint256 => Course) public courses;
    mapping(address => mapping(uint256 => bool)) public userCourses; // user => courseId => purchased
    uint256 public courseCount;

    // Events
    event CoursePurchased(address indexed buyer, uint256 indexed courseId, uint256 price);
    event CourseAdded(uint256 indexed courseId, string title, uint256 price);
    event CourseUpdated(uint256 indexed courseId, string title, uint256 price);

    // Course prices in wei (very small amounts for testing)
    uint256 public constant BASIC_PRICE = 0.000005 ether;     // ~$0.01 at current ETH prices
    uint256 public constant STANDARD_PRICE = 0.00001 ether;   // ~$0.02 at current ETH prices

    constructor() Ownable(msg.sender) {
        // Add initial courses
        addCourse("GPU Evolution: From CGA to RTX", "Complete history and working principles of graphics cards", BASIC_PRICE);
        addCourse("CPU Architecture: Pentium to Modern Era", "Evolution of processors and multi-threading concepts", BASIC_PRICE);
        addCourse("Motherboard Development Timeline", "Changes in motherboard architecture and features", BASIC_PRICE);
        addCourse("Storage Technology Evolution", "From punch cards to SSDs and NVMe drives", BASIC_PRICE);
        addCourse("Computer Memory Deep Dive", "RAM evolution and working principles", BASIC_PRICE);
    }

    function addCourse(string memory title, string memory description, uint256 price) public onlyOwner {
        courseCount++;
        courses[courseCount] = Course(courseCount, title, description, price, true);
        emit CourseAdded(courseCount, title, price);
    }

    function purchaseCourse(uint256 courseId) public payable nonReentrant {
        require(courseId > 0 && courseId <= courseCount, "Invalid course");
        require(courses[courseId].active, "Course not available");
        require(!userCourses[msg.sender][courseId], "Already purchased");
        require(msg.value == courses[courseId].price, "Incorrect payment amount");

        userCourses[msg.sender][courseId] = true;
        emit CoursePurchased(msg.sender, courseId, msg.value);
    }

    function updateCourse(uint256 courseId, string memory title, string memory description, uint256 price, bool active) public onlyOwner {
        require(courseId > 0 && courseId <= courseCount, "Invalid course");
        Course storage course = courses[courseId];
        course.title = title;
        course.description = description;
        course.price = price;
        course.active = active;
        emit CourseUpdated(courseId, title, price);
    }

    function getCourse(uint256 courseId) public view returns (Course memory) {
        require(courseId > 0 && courseId <= courseCount, "Invalid course");
        return courses[courseId];
    }

    function hasPurchased(address user, uint256 courseId) public view returns (bool) {
        return userCourses[user][courseId];
    }

    // Allow owner to withdraw course purchase funds
    function withdrawCourseFunds() external onlyOwner {
        uint256 balance = address(this).balance;
        require(balance > 0, "No funds to withdraw");
        
        (bool success, ) = payable(owner()).call{value: balance}("");
        require(success, "Transfer failed");
    }

    // Get all active courses
    function getActiveCourses() external view returns (uint256[] memory) {
        uint256[] memory activeCourses = new uint256[](courseCount);
        uint256 activeCount = 0;
        
        for (uint256 i = 1; i <= courseCount; i++) {
            if (courses[i].active) {
                activeCourses[activeCount] = i;
                activeCount++;
            }
        }
        
        // Resize array to actual count
        uint256[] memory result = new uint256[](activeCount);
        for (uint256 i = 0; i < activeCount; i++) {
            result[i] = activeCourses[i];
        }
        
        return result;
    }
}
