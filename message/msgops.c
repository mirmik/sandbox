#include "msgops.h"

#include <string.h>
#include <stdio.h>
#include <gxx/debug/dprint.h>


struct g0_message* g0_alloc_message() {
	return (struct g0_message*) malloc(sizeof(struct g0_message));
} 

void g0_dealloc_message(struct g0_message* msg) {
	free(msg);
}

void g0_utilize_message(struct g0_message* msg) {
	free(msg->data);
	free(msg);
}

/*static inline void g0_info(struct g0_message*, g0id_t receiver, g0id_t sender, void* data, size_t size) {
	msg->stsbyte = 0;
	msg->rid = receiver;
	msg->sid = sender;
	msg->data = data;
	msg->size = size;
}*/

g0id_t g0_send(g0id_t sender, g0id_t receiver, const void* data, size_t size) {
	struct g0_message* msg = g0_alloc_message();
	void* msgdata = malloc(size);
	memcpy(msgdata, data, size);

	g0id_t msgid = g0_init_message(msg);
	msg->sid = sender;
	msg->rid = receiver;
	msg->data = msgdata;
	msg->size = size;

	uint8_t sts = g0_transport_send(msg);
	return msgid;
}