#!/usr/bin/python
"""Email processor. 0.1

Usage:
  email.py
  email.py [-i <emails.json] [-o <email_report.json>]
  email.py (-h | --help)
  email.py (-v | --version)

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  -i FILE       Input file path,[default: ./emails.json]
  -o FILE       Output file path [default: ./email_report.json]
"""
import os
import pandas as pd
import datetime as dt
from docopt import docopt


def processor(filepath):
    report = {}
    emails = pd.read_json(filepath, convert_dates=['sentAt'])
    report['summary'] = get_summary(emails)

    return report


def get_summary(data):
    data['date'] = data.apply(
        lambda x: dt.datetime.strftime(x['sentAt'], '%Y-%m-%d'), axis=1)
    data['day'] = data.apply(
        lambda x: dt.datetime.strftime(x['sentAt'], '%A'), axis=1)
    summary = {}
    summary['totalEmails'] = len(data)
    summary['totalDays'] = len(data['date'].unique())
    summary['mostPopularDay'] = 'Tuesday'
    summary['mostPopularSendtime'] = '3pm'
    summary['monthlyFrequency'] = 7
    summary['averageTimeBetweenPromotions'] = '1D'
    return summary


def main():
    arguments = docopt(__doc__, version='Email processor 0.1')
    input_file = arguments['-i']
    output_file = arguments['-o']
    if not output_file.startswith(('/', './')):
        output_file = './' + output_file
    output_path = os.path.dirname(output_file)

    if not os.path.exists(input_file):
        raise IOError("File %s not found" % input_file)
    if not os.path.exists(output_path):
        raise IOError("Path %s not found" % output_path)

    report = processor(input_file)
    print(report)


if __name__ == '__main__':
    main()
