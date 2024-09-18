#! /usr/bin/env python
import sys
import pandas
from pathlib import Path
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Normalisation du tableau de données AGLAE après correction du sodium"
    )
    parser.add_argument(
        "filepath",
        type=Path,
        help="fichier excel du tableau des compositions à normaliser",
    )
    return parser.parse_args()


def get_compositions_table(filepath):
    data_frame = pandas.read_excel(filepath, index_col=[0, 1, 2, 3])
    print(data_frame)
    return data_frame


def normalize(row: pandas.Series):
    cleaned_row = row.map(lambda s: pandas.to_numeric(s, errors="coerce"))
    print(cleaned_row)
    total_comp_without_Na = 1000000 - cleaned_row.loc["Na2O PIGE"]
    row_without_Na = cleaned_row.drop("Na2O PIGE")
    sum_comp_without_Na = row_without_Na.sum()
    return row_without_Na.map(lambda x: x * total_comp_without_Na / sum_comp_without_Na)


def main():
    args = parse_args()
    print(args.filepath)
    compositions_table = get_compositions_table(args.filepath)
    normalized_compositions_table = compositions_table.apply(normalize, axis=1)
    normalized_compositions_table.map(lambda x: f"{x:.0f}").to_excel("youpi.xlsx")


if __name__ == "__main__":
    main()
