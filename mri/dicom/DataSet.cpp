
#include "pydicomlib.hpp"
using namespace boost::python;
using namespace dicom;

namespace
{
	template<VR vr>
	dicom::Value
	ExtractToValue(const boost::python::object& o)
	{
		typedef typename dicom::TypeFromVR<vr>::Type Type;
		Type data=boost::python::extract<Type>(o);//Will raise a python TypeError on bad type.
		return dicom::Value(vr, data);
	}

	//!Specialisation for Date
	template<>
	dicom::Value ExtractToValue<VR_DA>(const boost::python::object& o)
	{
		std::string s=boost::python::extract<std::string>(o);//assume date is sent a string?
		boost::gregorian::date d(boost::gregorian::from_undelimited_string(s));
		return dicom::Value(VR_DA,d);
	}

	template<VR vr>
	DataSet::value_type
	ExtractTagValuePair(Tag tag,const boost::python::object& o)
	{
		return DataSet::value_type(tag,ExtractToValue<vr>(o));
	}



	void DataSetInsertHelper(DataSet& ds,Tag tag,const boost::python::object& o)
	{
		VR vr=dicom::GetVR(tag);
		switch(vr)
		{
		case VR_AE:
			ds.insert(ExtractTagValuePair<VR_AE>(tag,o));
			break;
		case VR_AS:
			ds.insert(ExtractTagValuePair<VR_AS>(tag,o));
			break;
			/*	case VR_AT:
			ds.insert(ExtractTagValuePair<VR_AT>(tag,o));*/
			break;
		case VR_CS:
			ds.insert(ExtractTagValuePair<VR_CS>(tag,o));
			break;
		case VR_DA:
			ds.insert(ExtractTagValuePair<VR_DA>(tag,o));
			break;
		case VR_DS:
			ds.insert(ExtractTagValuePair<VR_DS>(tag,o));
			break;
		case VR_DT:
			ds.insert(ExtractTagValuePair<VR_DT>(tag,o));
			break;
		case VR_FD:
			ds.insert(ExtractTagValuePair<VR_FD>(tag,o));
			break;
		case VR_FL:
			ds.insert(ExtractTagValuePair<VR_FL>(tag,o));
			break;
		case VR_IS:
			ds.insert(ExtractTagValuePair<VR_IS>(tag,o));
			break;
		case VR_LO:
			ds.insert(ExtractTagValuePair<VR_LO>(tag,o));
			break;
		case VR_LT:
			ds.insert(ExtractTagValuePair<VR_LT>(tag,o));
			break;
		case VR_OB:
			ds.insert(ExtractTagValuePair<VR_OB>(tag,o));
			break;
		case VR_OW:
			ds.insert(ExtractTagValuePair<VR_OW>(tag,o));
			break;
		case VR_PN:
			ds.insert(ExtractTagValuePair<VR_PN>(tag,o));
			break;
		case VR_SH:
			ds.insert(ExtractTagValuePair<VR_SH>(tag,o));
			break;
		case VR_SL:
			ds.insert(ExtractTagValuePair<VR_SL>(tag,o));
			break;
		case VR_SQ:
			ds.insert(ExtractTagValuePair<VR_SQ>(tag,o));
			break;
		case VR_SS:
			ds.insert(ExtractTagValuePair<VR_SS>(tag,o));
			break;
		case VR_ST:
			ds.insert(ExtractTagValuePair<VR_ST>(tag,o));
			break;
		case VR_TM:
			ds.insert(ExtractTagValuePair<VR_TM>(tag,o));
			break;
		case VR_UI:
			ds.insert(ExtractTagValuePair<VR_UI>(tag,o));
			break;
		case VR_UL:
			ds.insert(ExtractTagValuePair<VR_UL>(tag,o));
			break;
		case VR_UN:
			ds.insert(ExtractTagValuePair<VR_UN>(tag,o));
			break;
		case VR_US:
			ds.insert(ExtractTagValuePair<VR_US>(tag,o));
			break;
		case VR_UT:			
			ds.insert(ExtractTagValuePair<VR_UT>(tag,o));
			break;
		default:
			throw dicom::exception("Unknown vr");
		}
	}

