#include <iostream>
#include <vector>

class A {
public:
	std::vector<const char*> vec;

	~A() {	
		std::cout << "~A" << std::endl;
		
		for(auto& str : vec) {
			std::cout << str;
		}
	}

	A& operator <<(const char* str) {
		std::cout << "operator" << std::endl;
		vec.push_back(str);
		return *this;
	}
};

A a() {
	return A();
}

int main() {
	std::cout << "begin" << std::endl;
	a() << "lalala" << "*destructor will invoked after this string*" << "yohanga";
	std::cout << std::endl << "end" << std::endl;	
}