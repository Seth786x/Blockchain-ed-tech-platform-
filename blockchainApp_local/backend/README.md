# EdTech Hardware Learning Platform - Backend

A FastAPI-based backend for the blockchain-powered educational platform focused on computer hardware learning.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud)
- pip

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
# Copy the example config (optional - defaults are provided)
cp .env.example .env
```

3. **Start MongoDB:**
```bash
# Local MongoDB
mongod

# Or use MongoDB Atlas (cloud)
# Update MONGODB_URL in config.py
```

4. **Initialize database with sample data:**
```bash
python init_db.py
```

5. **Start the server:**
```bash
python main.py
```

The API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

## 📊 Database Schema

### Collections

#### Users
```javascript
{
  _id: ObjectId,
  email: String,
  username: String,
  full_name: String,
  role: "student" | "instructor" | "school" | "donor" | "admin",
  wallet_address: String,
  hashed_password: String,
  created_at: Date,
  is_active: Boolean
}
```

#### Courses
```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  component: "cpu" | "gpu" | "ram" | "motherboard" | "storage",
  level: "beginner" | "intermediate" | "advanced",
  instructor_id: String,
  modules: Array,
  thumbnail_url: String,
  price: Number,
  created_at: Date,
  updated_at: Date,
  is_published: Boolean
}
```

#### Enrollments
```javascript
{
  _id: ObjectId,
  student_id: String,
  course_id: String,
  enrolled_at: Date,
  status: String,
  progress_percentage: Number,
  completed_modules: Array
}
```

#### Donations
```javascript
{
  _id: ObjectId,
  donor_id: String,
  amount_eth: Number,
  amount_usd: Number,
  transaction_hash: String,
  purpose: String,
  target_school_id: String,
  status: "pending" | "confirmed" | "allocated" | "completed",
  created_at: Date,
  confirmed_at: Date
}
```

#### Schools
```javascript
{
  _id: ObjectId,
  name: String,
  address: String,
  contact_email: String,
  contact_phone: String,
  principal_name: String,
  wallet_address: String,
  total_students: Number,
  verified: Boolean,
  created_at: Date
}
```

#### Resource Requests
```javascript
{
  _id: ObjectId,
  school_id: String,
  resource_type: "hardware_kit" | "software_license" | "equipment" | "funding",
  description: String,
  quantity: Number,
  estimated_cost_usd: Number,
  priority: Number,
  status: "pending" | "approved" | "allocated" | "delivered",
  justification: String,
  created_at: Date,
  updated_at: Date
}
```

## 🔗 API Endpoints

### Authentication (`/api/auth`)

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "role": "student",
  "password": "password123",
  "wallet_address": "0x..."
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>
```

### Courses (`/api/courses`)

#### Get All Courses
```http
GET /api/courses?component=cpu&level=beginner&limit=10&skip=0
```

#### Get Course by ID
```http
GET /api/courses/{course_id}
```

#### Create Course (Instructors/Admins)
```http
POST /api/courses
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Course Title",
  "description": "Course description",
  "component": "cpu",
  "level": "beginner",
  "price": 0.01
}
```

#### Enroll in Course
```http
POST /api/courses/{course_id}/enroll
Authorization: Bearer <token>
```

#### Get Course Progress
```http
GET /api/courses/{course_id}/progress
Authorization: Bearer <token>
```

#### Complete Module
```http
POST /api/courses/{course_id}/modules/{module_id}/complete
Authorization: Bearer <token>
```

### Donations (`/api/donations`)

#### Get Donations
```http
GET /api/donations?status=confirmed&limit=10
Authorization: Bearer <token>
```

#### Create Donation
```http
POST /api/donations
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount_eth": 0.1,
  "purpose": "Hardware equipment",
  "transaction_hash": "0x...",
  "target_school_id": "school_id"
}
```

#### Get Donation Statistics
```http
GET /api/donations/stats/total
```

#### Get Donor Leaderboard
```http
GET /api/donations/leaderboard
```

### Resources (`/api/resources`)

#### Get Schools
```http
GET /api/resources/schools?verified=true&limit=10
```

#### Register School
```http
POST /api/resources/schools
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "School Name",
  "address": "School Address",
  "contact_email": "contact@school.edu",
  "contact_phone": "+1-555-0123",
  "principal_name": "Principal Name",
  "wallet_address": "0x...",
  "total_students": 500
}
```

#### Get Resource Requests
```http
GET /api/resources/requests?status=pending&limit=10
Authorization: Bearer <token>
```

#### Create Resource Request
```http
POST /api/resources/requests
Authorization: Bearer <token>
Content-Type: application/json

{
  "resource_type": "hardware_kit",
  "description": "Computer hardware kits",
  "quantity": 25,
  "estimated_cost_usd": 5000.0,
  "priority": 5,
  "justification": "Students need hands-on experience"
}
```

## 🔑 Test Accounts

After running `python init_db.py`, you can use these test accounts:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@edtech.com | admin123 |
| Instructor | instructor@edtech.com | instructor123 |
| Student | student@edtech.com | student123 |
| Donor | donor@edtech.com | donor123 |
| School | school@edtech.com | school123 |

## 🧪 Testing the API

### Using curl

1. **Login and get token:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "student@edtech.com", "password": "student123"}'
```

2. **Get courses (with token):**
```bash
curl -X GET "http://localhost:8000/api/courses" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

3. **Get donation statistics:**
```bash
curl -X GET "http://localhost:8000/api/donations/stats/total"
```

### Using the Interactive API Docs

Visit http://localhost:8000/docs for the interactive Swagger UI documentation.

## 🔧 Configuration

Update `config.py` or set environment variables:

```bash
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=edtech_hardware

# JWT
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production
```bash
# Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000

# Using gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📝 Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=edtech_hardware

# JWT
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Blockchain
ETHEREUM_RPC_URL=https://sepolia.infura.io/v3/your-infura-project-id
PRIVATE_KEY=your-private-key-for-deployment

# IPFS
IPFS_API_URL=http://localhost:5001

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Connection Error:**
   - Ensure MongoDB is running
   - Check connection string in config.py
   - Verify network connectivity

2. **Import Errors:**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **JWT Token Issues:**
   - Verify SECRET_KEY is set
   - Check token expiration time

4. **CORS Errors:**
   - Update ALLOWED_ORIGINS in config.py
   - Ensure frontend URL is included

## 📚 Next Steps

1. **Frontend Integration:** Connect the Vue.js frontend
2. **Blockchain Integration:** Implement smart contract calls
3. **IPFS Integration:** Add file upload/download functionality
4. **Testing:** Add comprehensive test suite
5. **Deployment:** Deploy to production environment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Built with ❤️ for transparent education funding and computer hardware learning.** 