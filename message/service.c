#include "service.h"
#include <gxx/datastruct/array.h>

//#include <stdio.h>
//#include <gxx/debug/dprint.h>

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

g0id_t g0_init_service(struct g0_service* srv) {
	srv->id = g0_getid_service();
	hlist_add_next(&srv->hlnk, &service_htable[srv->id % G0_SERVICE_TABLE_SIZE].first);
	dlist_init(&srv->imsgs);
	return srv->id;
}

struct g0_service* g0_find_service(g0id_t id) {
	struct hlist_node* it;
	struct g0_service* entry;
	size_t cell = id % G0_SERVICE_TABLE_SIZE;
	hlist_for_each(it, &service_htable[cell]) {
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

g0id_t g0_init_message(struct g0_message* msg) {
	msg->stsbyte = 0;
	msg->qid = g0_getid_message();
	hlist_add_next(&msg->hlnk, &message_htable[msg->qid % G0_MESSAGE_TABLE_SIZE].first);
	return msg->qid;
}

uint8_t g0_transport_send(struct g0_message* msg) {
	struct g0_service* srvs = g0_find_service(msg->rid);
	dlist_add_prev(&msg->qlnk, &srvs->imsgs);
	srvs->service_ops->on_input(srvs, msg);
	return 0;
}