#ifndef GXX_ARGS_INVOKER_H
#define GXX_ARGS_INVOKER_H

#include <assert.h>
#include <tuple>

template<typename Func> struct ptrsignature;

template<typename Ret, typename Arg, typename ... OtherArgs>
struct ptrsignature<Ret(Arg, OtherArgs...)> {
	using rettype = Ret;
	using type = Ret (*) (Arg, OtherArgs ...);
	//using vtype = Ret (*) (void*, OtherArgs ...);
};

template<typename Arg, typename FuncGeneric>
class argument {
	using NoRefType = typename std::remove_reference<Arg>::type;
	using PtrType = typename std::remove_reference<Arg>::type*;
	using FuncType = typename ptrsignature<decltype(FuncGeneric::template func<NoRefType>)>::type;
	//using RetType = typename ptrsignature<decltype(FuncGeneric::template func<void>)>::rettype;
	
	PtrType m_ptr;
	FuncType fptr = &FuncGeneric::template func<NoRefType>;	

public:
	template<typename ... Args> RetType invoke(Args ... args) {
		return fptr(m_ptr, args ...);
	}

public:
	argument(PtrType ptr) : m_ptr(ptr) { m_ptr = ptr; }
};

template<typename Head, typename ... Tail>
class tuple : public tuple<Tail ...> {
	using Parent = tuple<Tail ...>;
	Head head;
public:
	template<typename UH, typename ... UT>
	tuple(UH&& head, UT&& ... tail) : head(head), Parent(std::forward<UT>(tail) ...) {}
};

template<typename Head>
class tuple<Head> {
	Head head;	
public:
	template<typename UH>
	tuple(UH&& head) : head(head) {}
};


template<typename FuncGeneric, typename ... Args>
class arglist {
public:
	union {
		argument<void,FuncGeneric> args[sizeof...(Args)];
		tuple<argument<Args, FuncGeneric> ...> builder;
		//std::tuple<argument<Args, FuncGeneric> ...> builder;
	};

	argument<void,FuncGeneric>& operator[](int i) {
		int index = sizeof...(Args) - 1 - i;
		assert(index >= 0);

		return args[index];
	}
public:
	template<typename ... UArgs>
	arglist(UArgs&& ... args) : builder((&args) ...) {}
};


#endif