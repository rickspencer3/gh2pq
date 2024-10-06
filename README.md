# What is this code for?
This code is for people who want to do data analysis on public github organizations. It supports this data analysis by using the github API to gather stars for each repo in each organization, and then storing each star in a parquet file, meant for easy analsyis with pandas or polars. 

Currently, the only github metric supports is star.

# How do I use the code?
## Prequisites
### API Key/Token
 * Go into your github settings under developer options, and create an API key that is able to access public repositories.
 * Add the API key to the code

Add your token where you would expect:
```python
token = ''
```

### List of Organizations
Then you need to give the code a list of github organizations. 

Replace this list with your list of organizations:
```python
organizations = []
```

For example, for SUSE related repos, I look at:
```python
organizations = [
                 'uyuni-project',
                 'opensuse',
                 'suse',
                 'os-autoinst',
                 'rancher',
                 'longhorn',
                 'k3s-io',
                 'kubewarden',
                 'harvester',
                 'neuvector',
                 'opinio',
                 'rancher-sandbox'
                 ]
```

## Run main.py
```shell
> python3 main.py
```

The script is currently very chatty on the console to provide feedback about where it is in the process. It should obviously be using logging, but this is fine for now.

The important thing is that it will create a separate parquet file for each organization in the ```/partitions``` directory. *WARNING* this will overwite existing parquet files.

The benefit of the partitions is that it makes it easier to continue if the program crashes or is otherwise interupted.

## Run compact.py (optional)
```shell
> python3 compact.py
```

This script will put all of the partitions into a single file called ```stars.parquet```. This is just for the convenience of having a single file to manage. ```compact.py``` is not run automatically. You need to do it yourself as an extra step if you want the single parquest file.