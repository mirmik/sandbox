#include "service.h"
#include <gxx/datastruct/array.h>

static g0id_t service_id_counter = 0;
static g0id_t message_id_counter = 0;

#ifndef GENOS_SERVICE_TABLE_SIZE
#define G0_SERVICE_TABLE_SIZE 20
#endif

#ifndef GENOS_MESSAGE_TABLE_SIZE
#define G0_MESSAGE_TABLE_SIZE 20
#endif

struct hlist_head service_htable [G0_SERVICE_TABLE_SIZE];
struct hlist_head message_htable [G0_MESSAGE_TABLE_SIZE];

g0id_t g0_getid_service() { 
	return ++service_id_counter; 
}

g0id_t g0_getid_message() { 
	return ++message_id_counter; 
}

uint16_t g0_registry_service(struct g0_service* srv) {
	srv->id = g0_getid_service();
	hlist_add_next(&srv->hlnk, &service_htable[srv->id % G0_SERVICE_TABLE_SIZE].first);
}

struct g0_service* g0_find_service(uint16_t id) {
	size_t cell = id % G0_SERVICE_TABLE_SIZE;

	struct hlist_node* it;
	struct g0_service* entry;
	hlist_for_each(it, service_htable) {
		entry = hlist_entry(it, struct g0_service, hlnk);
		if (id == entry->id) return entry;
	}
	return NULL;
}

void g0_init() {
	struct hlist_head* it;
	struct hlist_head* eit;
	for(it = service_htable, eit = service_htable + G0_SERVICE_TABLE_SIZE; it != eit; ++it) hlist_head_init(it);
	for(it = message_htable, eit = message_htable + G0_MESSAGE_TABLE_SIZE; it != eit; ++it) hlist_head_init(it);
}