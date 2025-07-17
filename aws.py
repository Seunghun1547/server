import boto3 

def detect_labels_local_file(photo):

    client=boto3.client('rekognition')
   
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    
    result = []

    for label in response["Labels"]:
        name = label["Name"]
        confidence = label["Confidence"]

        result.append(f"{name} : {confidence:.2f}%")

    r = "<br/>".join(map(str, result))
    # "Dog : 85.22%<br/>Cat : 76.11%"   
    return r

def compare_faces(sourceFile, targetFile):

    client = boto3.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')

    response = client.compare_faces(SimilarityThreshold=0,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})
    
    for faceMatch in response['FaceMatches']:
        similarity = faceMatch['Similarity']

# 4. aws.py안에 compare_faces 그 결과를 문자열로 "동일 인물일 확률은 15.24% 입니다" 리턴
    imageSource.close()
    imageTarget.close()
    return f"동일 인물일 확률은 {similarity:.2f}% 입니다"


