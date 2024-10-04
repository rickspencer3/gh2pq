

import requests
import pandas as pd
import fastparquet as fp
import os

token = "" # your github token with permissions to read public repos
headers = {'Authorization': f'token {token}',
           'Accept': 'application/vnd.github.v3.star+json' }
parquet_file_name = "stars.parquet"

organizations = [] # a list of org names

def get_stargazers_page(page=1, organization=None, repo=None):
    url = f'https://api.github.com/repos/{organization}/{repo}/stargazers'
    params = {
        'page': page,
        'per_page': 100,
        'accept': 'application/vnd.github.v3.star+json'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def fetch_repos_for_org(org):
    url = f"https://api.github.com/orgs/{org}/repos?type=public"
    response = requests.get(url)
    if response.status_code == 200:
        return [repo['name'] for repo in response.json()]
    else:
        print(f"Failed to fetch repositories for {org}")
        return []

def run():
    for organization in organizations:
        repos = fetch_repos_for_org(organization)
        for repo in repos:
            stargazers = collect_all_stars(organization, repo)
            rows = []
            for star in stargazers:
                row = star_row(organization, repo, star)
                rows.append(row)
            columns = ['login', 'time', 'organization', 'repo']
            df = pd.DataFrame(rows, columns=columns)
            if not os.path.exists(parquet_file_name):
                fp.write(parquet_file_name, df)
            else:
                fp.write(parquet_file_name, df, append=True)
            print(f'found {len(rows)} stars in {organization}/{repo}')

def star_row(organization, repo, star):
    row = {}  
    row["login"] = star["user"]["login"]
    row["time"] = star["starred_at"]
    row["organization"] = organization
    row["repo"] = repo
    return row
        

def collect_all_stars(organization, repo):
    stargazers = []
    page = 1
    while True:
        stars = get_stargazers_page(page, organization, repo)
        if not stars:
            break
        stargazers.extend(stars)
        page += 1
    return stargazers

if __name__ == "__main__":
    run()
