
#include "pydicomlib.hpp"

using namespace dicom;
using namespace boost::python;

namespace
{
	std::string ToString(Value& value)
	{
		std::stringstream s;
		s << value;
		return s.str();
	}

	template <VR vr>
	object
	ValueToPythonObject(const Value& value)
	{
		typename TypeFromVR<vr>::Type data;
		value >> data;
		return object(data);
	}


	///need to do a conversion to a python time object.  Any idea how?
	template <>
	object ValueToPythonObject<VR_DA>(const Value& value)
	{
		/*
			We have to use a workaround here, because of an obscure
			compiler bug with MSVC 7.06
		*/

		boost::gregorian::date d(0,0,0);
		value.Get(d);
		//const boost::gregorian::date& d=value.Get<boost::gregorian::date>();

		std::ostringstream Out;
		Out << boost::gregorian::to_simple_string(d);
		return object(Out.str());
	}

	/*
		amazingly enough, the following works.  Kudos to Dave Abrahams!
	*/

	template <>
	object ValueToPythonObject<VR_SQ>(const Value& value)
	{
		Sequence data;
		value.Get(data);
		boost::python::list l;
		for(Sequence::const_iterator I=data.begin();I!=data.end();I++)
			l.append(*I);
		return l;
	}

	object ValueToPythonObject1(Value& value)
	{
		switch(value.vr())
		{
		case VR_AE:
			return ValueToPythonObject<VR_AE>(value);
		case VR_AS:
			return ValueToPythonObject<VR_AS>(value);
		case VR_CS:
			return ValueToPythonObject<VR_CS>(value);
		case VR_DA:
			return ValueToPythonObject<VR_DA>(value);
		case VR_DS:
			return ValueToPythonObject<VR_DS>(value);
		case VR_DT:
			return ValueToPythonObject<VR_DT>(value);
		case VR_FD:
			return ValueToPythonObject<VR_FD>(value);
		case VR_FL:
			return ValueToPythonObject<VR_FL>(value);
		case VR_IS:
			return ValueToPythonObject<VR_IS>(value);
		case VR_LO:
			return ValueToPythonObject<VR_LO>(value);
		case VR_LT:
			return ValueToPythonObject<VR_LT>(value);
		case VR_OB:
			return ValueToPythonObject<VR_OB>(value);
		case VR_OW:
			return ValueToPythonObject<VR_OW>(value);
		case VR_PN:
			return ValueToPythonObject<VR_PN>(value);
		case VR_SH:
			return ValueToPythonObject<VR_SH>(value);
		case VR_SL:
			return ValueToPythonObject<VR_SL>(value);
		case VR_SQ:
			return ValueToPythonObject<VR_SQ>(value);
		case VR_SS:
			return ValueToPythonObject<VR_SS>(value);
		case VR_ST:
			return ValueToPythonObject<VR_ST>(value);
		case VR_TM:
			return ValueToPythonObject<VR_TM>(value);
		case VR_UI:
			return ValueToPythonObject<VR_UI>(value);
		case VR_UL:
			return ValueToPythonObject<VR_UL>(value);
		case VR_UN:
			return ValueToPythonObject<VR_UN>(value);
		case VR_US:
			return ValueToPythonObject<VR_US>(value);
		case VR_UT:
			return ValueToPythonObject<VR_UT>(value);
		default:
			throw BadVR(value.vr());
		}
	}

	VR ExtractVR(dicom::Value& v)
	{
		return v.vr();
	}
}//namespace


void AppendValueDefinition()
{
	class_<dicom::Value>("Value","A DICOM Value object",no_init)
		.def("__repr__",&ToString,			"get a string representation of value")
		.def("__call__",&ValueToPythonObject1)
		.add_property("vr",&ExtractVR)
	;
}
