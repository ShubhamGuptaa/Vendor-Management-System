*** Vendor Management System ***

* Introducing VMS *
This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

** Requirements **
- Python version 3.x
- Django Version 4.x

** Quick Installation & Setup **
- Clone the repository using the command
git clone https://www.github.com/ShubhamGuptaa/

- Create a virtual environment 
virtualenv venv or python3 -m venv myenv

- Install all the requirements using the command
pip install -r requirements.txt

- Create all the tables and schemas into the database using the command
python manage.py makemigrations
python manage.py migrate

- Start the django server using the command
python manage.py runserver


** Vendor Profile Management: **

*API Endpoints*
1. To create a new vendor
url: http://127.0.0.1:8000/api/vendors/ [POST Method]
Request Body:
{
    "name":"vemdor_name",
    "contact_number":"mobile_no.",
    "address":"address"
}

2. List all vendors
url: http://127.0.0.1:8000/api/vendors/ [GET Method]

3. Retrieve a specific vendor's details.
url: http://127.0.0.1:8000/api/vendors/{vendor_id}/ [GET Method]

4. To Update a vendor's details.
url: http://127.0.0.1:8000/api/vendors/{vendor_id}/ [PUT Method]
Request Body:
{
    "name":"vemdor_name",
    "contact_number":"mobile_no.",
    "address":"address"
}

5. Delete a vendor.
url: http://127.0.0.1:8000/api/vendors/{vendor_id}/ [DELETE Method]


** Purchase Order Tracking: **

*API Endpoints*
1. Create a purchase order.
url: http://127.0.0.1:8000/api/purchase_orders/ [POST Method]
Request Body:
{
  "vendor_id" : 1,
  "items": {
    "item 1": "qty",
    "item 2": "qty"
  }
}
Note: It will return a message with your PO number and Expected Delivery Date.
    - Initially the status will be 0 means pending for the PO , 0 means pending, 1 means completed and 2 means canceled.

2. List all purchase orders with an option to filter by vendor.
url: http://127.0.0.1:8000/api/purchase_orders/ [GET Method]

3. Retrieve details of a specific purchase order.
url: http://127.0.0.1:8000/api/purchase_orders/{po_id} [GET Method]

4. Update a purchase order.
url: http://127.0.0.1:8000/api/purchase_orders/{po_id} [PUT Method]
Request Body:
{
  "vendor_id" : 1,
  "items": {
    "item 1": "qty",
    "item 2": "qty"
  },
    "status":1,
    "quality_rating":5
}

5. Delete a purchase order.
url: http://127.0.0.1:8000/api/purchase_orders/{po_id} [DELETE Method]


** For vendors to acknowledge POs. **
- http://127.0.0.1:8000/api/purchase_orders/{po_id}/acknowledge [POST Method]
This endpoint will update acknowledgment_date and trigger the recalculation
of average_response_time.

** Retrieves the calculated performance metrics for a specific vendor. **
- http://127.0.0.1:8000/api/vendors/{vendor_id}/performance

It will return data including on_time_delivery_rate, quality_rating_avg, average_response_time, and fulfillment_rate.

Note:
- Here assuming the expected delivery date will be after 4 days from the date of purchage order.
- We have used signals here so that if any changes in purchage order models will automatically changes the performance metrics of the vendor.

DOC reference:- https://drive.google.com/file/d/1hLWc35hpLQ0EPDAZjZloomeAxgn3V7g9/view
