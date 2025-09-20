import requests
import json

# First, login as student
login_data = {
    "email": "student@edtech.com",
    "password": "student123"
}

print("=== TESTING ENROLLED COURSES API ===")

# Login
print("1. Logging in...")
try:
    response = requests.post("http://localhost:8000/api/auth/login", json=login_data)
    print(f"Login status: {response.status_code}")

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        print("✅ Login successful")
        
        # Test enrolled courses
        print("\n2. Fetching enrolled courses...")
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get("http://localhost:8000/api/courses/enrolled", headers=headers)
        print(f"Enrolled courses status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            courses = response.json()
            print(f"✅ Success! Found {len(courses)} enrolled courses:")
            for course in courses:
                if 'course' in course:
                    print(f"  - {course['course']['title']} (ID: {course['course']['_id']})")
                    print(f"    Progress: {course.get('progress_percentage', 0)}%")
                else:
                    print(f"  - Course data missing in enrollment {course.get('_id', 'unknown')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Try to get more debugging info
            print(f"Response content type: {response.headers.get('content-type', 'unknown')}")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("Could not parse error response as JSON")
            
    else:
        print(f"❌ Login failed: {response.text}")
        
except Exception as e:
    print(f"❌ Exception occurred: {e}")
    import traceback
    traceback.print_exc()
