#ifndef GMSGPACK_H
#define GMSGPACK_H

#include <sys/cdefs.h>
#include <inttypes.h>

static const char GMSG_FRAMEEND = 0xC0;
static const char GMSG_FRAMEESC = 0xDB;
static const char GMSG_TEND = 0xDC;
static const char GMSG_TESC = 0xDD;

struct gmsg_s {
	//cnt
	char* buf;
	uint16_t len;

	//runt
	char* ptr;
	uint8_t crc;
};
typedef struct gmsg_s gmsg_t;

__BEGIN_DECLS

void gmsg_init(gmsg_t* gmsg, char* buf, uint16_t len);
int gmsg_add_end(gmsg_t* gmsg);
int gmsg_add_crc(gmsg_t* gmsg);

int gmsg_start(gmsg_t* gmsg);
int gmsg_finish(gmsg_t* gmsg);
int gmsg_add_part(gmsg_t* gmsg, const void* part, uint16_t length);

__END_DECLS

#endif