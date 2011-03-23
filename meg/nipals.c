/*
nipals.c

The c_nipals python extension for pca_module
(made by Henning Risvik, May 2007)
*/

#include "Python.h"

// the arrayobject.h, change to correct path depending on your numpy/Numeric installation
#include "/usr/lib/python2.5/site-packages/numpy/core/include/numpy/arrayobject.h"
#include "math.h"


#define IND1(a, i) *((double *)(a->data + i*a->strides[0]))
#define IND2(a, i, j) *((double *)(a->data + i*a->strides[0] + j*a->strides[1]))
#define IND3(a, i, j, k) *((double *)(a->data + i*a->strides[0] + j*a->strides[1] + k*a->strides[2]))
#define TYPECHECK(a, type) \
if (a->descr->type_num != type) { \
PyErr_Format(PyExc_TypeError, "array is not of correct type (%d)", type); \
return NULL; \
}


/* .... Custom C functions ..................*/

static void transpose(double **m, double **m_transposed, int cols, int rows)
/*
Transpose array m onto array m_transposed
*/
{
	int i, j;
	for (i = 0; i < cols; i++)
	{
		for (j = 0; j < rows; j++)
		{
			m_transposed[i][j] = m[j][i];
		}
    }
}

static double vector_inner(double *v, int length)
/* returns (v' * v)  */
{
    double val = 0;
    int i;
    for (i = 0; i < length; i++)
    { val += v[i]*v[i]; }
	return val;
}

static void vector_div(double *v, int length, double value)
/* v[0:length] / value */
{
    int i;
    for (i = 0; i < length; i++)
    { v[i] = v[i] / value; }
}


static void vector_mul(double *v, int length, double value)
/* v[0:length] * value */
{
    int i;
    for (i = 0; i < length; i++)
    { v[i] = v[i] * value; }
}

static void matrix_vector_prod(double **A, int cols, int rows, double *x, double *b)
/*
returns vector b of Ax = b

x must have length: cols
b must have length: rows
*/
{
	int i, j;
	double sum;
	for (i = 0; i < rows; i++)
	{
		sum = 0;
		for (j = 0; j < cols; j++)
		{
			sum += A[i][j] * x[j];
		}
		b[i] = sum;
    }
}

static void get_column(double *t, double **E, int cols, int rows)
/* sets acceptable t  */
{
    int i, j;
    for (i = 0; i < cols; i++)
    {
	    for (j = 0; j < rows; j++)
	    {
		  t[j] = E[j][i];
	    }
	    if (vector_inner(t, rows) > 0)
        { return; }
    }
    return;
}

static void remove_tp(double **E, int cols, int rows, double *t, double *p)
/*
Essentially: E = E - (tp')

Here it is done element-wise.
*/
{
  int i, j;
  for (i = 0; i < rows; i++)
  {
    for (j = 0; j < cols; j++)
    {
        E[i][j] = E[i][j] - (t[i]*p[j]);
    }
  }
}

static double total_residual_obj_var(double **e, int cols, int rows, double e_tot0)
/* get total residual variance of E-matrix */
{
  int i, j;
  double sum, e_tot;
  e_tot = 0;
  for (i = 0; i < rows; i++)
  {
	sum = 0;
    for (j = 0; j < cols; j++)
    {
        sum += pow(e[i][j], 2);
    }
    e_tot += sum / e_tot0; // scaling to correct size
  }
  return e_tot;
}

static double total_residual_obj_var_e0(double **e, int cols, int rows)
/* get total residual variance of E[0] */
{
  int i, j;
  double sum, e_tot0;

  e_tot0 = 0;
  for (i = 0; i < rows; i++)
  {
	sum = 0;
    for (j = 0; j < cols; j++)
    {
        sum += pow(e[i][j], 2);
    }
    e_tot0 += sum;
  }
  return e_tot0;
}


/* .... Python callable functions ..................*/

