
#include "pydicomlib.hpp"

using namespace dicom;
using namespace boost::python;

namespace
{

/*!
	The use case is:

	>>> import dicom
	>>> uid=dicom.UIDS.MAMMO_PRES_IMAGE_STORAGE_SOP_CLASS


	Note we have to jump through a few hoops with the use of scope() 
	to achieve this.

	I don't know if there's a nice way of adding docstrings to these entries.
*/

	void AppendUIDS()
	{
		scope().attr("VERIFICATION_SOP_CLASS") = VERIFICATION_SOP_CLASS;


		scope().attr("CR_IMAGE_STORAGE_SOP_CLASS") = CR_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("CT_IMAGE_STORAGE_SOP_CLASS") = CT_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("USOLD_MF_IMAGE_STORAGE_SOP_CLASS") = USOLD_MF_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("US_MF_IMAGE_STORAGE_SOP_CLASS") = US_MF_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("MR_IMAGE_STORAGE_SOP_CLASS") = MR_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("USOLD_IMAGE_STORAGE_SOP_CLASS") = USOLD_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("US_IMAGE_STORAGE_SOP_CLASS") = US_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("SC_IMAGE_STORAGE_SOP_CLASS") = SC_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("NM_IMAGE_STORAGE_SOP_CLASS") = NM_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("XA_IMAGE_STORAGE_SOP_CLASS") = XA_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("XRF_IMAGE_STORAGE_SOP_CLASS") = XRF_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("XA2_IMAGE_STORAGE_SOP_CLASS") = XA2_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("PET_IMAGE_STORAGE_SOP_CLASS") = PET_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("DX_PRES_IMAGE_STORAGE_SOP_CLASS") = DX_PRES_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("DX_PROC_IMAGE_STORAGE_SOP_CLASS") = DX_PROC_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("MAMMO_PRES_IMAGE_STORAGE_SOP_CLASS") = MAMMO_PRES_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("MAMMO_PROC_IMAGE_STORAGE_SOP_CLASS") = MAMMO_PROC_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("BASIC_TEXT_SR_STORAGE_SOP_CLASS") = BASIC_TEXT_SR_STORAGE_SOP_CLASS;
		scope().attr("ENHANCED_SR_STORAGE_SOP_CLASS") = ENHANCED_SR_STORAGE_SOP_CLASS;
		scope().attr("COMPREHENSIVE_SR_STORAGE_SOP_CLASS") = COMPREHENSIVE_SR_STORAGE_SOP_CLASS;
		scope().attr("INTRAORAL_PRES_IMAGE_STORAGE_SOP_CLASS") = INTRAORAL_PRES_IMAGE_STORAGE_SOP_CLASS;
		scope().attr("INTRAORAL_PROC_IMAGE_STORAGE_SOP_CLASS") = INTRAORAL_PROC_IMAGE_STORAGE_SOP_CLASS;

		//


		scope().attr("PATIENT_ROOT_QR_FIND_SOP_CLASS") = PATIENT_ROOT_QR_FIND_SOP_CLASS;
		scope().attr("PATIENT_ROOT_QR_MOVE_SOP_CLASS") = PATIENT_ROOT_QR_MOVE_SOP_CLASS;
		scope().attr("PATIENT_ROOT_QR_GET_SOP_CLASS") = PATIENT_ROOT_QR_GET_SOP_CLASS;
		scope().attr("STUDY_ROOT_QR_FIND_SOP_CLASS") = STUDY_ROOT_QR_FIND_SOP_CLASS;
		scope().attr("STUDY_ROOT_QR_MOVE_SOP_CLASS") = STUDY_ROOT_QR_MOVE_SOP_CLASS;
		scope().attr("STUDY_ROOT_QR_GET_SOP_CLASS") = STUDY_ROOT_QR_GET_SOP_CLASS;
		scope().attr("PATIENT_STUDY_ONLY_QR_FIND_SOP_CLASS") = PATIENT_STUDY_ONLY_QR_FIND_SOP_CLASS;
		scope().attr("PATIENT_STUDY_ONLY_QR_MOVE_SOP_CLASS") = PATIENT_STUDY_ONLY_QR_MOVE_SOP_CLASS;
		scope().attr("PATIENT_STUDY_ONLY_QR_GET_SOP_CLASS") = PATIENT_STUDY_ONLY_QR_GET_SOP_CLASS;
		scope().attr("MODALITY_WORKLIST_SOP_CLASS") = MODALITY_WORKLIST_SOP_CLASS;


		/*
			Transfer syntaxes
		*/
		scope().attr("IMPL_VR_LE_TRANSFER_SYNTAX") = IMPL_VR_LE_TRANSFER_SYNTAX;
		scope().attr("EXPL_VR_LE_TRANSFER_SYNTAX")= EXPL_VR_LE_TRANSFER_SYNTAX;
		scope().attr("DEFLATED_EXPL_VR_LE_TRANSFER_SYNTAX")= DEFLATED_EXPL_VR_LE_TRANSFER_SYNTAX;
		scope().attr("EXPL_VR_BE_TRANSFER_SYNTAX")= EXPL_VR_BE_TRANSFER_SYNTAX;
		scope().attr("JPEG_BASELINE_TRANSFER_SYNTAX")= JPEG_BASELINE_TRANSFER_SYNTAX;
		scope().attr("JPEG_LOSSLESS_NON_HIERARCHICAL")= JPEG_LOSSLESS_NON_HIERARCHICAL;


	}
	
	//!We don't give this any members, we add them via the boost::python mechanism below
	struct UIDS{};


	//UID makeUID(const std::string& Prefix);

}//namespace


void AppendUIDDefinitions()
{

	//First expose the UID class

	class_<dicom::UID>("UID",init<std::string>())	
		.def("__repr__",&UID::str)
		;

	def("makeUID",dicom::makeUID,"Creates a new unique UID with a given prefix")
		;
	//now make all the UIDS that we know about static members of the UIDS class

	scope outer_scope=scope();						//Get current scope.
	scope uids_scope= class_<UIDS>("UIDS");			//Note that this changes the default scope!
	
	AppendUIDS();									//See above.

	scope reset = outer_scope;						//resets current scope.


}
