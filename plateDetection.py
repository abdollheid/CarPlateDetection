import numpy as np
import cv2 , sys , Image , commands , time  , threading , requests 
import dropbox , os
from dropbox.files import *


args = sys.argv



try :
	accessToken = args[1] 
except  : 
	print "no access token were specified"  
	exit (1)

dbx = dropbox.Dropbox(accessToken)


thereIsPlate = False 

plateNumber = ""

rightOne = "3NEV724"

class TestParallel1(threading.Thread):
	
	def run(self) :
			
		st = commands.getstatusoutput("alpr -c us " + self.getName() + " -n 1" )
		thereIsPlate  , plateNumber = self.getLicence(st)
		print thereIsPlate , 
		if(thereIsPlate):
			print plateNumber , 
			if (plateNumber == rightOne) :
				print("Matched")				
		  	else :
				upload("theFrame.jpg" , "/theFrameOnRemote.jpg") 
				print("no match")
				
		else :
			print("no plate were found") 




	def getLicence(self , st) : 

		found = True 

		st = self.buildStr(st) 
		if (st.find('No license plates found') != -1 ) :
			found = False 
			return False , "" 
	

		return True , self.buildPlate(st)  



	def buildStr(self , st) :
		strr = ""
		for c in st :
			strr += str(c) 
		return strr 


	def buildPlate(self , st) :
		plate = ""
		ready = False 
		for c in st : 
			if(c == "\t") :
				break 
			if(ready) : 
				if(c != " ") : 
					plate += str(c) 
			if(c == "-") : 
				ready = True 
		return plate




def upload(localPath , remotePath):
    """Upload a file.
    Return the request response, or None in case of error.
    """




    with open(localPath, 'rb') as f:
        data = f.read()

        try:
            res = dbx.files_upload(data , remotePath, mode = WriteMode("overwrite"))
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None

    print('uploaded as', res.name.encode('utf8'))
    return res





cap = cv2.VideoCapture(0)


if not cap.isOpened() :
	print("cap was not opened")
	cap.open()

secValue = time.time() ; 
everyDelta = secValue 

# gmtime().tm_sec < secValue + 5
while(time.time() < secValue + 120):
    # Capture frame-by-frame
	ret, frame = cap.read()


    # Display the resulting frame
	cv2.imshow('frame', frame) 		
	
   
 # Our operations on the frame come here

	

	if(everyDelta + 2 < time.time() ) : 
		thereIsPlate = False 
		img = Image.fromarray(frame)
		img.save("theFrame.jpg")   
		TestParallel1(name ="theFrame.jpg").start()
		everyDelta =time.time()
		
     
 	

	
	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break





# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
