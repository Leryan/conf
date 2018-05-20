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

#include <math.h>
#include <curses.h>
#include <stdlib.h>
#include <unistd.h>
#include <pfbazar_forme.h>

#define PAS_Y 1.0

static void forme_sel_char(forme_s *r, const unsigned int seg);
static void forme_init_decalage(forme_s *r);

void forme_decale(forme_s *r, cpx_s decalage)
{
    unsigned int i;

    for(i = 0; i < r->points; i++)
    {
        r->pts[i].a += decalage.a;
        r->pts[i].b += decalage.b;
    }

    r->centre_rotation.a += decalage.a;
    r->centre_rotation.b += decalage.b;
}

void forme_excentre(forme_s *r, cpx_s n_centre)
{
    r->centre_rotation.a = n_centre.a;
    r->centre_rotation.b = n_centre.b;
}

static void forme_init_decalage(forme_s *r)
{
    double mod, prevmod;
    unsigned int i;

    for(i = 0, prevmod = 0.0; i < r->points; i++)
    {
        mod = cpx_module(&r->pts[i], cpx_creer(0.0, 0.0));
        if(prevmod < mod)
        {
            prevmod = mod;
        }
    }

    forme_decale(r, cpx_creer(prevmod, prevmod));
}

void forme_zoom(forme_s *r, const double zoom)
{
    unsigned int i;
    double arg, mod;

    for(i = 0; i < r->points; i++)
    {
        arg = cpx_argument(&r->pts[i], r->centre_rotation);
        mod = cpx_module(&r->pts[i], r->centre_rotation);

        r->pts[i].a = cos(arg) * mod * zoom;
        r->pts[i].b = sin(arg) * mod * zoom;
    }
}

void d_permutation(double *v1, double *v2)
{
    double v;

    v = *v1;
    *v1 = *v2;
    *v2 = v;
}

static void forme_sel_char(forme_s *r, const unsigned int seg)
{
#define COUCHE 0
#define GAUCHE 1
#define DEBOUT 2
#define DROITE 3
    double arg = cpx_argument(&r->pts[seg], r->centre_rotation);
    /*
     * C'est moche, laid, pas beau, à optimiser.
     */
    arg *= 180 / M_PI;

    if((150 < arg && arg < -150) || (-30 < arg && arg < 30))
    {
        r->d_sym = r->charset[DROITE];
    }
    else if((30 <= arg && arg < 60) || (-150 <= arg && arg < -120))
    {
        r->d_sym = r->charset[COUCHE];
    }
    else if((60 <= arg && arg < 120) || (-120 <= arg && arg <= -60))
    {
        r->d_sym = r->charset[GAUCHE];
    }
    else
    {
        r->d_sym = r->charset[DEBOUT];
    }
}

void forme_trace_seg(forme_s *r, const unsigned int seg)
{
    double a, x, b, y, x1, y1, x2, y2;

    x1 = r->pts[seg].a;
    y1 = r->pts[seg].b;
    x2 = r->pts[(seg + 1) & (r->points - 1)].a;
    y2 = r->pts[(seg + 1) & (r->points - 1)].b;

    if(r->ascii_art)
    {
        forme_sel_char(r, seg);
    }
    else
    {
        r->d_sym = r->charset[4];
    }

    if(round(x1) != round(x2))
    {
        //Comme l'informatique est bête, si on fait le calcul dans le
        //mauvais sens ça va pas le faire.
        if(x1 > x2)
        {
            d_permutation(&x1, &x2);
            d_permutation(&y1, &y2);
        }

        a = (y2 - y1) / (x2 - x1);
        x = x1;
        b = y2 - a * x2;
        y = y1;

        if(y > y2)
        {
            d_permutation(&y, &y2);
        }

        while(1)
        {
            //Si pour un déplacement de 1 sur x on se déplace de y > 1 : pas bon
            if(1 < a || a < -1)
            {
                y += 1.0;
                x = (y - b) / a;
            }
            else
            {
                x += 1.0;
                y = a * x + b;
            }

            /*Ce hack s'explique (peut-être) par le fait que la valeur de x
             * au début n'est pas la bonne suivant le coeff a et reste donc en
             * x1. Ce qui donne un x invariant et une position y suivant un
             * point.
             */
            if(x < x2 && y < y2)
            {
                mvaddch(y, x, r->d_sym);
            }
            else
            {
                break;
            }
        }
    }
    else
    {
        if(y1 > y2)
        {
            d_permutation(&y1, &y2);
        }
        for(y = y1; y <= y2; y += PAS_Y)
        {
            mvaddch(y, x1, r->d_sym);
        }
    }
    mvaddch(r->pts[seg].b, r->pts[seg].a, r->d_sym);
}

void forme_trace(forme_s *r, const short c_pair, const short color1, const short color2)
{
    unsigned int seg;

    init_pair(c_pair, color1, color2);
    attron(COLOR_PAIR(c_pair));

    for(seg = 0; seg < r->points; seg++)
    {
        forme_trace_seg(r, seg);
    }
}

void forme_init_longueurs(forme_s *r, unsigned char *charset, const double dec_x, const double dec_y, const double longueur, const double hauteur, const char ascii_art, const char centrage)
{
#define LON (longueur / 2.0)
#define HAU (hauteur / 2.0)
    double points[8] = { -LON, HAU, -LON, -HAU, LON, -HAU, LON, HAU};

    forme_init_coords(r, charset, dec_x, dec_y, 4, points, ascii_art, centrage);
}

void forme_init_coords(forme_s *r, unsigned char *charset, const double dec_x, const double dec_y, const unsigned int points, const double *coords, const char ascii_art, const char centrage)
{
    unsigned int i;

    r->pts = malloc(sizeof(cpx_s) * points);

    for(i = 0; i < points; i++)
    {
        r->pts[i].a = coords[i * 2];
        r->pts[i].b = coords[(i * 2) + 1];
    }

    r->ascii_art = ascii_art;
    r->points = points;
    r->charset = charset;
    r->d_sym = charset[0];

    if(centrage)
    {
        r->centre_rotation.a = 0.0;
        r->centre_rotation.b = 0.0;
        forme_init_decalage(r);
    }
    else
    {
        for(i = 0; i < r->points; i++)
        {
            r->pts[i].a += dec_x;
            r->pts[i].b += dec_y;
        }
        r->centre_rotation.a = dec_x;
        r->centre_rotation.b = dec_y;
    }
}

void forme_free(forme_s *r)
{
    free(r->pts);
}

void forme_rotation(forme_s *r, const double angle)
{
    unsigned int i;

    for(i = 0; i < r->points; i++)
    {
        cpx_rotation(&r->pts[i], r->centre_rotation, angle);
    }
}
