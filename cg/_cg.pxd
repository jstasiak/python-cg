from libcpp cimport bool

cdef extern from "Cg/cgGL.h" nogil:
	ctypedef void* CGcontext
	ctypedef void* CGeffect
	ctypedef void* CGtechnique
	ctypedef void* CGpass

	CGcontext cgCreateContext()
	void cgDestroyContext(CGcontext context)
	bool cgIsContext(CGcontext context)

	void cgGLRegisterStates(CGcontext context)

	const char* cgGetLastListing(CGcontext context)

	CGeffect cgCreateEffectFromFile(CGcontext context, const char* filename, const char** args)

	CGtechnique cgGetFirstTechnique(CGeffect effect)
	CGtechnique cgGetNextTechnique(CGtechnique technique)
	bool cgValidateTechnique(CGtechnique technique)

	CGpass cgGetFirstPass(CGtechnique technique)
	CGpass cgGetNextPass(CGpass pass_)
	void cgSetPassState(CGpass pass_)
	void cgResetPassState(CGpass pass_)
