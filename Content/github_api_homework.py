# -*- coding: utf-8 -*-
"""
# AUTHENTICATION, FILE SAVING AND LOGGING
"""

#logging configuration

import logging
import time
import requests
import getpass
import os

log_directory = '/content/logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file_path = os.path.join(log_directory, 'github_api_session.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.propagate = False

# get github PAT securely w/getpass

import getpass

GITHUB_TOKEN = getpass.getpass('Enter your GitHub Personal Access Token: ')
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

logger.info("GitHub PAT and headers initialized.")

# saves extracted data in a JSON file
# files can be found in the 'Files' section of Colab

import json

def saveToJSON(data, filename):
  try:
    with open(filename, 'w') as f:
      json.dump(data, f, indent=4)
      logger.info(f"Data successfully saved to {filename}")
  except IOError as e:
        logger.error(f"Failed to save data to {filename}: {e}")

"""
# CLIENT NEEDS - EXTRACTION FUNCTIONS
"""

# search public repos
# standard is 5 commits per page, 1 page extracted

def searchRepos(query, per_page=5, page=1):
    logger.info(f"Searching repositories for query: '{query}', page: {page}, per_page: {per_page}")
    url = 'https://api.github.com/search/repositories'
    params = {'q': query, 'per_page': per_page, 'page': page}
    response = safeRequest(url, headers=headers, params=params)
    return response.json()
    logger.debug(f"Search repos response (first 200 chars): {str(data)[:200]}...")

# list commits for a repo
# standard is 5 commits per page, 1 page extracted

def listCommits(owner, repo, per_page=5, page=1):
    logger.info(f"Listing commits for {owner}/{repo}, page: {page}, per_page: {per_page}")
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    params = {'per_page': per_page, 'page': page}
    response = safeRequest(url, headers=headers, params=params)
    return response.json()
    logger.debug(f"List commits response (first 200 chars): {str(data)[:200]}...")

# get contents for a repo

def getContents(owner, repo, path='', params=None):
    logger.info(f"Getting contents for {owner}/{repo} at path: {path}")
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = safeRequest(url, headers=headers, params=params)
    return response.json()
    logger.debug(f"Get contents response (first 200 chars): {str(data)[:200]}...")

# pagination example

def getAllCommits(owner, repo, max_pages=2):
    logger.info(f"Fetching all commits for {owner}/{repo} up to {max_pages} pages.")
    allCommits = []
    for page in range(1, max_pages + 1):
        commits = listCommits(owner, repo, per_page=100, page=page)
        if not commits:
            logger.info(f"No more commits found or empty response for page {page}.")
            break
        if 'message' in commits and commits.get('documentation_url'):
            logger.warning(f"API returned an error message for commits on page {page}: {commits['message']}")
            break
        allCommits.extend(commits)
        logger.info(f"Added {len(commits)} commits from page {page}. Total commits so far: {len(allCommits)}")
    logger.info(f"Finished fetching commits for {owner}/{repo}. Total: {len(allCommits)}")
    return allCommits

"""
# ERROR HANDLING
"""

# function safe request - error handling, including rate limit exceptions

import time

def safeRequest(url, headers, params=None):
    logger.debug(f"Attempting request to: {url} with params: {params}")
    try:
        while True:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers and response.headers['X-RateLimit-Remaining'] == '0':
                reset_time = int(response.headers['X-RateLimit-Reset'])
                sleep_time = max(reset_time - time.time(), 0)
                logger.warning(f'Rate limit reached. Sleeping for {sleep_time:.2f} seconds until {time.ctime(reset_time)}.')
                time.sleep(sleep_time)
            elif response.status_code != 200:
                logger.error(f"API Error: {response.status_code} - {response.text} for URL: {url}")
                response.raise_for_status()
            else:
                logger.info(f"Successful request to {url}. Status: {response.status_code}")
                return response
    except requests.exceptions.RequestException as e:
      logger.error(f"Request failed: {e} for URL: {url}")
      raise

"""
# TESTING
"""

logger.info("Starting API tests...")

# test 1a - searchRepos - search about data science

def test_searchRepos_success():
    logger.info("Running test: searchRepos_success")
    try:
        query = "data science"
        repos = searchRepos(query)
        assert repos is not None, "searchRepos returned None"
        assert 'items' in repos, "searchRepos response missing 'items' key"
        assert len(repos['items']) > 0, f"searchRepos for '{query}' returned no items"
        saveToJSON(repos, f'{query.replace(" ", "_")}_repos_test.json')
        logger.info("Test 'searchRepos_success' passed.")
    except Exception as e:
        logger.error(f"Test 'searchRepos_success' failed: {e}")

# test 1b - searchRepos - search w/ no results

def test_searchRepos_noResults():
    logger.info("Running test: searchRepos_noResults")
    try:
        query = "thereisnotarepositorynamedlikethis"
        repos = searchRepos(query, per_page=1, page=1)
        assert repos is not None, "searchRepos returned None for no results query"
        assert 'items' in repos, "searchRepos response missing 'items' key for no results query"
        assert len(repos['items']) == 0, f"searchRepos for '{query}' returned items when none expected"
        logger.info("Test 'searchRepos_noResults' passed.")
    except Exception as e:
        logger.error(f"Test 'searchRepos_noResults' failed: {e}")

