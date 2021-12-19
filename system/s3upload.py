# pre: python3.6, pip3 reinstall 
# pip3 install boto3


import boto3
import os
import time
from datetime import datetime
from botocore.client import Config

# 버킷 생성
def create_bucket(bucket):
    print("make new AWS S3 bucket " + bucket)
    bucket_info = s3.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'} # Seoul
    )

    return bucket_info

# 버킷으로 객체 업로드
def upload_object_to_bucket(filepath, extension, filename, bucket):

    # 텍스트 파일일시 
    if extension == '.txt':
        print("New text Issue Occur!!")
        print("upload to text bucket about new ISSUE")
        nowTime = int(datetime.today().strftime("%Y%m%d%H%M%S"))
        upload_filename = str(nowTime) + extension
        s3.upload_file(filepath + extension, bucket + '-text' , upload_filename)

    # 이미지 파일일시
    elif extension == '.jpg' or extension == '.png' or extension == '.jpeg':
        print("New image Issue Occur!!")
        print("upload to image bucket about new ISSUE")
        img_data = open(filepath + extension, 'rb')

        news3 = boto3.resource(
        's3',  # aws s3
        aws_access_key_id="",         # IAM access ID
        aws_secret_access_key="",   # IAM secret key
        config = Config(signature_version='s3v4')  
        )

        nowTime = int(datetime.today().strftime("%Y%m%d%H%M%S"))
        upload_filename = str(nowTime) + extension

        news3.Bucket(bucket + '-image').put_object(Key = upload_filename, Body = img_data, ContentType = 'image/' + extension[1:])






if __name__ == "__main__":

    background_path = os.path.dirname(os.path.realpath(__file__)) # 현재 파일 경로
    issue_data_path = background_path + '/issue_data'
    issue_data_folder_list = os.listdir(issue_data_path)

    s3 = boto3.client(
        's3',  # aws s3
        aws_access_key_id="",         # IAM access ID
        aws_secret_access_key=""   # IAM secret key
    )

    bucket_response = s3.list_buckets()
    bucket_list = [bucket['Name'] for bucket in bucket_response['Buckets']] # 
    target_image_bucket = ''
    target_text_bucket = ''
    target_bucket = ''
    under_2_issue_folders = []




    while True:
        print('no issue state')
        update_issue_folder = os.listdir(issue_data_path)


        if sorted(issue_data_folder_list)!= sorted(update_issue_folder):


            nowTime = int(datetime.today().strftime("%Y%m%d%H%M%S")) // 100
            nowMonth = nowTime // 1000000
            target_bucket = str(nowMonth)

            check_image_bucket_target = str(nowMonth) + '-image'
            check_text_bucket_target = str(nowMonth) + '-text'

            if check_image_bucket_target not in bucket_list:
                bucket_list.append(check_image_bucket_target)
                target_bucket = check_image_bucket_target
                create_bucket(check_image_bucket_target)

            if check_text_bucket_target not in bucket_list:
                bucket_list.append(check_text_bucket_target)
                target_text_bucket = check_text_bucket_target
                create_bucket(check_text_bucket_target)
            

            
            new_issue_folders = [x for x in update_issue_folder if x not in issue_data_folder_list]


            for new_issue_folder in new_issue_folders:
                
                upload_object_list = os.listdir(issue_data_path + '/' + new_issue_folder )

                print(upload_object_list)
                print(under_2_issue_folders)
                if len(upload_object_list) < 2:

                    if (new_issue_folder in under_2_issue_folders) == True:
                        print(new_issue_folder + "has 0 or 1 number of data, please update")

                    else:
                        under_2_issue_folders.append(new_issue_folder)
                        for upload_object in upload_object_list:
                            filepath,extension = os.path.splitext(issue_data_path + '/' + new_issue_folder + '/' + upload_object)
                            upload_object_to_bucket(filepath, extension, upload_object, target_bucket)
                
        


                elif len(upload_object_list) >= 2:

                    if (new_issue_folder in under_2_issue_folders) == True:
                        #upload_object_list.remove(new_issue_folder)
                        issue_data_folder_list.append(new_issue_folder)
                        under_2_issue_folders.remove(new_issue_folder)

                        for upload_object in upload_object_list:
                            filepath,extension = os.path.splitext(issue_data_path + '/' + new_issue_folder + '/' + upload_object)
                    
                            upload_object_to_bucket(filepath, extension, upload_object, target_bucket)

                    else:
                        issue_data_folder_list.append(new_issue_folder)
                        for upload_object in upload_object_list:
                            filepath,extension = os.path.splitext(issue_data_path + '/' + new_issue_folder + '/' + upload_object)
                    
                            upload_object_to_bucket(filepath, extension, upload_object, target_bucket)


            



        time.sleep(3)