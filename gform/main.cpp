#include <iostream>
#include <cxxgform.h>

int main() {
	std::cout << "HelloWorld" << std::endl;

	gform::Node root(gform::NodeType::Dictionary);
	root.as_int();
}