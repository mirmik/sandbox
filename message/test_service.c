#include "test_service.h"
#include <stdio.h>

void service_panic(struct g0_service* srvs, struct g0_message* msg) {
	debug_print("service_panic\n");
	abort();
}

void test_service_on_input(struct g0_service* srvs, struct g0_message* msg) {
	struct test_service* tsrvs = (struct test_service*) srvs;
	printf("%s input message: \n\tqid: %d\n\tsid: %d\n\trid: %d\n\ttxt: %*s\n\trepl: %d\n", tsrvs->name, msg->qid, msg->sid, msg->rid, (int)msg->size, (char*)msg->data, (int)msg->repled);
}

void test_service_on_reply(struct g0_service* srvs, struct g0_message* msg) {
	struct test_service* tsrvs = (struct test_service*) srvs;
	printf("%s replied message: \n\tqid: %d\n\tsid: %d\n\trid: %d\n\ttxt: %*s\n\trepl: %d\n", tsrvs->name, msg->qid, msg->sid, msg->rid, (int)msg->size, (char*)msg->data, (int)msg->repled);
	g0_utilize_message(msg);
}

void echo_service_on_input(struct g0_service* srvs, struct g0_message* msg) {
	struct echo_service* tsrvs = (struct echo_service*) srvs;
	printf("%s input message: \n\tqid: %d\n\tsid: %d\n\trid: %d\n\ttxt: %*s\n\trepl: %d\n", tsrvs->name, msg->qid, msg->sid, msg->rid, (int)msg->size, (char*)msg->data, (int)msg->repled);
	g0_transport_reply(msg);	
}

const struct g0_service_operations test_service_ops = {
	.on_input = test_service_on_input,
	.on_reply = test_service_on_reply
};

const struct g0_service_operations echo_service_ops = {
	.on_input = echo_service_on_input,
	.on_reply = service_panic
};

g0id_t test_service_init(struct test_service* tserv, const char* name) {
	tserv->serv.service_ops = &test_service_ops;
	tserv->name = name;
	return g0_init_service(&tserv->serv);
}

g0id_t echo_service_init(struct echo_service* eserv, const char* name) {
	eserv->serv.service_ops = &echo_service_ops;
	eserv->name = name;
	return g0_init_service(&eserv->serv);
}
