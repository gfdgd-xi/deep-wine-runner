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

#include <windows.h>
#include <stdio.h>
#include <shlobj.h>

#define REGSHOT_HIVE_SIGNATURE_182  "REGSHOTHIVE"
#define REGSHOT_HIVE_SIGNATURE      "RSHIVE183"

#define HIVEBEGINOFFSET 512         // Hive file out put header computerlen*2+sizeof(systemtime)+32 must <hivebeginoffset!!!!!!!!!!!!!!

#ifdef USEHEAPALLOC_DANGER

// MSDN doc say use HEAP_NO_SERIALIZE is not good for process heap :( so change fromm 1 to 0 20111216 ,slower than using 1
#define MYALLOC(x)  HeapAlloc(hHeap,0,x)
#define MYALLOC0(x) HeapAlloc(hHeap,8,x) // HEAP_NO_SERIALIZE|HEAP_ZERO_MEMORY ,1|8
#define MYFREE(x)   HeapFree(hHeap,0,x)

#else

#define MYALLOC(x)  GlobalAlloc(GMEM_FIXED,x)
#define MYALLOC0(x) GlobalAlloc(GPTR,x)
#define MYFREE(x)   GlobalFree(x)

#endif

// Struct for hive version <=1.8.2
// Struct used for Windows Registry Key
struct _KEYCONTENT {
    LPSTR  lpkeyname;                          // Pointer to key's name
    struct _VALUECONTENT FAR *lpfirstvalue;    // Pointer to key's first value
    struct _KEYCONTENT FAR *lpfirstsubkey;     // Pointer to key's first subkey
    struct _KEYCONTENT FAR *lpbrotherkey;      // Pointer to key's brother
    struct _KEYCONTENT FAR *lpfatherkey;       // Pointer to key's father
    BYTE   bkeymatch;                          // Flag used at comparing, 1.8.2<= is byte

};
typedef struct _KEYCONTENT KEYCONTENT, FAR *LPKEYCONTENT;


// Struct used for Windows Registry Value
struct _VALUECONTENT {
    DWORD  typecode;                           // Type of value [DWORD,STRING...]
    DWORD  datasize;                           // Value data size in bytes
    LPSTR  lpvaluename;                        // Pointer to value name
    LPBYTE lpvaluedata;                        // Pointer to value data
    struct _VALUECONTENT FAR *lpnextvalue;     // Pointer to value's brother
    struct _KEYCONTENT FAR *lpfatherkey;       // Pointer to value's father[Key]
    BYTE   bvaluematch;                        // Flag used at comparing, 1.8.2<= is byte
};
typedef struct _VALUECONTENT VALUECONTENT, FAR *LPVALUECONTENT;


// Struct used for Windows File System
struct _FILECONTENT {
    LPSTR  lpfilename;                         // Pointer to filename
    DWORD  writetimelow;                       // File write time [LOW  DWORD]
    DWORD  writetimehigh;                      // File write time [HIGH DWORD]
    DWORD  filesizelow;                        // File size [LOW  DWORD]
    DWORD  filesizehigh;                       // File size [HIGH DWORD]
    DWORD  fileattr;                           // File attributes
    DWORD  cksum;                              // File checksum(plan to add in 1.8 not used now)
    struct _FILECONTENT FAR *lpfirstsubfile;   // Pointer to files[DIRS] first sub file
    struct _FILECONTENT FAR *lpbrotherfile;    // Pointer to files[DIRS] brother
    struct _FILECONTENT FAR *lpfatherfile;     // Pointer to files father
    BYTE   bfilematch;                         // Flag used at comparing, 1.8.2<= is byte
};
typedef struct _FILECONTENT FILECONTENT, FAR *LPFILECONTENT;


// Adjusted for filecontent saving. 1.8
struct _HEADFILE {
    struct _HEADFILE FAR *lpnextheadfile;      // Pointer to next headfile struc
    LPFILECONTENT          lpfilecontent;      // Pointer to filecontent
};
typedef struct  _HEADFILE HEADFILE, FAR *LPHEADFILE;

