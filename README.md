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

This 4 functions are aligned with the client need described on the assignment. 

The searchRepos function searches through the public repositories on Github from a specified query.
The listCommits function retrieves the specified page amount of commits from a specific repository.
The getContents function goes through a repository and gets the content of a specified file or directory.
The listAllCommits gathers all commits from a repository.

## My Challenges
While the development was without many roadblocks, I had some issues with understanding the PAT setup and usage. Thankfully, the GitHub API docs was very intuitive, so I easily found the section about personal access tokens, now with complete grasp of the tasks ahead.

This task was definitely out of my confort zone, but I'm confident in what I created and am delivering.

Thanks for the opportunity!!
