#!/bin/bash

timestamp=$(date +"%Y%m%d_%H%M%S")
pytest --headed --browser=chromium --alluredir=reports/allure-results-$timestamp --dist=loadscope

allure generate reports/allure-results -o reports/allure-report --clean

allure open reports/allure-report
