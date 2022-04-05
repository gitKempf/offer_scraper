from tempfile import NamedTemporaryFile
import shutil
import csv


def save_to_file(dataset: object) -> object:
    # name the output file to write to local disk
    output_filename = "offers.csv"
    delimiter = '|'
    alternative_to_delimiter = '/'

    # header of csv file to be written
    fields = [
        'offer_id',
        'section_id',
        'section_name',
        'category_name',
        'sub_category_name',
        'lang',
        'title',
        'ad_details_text',
        # 'details_list_json',
        'details_list_text',
        'contact_detail_date',
        'offer_contacts_offer_date',
        'offer_contacts_city',
        'offer_author_name',
        'author_name',
        'place',
        'phone_number',
        'fax_number',
        'email',
    ]

    # Remaping given spkraped new rows or rows from old file to a new format
    def remap(row_to_remap, fields):
        remaped_row = {}
        for key in fields:
            if key in row_to_remap.keys() and isinstance(row_to_remap[key], str):
                remaped_row[key] = row_to_remap[key].replace(delimiter, alternative_to_delimiter).replace('\n', '')
            else:
                remaped_row[key] = ''
        return remaped_row

    # Writing the dataset to file
    for row_to_write in dataset:
        tempfile = NamedTemporaryFile(mode='w', delete=False)
        with open(output_filename, 'r', encoding='utf8') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            writer = csv.DictWriter(tempfile, fieldnames=fields, delimiter='|')
            writer.writeheader()
            row_to_write_remaped = remap(row_to_write, fields)
            row_updated = False
            # Searching this row with this ID and updating
            # if new row not found, writing back old one to temp file
            for row in reader:
                row = remap(row, fields)
                if row['offer_id'] == str(row_to_write_remaped['offer_id']):
                    # print('updating row', row['offer_id'])
                    row = row_to_write_remaped
                    row_updated = True
                # print('writing row:', row['offer_id'], row_updated, row_to_write_remaped['offer_id'])
                writer.writerow(row)
            # print('updated', row_updated)
            # If file is empty or row is not found even once in file,
            # -> writing this new row to tmp file
            if not row_updated:
                # print('empty file writing:', row_to_write_remaped['offer_id'], row_updated)
                writer.writerow(row_to_write_remaped)
        # Switching temp to main file
        shutil.move(tempfile.name, output_filename)