// Pointers to Registry Key
LPKEYCONTENT    lpHeadLocalMachine;    // Pointer to HKEY_LOCAL_MACHINE 1
LPKEYCONTENT    lpHeadUsers;           // Pointer to HKEY_USERS 1
LPHEADFILE      lpHeadFile;            // Pointer to headfile
LPBYTE          lpTempHive;            // Pointer for loading hive files
HANDLE          hFileWholeReg;
DWORD           NBW;

//----------------- struct for saving designed by maddes ------------------------

struct _SAVEKEYCONTENT {
    DWORD  fpos_keyname;            // Pointer to key's name
    DWORD  fpos_firstvalue;         // Pointer to key's first value
    DWORD  fpos_firstsubkey;        // Pointer to key's first subkey
    DWORD  fpos_brotherkey;         // Pointer to key's brother
    DWORD  fpos_fatherkey;          // Pointer to key's father
    DWORD  bkeymatch;               // Flag used at comparing, 1.8.2 <= is byte

};
typedef struct _SAVEKEYCONTENT SAVEKEYCONTENT, FAR *LPSAVEKEYCONTENT;


// Struct used for Windows Registry Value
struct _SAVEVALUECONTENT {
    DWORD  typecode;                // Type of value [DWORD,STRING...]
    DWORD  datasize;                // Value data size in bytes
    DWORD  fpos_valuename;          // Pointer to value name
    DWORD  fpos_valuedata;          // Pointer to value data
    DWORD  fpos_nextvalue;          // Pointer to value's brother
    DWORD  fpos_fatherkey;          // Pointer to value's father[Key]
    DWORD  bvaluematch;             // Flag used at comparing, 1.8.2 <= is byte
};
typedef struct _SAVEVALUECONTENT SAVEVALUECONTENT, FAR *LPSAVEVALUECONTENT;


// Struct used for Windows File System
struct _SAVEFILECONTENT {
    DWORD  fpos_filename;            // Pointer to filename
    DWORD  writetimelow;             // File write time [LOW  DWORD]
    DWORD  writetimehigh;            // File write time [HIGH DWORD]
    DWORD  filesizelow;              // File size [LOW  DWORD]
    DWORD  filesizehigh;             // File size [HIGH DWORD]
    DWORD  fileattr;                 // File attributes
    DWORD  cksum;                    // File checksum(plan to add in 1.8 not used now)
    DWORD  fpos_firstsubfile;        // Pointer to files[DIRS] first sub file
    DWORD  fpos_brotherfile;         // Pointer to files[DIRS] brother
    DWORD  fpos_fatherfile;          // Pointer to files father
    DWORD  bfilematch;               // Flag used at comparing, 1.8.2 <= is byte
};
typedef struct _SAVEFILECONTENT SAVEFILECONTENT, FAR *LPSAVEFILECONTENT;


// Adjusted for filecontent saving. 1.8
struct _SAVEHEADFILE {
    DWORD  fpos_nextheadfile;       // Pointer to next headfile struc
    DWORD  fpos_filecontent;        // Pointer to filecontent
};
typedef struct  _SAVEHEADFILE SAVEHEADFILE, FAR *LPSAVEHEADFILE;


VOID ReAlignReg(LPKEYCONTENT lpKey, size_t nBase);
VOID ReAlignFileContent(LPFILECONTENT lpFC, size_t nBase);
VOID ReAlignFile(LPHEADFILE lpHF, size_t nBase);
BOOL LoadHive(LPCSTR lpFileName, LPKEYCONTENT FAR *lplpKeyHLM, LPKEYCONTENT FAR *lplpKeyUSER, LPHEADFILE FAR *lplpHeadFile);
BOOL SaveHive(LPCSTR lpFileName, LPKEYCONTENT lpKeyHLM, LPKEYCONTENT lpKeyUSER, LPHEADFILE lpHF);
