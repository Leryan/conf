/* Copyright (c) 2011, Florent PETERSCHMITT
 * All rights reserved.
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of Florent PETERSCHMITT nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <curses.h>
#include <unistd.h>
#include <pfbazar/pfbazar_forme.h>

#define SQ_VALx 15.0
#define SQ_VALy 5.0

int main(void)
{
    forme_s etoile, r, r2;
    int i, j;
    double m = 1.0;
    unsigned char charset[] = {'_', '\\', '|', '/', '*'};
    const double cetoile[] = {0.0, 16.0,
                              4.0, 4.0,
                              16.0, 0.0,
                              4.0, -4.0,
                              0.0, -16.0,
                              -4.0, -4.0,
                              -16.0, 0.0,
                              -4.0, 4.0
                             };

    initscr();
#ifdef WIN32
    resize_term(300, 300);
#endif
    curs_set(FALSE);
    start_color();

    forme_init_longueurs(&r, charset, 10.0, 10.0, 10.0, 10.0, 0, 1);
    forme_init_longueurs(&r2, charset, 20.0, 20.0, 10.0, 10.0, 0, 1);
    forme_init_coords(&etoile, charset, 10, 10, 8, cetoile, 0, 0);
    forme_excentre(&r2, cpx_creer(20.0, 20.0));
    for(i = 0; i < 1 * 180; i++)
    {
        /*if(i % 20 == 19)
        {
            m += 0.1;
            forme_zoom(&etoile, m);
        */
		forme_rotation(&r, 10.0);
        forme_trace(&r, 1, COLOR_RED, COLOR_BLACK);
        forme_trace(&etoile, 2, COLOR_GREEN, COLOR_BLACK);
        forme_trace(&r2, 3, COLOR_WHITE, COLOR_BLACK);
        refresh();
        usleep(25000);
        clear();
    }

    forme_free(&etoile);
    endwin();

    return EXIT_SUCCESS;
}