static PyObject *nipals(PyObject *self, PyObject *args)
/* fills the Scores and Loadings matrices and returns explained_var array */
{
  /*
  Estimation of PC components with the iterative NIPALS method:


  E[0] = mean_center(X)  (the E-matrix for the zero-th PC)

  t = E(:, 0)  (a column in X (mean centered) is set as starting t vector)

  for i=1 to (PCs):

    1  p=(E[i-1]'t) / (t't)  Project X onto t to find the corresponding loading p

    2  p = p * (p'p)^-0.5  Normalise loading vector p to length 1

    3  t = (E[i-1]p) / (p'p)  Project X onto p to find corresponding score vector t

    4  Check for convergence, if difference between eigenval_new and eigenval_old is larger than threshold*eigenval_new return to step 1

    5  E[i] = E[i-1] - tp'  Remove the estimated PC component from E[i-1]

    */
    PyArrayObject *Scores, *Loadings, *E, *explained_var;
	double threshold, eigenval_t, eigenval_p, eigenval_new;
	double eigenval_old = 0.0;
	double e_tot0, e_tot, tot_explained_var, temp;
	int i, j, PCs, cols, rows, cols_t, rows_t;
	int convergence, ready_for_compare;
	int dims[2]; // for explained_var creation


	/* Get arguments:  */
	if (!PyArg_ParseTuple(args, "O!O!O!id:nipals", &PyArray_Type,
	                                               &Scores,
		                                           &PyArray_Type,
		                                           &Loadings,
												   &PyArray_Type,
												   &E,
												   &PCs,
												   &threshold))
	{
		return NULL;
	}


    /* safety checks */
	if (NULL == Scores)  return NULL;
	if (NULL == Loadings)  return NULL;
	if (NULL == E)  return NULL;

    if (Scores->nd != 2)
    {  PyErr_Format(PyExc_ValueError,
       "Scores array has wrong dimension (%d)",
       Scores->nd); return NULL;
    }
    if (Loadings->nd != 2)
    {  PyErr_Format(PyExc_ValueError,
       "Loadings array has wrong dimension (%d)",
       Loadings->nd); return NULL;
    }
    if (E->nd != 2)
    {  PyErr_Format(PyExc_ValueError,
       "E array has wrong dimension (%d)",
       E->nd); return NULL;
    }

    //TYPECHECK(Scores, PyArray_DOUBLE);
    //TYPECHECK(Loadings, PyArray_DOUBLE);
    //TYPECHECK(E, PyArray_DOUBLE);

	rows = E->dimensions[0];
	cols = E->dimensions[1];
	/* Set 2d array pointer e */
	double *data_ptr;
    data_ptr = (double *) E->data; /* a is a PyArrayObject* pointer */
    double **e;
    e = (double **) malloc((rows)*sizeof(double*));
    for (i = 0; i < rows; i++)
    { e[i] = &(data_ptr[i*cols]); /* point row no. i in E->data */ }

	/* Set t vector */
	double t[rows];
	double p[cols];

	//for(i = 0; i < rows; i++)
	//{ t[i] = e[i][0]; }
    get_column(t, e, cols, rows);


	/* Create explained variance array */
	dims[0] = PCs;
	explained_var = (PyArrayObject *) PyArray_FromDims(1, dims, PyArray_DOUBLE);
	e_tot0 = total_residual_obj_var_e0(e, cols, rows);
	tot_explained_var = 0;


	/* Transposed E[0] */
	cols_t = rows; rows_t = cols;
    double **e_transposed;
    e_transposed = (double **) malloc((rows_t)*sizeof(double*));
    for (i = 0; i < rows_t; i++)
    { e_transposed[i] = (double *) malloc((cols_t)*sizeof(double)); }


	/* Do iterations (0, PCs) */
	for(i = 0; i < PCs; i++)
    {
	  convergence = 0;
	  ready_for_compare = 0;
	  transpose(e, e_transposed, cols, rows);

	  while(convergence == 0)
	  {
	    // 1  p=(E[i-1]'t) / (t't)  Project X onto t to find the corresponding loading p
	    matrix_vector_prod(e_transposed, cols_t, rows_t, t, p);
	    eigenval_t = vector_inner(t, rows);
	    vector_div(p, cols, eigenval_t);


	    // 2  p = p * (p'p)^-0.5  Normalise loading vector p to length 1
	    eigenval_p = vector_inner(p, cols);
	    temp = pow(eigenval_p, (-0.5));
	    vector_mul(p, cols, temp);


	    // 3  t = (E[i-1]p) / (p'p)  Project X onto p to find corresponding score vector t
	    matrix_vector_prod(e, cols, rows, p, t);
	    eigenval_p = vector_inner(p, cols);
	    vector_div(t, rows, eigenval_p);


	    // 4  Check for convergence
	    eigenval_new = vector_inner(t, rows);


	    if(ready_for_compare == 0)
	    {
			ready_for_compare = 1;
		}
	    else
	    {
			if((eigenval_new - eigenval_old) < threshold*eigenval_new)
			{ convergence = 1; }


		}
		eigenval_old = eigenval_new;
      }

	  // 5  E[i] = E[i-1] - tp'  Remove the estimated PC component from E[i-1] and sets result to E[i]
	  remove_tp(e, cols, rows, t, p);


	  /* Add current Scores and Loadings to collection */
	  for(j = 0; j < rows; j++){ IND2(Scores, j, i) = t[j]; }
	  for(j = 0; j < cols; j++){ IND2(Loadings, i, j) = p[j]; }

	  /* Update explained variance array */
	  e_tot = total_residual_obj_var(e, cols, rows, e_tot0); // for E[i]
	  IND1(explained_var, i) = 1 - e_tot - tot_explained_var; // explained var for PC[i]
	  tot_explained_var += IND1(explained_var, i);
    }

    free(e);
    for (i = 0; i < rows_t; i++)
    { free(e_transposed[i]); }
    free(e_transposed);

	return PyArray_Return(explained_var);
}