# test 2a - listCommits - list Spoon-Knife's commits

def test_listCommits_success():
    logger.info("Running test: listCommits_success")
    try:
        owner = "octocat"
        repo = "Spoon-Knife"
        commits = listCommits(owner, repo)
        assert commits is not None, "listCommits returned None"
        assert isinstance(commits, list), "listCommits response is not a list"
        assert len(commits) > 0, f"listCommits for {owner}/{repo} returned no commits"
        assert 'sha' in commits[0] and 'commit' in commits[0], "Commit object missing expected keys"
        saveToJSON(commits, f'{owner}_{repo}_commits_test.json')
        logger.info("Test 'list_commits_success' passed.")
    except Exception as e:
        logger.error(f"Test 'list_commits_success' failed: {e}")


# test 2b - listCommits - try to list non existing repo

def test_listCommits_nonExistentRepo():
    logger.info("Running test: listCommits_nonExistentRepo")
    try:
        owner = "nonexistentuser12345"
        repo = "nonexistentrepo67890"
        commits = listCommits(owner, repo)
        assert 'message' in commits and commits['message'] == 'Not Found', "Expected 'Not Found' message for non-existent repo"
        logger.info("Test 'listCommits_nonExistentRepo' passed (handled 404).")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.info("Test 'listCommits_nonExistentRepo' passed (404 HTTPError caught).")
        else:
            logger.error(f"Test 'listCommits_nonExistentRepo' failed with unexpected HTTPError: {e}")
    except Exception as e:
        logger.error(f"Test 'listCommits_nonExistentRepo' failed unexpectedly: {e}")

# test 3a - getContents - get cssBasics's README.md (my repo)

def test_getContents_success():
    logger.info("Running test: getContents_success")
    try:
        owner = "samambea"
        repo = "cssBasics"
        contents = getContents(owner, repo, path='README.md')
        assert contents is not None, "getContents returned None"
        assert 'name' in contents and contents['name'] == 'README.md', "Contents missing 'name' or incorrect"
        assert 'type' in contents and contents['type'] == 'file', "Contents not of type 'file'"
        saveToJSON(contents, f'{owner}_{repo}_README_contents_test.json')
        logger.info("Test 'get_contents_success' passed.")
    except Exception as e:
        logger.error(f"Test 'get_contents_success' failed: {e}")

# test 3b - getContents - get cssBasics's css folder (my repo)

def test_getContents_directory():
    logger.info("Running test: getContents_directory")
    try:
        owner = "samambea"
        repo = "cssBasics"
        contents = getContents(owner, repo, path='projWeb/css')
        assert contents is not None, "getContents returned None for directory"
        assert isinstance(contents, list), "Contents of directory not a list"
        assert len(contents) > 0, "Directory contents list is empty"
        assert 'type' in contents[0] and contents[0]['type'] == 'file', "Expected files in directory"
        saveToJSON(contents, f'{owner}_{repo}_css_dir_contents_test.json')
        logger.info("Test 'getContents_directory' passed.")
    except Exception as e:
        logger.error(f"Test 'getContents_directory' failed: {e}")

# test 3b - getContents - try to get cssBasics's non existent path (my repo)

def test_getContents_nonExistentPath():
    logger.info("Running test: getContents_nonExistentPath")
    try:
        owner = "samambea"
        repo = "cssBasics"
        path = "thisfiledoesn'texist"
        contents = getContents(owner, repo, path=path)
        assert 'message' in contents and contents['message'] == 'Not Found', "Expected 'Not Found' message for non-existent path"
        logger.info("Test 'getContents_nonExistentPath' passed (handled 404).")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.info("Test 'getContents_nonExistentPath' passed (404 HTTPError caught).")
        else:
            logger.error(f"Test 'getContents_nonExistentPath' failed with unexpected HTTPError: {e}")
    except Exception as e:
        logger.error(f"Test 'getContents_nonExistentPath' failed unexpectedly: {e}")

# test 4 - getAllCommits - pagination test

def test_getAllCommits_pagination():
    logger.info("Running test: getAllCommits_pagination")
    try:
        owner = "octocat"
        repo = "Spoon-Knife"
        commits_page1 = getAllCommits(owner, repo, max_pages=1)
        assert commits_page1 is not None, "getAllCommits returned None for 1 page"
        assert len(commits_page1) > 0, "getAllCommits returned no commits for 1 page"
        commits_page2 = getAllCommits(owner, repo, max_pages=2)
        assert commits_page2 is not None, "getAllCommits returned None for 2 pages"
        assert len(commits_page2) >= len(commits_page1), "getAllCommits with 2 pages returned fewer commits than 1 page"
        saveToJSON(commits_page2, f'{owner}_{repo}_allCommits_test.json')
        logger.info("Test 'getAllCommits_pagination' passed.")
    except Exception as e:
        logger.error(f"Test 'getAllCommits_pagination' failed: {e}")

def run_all_tests():
    test_searchRepos_success()
    test_searchRepos_noResults()
    test_listCommits_success()
    test_listCommits_nonExistentRepo()
    test_getContents_success()
    test_getContents_directory()
    test_getContents_nonExistentPath()
    test_getAllCommits_pagination()

run_all_tests()
logger.info("API tests completed.")