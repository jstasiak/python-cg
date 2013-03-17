cimport _cg
cimport _cgGL
cimport numpy
import numpy

# Contexts

cdef class CGcontext:
	cdef _cg.CGcontext handle

cdef _create_context(_cg.CGcontext handle):
	if not handle:
		return None

	obj = CGcontext()
	obj.handle = handle
	return obj

def cgCreateContext():
	return _create_context(_cg.cgCreateContext())

def cgDestroyContext(CGcontext context):
	_cg.cgDestroyContext(context.handle)

def cgIsContext(CGcontext context):
	return _cg.cgIsContext(context.handle)


# Errors

cdef u(const char* s):
	if s == NULL:
		return None
	else:
		return (<bytes>s).decode('utf-8')

def cgGetLastListing(CGcontext context):
	cdef const char* listing = _cg.cgGetLastListing(context.handle)
	return u(listing)

def cgGetError():
	return _cg.cgGetError()

def cgGetErrorString(_cg.CGerror error):
	cdef const char* description = _cg.cgGetErrorString(error)
	return u(description)

# OpenGL-specific

def cgGLRegisterStates(CGcontext context):
	_cgGL.cgGLRegisterStates(context.handle)

def cgGLSetTextureParameter(CGparameter parameter, unsigned int texture):
	_cgGL.cgGLSetTextureParameter(parameter.handle, texture)

def cgGLSetManageTextureParameters(CGcontext context, int flag):
	_cgGL.cgGLSetManageTextureParameters(context.handle, flag)

def cgGLGetManageTextureParameters(CGcontext context):
	return bool(_cgGL.cgGLGetManageTextureParameters(context.handle))


# Effects

cdef class CGeffect:
	cdef _cg.CGeffect handle 

cdef _create_effect(_cg.CGeffect handle):
	if not handle:
		return None

	effect = CGeffect()
	effect.handle = handle
	return effect

def cgCreateEffectFromFile(CGcontext context, unicode filename):
	cdef bytes filename_bytes = filename.encode('utf-8')
	return _create_effect(_cg.cgCreateEffectFromFile(context.handle, filename_bytes, NULL))

def cgCreateEffect(CGcontext context, unicode source):
	cdef bytes source_bytes = source.encode('utf-8')
	return _create_effect(_cg.cgCreateEffect(context.handle, source_bytes, NULL))

def cgDestroyEffect(CGeffect effect):
	_cg.cgDestroyEffect(effect.handle)

# Effect techniques

cdef class CGtechnique:
	cdef _cg.CGtechnique handle

cdef _create_technique(_cg.CGtechnique handle):
	if not handle:
		return None

	technique = CGtechnique()
	technique.handle = handle
	return technique

def cgGetFirstTechnique(CGeffect effect):
	return _create_technique(_cg.cgGetFirstTechnique(effect.handle))

def cgGetNextTechnique(CGtechnique technique):
	return _create_technique(_cg.cgGetNextTechnique(technique.handle))

def cgValidateTechnique(CGtechnique technique):
	return bool(_cg.cgValidateTechnique(technique.handle))

def cgGetTechniqueName(CGtechnique technique):
	return u(_cg.cgGetTechniqueName(technique.handle))


# Effect passes

cdef class CGpass:
	cdef _cg.CGpass handle

cdef _create_pass(_cg.CGpass handle):
	if not handle:
		return None

	pass_ = CGpass()
	pass_.handle = handle
	return pass_

def cgGetFirstPass(CGtechnique technique):
	return _create_pass(_cg.cgGetFirstPass(technique.handle))

def cgGetNextPass(CGpass pass_):
	return _create_pass(_cg.cgGetNextPass(pass_.handle))

def cgSetPassState(CGpass pass_):
	_cg.cgSetPassState(pass_.handle)

def cgResetPassState(CGpass pass_):
	_cg.cgResetPassState(pass_.handle)



def cgGetTypeString(_cg.CGtype type):
	return u(_cg.cgGetTypeString(type))


# Effect/program parameters
cdef class CGparameter:
	cdef _cg.CGparameter handle

cdef _create_parameter(_cg.CGparameter handle):
	if not handle:
		return None

	parameter = CGparameter()
	parameter.handle = handle
	return parameter

def cgGetFirstEffectParameter(CGeffect effect):
	return _create_parameter(_cg.cgGetFirstEffectParameter(effect.handle))

def cgGetNextParameter(CGparameter parameter):
	return _create_parameter(_cg.cgGetNextParameter(parameter.handle))

def cgGetParameterName(CGparameter parameter):
	return u(_cg.cgGetParameterName(parameter.handle))

def cgGetParameterBaseType(CGparameter parameter):
	return _cg.cgGetParameterBaseType(parameter.handle)

def cgGetParameterType(CGparameter parameter):
	return _cg.cgGetParameterType(parameter.handle)

def cgGetParameterRows(CGparameter parameter):
	return _cg.cgGetParameterRows(parameter.handle)

def cgGetParameterColumns(CGparameter parameter):
	return _cg.cgGetParameterColumns(parameter.handle)

def cgGetParameterSemantic(CGparameter parameter):
	return u(_cg.cgGetParameterSemantic(parameter.handle))

def cgSetParameterValueic(CGparameter parameter, int nelements,
		numpy.ndarray[numpy.int32_t, ndim=1] v):
	_cg.cgSetParameterValueic(parameter.handle, nelements, <int*>v.data)

def cgSetParameterValuefc(CGparameter parameter, int nelements,
		numpy.ndarray[numpy.float32_t, ndim=1] v):
	_cg.cgSetParameterValuefc(parameter.handle, nelements, <float*>v.data)

def cgSetParameterValuedc(CGparameter parameter, int nelements,
		numpy.ndarray[numpy.float64_t, ndim=1] v):
	_cg.cgSetParameterValuedc(parameter.handle, nelements, <double*>v.data)


def cgSetParameterValueir(CGparameter parameter, int nelements,
		numpy.ndarray[numpy.int32_t, ndim=1] v):
	_cg.cgSetParameterValueir(parameter.handle, nelements, <int*>v.data)

def cgSetParameterValuefr(CGparameter parameter, int nelements,
		numpy.ndarray[numpy.float32_t, ndim=1] v):
	_cg.cgSetParameterValuefr(parameter.handle, nelements, <float*>v.data)

def cgSetParameterValuedr(CGparameter parameter, int nelements,
		numpy.ndarray[numpy.float64_t, ndim=1] v):
	_cg.cgSetParameterValuedr(parameter.handle, nelements, <double*>v.data)



# Samplers

def cgSetSamplerState(CGparameter parameter):
	_cg.cgSetSamplerState(parameter.handle)
