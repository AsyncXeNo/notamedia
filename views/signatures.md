### **/signatures/new** POST
- Endpoint for creating a new signature
- **Access**:
    - SuperAdmin: Yes
    - Worker: Yes
    - Client: No
- **Request Payload:**
    - unique_name*: string
    - sender_full_name*: string
    - sender_short_name*: string
    - sender_designation*: string
    - sender_phone*: string
    - sender_email*: string
    - sender_company_website*: string
    - sender_picture*: base64 encoded string of image
    - sender_company_name*: string
- **Response Payload:**
    - signature_id: string,
    - unique_name: string

---

### **/signatures/delete** DELETE
- Endpoint for deleting a signature
- **Access**:
    - SuperAdmin: Yes
    - Worker: No
    - Client: No
- **Request Payload:**
    - unique_name*: string
- **Response Payload:**

---

### **/signatures/update** PUT
- Endpoint for updating a signature
- **Access**:
    - SuperAdmin: Yes
    - Worker: Yes
    - Client: No
- **Request Payload:**
    - unique_name*: string
    - new*: dictionary
        - sender_full_name: string
        - sender_short_name: string
        - sender_designation: string
        - sender_phone: string
        - sender_email: string
        - sender_company_website: string
        - sender_picture: base64 encoded string of image
        - sender_company_name: string
- **Response Payload:**

---

### **/signatures** GET
- Endpoint for fetching all signatures
- **Access**:
    - SuperAdmin: Yes
    - Worker: No
    - Client: No
- **Request Payload:**
    - unique_name*: string
- **Response Payload:**
    - list of all signatures