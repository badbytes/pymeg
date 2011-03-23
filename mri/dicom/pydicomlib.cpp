/*
	Expose dicomlib C++ classes into python, using boost::python.

	Note that due to limitations with VC++ we have to spread
	the definitions over multiple translation units (.cpp files)
	 to avoid overtaxing the compiler.
*/

#include "pydicomlib.hpp"
#include <algorithm> //std::copy()
#include <iterator>
#include <iostream>
#include <deque>
using namespace std;
using namespace boost::python;
using namespace dicom;

namespace
{

	void AssociationRejectionTranslator(dicom::AssociationRejection const& x) 
	{
		std::ostringstream out;
		out <<x.what() << endl
			<< x.GetReason () << endl
			<< x.GetResult () << endl
			<< x.GetSource ();
		
        PyErr_SetString(PyExc_UserWarning, out.str().c_str());
    }




	BOOST_PYTHON_MODULE(dicom)
	{
		scope().attr("__doc__" )	= "Python bindings for the 'dicomlib' DICOM library";
		scope().attr("__version__")	= "0.5.0";

		AppendValueDefinition();
		AppendDataSetDefinition();
		AppendUIDDefinitions();
		AppendVRDefinitions();
		AppendTagDefinitions();
		AppendClientConnectionDefinition();
		/*
		and hopefully more to come...
		.
		.
		.
		*/
    
         register_exception_translator<
              dicom::AssociationRejection>(&AssociationRejectionTranslator);
	}

}//namespace

