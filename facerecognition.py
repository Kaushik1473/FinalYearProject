import cv2
import os
import face_recognition
import base64
import pymongo
import datetime
import string
from random import choice

class FaceRecognizer:
  def __init__(self, *args, **kwargs):
    '''
    TODO:

    Initialize model for validation
    '''
    self.model = None ## face recognition model

  def recognize(self, image, userId=None):
    '''
    TODO:

    Checks if image is in database
    Returns True if exists, else False

    If userId is None, check if image exists in the database
    '''
    pass
  def register(self, image):
    '''
    TODO:

    Adds face to database
    Generates a userId and returns it
    '''
    pass
		
   def inputs(self,id,image):
    client = pymongo.MongoClient("mongodb+srv://kaushik:kd147953@project.hgun0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
    collection=client['EmployeeManagementSystem']
    db=collection["EmployeeData"]
    query={"EmployeeId":id}
    x=list(db.find(query))
    if len(x)==0:
        print("Access Denied")
    else:
        
				cv2.imwrite("NewFaceData.jpeg", frame)
        if self.Face_recognition(x[0]["FaceId"])==True:
            db1 = collection['EfficientWorkTime']
            x1=list(db1.find(query))
            print(x1)
            if(len(x1)==0):
                dict={"EmployeeId":id,
                      "First Enter Time":datetime.datetime.now().strftime('%H:%M:%S'),
                      "Enter Time":datetime.datetime.now().strftime('%H:%M:%S'),
                      "Exit Time":"",
                      "Work Time":"00:00:00"}
                db1.insert_one(dict)
            else:
                print("1. To Enter\n2. To Exit")
                ch=int(input())
                if(ch==1):
                    if(x1[0]["Exit Time"]!=""):
                        db1.update_one({"EmployeeId":id},{'$set':{'Enter Time':datetime.datetime.now().strftime('%H:%M:%S'),'Exit Time':''}})
                    else:
                        print("Employee already inside the office")
                else:
                    if(x1[0]['Exit Time']==''):
                        entime=datetime.datetime.strptime(x1[0]['Enter Time'],'%H:%M:%S')
                        extime=datetime.datetime.now().strftime('%H:%M:%S')
                        difference=datetime.datetime.strptime(extime,'%H:%M:%S')-entime
                        worktime=(datetime.datetime.strptime(x1[0]['Work Time'],'%H:%M:%S')+difference).strftime("%H:%M:%S")
                        db1.update_one({"EmployeeId":id},{'$set':{'Exit Time':extime,'Work Time':worktime}})
                    else:
                        print("Employee already outside the office")
            if x[0]["Department"] == 'ADMIN':
                print("Do you want to make changes in database?(Y/N)")
                ch=input()
                if(ch=='Y'):
                    Employee.Admin(db)
                else:
                    Employee.employee(x)
            else:
                Employee.employee(x)
        else:
            print("Access Denied")

        os.remove("NewFaceData.jpeg")
  def clickImage(self):

    print("Settle to capture Face Data")
    videoCaptureObject = cv2.VideoCapture(0)
    ret, frame = videoCaptureObject.read()
    videoCaptureObject.release()
    cv2.destroyAllWindows()
    cv2.imwrite("NewFaceData.jpeg", frame)


	def checkRepeatation(self,db):
			Face_collections = db.find({})
			for document in Face_collections:
					if Face_recognition(document["FaceId"]):
							print("EmployeeId",document["EmployeeId"],"already associated with face data")
							return True
			return False

	def Face_recognition(self,StoredImage):

			decodeit = open('Face.jpeg', 'wb')
			decodeit.write(base64.b64decode(StoredImage))
			decodeit.close()

			TestImage = face_recognition.load_image_file("NewFaceData.jpeg")
			StoredImage = face_recognition.load_image_file("Face.jpeg")
			TestImage = cv2.cvtColor(TestImage, cv2.COLOR_BGR2RGB)
			StoredImage = cv2.cvtColor(StoredImage, cv2.COLOR_BGR2RGB)
			encodeFace = face_recognition.face_encodings(TestImage)[0]
			encodeTest = face_recognition.face_encodings(StoredImage)[0]

			results = face_recognition.compare_faces([encodeFace],encodeTest)
			os.remove("Face.jpeg")
			return results[0]
	def Admin(self,db):
    print("Enter 1 to add new employee data")
    print("Enter 2 to update existing employee data")
    print("Enter 3 to delete existing employee data")
    ch=int(input())

    if ch==1:

        FaceData.clickImage()
        if FaceData.checkRepeatation(db)==False:

            with open('NewFaceData.jpeg','rb') as imageFile:
                employeeFaceId=base64.b64encode(imageFile.read())

            print("Enter Name, Age, PhoneNo, Department, YOJ, Gender")
            employeeName = input()
            employeeAge = int(input())
            employeePhoneNo = int(input())
            employeeDepartment = input()
            employeeYOJ = int(input())
            employeeGender = input()

            employeeData={"Name":employeeName,
                          "Age":employeeAge,
                          "PhoneNo":employeePhoneNo,
                          "Department":employeeDepartment,
                          "YOJ":employeeYOJ,
                          "FaceId":employeeFaceId,
                          "Gender":employeeGender
                          }
            random = ''.join(choice(string.digits) for _ in range(4))
            random=employeeDepartment[:2]+random

            while len(list(db.find({'EmployeeId':random})))>0:
                random = ''.join(choice(string.digits) for _ in range(4))
                random = employeeDepartment[:2] + random

            employeeData["EmployeeId"]=random
            db.insert_one(employeeData)
            print("New Employee added with EmployeeId :",random)

    elif ch==2:
        print("Enter EmployeeId whose data needs to be updated")
        employeeId = input()
        employee(list(db.find({'EmployeeId':employeeId})))
        print("Enter the number of changes to be made:")
        no_of_choice=int(input())
        while no_of_choice>0:
            updateData = {}
            print("Enter the field to be updated")
            field=input()
            if field=='EmployeeId':
                print("Field can not be changed")
            elif field=='FaceId':
                FaceData.clickImage()
                with open('NewFaceData.jpeg', "rb") as imageFile:
                    updatedData = base64.b64encode(imageFile.read())
                updateData[field] = updatedData
                db.update_one({'EmployeeId': employeeId}, {'$set': updateData})

            else:
                print('Enter the data to be updated')
                if field=='Age' or field=='PhoneNo' or field=='YOJ':
                    updatedData=int(input())
                else:
                    updatedData=input()
                updateData[field] = updatedData
                db.update_one({'EmployeeId': employeeId}, {'$set': updateData})

            no_of_choice-=1
        print('Employee data updated')


    elif ch==3:
        print("Enter EmployeeId whose data needs to be deleted")
        employeeId=input()
        db.delete_one({'EmployeeId':employeeId})
        print("Employee Data Deleted Successfully")

    return


	def employee(self,x):
			for i in x[0].keys():
					if i!='FaceId' and i!='_id':
							print(i,':',x[0][i])
			return
	
