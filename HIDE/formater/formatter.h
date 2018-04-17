#ifndef GXX_FORMATER_H
#define GXX_FORMATER_H

#include <iostream>
#include <vector>

namespace gxx {
	class formatter;

	class basic_formatter_node {
	protected:
		void* ptr;
		virtual void doit(formatter* fmt) = 0;
	};

	template<typename T>
	class formatter_node : basic_formatter_node {
		formatter_node(T& obj) : basic_formatter_node(&obj) {}
		void doit(formatter* fmt, const char* opts, size_t osz) {

		}
	};

	class formatter {
		std::string pattern;
		std::vector<basic_formatter_node> args;
		
		template<typename T> formatter& operator%(T& obj) {
			args.emplace_back<formatter_node<T>>(obj);
		}
	};
}

#endif