/*#include <stdlib.h>
#include <stdint.h>
#include <gxx/datastruct/dlist_head.h>
#include <gxx/datastruct/hlist_head.h>
#include <gxx/datastruct/array.h>
#include <gxx/debug/dprint.h>*/

#include "id_table.h"
#include "service.h"
#include "test_service.h"

#include <gxx/debug/dprint.h>




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
	g0_init();

	struct test_service srvs;
	test_service_init(&srvs);
/*
	int a = 33;
	double b = 33.6;

	struct iovec iov[] = {
		{&a, sizeof(a)},
		{&b, sizeof(b)},
		{NULL, 0}
	};*/

	//genos_sendv(iov, &srvs.serv, NULL, 0);*/
};