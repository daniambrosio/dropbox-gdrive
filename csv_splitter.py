import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="filaname of original csv file to be split")
    # parser.add_argument("delimiter", help="delimiter character used to separate values in the csv file", default=",", action="store_true")
    parser.add_argument("row_limit", type=int, help="limit of rows in each file after splitting", default=10000)
    # parser.add_argument("output_name_template", help="A style template for the numbered output files.", default="output_%s.csv")
    # parser.add_argument("output_path", help="Where to stick the output files", default=".")
    # parser.add_argument("keep_headers", help="Whether or not to print the headers in each output file.", default="True")

    args = parser.parse_args()

    if not args.row_limit:
        print "row_limit found: %s" % args.row_limit

    split(open(args.csv_file),row_limit=args.row_limit)

    return;

def split(filehandler, delimiter=',', row_limit=10000, 
    output_name_template='output_%s.csv', output_path='.', keep_headers=True):
    
    """
    Splits a CSV file into multiple pieces.
    Original gist at: https://gist.github.com/jrivero/1085501/a2401c345e8abb46f3623e08afbe36e59923f94e#file-csv_splitter-py
    
    A quick bastardization of the Python CSV library.
    Arguments:
        `row_limit`: The number of rows you want in each output file
        `output_name_template`: A %s-style template for the numbered output files.
        `output_path`: Where to stick the output files
        `keep_headers`: Whether or not to print the headers in each output file.
    Example usage:
    
        >> from toolbox import csv_splitter;
        >> csv_splitter.split(csv.splitter(open('/home/ben/Desktop/lasd/2009-01-02 [00.00.00].csv', 'r')));
    
    """
    import csv
    print "reading file %s" % filehandler
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
         output_name_template  % current_piece
    )
    print "creating output file %s" % current_out_path
    current_out_writer = csv.writer(open(current_out_path, 'wb'))
    current_limit = row_limit
    if keep_headers:
        headers = reader.next()
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
               output_name_template  % current_piece
            )
            print "New split - new file %s" % current_out_path
            current_out_writer = csv.writer(open(current_out_path, 'w'))
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)

if __name__ == '__main__':
    main()