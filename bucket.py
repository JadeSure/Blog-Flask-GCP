import os.path
import sys

from google.cloud import storage
PATH = os.path.join(os.getcwd() , 'chengccassgn1-ce7fd57eac11.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH

class Bucket():

    def __get_uploaded_image_url(self, bucketName, source_file_name):
        storage_client = storage.Client(PATH)
        bucket = storage_client.get_bucket(bucketName)
        uploadfile = os.path.join(os.getcwd(), source_file_name)
        bucket = storage_client.get_bucket(bucketName)
        blob = bucket.blob(source_file_name)
        blob.upload_from_filename(uploadfile)
        blob.make_public()

        return blob.public_url

    def __init__(self, bucket_name, source_file_name):
        self.image_url = self.__get_uploaded_image_url(bucket_name, source_file_name)
# def get_url(bucket_name, file_name):
#     client = storage.Client(PATH)
#     bucket = client.bucket(bucket_name)
#     blob = bucket.blob(file_name)
#     url_lifetime = None
#     serving_url = blob.generate_signed_url(url_lifetime = None)
#     return serving_url


if __name__ == '__main__':

    # upload_image('chengass1', 'girl.jpg')
    # print(get_url('chengass1', 'girl.jpg'))
    bucket_name = 'ass1forimages'
    source_file_name = 'Image/1.jpg'

    image_url = Bucket(bucket_name, source_file_name).image_url
    print(image_url)