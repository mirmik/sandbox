#include "test_service.h"
#include <stdio.h>

void test_service_on_input(struct g0_service* srvs, struct g0_message* msg) {
	struct test_service* tsrvs = (struct test_service*) srvs;
	printf("%s input message: \n\tqid: %d\n\tsid: %d\n\ttxt: %*s\n", tsrvs->name, msg->qid, msg->sid, (int)msg->size, (char*)msg->data);
}

const struct g0_service_operations test_service_ops = {
	.on_input = test_service_on_input
};

g0id_t test_service_init(struct test_service* tserv, const char* name) {
	tserv->serv.service_ops = &test_service_ops;
	tserv->name = name;
	return g0_init_service(&tserv->serv);
}
