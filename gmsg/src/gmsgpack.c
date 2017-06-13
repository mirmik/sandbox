#include <gmsg/gmsgpack.h>

void gmsg_init(gmsg_t* gmsg, char* buffer, uint16_t length) {
	gmsg->buf = buffer;
	gmsg->ptr = buffer;
	gmsg->len = length;
	gmsg->crc = 0;
}

int gmsg_add_start(gmsg_t* gmsg) {
	char* end = gmsg->buf + gmsg->len;
	if (end - gmsg->ptr < 2) return -1;
	*gmsg->ptr++ = GMSG_STARTBYTE0;
	*gmsg->ptr++ = GMSG_STARTBYTE1;
	return 0;
}