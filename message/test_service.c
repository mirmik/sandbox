#include "test_service.h"

void test_service_on_input(struct g0_message* msg) {
	debug_print("all good\n");
}

const struct g0_service_operations test_service_ops = {
	.on_input = test_service_on_input
};

void test_service_init(struct test_service* tserv) {
	tserv->serv.service_ops = &test_service_ops;
	g0_registry_service(&tserv->serv);
}
