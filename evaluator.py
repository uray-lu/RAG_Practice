"""Evaluate your RAG system"""
from argparse import ArgumentParser
import pandas as pd
from dotenv import load_dotenv
from utils.Config import(
    ragas_config,
    trulens_config
)
from eval.service.eval_service import eval_service
from utils import CsvService


load_dotenv()

def parse_args():
    """Parse command line arguments."""
    parser = ArgumentParser(
        prog='RAG_evaluate',
        description='Evaluate your RAG system'
    )

    # parameter: model_name, eval_file_path, output_file_path, methods
    parser.add_argument("--model_name",
                        default="gpt-3.5-turbo-16k",
                        help="model that help evaluate your result")
    parser.add_argument("--file_path",
                        help="evaluate file, only support csv file currently",
                        type=str)
    parser.add_argument("--output_path",
                        help="output path for result, only support csv file currently",
                        type=str)
    parser.add_argument('--methods',
                        choices=[
                            'groundness', 'context_relevancy', 
                            'answer_relevancy', 'context_precision'
                        ],
                        default= trulens_config.methods + ragas_config.methods,
                        nargs='+',
                        help='choose evulation method')
    parser.add_argument('--gpt_reason',
                        action= "store_true",
                        help='if you want to save gpt cot result, set True')
    return parser.parse_args()

def main():
    """handle evaluate"""
    args = parse_args()

    if not (CsvService.is_csv_file(args.file_path) and CsvService.is_csv_file(args.output_path)):
        raise ValueError("Sorry, only support csv file")

    try:
        eval_data_csv = pd.read_csv(args.file_path)
    except Exception as e:
        raise ValueError("Error reading the CSV file:") from e

    try:
        eval_service(eval_data_csv, args)
        eval_data_csv.to_csv(args.output_path)
    except Exception as e:
        raise ValueError("Error during evaluation process:") from e

if __name__ == '__main__':
    main()
