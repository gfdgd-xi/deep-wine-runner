/*
    Copyright 2011 Regshot Team

    Regshot is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Regshot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Regshot; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#include "global.h"

//--------------------------------------------------
// Realign key & value content after loading from hive file
//--------------------------------------------------
VOID ReAlignReg(LPKEYCONTENT lpKey, size_t nBase)
{
    LPVALUECONTENT lpv;

    if (lpKey->lpkeyname != NULL) {
        lpKey->lpkeyname += nBase;
    }
    if (lpKey->lpfirstvalue != NULL) {
        lpKey->lpfirstvalue = (LPVALUECONTENT)((LPBYTE)lpKey->lpfirstvalue + nBase);
    }
    if (lpKey->lpfirstsubkey != NULL) {
        lpKey->lpfirstsubkey = (LPKEYCONTENT)((LPBYTE)lpKey->lpfirstsubkey + nBase);
    }
    if (lpKey->lpbrotherkey != NULL) {
        lpKey->lpbrotherkey = (LPKEYCONTENT)((LPBYTE)lpKey->lpbrotherkey + nBase);
    }
    if (lpKey->lpfatherkey != NULL) {
        lpKey->lpfatherkey = (LPKEYCONTENT)((LPBYTE)lpKey->lpfatherkey + nBase);
    }


    for (lpv = lpKey->lpfirstvalue; lpv != NULL; lpv = lpv->lpnextvalue) {

        if (lpv->lpvaluename != NULL) {
            lpv->lpvaluename += nBase;
        }
        if (lpv->lpvaluedata != NULL) {
            lpv->lpvaluedata += nBase;
        }
        if (lpv->lpnextvalue != NULL) {
            lpv->lpnextvalue = (LPVALUECONTENT)((LPBYTE)lpv->lpnextvalue + nBase);
        }
        if (lpv->lpfatherkey != NULL) {
            lpv->lpfatherkey = (LPKEYCONTENT)((LPBYTE)lpv->lpfatherkey + nBase);
        }

    }

    if (lpKey->lpfirstsubkey != NULL) {
        ReAlignReg(lpKey->lpfirstsubkey, nBase);
    }

    if (lpKey->lpbrotherkey != NULL) {
        ReAlignReg(lpKey->lpbrotherkey, nBase);
    }
}


//--------------------------------------------------
// Realign filecontent, called by ReAlignFile()
//--------------------------------------------------
VOID ReAlignFileContent(LPFILECONTENT lpFC, size_t nBase)
{

    if (lpFC->lpfilename != NULL) {
        lpFC->lpfilename += nBase;
    }
    if (lpFC->lpfirstsubfile != NULL) {
        lpFC->lpfirstsubfile = (LPFILECONTENT)((LPBYTE)lpFC->lpfirstsubfile + nBase);
    }
    if (lpFC->lpbrotherfile != NULL) {
        lpFC->lpbrotherfile = (LPFILECONTENT)((LPBYTE)lpFC->lpbrotherfile + nBase);
    }
    if (lpFC->lpfatherfile != NULL) {
        lpFC->lpfatherfile = (LPFILECONTENT)((LPBYTE)lpFC->lpfatherfile + nBase);
    }


    if (lpFC->lpfirstsubfile != NULL) {
        ReAlignFileContent(lpFC->lpfirstsubfile, nBase);
    }

    if (lpFC->lpbrotherfile != NULL) {
        ReAlignFileContent(lpFC->lpbrotherfile, nBase);
    }

}


//--------------------------------------------------
// Realign file, walk through chain
//--------------------------------------------------
VOID ReAlignFile(LPHEADFILE lpHF, size_t nBase)
{
    LPHEADFILE  lphf;

    for (lphf = lpHF; lphf != NULL; lphf = lphf->lpnextheadfile) {

        if (lphf->lpnextheadfile != NULL) {
            lphf->lpnextheadfile = (LPHEADFILE)((LPBYTE)lphf->lpnextheadfile + nBase);
        }
        if (lphf->lpfilecontent != NULL) {
            lphf->lpfilecontent = (LPFILECONTENT)((LPBYTE)lphf->lpfilecontent + nBase);
        }

        if (lphf->lpfilecontent != NULL) {    // I wouldn't find crash bug(loadhive->readfile) in 1.8.0 if I had added it in that version
            ReAlignFileContent(lphf->lpfilecontent, nBase);
        }
    }
}
