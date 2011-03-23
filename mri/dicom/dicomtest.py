#!/bin/env python
#pydicomlib test suite
#
# This is the test script we use internally against our install of scippy
# The tests will only succeed if you're storing the same images as us, which is unlikely
# However, you can modify it for your own needs, or use it as an example of how to
# use the python dicom library.


import dicom
import os
import time
from dicom import UID

def OpenDataset():
    ds=dicom.open("test_dicom_file")
    return ds

def TestOpeningADataset():
	ds=OpenDataset()
	print "succesfully opened dataset"

def TestWritingADataset(ds):
	dicom.write(ds,"test_output_file")

def MakeClientConnection(host='localhost',client='client',server='server'):
	pcs=dicom.PresentationContexts()
	pcs.Add(dicom.UIDS.VERIFICATION_SOP_CLASS)
	pcs.Add(dicom.UIDS.MAMMO_PRES_IMAGE_STORAGE_SOP_CLASS)
	pcs.Add(dicom.UIDS.STUDY_ROOT_QR_FIND_SOP_CLASS)
	pcs.Add(dicom.UIDS.PATIENT_ROOT_QR_FIND_SOP_CLASS)
	pcs.Add(dicom.UIDS.STUDY_ROOT_QR_MOVE_SOP_CLASS)
	pcs.Add(dicom.UIDS.PATIENT_ROOT_QR_MOVE_SOP_CLASS)
	pcs.Add(dicom.UIDS.MAMMO_PROC_IMAGE_STORAGE_SOP_CLASS)
	c=dicom.ClientConnection(host,104,client,server,pcs)
	return c

def PatientQuery():
	query=dicom.DataSet()
	query.insert(dicom.Tag.QR_LEVEL,'PATIENT')#should really be 'PATIENT'
	query.insert(dicom.Tag.PAT_NAME,'*')
	query.insert(dicom.Tag.PAT_ID,'*')
	return query

def StudyQuery():
	query=dicom.DataSet()
	query.insert(dicom.Tag.QR_LEVEL,'STUDY')
#	query.insert(dicom.Tag.STUDY_INST_UID,UID('*'))
 	query.insert(dicom.Tag.PAT_NAME,'*')
	return query#should find 5 studies.

def MultiplicityQuery1():
	query=dicom.DataSet()
	query.insert(dicom.Tag.QR_LEVEL,'IMAGE')
	query.insert(dicom.Tag.STUDY_INST_UID,UID('*'))
 	query.insert(dicom.Tag.SERIES_INST_UID,UID('*'))
	query.insert(dicom.Tag.SOP_INST_UID,UID('*'))
	query.insert(dicom.Tag.WINDOW_CENTER,'2341')#does exist
	query.insert(dicom.Tag.WINDOW_CENTER,'2342')#doesn't exist
	return query#should find 1 image

#
#try the following SQL to illustrate the next test:
# select parent,attribute.value from attribute,tag where attribute.tag=tag.value  and tag.description='WindowCenter';
#
def MultiplicityQuery2():
	query=dicom.DataSet()
	query.insert(dicom.Tag.QR_LEVEL,'IMAGE')
	query.insert(dicom.Tag.STUDY_INST_UID,UID('*'))
 	query.insert(dicom.Tag.SERIES_INST_UID,UID('*'))
	query.insert(dicom.Tag.SOP_INST_UID,UID('*'))
	query.insert(dicom.Tag.WINDOW_CENTER,'2341')#does exist
	query.insert(dicom.Tag.WINDOW_CENTER,'2365')#also exists in same image
	query.insert(dicom.Tag.WINDOW_CENTER,'2023')#exists in differentt image
	return query#should find 2 image

def UIDListQuery():
	query=dicom.DataSet()
	query.insert(dicom.Tag.QR_LEVEL,'IMAGE')
	query.insert(dicom.Tag.STUDY_INST_UID,UID('*'))
 	query.insert(dicom.Tag.SERIES_INST_UID,UID('*'))
	query.insert(dicom.Tag.SOP_INST_UID,UID('1.2.840.113619.2.66.2159378590.1778000418141943.11'))
	query.insert(dicom.Tag.SOP_INST_UID,UID('1.2.840.113619.2.66.2159378590.19003000418141934.3'))
	return query#should find 2 image



def Verify(query_maker,expected_results,root=dicom.QueryRetrieveRoot.STUDY_ROOT):
	query = query_maker()
	c=MakeClientConnection()
	result=c.Find(query,root)
	if(len(result)==expected_results):
		print query_maker.__name__ + " passed"
	else:
		print query_maker.__name__ + " failed"
		print "Length:" + str(len(result))
		print result


def MakeImageQuery():
	query=dicom.DataSet()
	query.insert(dicom.Tag.QR_LEVEL,'IMAGE')
	query.insert(dicom.Tag.STUDY_INST_UID,UID('*'))
 	query.insert(dicom.Tag.SERIES_INST_UID,UID('*'))
	query.insert(dicom.Tag.SOP_INST_UID,UID('*'))
 	query.insert(dicom.Tag.ANODE_MATERIAL,'RHODIUM')
	return query


def MakeStudyMoveRequest():
	query=dicom.DataSet()
	query.insert(dicom.Tag.QR_LEVEL,'STUDY')
	query.insert(dicom.Tag.STUDY_INST_UID,UID('1.2.840.113619.2.66.2159378590.19003000418141451.20000'))
	return query

def MakePatientMoveRequest():
	query=dicom.DataSet()
	query.insert(dicom.Tag.QR_LEVEL,'PATIENT')
	query.insert(dicom.Tag.PAT_ID,'970814')
	query.insert(dicom.Tag.PAT_ID,'957157')
	return query

def TestACMove():
	"""
	should do a c-find on some criteria, then ask for
	returned uids to be moved somewhere.
	"""
	query=MakeStudyMoveRequest()
	c=MakeClientConnection()
	result=c.Move('lite',query,dicom.QueryRetrieveRoot.STUDY_ROOT)
	return result

def TestPatientCMove():
	query=MakePatientMoveRequest()
	c=MakeClientConnection()
	result=c.Move('lite',query,dicom.QueryRetrieveRoot.PATIENT_ROOT)
	return result


def SubmitLotsOfImages():
	c=MakeClientConnection()
	directory=str()
	if(os.uname()[0]=='Linux'):
		directory='/mnt/windows/TestRead/'
	else:
		directory="C:\\TestRead\\StoreTest\\"
	images=os.listdir(directory)
	for image in images:
		ds=dicom.open(directory+image)
		ret=c.Store(ds)
		print ret


def RunTests():

	TestOpeningADataset()
	Verify(MakeImageQuery,6)
	Verify(MultiplicityQuery1,1)
	Verify(MultiplicityQuery2,2)
	Verify(UIDListQuery,2)
	Verify(StudyQuery,5)
	Verify(PatientQuery,5,dicom.QueryRetrieveRoot.PATIENT_ROOT)

if __name__ == '__main__':
	t=time.time()
	try:
 		RunTests()
#		TestPatientCMove()
	except RuntimeError, e:
		print e
	t=time.time()-t
	print "Tests took: " + str(t) + " seconds to complete"