	void DataSetEraseHelper(dicom::DataSet& data,Tag tag)
	{
		data.erase(tag);
	}

	void DataSetReplaceHelper(dicom::DataSet& ds,dicom::Tag tag, const boost::python::object& o)
	{
		ds.erase(tag);
		DataSetInsertHelper(ds,tag,o);
	}

	//!Get Values for given Tag.
	/*!
		returns a list of value objects.
	*/

	boost::python::list
	DataSetGetHelper(DataSet& ds, Tag tag)
	{
		boost::python::list l;
//		std::pair<DataSet::iterator,DataSet::iterator> p=ds.equal_range(tag);
		std::vector<Value> values=ds.Values(tag);
		for(std::vector<Value>::iterator I = values.begin();I!=values.end();I++)
			l.append(*I);
		//for(DataSet::iterator I =p.first;I!=p.second;I++)
			//l.append(I->second);
		return l;
	}

	//!Print dataset to a string.  This could equally well be implemented in pure python
	std::string DumpDataSet(DataSet& ds)
	{
		std::ostringstream os;
		os << ds;
		return os.str();
	}

	Tag GetTag(dicom::DataSet::value_type v)
	{
		return v.first;
	}
	Value GetValue(dicom::DataSet::value_type v)
	{
		return v.second;
	}

	std::string TagValuePairToString(const dicom::DataSet::value_type& p)
	{
		std::ostringstream s;
		s << dicom::GetName(p.first) << " : " << p.second;
		return s.str();
	}

	DataSet OpenDataSet(std::string FileName)
	{
		std::ifstream In(FileName.c_str(),std::ios::binary|std::ios::in);
		if(!In)
			throw dicom::exception("can't open file.");
		DataSet data;
		dicom::ReadFromStream(In,data);
		return data;
	}

	void WriteDataSet(DataSet& data, std::string FileName)
	{
		//I'm not sure that using implicit is a good idea here.
		//dicom::TS ts(dicom::IMPL_VR_LE_TRANSFER_SYNTAX);
		dicom::TS ts(dicom::EXPL_VR_LE_TRANSFER_SYNTAX);
		std::ofstream out(FileName.c_str(),std::ios::binary);
		if(!out)
			throw dicom::exception("Can't open file for writing");
		dicom::WriteToStream(data,out,ts);
	}


}//namespace

void AppendDataSetDefinition()
{
	// need this to make iterators work properly.
	class_<dicom::DataSet::value_type>("TagValuePair",no_init)
		.add_property("Tag",&GetTag)
		.add_property("Value",&GetValue)
		.def("__repr__",&TagValuePairToString)
	;

	class_<dicom::DataSet>("DataSet","A dataset is a set of Tag-Value pairs")
		.def("__len__",&dicom::DataSet::size,		"how many attributes in dataset")
		.def("__getitem__",DataSetGetHelper,		"use [] to get a list of values with a given tag")
		.def("__iter__",iterator<dicom::DataSet>())	//adding a docstring here caused a compilation error!
		.def("__repr__",DumpDataSet,				"prints entire contents of dataset")
		.def("count",&dicom::DataSet::count,		"count occurances of a given tag")
		.def("insert",DataSetInsertHelper,			"insert a value for a given tag.  This will NOT delete existing values")
		.def("replace",DataSetReplaceHelper,		"insert a value for a given tag.  This WILL delete existing values")
		.def("erase",DataSetEraseHelper,			"erase all elements with a given tag")
	;

	def("open",OpenDataSet,	"open a dicom file, returns a DataSet");
	def("write",WriteDataSet,	"writes a DataSet to a file");


}
