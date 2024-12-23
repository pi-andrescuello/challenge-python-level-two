
# Flask Project

<p align="center">
  <img align="center" width="100%" src="https://res.cloudinary.com/five-drive/image/upload/v1723133464/yndodcscs6z7e1br7ahf.png"/>
</p>

This is a Flask-based application with a structured project layout, Docker support, and testing capabilities. It includes authentication, client management, and external services integration.


## Installation

To get started with this project, follow these steps:

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. **Set Up the Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**

    Create a `.env` file in the root directory and add the necessary environment variables. You can use the `.env.example` file as a reference.

5. **Run Migrations**

    ```bash
    flask db upgrade
    ```

6. **Run the Application**

    ```bash
    python main.py
    ```

## Docker

To build and run the application using Docker, use the provided Docker configurations:

1. **Build and Run for Development**

    ```bash
    docker-compose -f docker/develop/docker-compose.yml up --build
    ```

2. **Build and Run for Testing**

    ```bash
    docker-compose -f docker/testing/docker-compose.yml up --build
    ```

3. **Build and Run for Production**

    ```bash
    docker-compose -f docker/production/docker-compose.yml up --build
    ```

## Testing

To run tests, activate the virtual environment and use `pytest`:

```bash
pytest