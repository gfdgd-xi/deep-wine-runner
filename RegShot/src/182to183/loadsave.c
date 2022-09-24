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

char str_RegshotHiveSignature182[] = REGSHOT_HIVE_SIGNATURE_182;
char str_RegshotHiveSignature183[] = REGSHOT_HIVE_SIGNATURE;
LPBYTE lpOldHiveHeader;

SAVEKEYCONTENT skc;
SAVEVALUECONTENT svc;
SAVEFILECONTENT sfc;


//--------------------------------------------------
// Registry save engine
//--------------------------------------------------
VOID SaveRegKey(LPKEYCONTENT lpKeyContent, DWORD nFPCurrentFatherKey, DWORD nFPCaller)
{
    DWORD   nFPTemp4Write;
    DWORD   nFPHeader;
    DWORD   nFPCurrent;
    DWORD   nLenPlus1;
    INT     nPad;
    INT     nPad1;
    LPVALUECONTENT lpv;

    // Note use (DWORD) to disable warning of lost of data to convert size_t to dword, in current windows,it is safe that registry's xxxxname is stay in DWORD long
    nLenPlus1 = (DWORD)strlen(lpKeyContent->lpkeyname) + 1;                     // Get len+1
    nPad = (nLenPlus1 % sizeof(DWORD) == 0) ? 0 : (sizeof(DWORD) - nLenPlus1 % sizeof(DWORD));
    nFPHeader = SetFilePointer(hFileWholeReg, 0, NULL, FILE_CURRENT);           // Save head fp

    // using struct ,idea from maddes
    skc.fpos_keyname = nFPHeader + sizeof(SAVEKEYCONTENT);
    skc.fpos_firstvalue = (lpKeyContent->lpfirstvalue != NULL) ? (nFPHeader + sizeof(SAVEKEYCONTENT) + nLenPlus1 + nPad) : 0;
    skc.fpos_firstsubkey = 0;   // it is filled later.
    skc.fpos_brotherkey = 0;    // it is filled later
    skc.fpos_fatherkey = nFPCurrentFatherKey;
    skc.bkeymatch = 0;
    WriteFile(hFileWholeReg, &skc, sizeof(skc), &NBW, NULL);

    WriteFile(hFileWholeReg, lpKeyContent->lpkeyname, nLenPlus1, &NBW, NULL); // Save the current keyname

    nFPTemp4Write = 0;
    if (nPad > 0) {
        WriteFile(hFileWholeReg, &nFPTemp4Write, nPad, &NBW, NULL);
    }


    // Save the sub-value of current KeyContent
    for (lpv = lpKeyContent->lpfirstvalue; lpv != NULL; lpv = lpv->lpnextvalue) {

        nLenPlus1 = (DWORD)strlen(lpv->lpvaluename) + 1;
        nPad = (nLenPlus1 % sizeof(DWORD) == 0) ? 0 : (sizeof(DWORD) - nLenPlus1 % sizeof(DWORD));              // determine if pad to 4bytes is needed
        nPad1 = (lpv->datasize % sizeof(DWORD) == 0) ? 0 : (sizeof(DWORD) - lpv->datasize % sizeof(DWORD));

        nFPCurrent = SetFilePointer(hFileWholeReg, 0, NULL, FILE_CURRENT);  // Save fp
        svc.typecode = lpv->typecode;
        svc.datasize = lpv->datasize;
        svc.fpos_valuename = nFPCurrent + sizeof(SAVEVALUECONTENT);         // size must same for valuecontent and savevaluecontent
        svc.fpos_valuedata = (lpv->datasize > 0) ? (nFPCurrent + sizeof(SAVEVALUECONTENT) + nLenPlus1 + nPad) : 0;    // if no lpvaluedata, we write 0
        svc.fpos_nextvalue = (lpv->lpnextvalue != NULL) ? (nFPCurrent + sizeof(SAVEVALUECONTENT) + nLenPlus1 + nPad + lpv->datasize + nPad1) : 0;   // if no nextvalue we write 0
        svc.fpos_fatherkey = nFPHeader;
        svc.bvaluematch = 0;
        WriteFile(hFileWholeReg, &svc, sizeof(svc), &NBW, NULL);


        WriteFile(hFileWholeReg, lpv->lpvaluename, nLenPlus1, &NBW, NULL);  // Save lpvaluename

        nFPTemp4Write = 0;
        if (nPad > 0) {
            WriteFile(hFileWholeReg, &nFPTemp4Write, nPad, &NBW, NULL);
        }

        if (lpv->datasize > 0) {
            WriteFile(hFileWholeReg, lpv->lpvaluedata, lpv->datasize, &NBW, NULL); // Save lpvaluedata

            if (nPad1 > 0) {
                WriteFile(hFileWholeReg, &nFPTemp4Write, nPad1, &NBW, NULL);
            }
        }

    }

    if (lpKeyContent->lpfirstsubkey != NULL) {
        // pass this keycontent's position as subkey's fatherkey's position and pass the "lpfirstsubkey field"
        SaveRegKey(lpKeyContent->lpfirstsubkey, nFPHeader, nFPHeader + 2 * sizeof(DWORD));
    }

    if (lpKeyContent->lpbrotherkey != NULL) {
        // pass this key's fatherkey's position as brother's father and pass "lpbrotherkey field"
        SaveRegKey(lpKeyContent->lpbrotherkey, nFPCurrentFatherKey, nFPHeader + 3 * sizeof(DWORD));
    }

    if (nFPCaller > 0) { // save position of current key in current father key
        nFPCurrent = SetFilePointer(hFileWholeReg, 0, NULL, FILE_CURRENT);
        SetFilePointer(hFileWholeReg, nFPCaller, NULL, FILE_BEGIN);
        WriteFile(hFileWholeReg, &nFPHeader, sizeof(nFPHeader), &NBW, NULL);
        SetFilePointer(hFileWholeReg, nFPCurrent, NULL, FILE_BEGIN);
    }

}

