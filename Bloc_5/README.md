Link to video : https://share.vidyard.com/watch/LEAubTFd3yKNarZLrJ3DnB?

## Project Overview
GetAround is a car rental platform where users can rent cars from individuals for a specific duration, ranging from a few hours to a few days. The goal of this project is to analyze the rental process and implement a minimum delay between two rentals to mitigate issues related to late returns at checkout. By preventing back-to-back rentals with insufficient time for the car to be returned, the project aims to reduce friction for the next driver and improve overall user satisfaction.

### Project Structure
The repository is organized as follows:

* `data` : Contains the dataset files used for the analysis and machine learning.
* `notebooks`: Jupyter notebooks containing the data analysis and machine learning code.
* `web_dashboard`: Code and resources for the web dashboard used for data visualization and analysis.
* `api`: Code and resources for the API implementation, including the `/predict_price` endpoint for pricing optimization.
* `docs` : Documentation files for the project.

### Setup and Installation
To set up the project locally, follow these steps:

* Clone the repository: `git clone https://github.com/your-username/getaround.git`
* Navigate to the project directory: `cd getaround`
* Install the required dependencies: `pip install -r requirements.txt`

### Data Analysis
The data analysis is performed using Jupyter notebooks available in the notebooks directory. The notebooks cover various analyses, including the impact of late check-ins, owner's revenue affected by the minimum delay feature, and problematic cases solved based on different thresholds and scopes. The analysis provides insights into the rental process and helps inform decision-making.

### Web Dashboard
The `web_dashboard` directory contains the code for a web-based dashboard that visualizes the analysis results. The dashboard is built using the Streamlit framework and provides an interactive interface to explore the data insights. To run the dashboard locally, use the following command: streamlit run app.py.

### API - Pricing Optimization
The `api` directory contains the code and resources for the API implementation. The API includes an endpoint `/predict` that uses machine learning models to suggest optimum prices for car owners. The endpoint accepts POST requests with JSON input data and returns the predicted prices. Detailed documentation for the API can be found in the `/docs` endpoint of the deployed API.

### Documentation
The /docs directory contains documentation files for the project. It includes information about the project, setup instructions, and API documentation. The API documentation provides details about the endpoints, required input, and expected output.

### Online Deployment
The project is deployed online for easy access. You can find the deployed web dashboard and API at the following URLs:

Web Dashboard: `https://chris-getaround-streamlit.herokuapp.com`
API Endpoint: `https://chris-getaround-api.herokuapp.com/docs`
