#include <iostream>
#include <argsinvoker.h>
#include <utility>

class A {

};

struct generic {
public:
	template<typename T> static void func(T* ptr, int i);
};

template<> 
void generic::func<int>(int* ptr, int i) {
	std::cout << "dasfdasf" << *ptr << i << std::endl;
}

template<> 
void generic::func<A>(A* ptr, int i) {
	std::cout << "A" << i << std::endl;
}

//using ft = decltype(generic::func<int>);

template<typename ... Args>
void format(const char* fmt, Args&& ... args) {
	arglist<generic, Args ...> argslist(std::forward<Args>(args) ...);

	std::cout << "fmt" << fmt << std::endl;

	argslist[2].invoke(34);
	argslist[1].invoke(1);
	argslist[0].invoke(1);
}

int main() {
	std::cout << "HelloWorld" << std::endl;

	A a;

	format("{0}, {1}", 30, 50, a);
}