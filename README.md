# Data-Source-API-Analyst-Test
Homework assignment for Data Source API Analyst role @ Improvado

This repository houses a Google Colab notebook providing a Python script for interacting with the GitHub API, aligning with the given instructions. The following Python libraries were used: requests, getpass, json, os, logging, time. (All are standard or pre-installed in Colab).

## Features
  - Authentication: Assures that GitHub's PATs are handled securely with 'getpass'.
  - Logging: Logs are available in the output console as a separate file in Colab's temporary file system.
  - Data Saving: Saves the data extracted by testing also in Colab's temporary file system.
  - API Interaction Functions:

  - Error Handling: Includes a safeRequest function to manage HTTP errors and automatically handle GitHub API rate limits by pausing execution until the limit resets.
  - Testing: Built-in test suite to verify the functionality of all the API interaction functions, covering success, no-results, and error scenarios.

## Authentication

  The script requires a GitHub Personal Access Token (PAT) to authenticate API requests. It can be either a Fine-grained PAT or a classic token. This requires setup by the user on their own GitHub account.
  When the authentication cell is run, a pop up box will open so that the token is entered. Enter the PAT and confirm with Enter. The token will not be displayed for security.

## Core Functions

The notebook defines 4 main Python functions to interact with the GitHub API. 
