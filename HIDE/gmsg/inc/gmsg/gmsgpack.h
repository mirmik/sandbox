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

struct unpack_strm_gmsg_s {
	//cnt
	char* buf;
	uint16_t len;

	//runt
	char* ptr;
	uint8_t esc;
	uint8_t crc;
};
typedef struct unpack_strm_gmsg_s unpack_gmsg_t;

__BEGIN_DECLS

void gmsg_init(gmsg_t* gmsg, char* buf, uint16_t len);
void gmsg_reinit(gmsg_t* gmsg);
int gmsg_add_end(gmsg_t* gmsg);
int gmsg_add_crc(gmsg_t* gmsg);

int gmsg_start(gmsg_t* gmsg);
int gmsg_finish(gmsg_t* gmsg);
int gmsg_add_part(gmsg_t* gmsg, const void* part, uint16_t length);

void gmsg_unpack_init(unpack_gmsg_t* gmsg, char* buf, uint16_t len);
void gmsg_unpack_reinit(unpack_gmsg_t* gmsg);
int gmsg_unpack_new_char(unpack_gmsg_t* gmsg, char c);
uint8_t gmsg_unpack_subcrc(unpack_gmsg_t* gmsg);

__END_DECLS

#endif