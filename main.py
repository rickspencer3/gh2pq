

import requests
import pandas as pd
import fastparquet as fp
import os

token = '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'
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3.star+json' }

organizations = [
                #  'uyuni-project',
                #  'opensuse',
                #  'suse',
                #  'os-autoinst',
                #  'rancher',
                 'longhorn',
                 'k3s-io',
                 'kubewarden',
                 'harvester',
                 'neuvector',
                 'opinio',
                 'rancher-sandbox'
                 ]

def get_stargazers_page(page=1, organization=None, repo=None):
    url = f'https://api.github.com/repos/{organization}/{repo}/stargazers'
    params = {
        'page': page,
        'per_page': 100,
        'accept': 'application/vnd.github.v3.star+json'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 403:
        print("**** Rate Limit Exceeded ****")
        exit(1)
    batch = response.json()
    return(batch)

def fetch_repos_for_org(org):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{org}/repos?type=public&page={page}&per_page=100"  # 'per_page=100' is the maximum allowed
        response = requests.get(url)
        if response.status_code == 200:
            batch = response.json()
            if not batch:  # Break the loop if the current page is empty
                break
            repos.extend([repo['name'] for repo in batch])
            page += 1
        else:
            print(f"Failed to fetch repositories for {org} on page {page}")
            break
    return repos

def run():
    os.makedirs("partitions", exist_ok=True)
    for organization in organizations:
        print(f"fetching repos for {organization}")
        repos = fetch_repos_for_org(organization)
        print(f" found {len(repos) in {organization}}")
        org_rows = []
        for repo in repos:
            print(f" fetching stars for {repo} in {organization}")
            stargazers = collect_all_stars(organization, repo)
            repo_rows = []
            for star in stargazers:
                row = star_row(organization, repo, star)
                repo_rows.append(row)
            columns = ['login', 'time', 'organization', 'repo']
            print(f'  found {len(repo_rows)} stars in {organization}/{repo}')
            org_rows.extend(repo_rows)
        df = pd.DataFrame(org_rows, columns=columns)
        parquet_path = os.path.join("partitions", f"{organization}.parquet")
        fp.write(parquet_path, df)

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
        print(f"  fetched page {page} of stars for {repo} in {organization}")
        if not stars:
            break
        stargazers.extend(stars)
        page += 1
    return stargazers

if __name__ == "__main__":
    run()
