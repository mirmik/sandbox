#include <stdlib.h>
#include <stdint.h>
#include <gxx/datastruct/dlist_head.h>
#include <gxx/datastruct/hlist_head.h>
#include <gxx/datastruct/array.h>
#include <gxx/debug/dprint.h>

#include "id_table.h"

size_t service_id_counter = 0;
size_t message_id_counter = 0;
struct id_table service_table; 
struct id_table message_table;

size_t generate_service_id() { return ++service_id_counter; }
size_t generate_message_id() { return ++message_id_counter; }

//void id_table_init(struct id_table* tbl, );

struct service;

typedef struct {
	struct dlist_head lnk;

	size_t sid; 
	size_t rid;
	size_t qid;

	void* data;
	size_t size;

	struct {
		uint8_t sended : 1;
		uint8_t recved : 1;
		uint8_t repled : 1;
		uint8_t noreply : 1;
	};
} msg_t;

struct service_operations {
	void (*on_input)(msg_t*);
};

struct service {
	id_t id;
	struct hlist_node hnode;
	const struct service_operations* service_ops;
};

id_t genos_registry_service(struct service* srv) {
	debug_print("genos_registry_service\n");
	srv->id = generate_service_id();
	hlist_add_next(&srv->hnode, &service_table.harray[srv->id % service_table.size].first);
}


struct iovec {
	void* data;
	size_t size;
};

void test_service_on_input(msg_t* msg) {
	debug_print("all good\n");
}

const struct service_operations test_service_ops = {
	.on_input = test_service_on_input
};

struct test_service {
	struct service serv;
};

void test_service_init(struct test_service* tserv) {
	tserv->serv.service_ops = &test_service_ops;
	genos_registry_service(&tserv->serv);
}

/*
void genos_message_transport(msg_t* msg) {

}
/*
void 

#ifdef GENOS_MESSAGE_USE_SERVICE_ID
void genos_message_sendv(struct iovec* iov, size_t rid, size_t sid, uint8_t needreply) {

}
#else
void genos_sendv(struct iovec* iov, struct service * rptr, struct service * sptr, uint8_t needreply) {
	debug_print("genos_message_sendv\n");
	msg_t* msg = genos_msg_createv(iov, rptr, sptr, needreply);
	genos_message_transport(msg);
}
#endif
*/


int main() {
	id_table_init(&service_table, 20);
	id_table_init(&message_table, 20);


	struct test_service srvs;
	test_service_init(&srvs);

	int a = 33;
	double b = 33.6;

	struct iovec iov[] = {
		{&a, sizeof(a)},
		{&b, sizeof(b)},
		{NULL, 0}
	};

	//genos_sendv(iov, &srvs.serv, NULL, 0);*/
};