//--------------------------------------------------
// File save engine (It is stupid again!) added in 1.8
// 1.8.3 changed some struct
// modi 20111216
//--------------------------------------------------
VOID SaveFileContent(LPFILECONTENT lpFileContent, DWORD nFPCurrentFatherFile, DWORD nFPCaller)
{

    DWORD   nFPTemp4Write;
    DWORD   nFPHeader;
    DWORD   nFPCurrent;
    DWORD   nLenPlus1;
    int     nPad;

    nLenPlus1 = (DWORD)strlen(lpFileContent->lpfilename) + 1;                     // Get len+1
    nFPHeader = SetFilePointer(hFileWholeReg, 0, NULL, FILE_CURRENT);             // Save head fp
    // using struct, idea from maddes
    sfc.fpos_filename = nFPHeader + sizeof(SAVEFILECONTENT);                      // 1.8.3 11*4 former is 10*4+1
    sfc.writetimelow = lpFileContent->writetimelow;
    sfc.writetimehigh = lpFileContent->writetimehigh;
    sfc.filesizelow = lpFileContent->filesizelow;
    sfc.filesizehigh = lpFileContent->filesizehigh;
    sfc.fileattr = lpFileContent->fileattr;
    sfc.cksum = lpFileContent->cksum;
    sfc.fpos_firstsubfile = 0;
    sfc.fpos_brotherfile = 0;
    sfc.fpos_fatherfile = nFPCurrentFatherFile;
    sfc.bfilematch = 0;
    WriteFile(hFileWholeReg, &sfc, sizeof(sfc), &NBW, NULL);

    WriteFile(hFileWholeReg, lpFileContent->lpfilename, nLenPlus1, &NBW, NULL); // Save the current filename

    nPad = (nLenPlus1 % sizeof(DWORD) == 0) ? 0 : (sizeof(DWORD) - nLenPlus1 % sizeof(DWORD));

    nFPTemp4Write = 0;
    if (nPad > 0) {
        WriteFile(hFileWholeReg, &nFPTemp4Write, nPad, &NBW, NULL);         // Save the current filename
    }

    if (lpFileContent->lpfirstsubfile != NULL) {
        // pass this filecontent's position as subfile's fatherfile's position and pass the "lpfirstsubfile field"
        SaveFileContent(lpFileContent->lpfirstsubfile, nFPHeader, nFPHeader + 7 * sizeof(DWORD));
    }

    if (lpFileContent->lpbrotherfile != NULL) {
        // pass this file's fatherfile's position as brother's father and pass "lpbrotherfile field"
        SaveFileContent(lpFileContent->lpbrotherfile, nFPCurrentFatherFile, nFPHeader + 8 * sizeof(DWORD));
    }

    if (nFPCaller > 0) {    // save position of current file in current father file
        nFPCurrent = SetFilePointer(hFileWholeReg, 0, NULL, FILE_CURRENT);
        SetFilePointer(hFileWholeReg, nFPCaller, NULL, FILE_BEGIN);
        WriteFile(hFileWholeReg, &nFPHeader, sizeof(nFPHeader), &NBW, NULL);
        SetFilePointer(hFileWholeReg, nFPCurrent, NULL, FILE_BEGIN);
    }

}

