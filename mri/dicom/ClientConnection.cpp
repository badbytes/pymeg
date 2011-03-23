
#include "pydicomlib.hpp"
using namespace boost::python;
using namespace dicom;

namespace
{
	boost::python::list
	ClientConnection_FindHelper(ClientConnection& connection,const DataSet& Query,QueryRetrieve::Root root)
	{
		std::vector<DataSet> Results=connection.Find(Query,root/*QueryRetrieve::STUDY_ROOT*/);

		boost::python::list l;
		for(std::vector<DataSet>::const_iterator I =Results.begin();I!=Results.end();I++)
			l.append(*I);

		return l;
	}

	void PresentationContextAddHelper1(dicom::PresentationContexts& pcs,const UID& uid)
	{
		pcs.Add(uid);
	}

	void PresentationContextAddHelperTS(dicom::PresentationContexts& pcs, const UID& uid,dicom::TS ts)
	{
		//dicom::TS ts(dicom::JPEG_LOSSLESS_NON_HIERARCHICAL);
		pcs.Add(uid,ts);
	}


	std::string AcceptedPresentationContexts(dicom::ClientConnection& connection)
	{
		std::ostringstream out;
		for(int i=0;i<connection.AcceptedPresentationContexts_.size();i++)
		{
			out << connection.AcceptedPresentationContexts_[i].TrnSyntax_.UID_.str() << std::endl;
		}
		return out.str();
	}

	//void ClientConnectionStoreJpeg(dicom::ClientConnection& connection, dicom::DataSet& dataset)
	//{
	//	dicom::TS ts(dicom::JPEG_LOSSLESS_NON_HIERARCHICAL);
	//	connection.Store(dataset,ts);
	//}
}//namespace

void AppendClientConnectionDefinition()
{
	enum_<QueryRetrieve::Root>("QueryRetrieveRoot")
		.value("STUDY_ROOT",dicom::QueryRetrieve::STUDY_ROOT)
		.value("PATIENT_ROOT",dicom::QueryRetrieve::PATIENT_ROOT)
		.value("PATIENT_STUDY_ONLY",dicom::QueryRetrieve::PATIENT_STUDY_ONLY)
		;


	/*
		this would be used like
		uids=dicom.UIDS()
		uid=uids.MAMMO_PRES_IMAGE_STORAGE_SOP_CLASS
		pcs=dicom.PresentationContexts()
		pcs.Add(uid)
		c=dicom.ClientConnection('localhost',5678,'AE1','AE2',pcs)
	*/
	class_<dicom::PresentationContexts>("PresentationContexts")
		.def("Add",&PresentationContextAddHelper1)
		.def("AddTS",&PresentationContextAddHelperTS)
		;

	class_<dicom::ClientConnection>(
		"ClientConnection",
		init<std::string,short,std::string,std::string,const dicom::PresentationContexts&>()
		)
		.def("Store",&dicom::ClientConnection::Store)
		//.def("StoreJpeg",ClientConnectionStoreJpeg)
		.def("Find",ClientConnection_FindHelper)
		.def("Move",&dicom::ClientConnection::Move)
		.def("Echo",&dicom::ClientConnection::Echo)
		.def("AcceptedPresentationContexts",AcceptedPresentationContexts)
		;


	class_<dicom::TS>("TransferSyntax",
		init<const dicom::UID&>())
		.def("isExplicitVR",&dicom::TS::isExplicitVR)
		.def("isBigEndian",&dicom::TS::isBigEndian)
		.def("isDeflated",&dicom::TS::isDeflated)
		.def("isEncoded",&dicom::TS::isEncoded)
		.def("getUID",&dicom::TS::getUID)
		;
}

