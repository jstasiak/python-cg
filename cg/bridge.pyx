cimport _cg

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

def cgGetLastListing(CGcontext context):
	cdef const char* listing = _cg.cgGetLastListing(context.handle)
	if not listing:
		return None
	else:
		return (<bytes>listing).decode('utf-8')

# OpenGL-specific

def cgGLRegisterStates(CGcontext context):
	_cg.cgGLRegisterStates(context.handle)


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
	filename_bytes = filename.encode('utf-8')
	return _create_effect(_cg.cgCreateEffectFromFile(context.handle, filename_bytes, NULL))


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
	return _cg.cgValidateTechnique(technique.handle)


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