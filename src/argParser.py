import argparse


class ArgParser:
    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="Algorithm, order, source file, solution file, statistics file.")
        parser.add_argument('algorithm')
        parser.add_argument('order')
        parser.add_argument('source_file')
        parser.add_argument('solution_file')
        parser.add_argument('statistic_file')
        return parser.parse_args()
