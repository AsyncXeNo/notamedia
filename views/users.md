### **/users/login** POST
- Endpoint for user login
- **Access**:
    - SuperAdmin: Yes
    - Worker: Yes
    - Client: Yes
- **Request Payload:**
    - username*: string
    - password*: string
- **Response Payload:**
    - name: string
    - type: integer
    - token: string

---

### **/users/new** POST
- Endpoint for user registration
- **Access**:
    - SuperAdmin: Yes
    - Worker: No
    - Client: No
- **Request Payload:**
    - username*: string
    - password*: string
    - user_type*: integer
    - is_active*: boolean
- **Response Payload:**
    - user_id: string
    - username: string
    - is_active: boolean

---

### **/users/delete** DELETE
- Endpoint for user deletion
- **Access**:
    - SuperAdmin: Yes
    - Worker: No
    - Client: No
- **Request Payload:**
    - username*: string
- **Response Payload:**

---

### **/users/update** PUT
- Endpoint for user updation
- **Access**:
    - SuperAdmin: Yes
    - Worker: No
    - Client: No
- **Request Payload:**
    - username*: string
    - new*: dictionary
        - password: string
        - active: boolean
- **Response Payload:**

---

### **/users** GET
- Endpoint for fetching all users
- **Access**:
    - SuperAdmin: Yes
    - Worker: No
    - Client: No
- **Request Payload:**
    - list of all users