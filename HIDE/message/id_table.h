#ifndef GENOS_ID_TABLE_H
#define GENOS_ID_TABLE_H

#include <stdint.h>
#include <stdlib.h>
#include <gxx/datastruct/hlist_head.h>

//typedef size_t id_t;

/*struct id_table {
	size_t size;
	struct hlist_head* harray;
};

static inline void id_table_init(struct id_table* qtbl, size_t sz) {
	qtbl->harray = (struct hlist_head*) malloc(sz * sizeof(struct hlist_head));
	qtbl->size = sz;
	for(struct hlist_head *it = qtbl->harray, *eit = qtbl->harray + sz; it != eit; ++it) {
		hlist_head_init(it);
	}
}

static inline struct hlist_node* id_table_find(struct id_table* tbl, id_t id, size_t keyoff) {
	struct hlist_head* ceil = &tbl->harray[id % tbl->size];
	struct hlist_node* it;
	hlist_for_each(it, ceil) {
		if (*((id_t*)((char*)it + keyoff)) == id) return it;
	}
	return 0;
}*/

#endif