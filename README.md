### Vendor Management System
## Description
This is a Vendor Management System developed using Django and Django REST Framework. The system manages vendor profiles, tracks purchase orders, and calculates vendor performance metrics.

## Setup
## Prerequisites
Python (3.x recommended)
Django
Django REST Framework
Other dependencies (specified in requirements.txt)

## Installation
Clone the repository:
Copy code
```
git clone https://github.com/your-username/your-project.git
cd your-project
```
Create a virtual environment:
Copy code
```
python -m venv venv
```

Activate the virtual environment:

Copy code
```
venv\Scripts\activate
```

Install dependencies:

Copy code
```
pip install -r requirements.txt
```

Apply database migrations:

Copy code
```
python manage.py makemigrations
python manage.py migrate
```

Run the development server:

Copy code
```
python manage.py runserver
```

## API Endpoints
Document with sample API(Request Body, response etc): <a href="https://docs.google.com/document/d/1L-MSVn9qpE5R5A45_hb-RtaEkuCoKzsDPn45xuUnLDQ/edit?usp=sharing">API Documentaion</a>

You will also get API collection file in this project. Check for the file with the name "API-collection_VendorsManagement".
Register a new user: POST /api/users/register/
Login: POST /api/users/login/
Logout: DELETE /api/users/logout/

Vendor Profiles:
Create a new vendor: POST /api/vendors/
List all vendors: GET /api/vendors/
Retrieve a specific vendor's details: GET /api/vendors/{vendor_id}/
Update a vendor's details: PUT /api/vendors/{vendor_id}/
Delete a vendor: DELETE /api/vendors/{vendor_id}/
Purchase Orders:

Create a purchase order: POST /api/purchase_orders/
List all purchase orders: GET /api/purchase_orders/
Retrieve details of a specific purchase order: GET /api/purchase_orders/{po_id}/
Update a purchase order: PUT /api/purchase_orders/{po_id}/
Delete a purchase order: DELETE /api/purchase_orders/{po_id}/
Vendor Performance:


Testing APIs
You can test the APIs using tools like Postman or curl. Ensure you include the necessary headers and request bodies as described in the API documentation.
