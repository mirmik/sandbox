#ifndef GENOS_SERVICE_TEST_SERVICE_H
#define GENOS_SERVICE_TEST_SERVICE_H

#include "service.h"
#include <gxx/debug/dprint.h>

struct test_service {
	struct g0_service serv;
	const char* name;
};

__BEGIN_DECLS

g0id_t test_service_init(struct test_service* tserv, const char* name);

__END_DECLS

#endif