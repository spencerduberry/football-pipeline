# Football API project

## Data source
Use a simple football api to get stats on matches and stuff

`https://pypi.org/project/football-data-api/`

## Stage 1 (DE focused)
- Get the raw data from the API, at first all locally then in future can think about hosting/chron jobs
- Use the medallion architecture to serve the data to the next stage:
    - raw layer - landing zone: these are raw files that we keep for persistent storage (using parquet)
    - bronze layer - minor cleaning and apply schemas
    - silver layer - split into fact and dimension tables (normalise)
    - gold layer - final transformations and aggregations to supply to the end user

### Tools
- at first just `python`, `pandas` and some `sqlite3` etc, in future we can expand to `polars` or `spark`
- the pipe should be general enough to take multiple sources and run on yaml config files
- everything should be unit tested

## Stage 2 (DA focused)
- Basic data analysis on the tables that are created in the gold layer
- mainly using SQL this can also include data-vis stuff 

## Tools
- `SQL` (obv)
- can look at other flavours like `postgres` or `mysql`
- for vis can look at `powerbi` or `tableau` (if it's free)


## Stage 3 (DS focused)
- using the data and insights of the previous 2 stages use a variety of ML models to predict the results of the next match
- this will likely be using `sklearn`, `pytorch` or something similar
- this will also expose any DQ issues from the previous stages

## Tools
- `python` again lets keep it easy



# Stage 1

## raw layer


### files needed
```
├── configs
│   └── raw_config.yaml
├── src
│   └── football_pipeline
│       ├── __init__.py
│       ├── __main__.py
│       ├── io.py
│       └── transform.py
├── tests
│   └── __init__.py
├── pyproject.toml
└── README.md
::
```


### functions needed:
```python
# io.py
def read_yaml(path: str) -> dict:
    pass


def write_to_parquet(path: str, df) -> bool:
    pass


def extract_data(???) -> df:
    pass


# transform.py
def add_ingestion_columns(df) -> df:
    pass


# pipelines
def run_raw_layer_pipe(config_path: str) -> bool:
    # read the yaml config
    config = read_yaml(config_path)

    # validate the config 
    # TODO

    # for each of the config settings:
        # use the config to query the api

        # check that the data is new - this could be as simple as only querying the data with yesterday's date
        # if not exit early

        # add the ingestion columns
        df = add_ingestion_columns(df)

        # create the directory path to where to save the data - os.makedir(path, exist_ok=True)

        # write the data to the save path
        result = write_to_parquet(path, df)

        # ensure that successfully saved
            # this could mean updating a log file/table with pipeline metadata
        
        # return result  

```