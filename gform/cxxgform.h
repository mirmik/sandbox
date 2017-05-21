#ifndef CXXGFORM_H
#define CXXGFORM_H

#include <exception>
#include <string>
#include <vector>
#include <map>

namespace __detail {
	template<typename type>
	void destructor(type* ptr) {
		ptr->~type();
	}
}

namespace gform {

	class exception : public std::exception {
		const char* err;

		virtual const char* what() const throw() {
			return err;
		}

	public:
		exception(const char* err) : err(err) {};
	};

	enum class NodeType : uint8_t {
		Int8 = 0,
		Int16 = 1,
		Int32 = 2,
		Int64 = 3,
		UInt8 = 4,
		UInt16 = 5,
		UInt32 = 6,
		UInt64 = 7,
		Float = 8,
		Double = 9,
		
		String8bit = 10,
		
		ArrayTyped = 11,
		Array = 12,
	
		DictionaryTyped = 13,
		Dictionary = 14,
	};
	
	class Node {
		NodeType m_type;
	
		union {
			int64_t		m_i64;
			uint64_t	m_u64;
			float m_flt;
	
			std::string m_str;
			std::vector<Node> m_vec;
			std::map<std::string, Node> m_dict;
	
		};
	public:
		Node(NodeType type) {
			init(type);
		}
	
		Node(int8_t i) { m_type = NodeType::Int8; m_i64 = i; }
		Node(int16_t i) { m_type = NodeType::Int16; m_i64 = i; }
		Node(int32_t i) { m_type = NodeType::Int32; m_i64 = i; }
		Node(int64_t i) { m_type = NodeType::Int64; m_i64 = i; }
		Node(uint8_t i) { m_type = NodeType::UInt8; m_u64 = i; }
		Node(uint16_t i) { m_type = NodeType::UInt16; m_u64 = i; }
		Node(uint32_t i) { m_type = NodeType::UInt32; m_u64 = i; }
		Node(uint64_t i) { m_type = NodeType::UInt64; m_u64 = i; }
		Node(std::string str) { m_type = NodeType::String8bit; new (&m_str) std::string(str); }

		~Node() {
			invalidate();
		}
	
		int64_t as_int() {
			if (m_type <= NodeType::Int64 && m_type >= NodeType::Int8) {
				return m_i64;
			}

			if (m_type <= NodeType::UInt64 && m_type >= NodeType::UInt8) {
				return (int64_t) m_u64;
			}

			throw exception("Can't convert to int");
		}

		uint64_t as_uint() {
			if (m_type <= NodeType::Int64 && m_type >= NodeType::Int8) {
				return (uint64_t) m_i64;
			}

			if (m_type <= NodeType::UInt64 && m_type >= NodeType::UInt8) {
				return m_u64;
			}

			throw exception("Can't convert to int");
		}

	private:
		void init(NodeType type){
			m_type = type;
			switch (type) {
				case NodeType::Int8: 
				case NodeType::Int16:
				case NodeType::Int32:
				case NodeType::Int64:
				case NodeType::UInt8:
				case NodeType::UInt16:
				case NodeType::UInt32:
				case NodeType::UInt64: 
				case NodeType::Float: 
				case NodeType::Double: 
					break;
				
				case NodeType::Array: 
				case NodeType::ArrayTyped: 
					new (&m_vec) std::vector<Node>();
					break;
				
				case NodeType::Dictionary: 
				case NodeType::DictionaryTyped: 
					new (&m_dict) std::map<std::string, Node>();
					break;
				
				case NodeType::String8bit: 
					new (&m_str) std::string();
					break;
				
				default: 
					throw exception("NotImplemented"); 
					break;
			}
		}

		void invalidate(){
			switch (m_type) {
				case NodeType::Int8: 
				case NodeType::Int16:
				case NodeType::Int32:
				case NodeType::Int64:
				case NodeType::UInt8:
				case NodeType::UInt16:
				case NodeType::UInt32:
				case NodeType::UInt64: 
				case NodeType::Float: 
				case NodeType::Double: 
					break;
				
				case NodeType::Array: 
				case NodeType::ArrayTyped: 
					__detail::destructor(&m_vec);
					break;
				
				case NodeType::Dictionary: 
				case NodeType::DictionaryTyped: 
					__detail::destructor(&m_dict);
					break;
				
				case NodeType::String8bit: 
					__detail::destructor(&m_str);
					break;
				
				default: 
					throw exception("NotImplemented"); 
					break;
			}
		}
	};	
}

#endif