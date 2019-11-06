#!/usr/bin/env python
import pandas as pd
import numpy as np
import math
import argparse
import os
from datetime import datetime

def format_report(filename, output_dir):
		# Read the input file
		original_morrisons_dataframe = pd.read_csv(filename)
		
		# Remove rows with missing barcodes i.e barcode entry will be zero
		filtered_df = original_morrisons_dataframe[original_morrisons_dataframe["Barcode"].str.len().gt(5)]

		# Break down filtered df into two dataframes -  valid_barcodes with 9 chars, and swapped_barcodes with < 9 chars
		valid_barcodes = filtered_df[filtered_df["Barcode"].str.len().gt(8)]
		swapped_barcodes = filtered_df[filtered_df["Barcode"].str.len().lte(8)]

		# Now in the swapped_barcodes dataframe, swap MF_CODE and barcode columns
		renamed_df = swapped_barcodes.rename(columns ={"MF_CODE" : "Barcode", "Barcode" : "MF_CODE"})
		cols = list(renamed_df.columns)
		a, b = cols.index("MF_CODE"), cols.index("Barcode")
		cols[b], cols[a] = cols[a], cols[b]
		renamed_df = renamed_df[cols]

		# Some rows will have missing barcodes, descriptions, product IDs etc, so we need to remove them
		swapped_barcodes = renamed_df.dropna(subset=["Barcode"])

		# Now swapped_barcodes also contains valid barcodes, so let's merge it back into valid_codes
		merged_df = valid_barcodes.append(swapped_barcodes, sort = False)

		# Sort by barcode in increasing order
		sorted_df = merged_df.sort_values(by=["Aisle Name"], axis = 0, ascending = True, na_position ="first")	

		# Only retain the following columns ["Barcode, Aisle Name, Product ID, Description, MF_Code"]
		cols_of_interest = ["Barcode", "Aisle Name", "Product Id", "Description", "MF_CODE"]
		sorted_df = sorted_df[cols_of_interest]

		# Now write the final output file
		datestring = datetime.strftime(datetime.now(), "%Y-%m-%d")
		full_output_path = os.path.join(output_dir, "OFF_PLAN_REPORT_" + datestring + ".csv")
		sorted_df.to_csv(full_output_path)

def main():
		parser = argparse.ArgumentParser(description="Morrisons off plan formatting script")
		parser.add_argument("-f", "--filename", required=True, help="Path to file to be formated")
		parser.add_argument("-o", "--output_dir", required=True, help="Path to where the file will be saved")
		args = parser.parse_args()
		format_report(args.filename, args.output_dir)

if __name__ == "__main__":
		main()
