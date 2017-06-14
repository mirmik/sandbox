#include <gmsg/gmsgpack.h>
#include <stdio.h>
#include <ctype.h>

#define HEXDUMP_COLS 8

gmsg_t pack;
char buf[128];

void hexdump(void *mem, unsigned int len)
{
	unsigned int i, j;
	
	for(i = 0; i < len + ((len % HEXDUMP_COLS) ? (HEXDUMP_COLS - len % HEXDUMP_COLS) : 0); i++)
	{
		/* print offset */
		if(i % HEXDUMP_COLS == 0) {
			printf("0x%06x: ", i);
		}

		/* print hex data */
		if(i < len) {
			printf("%02x ", 0xFF & ((char*)mem)[i]);
		}

		/* end of block, just aligning for ASCII dump */
		else {
			printf("   ");
		}
		
		/* print ASCII dump */
		if(i % HEXDUMP_COLS == (HEXDUMP_COLS - 1)) {
			for(j = i - (HEXDUMP_COLS - 1); j <= i; j++) {
				
				/* end of block, not really printing */
				if(j >= len) {
					putchar(' ');
				}

				/* printable char */
				else if(isprint(((char*)mem)[j])) {
					putchar(0xFF & ((char*)mem)[j]);        
				}

				/* other char */
				else {
					putchar('.');
				}
			}
			putchar('\n');
		}
	}
}


static unsigned char crc8(unsigned char *pcBlock, unsigned int len)
{
    unsigned char crc = 0xFF;
    unsigned int i;

    while (len--)
    {
        crc ^= *pcBlock++;
        for (i = 0; i < 8; i++)
            crc = crc & 0x80 ? (crc << 1) ^ 0x31 : crc << 1;
    }
    return crc;
}


int main() {
	gmsg_init(&pack, buf, 128);

	gmsg_start(&pack);
	gmsg_add_part(&pack, "Hello\xC0World", 11);
	//gmsg_add_part(&pack, "Hello", 5);
	gmsg_finish(&pack);

	hexdump(pack.buf, pack.ptr - pack.buf);
	printf("%X\r\n", crc8("Hello\xDB\xDCWorld", 12));
}