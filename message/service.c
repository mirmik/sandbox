#include "service.h"
#include <gxx/datastruct/array.h>

static g0id_t service_id_counter = 0;
static g0id_t message_id_counter = 0;

#ifndef GENOS_SERVICE_TABLE_SIZE
#define G0_SERVICE_TABLE_SIZE 20
#endif

struct hlist_head service_htable [G0_SERVICE_TABLE_SIZE];

g0id_t g0_getid_service() { 
	return ++service_id_counter; 
}

g0id_t g0_getid_message() { 
	return ++message_id_counter; 
}

g0id_t g0_init_service(struct g0_service* srv) {
	srv->id = g0_getid_service();
	hlist_add_next(&srv->hlnk, &service_htable[srv->id % G0_SERVICE_TABLE_SIZE].first);
	//dlist_init(&srv->imsgs);
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
	for(struct hlist_head *it = service_htable, *eit = service_htable + G0_SERVICE_TABLE_SIZE; it != eit; ++it) hlist_head_init(it);
}

g0id_t g0_init_message(struct g0_message* msg) {
	msg->stsbyte = 0;
	msg->qid = g0_getid_message();
	return msg->qid;
}

uint8_t g0_transport_send(struct g0_message* msg) {
	struct g0_service* srvs = g0_find_service(msg->rid);
	if (srvs == NULL) return -1;
	//dlist_add_prev(&msg->qlnk, &srvs->imsgs);
	srvs->service_ops->on_input(srvs, msg);
	return 0;
}

uint8_t g0_transport_reply(struct g0_message* msg) {
	if (msg->noreply) {
		g0_utilize_message(msg);
		return 0;
	}
	struct g0_service* srvs = g0_find_service(msg->sid);
	if (srvs == NULL) return -1;
	msg->repled = 1;
	srvs->service_ops->on_reply(srvs, msg);
	return 0;
}