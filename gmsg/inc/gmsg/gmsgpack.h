#ifndef GMSGPACK_H
#define GMSGPACK_H

#include <sys/cdefs.h>
#include <inttypes.h>

#define GMSG_STARTBYTE0 0xAB
#define GMSG_STARTBYTE1 0x3C

struct gmsg_s {
	//cnt
	char* buf;
	uint16_t len;

	//runt
	char* ptr;
	uint16_t crc;
};
typedef struct gmsg_s gmsg_t;

__BEGIN_DECLS

void gmsg_init(gmsg_t* gmsg, char* buf, uint16_t len);
int gmsg_add_start(gmsg_t* gmsg);



__END_DECLS

#endif