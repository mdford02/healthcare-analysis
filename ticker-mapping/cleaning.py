import pandas as pd
import pathlib

def read_to_df(path_to_data, encoding="utf-8"):
    # df = pd.read_table(filepath_or_buffer=path_to_data, sep="|", encoding="ASCII")
    df = pd.read_csv(path_to_data, encoding = encoding)
    return df


def get_510_dataframe(filename):
    relative_path = "healthcare-pb-mapping/510k_data"
    path_to_data = pathlib.Path.cwd() / relative_path / filename

    df = read_to_df(path_to_data, encoding = 'unicode_escape')
    
    return df

def get_pitchbook_data(filenames: list):
    relative_path = "healthcare-pb-mapping/mapping_csvs"
    dfs = []
    
    for filename in filenames:
        path_to_data = pathlib.Path.cwd() / relative_path / filename

        df = read_to_df(path_to_data)
        dfs.append(df)
    
    return dfs
