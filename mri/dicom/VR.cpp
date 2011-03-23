
#include "pydicomlib.hpp"
using namespace boost::python;
using namespace dicom;

void AppendVRDefinitions()
{
	enum_<VR>("VR")
		.value("AE",dicom::VR_AE)
		.value("AS",dicom::VR_AS)
		.value("AT",dicom::VR_AT)
		.value("CS",dicom::VR_CS)
		.value("DA",dicom::VR_DA)
		.value("DS",dicom::VR_DS)
		.value("DT",dicom::VR_DT)
		.value("FD",dicom::VR_FD)
		.value("FL",dicom::VR_FL)
		.value("IS",dicom::VR_IS)
		.value("LO",dicom::VR_LO)
		.value("LT",dicom::VR_LT)
		.value("OB",dicom::VR_OB)
		.value("OW",dicom::VR_OW)
		.value("PN",dicom::VR_PN)
		.value("SH",dicom::VR_SH)
		.value("SL",dicom::VR_SL)
		.value("SQ",dicom::VR_SQ)
		.value("SS",dicom::VR_SS)
		.value("ST",dicom::VR_ST)
		.value("TM",dicom::VR_TM)
		.value("UI",dicom::VR_UI)
		.value("UL",dicom::VR_UL)
		.value("UN",dicom::VR_UN)
		.value("US",dicom::VR_US)
		.value("UT",dicom::VR_UT)
		;

		//can we do something clever to make this the docstrings?
		def("GetVRName",&dicom::GetVRName,	"convert a VR enum value to a human-readable string");


}
