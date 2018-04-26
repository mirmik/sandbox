#ifndef GENOS_VCHANNEL_H
#define GENOS_VCHANNEL_H

struct vchannel_service : public service {
	dlist_head vlist;
};

#endif