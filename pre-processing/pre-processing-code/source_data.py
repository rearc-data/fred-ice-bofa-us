import os
import boto3
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from multiprocessing.dummy import Pool


def data_to_s3(frmt):
    # throws error occured if there was a problem accessing data
    # otherwise downloads and uploads to s3

    source_dataset_url = 'https://fred.stlouisfed.org/graph/fredgraph'

    try:
        response = urlopen(source_dataset_url + frmt)

    except HTTPError as e:
        raise Exception('HTTPError: ', e.code, frmt)

    except URLError as e:
        raise Exception('URLError: ', e.reason, frmt)

    else:
      #  data_set_name = os.environ['DATA_SET_NAME']
        data_set_name = 'AVtest'
        filename = data_set_name
        file_location = 'C:/Users/Ayush Varma/Desktop/' + filename

        with open(file_location, 'wb') as f:
            print('hi')
            f.write(response.read())
            f.close()

        # variables/resources used to upload to s3
        # s3_bucket = os.environ['S3_BUCKET']
        # new_s3_key = data_set_name + '/dataset/'
        # s3 = boto3.client('s3')

        # s3.upload_file(file_location, s3_bucket, new_s3_key + filename)

        print('Uploaded: ' + filename)

        # deletes to preserve limited space in aws lamdba
        # os.remove(file_location)

        # dicts to be used to add assets to the dataset revision
        # return {'Bucket': s3_bucket, 'Key': new_s3_key + filename}


def source_dataset():

    # list of enpoints to be used to access data included with product
    data_endpoints = [
        '.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=BAMLH0A0HYM2&scale=left&cosd=2015-07-16&coed=2020-07-16&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily%2C%20Close&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2020-07-17&revision_date=2020-07-17&nd=1996-12-31',

        '.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=BAMLH0A0HYM2&scale=left&cosd=2015-07-16&coed=2020-07-16&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily%2C%20Close&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2020-07-17&revision_date=2020-07-17&nd=1996-12-31'
    ]

    # multithreading speed up accessing data, making lambda run quicker
    with (Pool(2)) as p:
        asset_list = p.map(data_to_s3, data_endpoints)

    # asset_list is returned to be used in lamdba_handler function
    return asset_list


source_dataset()
