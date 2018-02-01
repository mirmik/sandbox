#ifndef G0_SERVICE_H
#define G0_SERVICE_H

#include <gxx/datastruct/dlist_head.h>
#include "id_table.h"

typedef uint16_t g0id_t;

struct g0_message {
	struct dlist_head lnk;

	g0id_t sid; 
	g0id_t rid;
	g0id_t qid;

	void* data;
	size_t size;

	struct {
		uint8_t sended : 1;
		uint8_t recved : 1;
		uint8_t repled : 1;
		uint8_t noreply : 1;
	};
};

struct g0_service_operations {
	void (*on_input)(struct g0_message*);
};

struct g0_service {
	g0id_t id;
	struct hlist_node hlnk;
	const struct g0_service_operations* service_ops;
};

__BEGIN_DECLS

g0id_t g0_getid_service();
g0id_t g0_getid_message();

g0id_t g0_registry_service(struct g0_service* srv);
void g0_init();

__END_DECLS

#endif