//---------------------------------------------------------------------------------
// Load registry from HIVE file (After this, we should realign the data in memory)
//---------------------------------------------------------------------------------
BOOL LoadHive(LPCSTR lpFileName, LPKEYCONTENT FAR *lplpKeyHLM, LPKEYCONTENT FAR *lplpKeyUSER,
              LPHEADFILE FAR *lplpHeadFile)
{
    DWORD   nFileSize;
    DWORD   nOffSet = 0;
    size_t  nBase;
    DWORD   i, j;
    DWORD   nRemain;
    DWORD   nReadSize;
    BOOL    bRet = FALSE;
    LPBYTE  lpHive;

    hFileWholeReg = CreateFile(lpFileName, GENERIC_READ , FILE_SHARE_READ , NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFileWholeReg != INVALID_HANDLE_VALUE) {
        lpHive = MYALLOC0(16);
        ReadFile(hFileWholeReg, lpHive, 16, &NBW, NULL);

        if (strcmp(str_RegshotHiveSignature182, (const char *)(lpHive)) != 0) {
            printf("Error:Does not detect regshot_hive_signagure used by version <=1.8.2"); //changed in 1.8.3
            bRet = FALSE;
        } else {
            nFileSize = GetFileSize(hFileWholeReg, NULL);
            MYFREE(lpHive);

            lpHive = MYALLOC(nFileSize);
            nBase = (size_t) lpHive;
            lpOldHiveHeader = lpHive;

            ReadFile(hFileWholeReg, &nOffSet, 4, &NBW, NULL);
            *lplpKeyHLM = (LPKEYCONTENT)(nBase + nOffSet);

            ReadFile(hFileWholeReg, &nOffSet, 4, &NBW, NULL);
            *lplpKeyUSER = (LPKEYCONTENT)(nBase + nOffSet);

            ReadFile(hFileWholeReg, &nOffSet, 4, &NBW, NULL);
            if (nOffSet == 0) {
                *lplpHeadFile = NULL;
            } else {
                *lplpHeadFile = (LPHEADFILE)(nBase + nOffSet);
            }

            SetFilePointer(hFileWholeReg, 0, NULL, FILE_BEGIN);

#define READ_BATCH_SIZE 8192

            printf("Reading %s....", lpFileName);
            for (i = 0, j = 0, nRemain = nFileSize;; i += READ_BATCH_SIZE, j++) {
                if (nRemain >= READ_BATCH_SIZE) {
                    nReadSize = READ_BATCH_SIZE;
                } else {
                    nReadSize = nRemain;
                }
                ReadFile(hFileWholeReg, (lpHive) + i, nReadSize, &NBW, NULL); // read the whole file now
                if (NBW != nReadSize) {
                    printf("Reading ERROR!");
                    break;
                }
                nRemain -= nReadSize;
                if (nRemain == 0) {
                    break;
                }

            }
#undef READ_BATCH_SIZE

            ReAlignReg(*lplpKeyHLM, nBase);
            ReAlignReg(*lplpKeyUSER, nBase);

            if (*lplpHeadFile != NULL) {
                ReAlignFile(*lplpHeadFile, nBase);
            }

            bRet = TRUE;

        }
        CloseHandle(hFileWholeReg);
    } else {
        printf("Error:Can not open file!\n");
        bRet = FALSE;
    }

    return(bRet);

}


