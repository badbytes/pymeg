


#ifndef PYDICOMLIB_HPP_INCLUDE_GUARDEUI7894DI9E994YD
#define PYDICOMLIB_HPP_INCLUDE_GUARDEUI7894DI9E994YD


#include <boost/python.hpp>
#include <boost/date_time/gregorian/gregorian.hpp>
#include <fstream>
#include <string>
#include "dicomlib/dicomlib.hpp"

/*
	We have to split the export definitions over multiple
	functions to avoid hitting error c1204, ('Compiler limit:internal structure overflow')
	in MSVC v7
	See the Boost.python FAQ for more info.
*/


void AppendValueDefinition();
void AppendEnumDefinitions();
void AppendTagDefinitions();
void AppendVRDefinitions();
void AppendUIDDefinitions();
void AppendClientConnectionDefinition();
void AppendDataSetDefinition();

#endif //PYDICOMLIB_HPP_INCLUDE_GUARDEUI7894DI9E994YD
