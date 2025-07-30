## Ultralytics Web Automation Framework
   This is a Pytest + Playwright-based automation framework to test core workflows of Ultralytics Hub
(https://hub.ultralytics.com), including dataset upload, project creation, model training, inference, and export functionalities. It uses the Page Object Model (POM) design pattern for maintainability and scalability. It is designed to be realistic, with proper setup/teardown, test data management, and robust error handling. It also includes video recording, screenshots, and Allure reporting for better visibility into test execution.

------------------------------------------------------------------------------------------------------------
## Prerequisites
- Python 3.9+
- Playwright installed (`pip install playwright`)
- Playwright browsers installed (`playwright install`)
- Ultralytics Hub account
- Basic understanding of Pytest and Playwright
------------------------------------------------------------------------------------------------------------
## Tech Stack Used: 
- Python 3.9+
- Playwright
- Pytest
- Allure Reporting
- Video & Screenshot Recording
- Page Object Model (POM)

------------------------------------------------------------------------------------------------------------
## Project Structure
```
.
├── config			#Test config and credentials
│   ├── __init__.py
│   ├── config.py
│   └── settings.json
├── downloads		#Download Files
│   └── model_export
├── logs			#Log files for test execution
├── minimal_requirements.txt
├── model_scripts		#Script to trigger YOLO training
│   └── train_model_script.py
├── pages			#Page Object classes (POM structure)
│   ├── __init__.py
│   ├── base_page.py
│   ├── dashboard_page.py
│   ├── datasets_page.py
│   ├── login_page.py
│   ├── models_page.py
│   ├── projects_page.py
│   └── training_page.py
├── pytest.ini 		#Pytest config (browser, video, logging)
├── README.md		#Project overview and setup guide
├── reports			#Allure results and logs
│   └── allure-results-20250730_190157
├── requirements.txt		#Full list of dependencies
├── run_tests.sh		#Shell script to run tests
├── screenshots                  #Screenshots captured on test failure
│   ├── models_page_test_model_export_in_all_formats[chromium0]_1753898585.png
│   └── models_page_test_train_model[chromium1]_1753898608.png
├── test_data	 		#Dataset, images, test input data
│   ├── coco8.zip
│   ├── inference.jpg
│   ├── model_export_data.py
│   ├── model_interence_data.py
│   └── model_training_data.py
├── tests				#All test scenario files
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_scenario_1_upload_dataset.py
│   ├── test_scenario_2_create_project.py
│   ├── test_scenario_3_train_model.py
│   ├── test_scenario_4_inference.py
│   └── test_scenario_5_model_export.py
├── utils 			          #Helpers, CLI triggers, logger
│   ├── __init__.py
│   ├── cli_connection.py
│   ├── helpers.py
│   └── logger.py
├── videos			        #Playwright screen recordings
    ├── 693b44cfd4211e5b404e499a3d538029.webm
    ├── weights
    └── hub


```
------------------------------------------------------------------------------------------------------------
## Features 
-  Config-driven: `settings.json` handles secrets & URLs
-  Modular: Clear POM structure for maintainability
-  Videos + Screenshots for every test step
-  Allure-ready with logging and custom metadata
-  Handles real-world async behaviors (model training, export)
-  Built with realistic naming, setup/teardown, test data

------------------------------------------------------------------------------------------------------------
## Scenarios Covered

| Scenario              | Description                                                  |
|-----------------------|------------------------------------------------------------- |
| Upload Dataset        | Upload `coco8.zip` to Datasets section                       |
| Create Project        | Link uploaded dataset to a new project                       |
| Train Model           | Start training via Ultralytics BYO agent                     |
| Inference             | Upload image and validate predictions (vase, potted plant)   |
| Export Model          | Export YOLO11n in all supported formats (ONNX, CoreML, etc.) |

------------------------------------------------------------------------------------------------------------
## Setup Instructions
1. Clone the Project
    `git clone <your-repo-url>`
    `cd qa_automation_ultralytics`

2. Create & Activate Virtual Env
    `python -m venv venv`
    `source venv/bin/activate`   # on Windows: `venv\Scripts\activate`

3. Install Dependencies
    `pip install -r requirements.txt`
    `playwright install`

4. Update Configuration
     Edit config/settings.json:

   {
       "base_url": "https://hub.ultralytics.com",
       "username": "your_email@example.com",
       "password": "your_password",
   }

5. Create .env File
    `TEST_USERNAME=<your_ultralytics_username>`
    `TEST_PASSWORD=<your_ultralytics_password>`

6. Export Environment Variables
    `export TEST_USERNAME="<your_ultralytics_username>"`
    `export TEST_PASSWORD="<your_ultralytics_password>"`

------------------------------------------------------------------------------------------------------------
## Running Tests
Single Test
`pytest tests/<your-test-name>.py --headed`

Run All Tests Squentially
    Run all tests using the following command:
    `bash run_tests.sh`

------------------------------------------------------------------------------------------------------------
## Parallel Execution

   To run tests in parallel, 
    1. Install `pytest-xdist`:
        pip install pytest-xdist
    2. Use the `--dist=loadscope` option to run tests in parallel
    `pytest --headed --browser=chromium --alluredir=reports/allure-results --dist=loadscope`
    
------------------------------------------------------------------------------------------------------------
## Allure Reporting
  1. Allure results are generated in `reports/allure-results`
  2. HTML report can be viewed using:
     `allure serve reports/allure-results`
  3. To generate a static report:
     `allure generate reports/allure-results -o reports/allure-report --clean`

------------------------------------------------------------------------------------------------------------
## Video Recording
   Test videos are recorded via Playwright. Videos of each test run are saved in the `videos` directory.

## Screenshots
   Screenshots are taken on failure and saved in the `screenshots` directory.

------------------------------------------------------------------------------------------------------------
## Author
   Shivkumar Hiremath
   [LinkedIn](https://www.linkedin.com/in/shivkumar-hiremath/)