static PyObject *nipals2(PyObject *self, PyObject *args)
/* fills the Scores- and Loadings-matrix and E-matrices */
{
  /*
  Estimation of PC components with the iterative NIPALS method:


  E[0] = mean_center(X)  (the E-matrix for the zero-th PC)

  t = E(:, 0)  (a column in X (mean centered) is set as starting t vector)

  for i=1 to (PCs):

    1  p=(E[i-1]'t) / (t't)  Project X onto t to find the corresponding loading p

    2  p = p * (p'p)^-0.5  Normalise loading vector p to length 1

    3  t = (E[i-1]p) / (p'p)  Project X onto p to find corresponding score vector t

    4  Check for convergence, if difference between eigenval_new and eigenval_old is larger than threshold*eigenval_new return to step 1

    5  E[i] = E[i-1] - tp'  Remove the estimated PC component from E[i-1]

    */
    PyArrayObject *Scores, *Loadings, *E, *Error_matrices;
	double threshold, eigenval_t, eigenval_p, eigenval_new;
	double eigenval_old = 0.0;
	double temp;
	int i, j, k, PCs, cols, rows, cols_t, rows_t;
	int convergence, ready_for_compare;


	/* Get arguments:  */
	if (!PyArg_ParseTuple(args, "O!O!O!O!id:nipals2", &PyArray_Type,
	                                               &Scores,
		                                           &PyArray_Type,
		                                           &Loadings,
												   &PyArray_Type,
												   &E,
												   &PyArray_Type,
												   &Error_matrices,
												   &PCs,
												   &threshold))
	{
		return NULL;
	}


    /* safety checks */
	if (NULL == Scores)  return NULL;
	if (NULL == Loadings)  return NULL;
	if (NULL == E)  return NULL;

    if (Scores->nd != 2)
    {  PyErr_Format(PyExc_ValueError,
       "Scores array has wrong dimension (%d)",
       Scores->nd); return NULL;
    }
    if (Loadings->nd != 2)
    {  PyErr_Format(PyExc_ValueError,
       "Loadings array has wrong dimension (%d)",
       Loadings->nd); return NULL;
    }
    if (E->nd != 2)
    {  PyErr_Format(PyExc_ValueError,
       "E array has wrong dimension (%d)",
       E->nd); return NULL;
    }
    if (Error_matrices->nd != 3)
    {  PyErr_Format(PyExc_ValueError,
       "Error_matrices array has wrong dimension (%d)",
       Error_matrices->nd); return NULL;
    }


    //TYPECHECK(Scores, PyArray_DOUBLE);
    //TYPECHECK(Loadings, PyArray_DOUBLE);
    //TYPECHECK(E, PyArray_DOUBLE);

	rows = E->dimensions[0];
	cols = E->dimensions[1];
	/* Set 2d array pointer e */
	double *data_ptr;
    data_ptr = (double *) E->data; /* is a PyArrayObject* pointer */
    double **e;
    e = (double **) malloc((rows)*sizeof(double*));
    for (i = 0; i < rows; i++)
    { e[i] = &(data_ptr[i*cols]); /* point row no. i in E->data */ }


	/* Set 3d array pointer e_matrices
	double *data_ptr2;
    data_ptr2 = (double *) Error_matrices->data; // is a PyArrayObject* pointer
    double ***e_matrices;
    e_matrices = (double ***) malloc((rows)*sizeof(double*));
    for (i = 0; i < PCs; i++)
    {
        for (j = 0; j < rows; j ++)
        { e_matrices[i][j] = &(data_ptr2[i*cols*rows]);  } // point array (i,j) in Error_matrices->data
    }*/


	/* Set t vector */
	double t[rows];
	double p[cols];
	//for(i = 0; i < rows; i++)
	//{ t[i] = e[i][0]; }
    get_column(t, e, cols, rows);

	/* Transposed E[0] */
	cols_t = rows; rows_t = cols;
    double **e_transposed;
    e_transposed = (double **) malloc((rows_t)*sizeof(double*));
    for (i = 0; i < rows_t; i++)
    { e_transposed[i] = (double *) malloc((cols_t)*sizeof(double)); }


	/* Do iterations (0, PCs) */
	for(i = 0; i < PCs; i++)
    {
	  convergence = 0;
	  ready_for_compare = 0;
	  transpose(e, e_transposed, cols, rows);

	  while(convergence == 0)
	  {
	    // 1  p=(E[i-1]'t) / (t't)  Project X onto t to find the corresponding loading p
	    matrix_vector_prod(e_transposed, cols_t, rows_t, t, p);
	    eigenval_t = vector_inner(t, rows);
	    vector_div(p, cols, eigenval_t);


	    // 2  p = p * (p'p)^-0.5  Normalise loading vector p to length 1
	    eigenval_p = vector_inner(p, cols);
	    temp = pow(eigenval_p, (-0.5));
	    vector_mul(p, cols, temp);


	    // 3  t = (E[i-1]p) / (p'p)  Project X onto p to find corresponding score vector t
	    matrix_vector_prod(e, cols, rows, p, t);
	    eigenval_p = vector_inner(p, cols);
	    vector_div(t, rows, eigenval_p);


	    // 4  Check for convergence
	    eigenval_new = vector_inner(t, rows);


	    if(ready_for_compare == 0)
	    {
			ready_for_compare = 1;
		}
	    else
	    {
			if((eigenval_new - eigenval_old) < threshold*eigenval_new)
			{ convergence = 1; }


		}
		eigenval_old = eigenval_new;
      }

	  // 5  E[i] = E[i-1] - tp'  Remove the estimated PC component from E[i-1] and sets result to E[i]
	  remove_tp(e, cols, rows, t, p);


	  /* Add current Scores and Loadings to collection */
	  for(j = 0; j < rows; j++){ IND2(Scores, j, i) = t[j]; }
	  for(j = 0; j < cols; j++){ IND2(Loadings, i, j) = p[j]; }

	  /* Add current E to Error_matrices */
	  for(j = 0; j < rows; j++)
	  {
		  for(k = 0; k < cols; k++)
		  {
			  IND3(Error_matrices, i, j, k) = e[j][k];
		  }
	  }

    }

    free(e);
    for (i = 0; i < rows_t; i++)
    { free(e_transposed[i]); }
    free(e_transposed);

    return PyInt_FromLong(1);

}



/* ==== methods table ====================== */
static PyMethodDef c_nipals_methods[] = {
	{"nipals", nipals, METH_VARARGS},
	{"nipals2", nipals2, METH_VARARGS},
	{NULL, NULL}
	};


/* ==== Initialize ====================== */
PyMODINIT_FUNC initc_nipals()  {
	Py_InitModule("c_nipals", c_nipals_methods);
	import_array();  // for NumPy
}


/*
$ gcc -c nipals.c -I/cygdrive/c/cygwin/usr/include/python2.5
$ gcc -shared -o c_nipals.dll nipals.o -L/cygdrive/c/cygwin/lib/python2.5/config -lpython2.5
*/
