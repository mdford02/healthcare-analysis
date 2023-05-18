import pandas as pd
import pathlib
from .cleaning import *


def gather_all_datasources():
    approval_df = get_510_dataframe("510k_data.csv")
    pb_mapping, sub_timeseries = get_pitchbook_data(["crsp_pitchbook_mapping.csv", "subsidiary_timeseries.csv"])

    return approval_df, pb_mapping, sub_timeseries


def map_subsidiary_to_parent(company_name_string, sub_timeseries):
    """
    Helper for parent mapping function. Pass a company if it cannot be found in the mapping and try to find
    its entry in the subsidiary timeseries, then return the parent company to complete the mapping process (find the ticker)
    """
    raise NotImplemented



def map_510k_companies_to_tickers(approval_df, pb_mapping, sub_timeseries):
    """
    Iterate through the 510k decision dataframe, add a new column for the ticker of the company corresponding to each
    decision. Begin by trying to find the company's name in the base pitchbook mapping file, if it does not exist assume the listed
    company is a subsidiary and try to find its parent in the subsidiary timeseries, then find the parent's ticker in the pitchbook
    mapping, and enter that ticker as the column value.

    TODO: This will more than likely fail due to the brittle nature of string comparison and the fact that both sources seem to
    represent company names with different formatting standards, first should try to clean both sources a bit to get the names to match as closely
    as possible, then consider using Fuzz to match close companies? this could cause potential issues with subsidiary mapping as the
    threshold to determine if a company was found in the mapping would be quite arbitrary
    """
    raise NotImplemented


def main():
    approval_df, pb_mapping, sub_timeseries = gather_all_datasources()

    mapped_approval_df = map_510k_companies_to_tickers(approval_df, pb_mapping, sub_timeseries)
    destination = pathlib.Path.cwd() / "healthcare-pb-mapping/mapped_csvs/mapped_510k_decisions.csv"
    mapped_approval_df.to_csv(destination)
    

if __name__ == "__main__":
    main()

