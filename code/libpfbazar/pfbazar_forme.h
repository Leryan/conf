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

#include <pfbazar_complexe.h>

struct forme_forme_s
{
    cpx_s *pts;
    cpx_s centre_rotation;

    unsigned char *charset;
    unsigned char d_sym;
    unsigned int points;

    char ascii_art;
};

typedef struct forme_forme_s forme_s;

const cpx_s ComplexeNul;

/* initialisation */
void forme_init_coords(forme_s *r, unsigned char *charset, const double dec_x, const double dec_y, const unsigned int points, const double *coords, const char ascii_art, const char centrage);

void forme_init_longueurs(forme_s *r, unsigned char *charset, const double dec_x, const double dec_y, const double longueur, const double hauteur, const char ascii_art, const char centrage);
/* divers */
void d_permutation(double *v1, double *v2);
void forme_free(forme_s *r);
/* manipulation de la figure */
void forme_decale(forme_s *r, cpx_s decalage);
void forme_excentre(forme_s *r, cpx_s n_centre);
void forme_recentre(forme_s *r);
void forme_rotation(forme_s *r, const double angle);
void forme_zoom(forme_s *r, const double zoom);
/* traçage */
void forme_trace_seg(forme_s *r, const unsigned int seg);
void forme_trace(forme_s *r, const short c_pair, const short color1, const short color2);
