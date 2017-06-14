#include <gmsg/gmsgpack.h>

void gmsg_init(gmsg_t* gmsg, char* buffer, uint16_t length) {
	gmsg->buf = buffer;
	gmsg->ptr = buffer;
	gmsg->len = length;
	gmsg->crc = 0xFF;
}

int gmsg_add_end(gmsg_t* gmsg) {
	char* end = gmsg->buf + gmsg->len;
	
	if (end - gmsg->ptr < 1) return -1;
	
	*gmsg->ptr++ = GMSG_FRAMEEND;
	return 0;
}

int gmsg_add_crc(gmsg_t* gmsg) {
	char* end = gmsg->buf + gmsg->len;
	
	if (end - gmsg->ptr < 1) return -1;
	
	*gmsg->ptr++ = gmsg->crc;
	return 0;
}

int gmsg_start(gmsg_t* gmsg) {
	gmsg_add_end(gmsg);
}

int gmsg_finish(gmsg_t* gmsg) {
	gmsg_add_crc(gmsg);
	gmsg_add_end(gmsg);
}

static inline void __gmsg_take_crc(gmsg_t* gmsg, char c) {
	gmsg->crc ^= c;
	for (int i = 0; i < 8; i++)
		gmsg->crc = gmsg->crc & 0x80 ? (gmsg->crc << 1) ^ 0x31 : gmsg->crc << 1;
	
}

static inline void __gmsg_add_symb(gmsg_t* gmsg, char c) {
	*gmsg->ptr++ = c; 
	__gmsg_take_crc(gmsg, c);
}

int gmsg_add_part(gmsg_t* gmsg, const void* part, uint16_t length) {
	char* end = gmsg->buf + gmsg->len;
	char* r = (char*)part;

	while(length-- && gmsg->ptr != end) {
		switch (*r) {
			case (char)GMSG_FRAMEEND: 
				__gmsg_add_symb(gmsg, GMSG_FRAMEESC); 
				__gmsg_add_symb(gmsg, GMSG_TEND); 
				break;

			case (char)GMSG_FRAMEESC: 
				__gmsg_add_symb(gmsg, GMSG_FRAMEESC); 
				__gmsg_add_symb(gmsg, GMSG_TESC); 
				break;

			default:
				__gmsg_add_symb(gmsg, *r);
				break;
		}
		r++;
	}
	if (gmsg->ptr == end && length != 0) return -1;
	return 0;
}