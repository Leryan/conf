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
#include <pfbazar_complexe.h>

void cpx_rotation(cpx_s *const cpx, cpx_s const cpx_centre, const double angle)
{
    double mod, arg;

    arg = cpx_argument(cpx, cpx_centre) + angle * M_PI / 180.0;
    mod = cpx_module(cpx, cpx_centre);

    cpx->a = mod * cos(arg) + cpx_centre.a;
    cpx->b = mod * sin(arg) + cpx_centre.b;
}

double cpx_module(cpx_s *const cpx, cpx_s const cpx_centre)
{
    double a, b;

    a = cpx->a - cpx_centre.a;
    b = cpx->b - cpx_centre.b;

    return sqrt(a * a + b * b);
}

double cpx_argument(cpx_s *const cpx, cpx_s const cpx_centre)
{
    double a, b;

    a = cpx->a - cpx_centre.a;
    b = cpx->b - cpx_centre.b;

    if(a < 0.0)
    {
        if(b > 0.0)
        {
            return atan(b / a) + M_PI;
        }
        else
        {
            return atan(b / a) - M_PI;
        }
    }
    else
    {
        return atan(b / a);
    }
}

cpx_s cpx_creer(double a, double b)
{
    cpx_s z;

    z.a = a;
    z.b = b;

    return z;
}
