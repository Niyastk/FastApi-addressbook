# FastAPI Address CRUD App

This is a simple FastAPI application for performing CRUD (Create, Read, Update, Delete) operations on addresses. The app allows users to manage address records, including creating new addresses, listing all addresses, retrieving a single address by ID, updating an address, and deleting an address. Additionally, it provides functionality to retrieve addresses within a given distance and location coordinates.

## Features

- **Create new address:** Allows users to add a new address with a name, latitude, and longitude.
- **List all addresses:** Retrieves a list of all addresses stored in the database.
- **Retrieve address by ID:** Retrieves a single address record by its unique identifier (ID).
- **Update address:** Allows users to update the details of an existing address.
- **Delete address:** Deletes an address record from the database.
- **Retrieve addresses within a given distance:** Retrieves addresses that are within a specified distance from a given location coordinates.

## Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    ```

2. Navigate to the project directory:

    ```bash
    cd <project_directory>
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
4. create a .env file in the root directory
    ```bash
    touch .env
    ```
    add the following databse url in the .env file

    ```bash
    SQLALCHEMY_DATABASE_URL=sqlite:///./db/address_app.db
    ```
    
4. Run the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

## Testing

You can test the API endpoints using tools like `curl`, `Postman`, or built in Swagger.

### Example Requests

1. **Create new address:**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"address": "New York City", "latitude": 40.7128, "longitude": -74.006}' http://localhost:8000/addresses/
    ```
    Please note that there are validations for these items
    - **Latitude Validation**: Latitude values are validated to be between -90 and 90 degrees.
    - **Longitude Validation**: Longitude values are validated to be between -180 and 180 degrees.


    These are some of the test data for easy use

    ```bash
        {
            "address": "123 Main St, Anytown, USA",
            "latitude": 40.7128,
            "longitude": -74.006
        },
        {
            "address": "456 Elm St, Springfield, USA",
            "latitude": 40.7282,
            "longitude": -73.7949
        },
        {
            "address": "789 Oak St, Rivertown, USA",
            "latitude": 40.7128,
            "longitude": -74.006
        },
        {
            "address": "101 Pine St, Lakeside, USA",
            "latitude": 41.8781,
            "longitude": -87.6298
        },
        {
            "address": "202 Cedar St, Hillside, USA",
            "latitude": 41.789,
            "longitude": -87.597
        }
    ```


2. **List all addresses:**

    ```bash
    curl http://localhost:8000/addresses_all/
    ```

3. **Retrieve address by ID:**

    ```bash
    curl http://localhost:8000/addresses/<address_id>
    ```

4. **Update address:**

    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"address": "Updated Address", "latitude": 40.1234, "longitude": -75.4321}' http://localhost:8000/addresses/<address_id>
    ```
    ***Note***: Adding data with the same latitude and longitude will result in an error due to validation checks to ensure data uniqueness


5. **Delete address:**

    ```bash
    curl -X DELETE http://localhost:8000/addresses/<address_id>
    ```

6. **Retrieve addresses within a given distance:**

    ```bash
    curl "http://localhost:8000/nearby_adresses?latitude=40.7128&longitude=-74.006&distance=10"
    ```
    This dataset is suitable for testing purposes. You can increase the distance parameter to retrieve additional data.
     ```bash
        {"latitude": 40.7306,"longitude": -73.9352,"distance": 20}
     ```

## Main Dependencies

This project relies on several external dependencies to function properly. Here's a list of the main ones:

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **SQLAlchemy**: A powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Geopy**: A Python library that makes it easy to locate the coordinates of addresses, cities, countries, and landmarks across the globe.
- **Black**: Ensures consistent Python code formatting according to the PEP 8 style guide.
- **loguru**: Facilitates comprehensive event logging, with all logged events stored in a dedicated file named `app.log`.
