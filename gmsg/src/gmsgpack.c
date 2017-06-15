#include <gmsg/gmsgpack.h>

void gmsg_init(gmsg_t* gmsg, char* buffer, uint16_t length) {
	gmsg->buf = buffer;
	gmsg->ptr = buffer;
	gmsg->len = length;
	gmsg->crc = 0xFF;
}

void gmsg_reinit(gmsg_t* gmsg) {
	gmsg->ptr = gmsg->buf;
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
	gmsg->crc = 0xFF;
	gmsg_add_end(gmsg);
}

static inline void __gmsg_take_crc(uint8_t* crc, char c) {
	*crc ^= c;
	for (int i = 0; i < 8; i++)
		*crc = *crc & 0x80 ? (*crc << 1) ^ 0x31 : *crc << 1;
	
}

static inline void __gmsg_add_symb(gmsg_t* gmsg, char c) {
	*gmsg->ptr++ = c; 
	__gmsg_take_crc(&gmsg->crc, c);
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

void gmsg_unpack_init(unpack_gmsg_t* gmsg, char* buf, uint16_t len) {
	gmsg->buf = buf;
	gmsg->ptr = buf;
	gmsg->len = len;
	gmsg->esc = 0;
	gmsg->crc = 0xFF;
}

void gmsg_unpack_reinit(unpack_gmsg_t* gmsg) {
	gmsg->ptr = gmsg->buf;
	gmsg->crc = 0xFF;
}

uint8_t gmsg_unpack_subcrc(unpack_gmsg_t* gmsg) {
	char c = *--gmsg->ptr;
	return c;
}

int gmsg_unpack_new_char(unpack_gmsg_t* gmsg, char c) {
	__label__ __crcchar__;

	if (gmsg->len - (gmsg->ptr - gmsg->buf) == 0) return -2;

	if (gmsg->esc) {
		gmsg->esc = 0;
		switch(c) {
			case (char)GMSG_TEND:
				*gmsg->ptr++ = (char)GMSG_FRAMEEND;
				goto __crcchar__;
		
			case (char)GMSG_TESC:
				*gmsg->ptr++ = (char)GMSG_FRAMEESC;
				goto __crcchar__;

			default: 
				return -1;
		}
	}

	switch(c) {
		case (char)GMSG_FRAMEEND:
			if (gmsg->ptr - gmsg->buf <= 2) return -1;
			return 2;

		case (char)GMSG_FRAMEESC:
			gmsg->esc = 1;
			goto __crcchar__;

		default:
			*gmsg->ptr++ = c;
			goto __crcchar__;
	}

	__crcchar__:
	__gmsg_take_crc(&gmsg->crc, c);
	putchar(c);
	printf("%x", gmsg->crc);

	return 0;
}