//--------------------------------------------------
// Routine to call registry save engine and file save engine
//--------------------------------------------------
BOOL SaveHive(LPCSTR lpFileName, LPKEYCONTENT lpKeyHLM, LPKEYCONTENT lpKeyUSER,
              LPHEADFILE lpHF)
{
    DWORD nFPcurrent;
    DWORD nFPcurrent1;
    DWORD nFPTemp4Write;
    BOOL bRet;
    LPHEADFILE lphf;

    bRet = FALSE;

    if (lpKeyHLM != NULL || lpKeyUSER != NULL) {

        hFileWholeReg = CreateFile(lpFileName, GENERIC_WRITE, 0, NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);
        if (hFileWholeReg != INVALID_HANDLE_VALUE) {

            WriteFile(hFileWholeReg, str_RegshotHiveSignature183, sizeof(str_RegshotHiveSignature183) - 1, &NBW, NULL);

            // 0   signature( <= 12) last 4 bytes may be used in furture
            // 16  startoflpkeyhlm (512)
            // 20  startoflpkeyuser(???)
            // 24  fileheadchain begin (new) ->(file -> nextfilehead(4) next4bytes is filecontent) added in 1.8
            // 28  future use!
            // 32  computer name
            // 96  username
            // 160 systemtime

            // Save the position of H_L_M
            nFPcurrent = HIVEBEGINOFFSET; // computerlen*2+sizeof(systemtime)+32 must <hivebeginoffset
            SetFilePointer(hFileWholeReg, 16, NULL, FILE_BEGIN);
            WriteFile(hFileWholeReg, &nFPcurrent, 4, &NBW, NULL);
            SetFilePointer(hFileWholeReg, 28, NULL, FILE_BEGIN);
            WriteFile(hFileWholeReg, lpOldHiveHeader + 28, HIVEBEGINOFFSET - 28, &NBW, NULL);

            SetFilePointer(hFileWholeReg, HIVEBEGINOFFSET, NULL, FILE_BEGIN);

            printf("\nWriting %s....", lpFileName);
            if (lpKeyHLM != NULL) {
                SaveRegKey(lpKeyHLM, 0, 0);
            }

            // Save the position of hkeyUsr
            nFPcurrent = SetFilePointer(hFileWholeReg, 0, NULL, FILE_CURRENT);
            SetFilePointer(hFileWholeReg, 20, NULL, FILE_BEGIN);
            WriteFile(hFileWholeReg, &nFPcurrent, 4, &NBW, NULL);
            SetFilePointer(hFileWholeReg, nFPcurrent, NULL, FILE_BEGIN);

            if (lpKeyUSER != NULL) {
                SaveRegKey(lpKeyUSER, 0, 0);
            }

            if (lpHF != NULL) {
                // Write start position of file chain
                nFPcurrent = SetFilePointer(hFileWholeReg, 0, NULL, FILE_CURRENT);
                SetFilePointer(hFileWholeReg, 24, NULL, FILE_BEGIN);
                WriteFile(hFileWholeReg, &nFPcurrent, 4, &NBW, NULL);   // write start pos at 24
                SetFilePointer(hFileWholeReg, nFPcurrent, NULL, FILE_BEGIN);

                for (lphf = lpHF; lphf != NULL;) {
                    nFPcurrent = SetFilePointer(hFileWholeReg, 0, NULL, FILE_CURRENT);           // save place for next filehead in chain
                    SetFilePointer(hFileWholeReg, sizeof(LPSAVEHEADFILE), NULL, FILE_CURRENT);       // move 4 or 8 bytes, leave space for lpnextfilecontent
                    nFPTemp4Write = nFPcurrent + sizeof(LPSAVEHEADFILE) + sizeof(LPSAVEFILECONTENT);
                    WriteFile(hFileWholeReg, &nFPTemp4Write, sizeof(nFPTemp4Write), &NBW, NULL); // write lpfilecontent ,bug in r107

                    SaveFileContent(lphf->lpfilecontent, 0, 0);
                    nFPcurrent1 = SetFilePointer(hFileWholeReg, 0, NULL, FILE_CURRENT);
                    nFPTemp4Write = nFPcurrent1;
                    SetFilePointer(hFileWholeReg, nFPcurrent, NULL, FILE_BEGIN);
                    lphf = lphf->lpnextheadfile;
                    if (lphf != NULL) {
                        WriteFile(hFileWholeReg, &nFPTemp4Write, sizeof(nFPTemp4Write), &NBW, NULL);
                    } else {
                        nFPTemp4Write = 0;
                        WriteFile(hFileWholeReg, &nFPTemp4Write, sizeof(nFPTemp4Write), &NBW, NULL);
                        break;
                    }
                    SetFilePointer(hFileWholeReg, nFPcurrent1, NULL, FILE_BEGIN);
                }
            }

            CloseHandle(hFileWholeReg);
            printf("\nDone.\n");
            bRet = TRUE;
        } else {
            printf("Error:Can not create file!\n");
            bRet = FALSE;
        }

    }
    return bRet;
}
