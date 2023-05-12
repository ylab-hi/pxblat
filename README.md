# pyblat

<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>
pyblat
</h1>
<h3 align="center">📍 pyblat: Bringing Python to the Next Level!</h3>
<h3 align="center">🚀 Developed with the software and tools below.</h3>
<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="" />
<img src="https://img.shields.io/badge/Markdown-000000.svg?style=for-the-badge&logo=Markdown&logoColor=white" alt="pack" />
<img src="https://img.shields.io/badge/C++-00599C.svg?style=for-the-badge&logo=C++&logoColor=white" alt="h" />
<img src="https://img.shields.io/badge/C-A8B9CC.svg?style=for-the-badge&logo=C&logoColor=black" alt="python" />
</p>

</div>

---

## TODO

- [x] parser gfclient result
- [ ] parse gfserver query result
- [ ] multi-connection server
- [ ] benchmarking multi connection and original version
- [ ] test result with original version
- [ ] fix build.py to build ssl, hts, maybe libuv when install with pip
- [ ] add tool to conda channel
- [ ] add too to dokerhub
- [ ] add tool to pip
- [ ] change abort to throw exceptions

A binding for blat server and client

## 📚 Table of Contents

- [📚 Table of Contents](#-table-of-contents)
- [📍Overview](#-introdcution)
- [🔮 Features](#-features)
- [⚙️ Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🏎💨 Getting Started](#-getting-started)
- [🗺 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [🪪 License](#-license)
- [📫 Contact](#-contact)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 📍Overview

Pyblat is a Python library for dealing with BLAST-formatted files. It is capable of reading, writing, and parsing multiple types of BLAST outputs, as well as performing

## 🔮 Feautres

> `[📌  INSERT-PROJECT-FEATURES]`

---

<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-github-open.svg" width="80" />

## ⚙️ Project Structure

---

<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-src-open.svg" width="80" />

## 💻 Modules

<details closed><summary>Aux</summary>

| File           | Summary                                                                                                                                                                                                                                                                                              | Module                                   |
| :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------- |
| bandExt.h      | This code provides functions for banded Smith - Waterman extension of alignments , allowing for small gaps and mismatches . It allows for the extension of an alignment from a given start point , either forwards or backwards , with a maximum gap size and                                        | src/pyblat/extc/include/aux/bandExt.h    |
| base64.h       | This code provides functions for encoding and decoding strings using the Base64 algorithm . It includes functions for encoding a string , validating a string , and decoding a string . It is written in C and C++ .                                                                                 | src/pyblat/extc/include/aux/base64.h     |
| cheapcgi.h     | Error fetching summary.                                                                                                                                                                                                                                                                              | src/pyblat/extc/include/aux/cheapcgi.h   |
| filePath.h     | This code provides functions for parsing and manipulating file paths . It includes functions for splitting a full path into components , expanding relative paths to more absolute ones , making relative paths from one absolute directory / file to another , and checking that a path is relative | src/pyblat/extc/include/aux/filePath.h   |
| gfxPoly.h      | This code defines a struct gfxPoly , which is a two - dimensional polygon . It contains functions to create a new polygon , free up resources associated with a polygon , and add points to a polygon .                                                                                              | src/pyblat/extc/include/aux/gfxPoly.h    |
| hex.h          | This code provides functions for converting between binary and hexadecimal values . It includes functions for converting a nibble , byte , or binary string to hexadecimal , as well as functions for converting a hexadecimal character , byte                                                      | src/pyblat/extc/include/aux/hex.h        |
| htmlPage.h     | This code provides functions for reading , parsing , and submitting HTML pages and forms . It includes functions for reading cookies , parsing tags , and setting variables . It also includes functions for validating and printing HTML pages and forms .                                          | src/pyblat/extc/include/aux/htmlPage.h   |
| htmshell.h     | Htmshell.h is a library of functions used to generate HTML files on the fly . It includes functions to create cookies , encode and decode strings , print out HTML tags , and more . It is typically included with cheapcgi.h                                                                        | src/pyblat/extc/include/aux/htmshell.h   |
| https.h        | This code defines a function , netConnectHttps ( ) , which establishes an HTTPS connection with a server and returns a socket for the connection . If an error occurs , -1 is returned .                                                                                                             | src/pyblat/extc/include/aux/https.h      |
| internet.h     | This code provides functions for working with internet addresses , such as converting between IPV4 and IPV6 strings , creating masks , and checking if an IP address is in a subnet . It also includes functions for manipulating CIDR addresses and                                                 | src/pyblat/extc/include/aux/internet.h   |
| kxTok.h        | KxTok is a quick little tokenizer for stuff first loaded into memory . It was originally developed for the " Key eXpression " evaluator and can be used for public , private , or commercial purposes . It tokenizes text                                                                            | src/pyblat/extc/include/aux/kxTok.h      |
| memgfx.h       | Error fetching summary.                                                                                                                                                                                                                                                                              | src/pyblat/extc/include/aux/memgfx.h     |
| mime.h         | This file contains functions for parsing MIME messages , especially from a cgi from a multipart web form . It includes functions for parsing typical mime header lines , initializing a mimeBuf structure , and parsing multipart MIME messages                                                      | src/pyblat/extc/include/aux/mime.h       |
| portimpl.h     | This code provides functions for creating temporary files , determining the speed of the CPU , and returning the relative path to the trash directory for CGI binaries . It also contains structures for each web server supported , which are used to decide which functions to use during          | src/pyblat/extc/include/aux/portimpl.h   |
| rbTree.h       | rbTree is a type of binary tree which automatically keeps relatively balanced during inserts and deletions . It was originally created by Shane Saunders and adapted into local conventions by Jim Kent . It contains functions to add , find , remove , traverse , and dump                         | src/pyblat/extc/include/aux/rbTree.h     |
| srcVersion.h   | This code is a copyright statement for The Regents of the University of California , with a source version of 447 .                                                                                                                                                                                  | src/pyblat/extc/include/aux/srcVersion.h |
| axt.c          | Prompt too long to generate summary.                                                                                                                                                                                                                                                                 | src/pyblat/extc/src/aux/axt.c            |
| bandExt.c      | Error fetching summary.                                                                                                                                                                                                                                                                              | src/pyblat/extc/src/aux/bandExt.c        |
| base64.c       | This code provides functions to encode and decode strings using the Base64 algorithm . It includes functions to validate the input string , remove whitespace , and optionally return the size of the decoded string . It is copyright ( C ) 2011 The Regents                                        | src/pyblat/extc/src/aux/base64.c         |
| binRange.c     | This code provides functions to handle binning , which helps to restrict attention to parts of a database that contain information about a particular window on a chromosome . It works without modification for chromosome sizes up to 2Gb-1 . It includes functions to add                         | src/pyblat/extc/src/aux/binRange.c       |
| blastOut.c     | Error fetching summary.                                                                                                                                                                                                                                                                              | src/pyblat/extc/src/aux/blastOut.c       |
| cheapcgi.c     | Prompt too long to generate summary.                                                                                                                                                                                                                                                                 | src/pyblat/extc/src/aux/cheapcgi.c       |
| ffSeedExtend.c | Prompt too long to generate summary.                                                                                                                                                                                                                                                                 | src/pyblat/extc/src/aux/ffSeedExtend.c   |
| filePath.c     | This file contains functions for parsing file paths , such as converting ' \ ' to ' / ' , splitting a full path into components , expanding relative paths , and making relative paths . It also contains functions for processing symlinks and include files .                                      | src/pyblat/extc/src/aux/filePath.c       |
| hex.c          | This code provides functions for converting between hexidecimal characters and binary values . It includes functions for converting a nibble , byte , or binary string to hexidecimal characters , as well as functions for converting hexidecimal characters to                                     | src/pyblat/extc/src/aux/hex.c            |
| htmlPage.c     | Prompt too long to generate summary.                                                                                                                                                                                                                                                                 | src/pyblat/extc/src/aux/htmlPage.c       |
| htmshell.c     | Prompt too long to generate summary.                                                                                                                                                                                                                                                                 | src/pyblat/extc/src/aux/htmshell.c       |
| https.c        | Error fetching summary.                                                                                                                                                                                                                                                                              | src/pyblat/extc/src/aux/https.c          |
| intExp.c       | This code is a numerical expression evaluator that can handle both ints and doubles . It includes functions for advancing to the next token , returning a number , handling parenthetical expressions , unary minus , multiplication and division , addition and subtraction                         | src/pyblat/extc/src/aux/intExp.c         |
| internet.c     | Error fetching summary.                                                                                                                                                                                                                                                                              | src/pyblat/extc/src/aux/internet.c       |
| maf.c          | Error fetching summary.                                                                                                                                                                                                                                                                              | src/pyblat/extc/src/aux/maf.c            |
| mafFromAxt.c   | This code provides two functions , mafFromAxtTemp and mafFromAxt , which convert an axt into a maf . mafFromAxtTemp is quicker to run but the axt and maf are not independent                                                                                                                        | src/pyblat/extc/src/aux/mafFromAxt.c     |
| mime.c         | Error fetching summary.                                                                                                                                                                                                                                                                              | src/pyblat/extc/src/aux/mime.c           |
| net.c          | Prompt too long to generate summary.                                                                                                                                                                                                                                                                 | src/pyblat/extc/src/aux/net.c            |
| netlib.c       | Prompt too long to generate summary.                                                                                                                                                                                                                                                                 | src/pyblat/extc/src/aux/netlib.c         |
| ooc.c          | This code provides functions to handle overused N - mers ( tiles ) in genome indexing schemes . It includes functions to set items of tileCounts to maxPat if they are in oocFile , and to mask out simple repeats in                                                                                | src/pyblat/extc/src/aux/ooc.c            |
| patSpace.c     | Error fetching summary.                                                                                                                                                                                                                                                                              | src/pyblat/extc/src/aux/patSpace.c       |
| portimpl.c     | This code provides a set of functions for making the same code run under different web servers . It includes functions for creating temporary files , setting up environment variables , creating directories , and finding paths in directories and subdirectories .                                | src/pyblat/extc/src/aux/portimpl.c       |
| rangeTree.c    | Error fetching summary.                                                                                                                                                                                                                                                                              | src/pyblat/extc/src/aux/rangeTree.c      |
| rbTree.c       | Error fetching summary.                                                                                                                                                                                                                                                                              | src/pyblat/extc/src/aux/rbTree.c         |
| repMask.c      | This code provides functions to link the database and RAM representations of objects from the RepeatMasker .out file . It includes functions to load a row from the repeatMaskOut table into a struct , create a repeatMaskOut from a comma separated string                                         | src/pyblat/extc/src/aux/repMask.c        |
| servBrcMcw.c   | This code defines a webServerSpecific struct for the .brc.mcw.edu server , which includes functions for making temp names , getting the CGI directory , calculating speed , and getting the trash directory .                                                                                        | src/pyblat/extc/src/aux/servBrcMcw.c     |
| servCrunx.c    | This code defines a webServerSpecific struct for a local Linux server , including functions for making temporary names , getting the CGI directory , calculating speed , and getting the trash directory .                                                                                           | src/pyblat/extc/src/aux/servCrunx.c      |
| servcis.c      | This code defines a webServerSpecific struct with various functions and variables related to a Comp Science department web server . It includes functions for making temp names , accessing the CGI directory , determining the speed of the server , and accessing the trash directory . It         | src/pyblat/extc/src/aux/servcis.c        |
| servmsII.c     | This code defines a webServerSpecific struct for the Microsoft II Web Server , which includes functions for making a temp name , getting the CGI directory , getting the trash directory , and getting the speed . It is copyright 2002 Jim Kent , but license is                                    | src/pyblat/extc/src/aux/servmsII.c       |
| servpws.c      | This code defines a webServerSpecific struct for Microsoft Personal Web Server , which includes functions for making temp names , getting the CGI directory , calculating speed , and getting the trash directory .                                                                                  | src/pyblat/extc/src/aux/servpws.c        |
| sqlList.c      | Prompt too long to generate summary.                                                                                                                                                                                                                                                                 | src/pyblat/extc/src/aux/sqlList.c        |
| sqlNum.c       | sqlNum.c provides routines to convert from ascii to integer representation of numbers . It includes functions to convert from strings to unsigned integers , signed integers , unsigned longs , signed longs , floats , and doubles . It also includes functions                                     | src/pyblat/extc/src/aux/sqlNum.c         |
| wildcmp.c      | This code provides functions for wildcard matching , such as ' \* ' and ' ? ' , over a list of strings . It includes functions for case - sensitive matching , as well as functions for matching using ' % ' and ' \_ ' wildcards                                                                    | src/pyblat/extc/src/aux/wildcmp.c        |

</details>

<details closed><summary>Binder</summary>

| File           | Summary                                                                                                                                                                                                                                                                     | Module                                         |
| :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------- |
| .clang-format  | This code disables the formatting of the code and never sorts the includes .                                                                                                                                                                                                | src/pyblat/extc/bindings/binder/.clang-format  |
| \_extc.cpp     | This code is a Python binding module for C++ code . It includes libraries for maps , algorithms , functions , memory , exceptions , and strings . It also includes a pybind11 module and a function for getting modules . It defines a vector of                            | src/pyblat/extc/bindings/binder/\_extc.cpp     |
| \_extc.modules | cppbinding is a library for creating bindings between C++ and other languages . It provides a simple and efficient way to create bindings between C++ and other languages , allowing developers to easily integrate C++ code into their projects . It supports a wide range | src/pyblat/extc/bindings/binder/\_extc.modules |
| \_extc.sources | This code contains five C++ files that are related to the extc library . faToTwoBit.cpp is used to convert a FASTA file to a two - bit file . gfClient.cpp and gfServer.cpp                                                                                                 | src/pyblat/extc/bindings/binder/\_extc.sources |
| faToTwoBit.cpp | This code is a C++ function that binds the faToTwoBit function from the faToTwoBit.hpp header file to the Python programming language . It takes in a vector of strings , a string , and four boolean values as parameters                                                  | src/pyblat/extc/bindings/binder/faToTwoBit.cpp |
| gfClient.cpp   | This code binds the gfClientOption class to the cppbinding module in Python , allowing for the use of the gfClientOption class in Python . It includes functions for setting the hostName , portName , tType , qType                                                        | src/pyblat/extc/bindings/binder/gfClient.cpp   |
| gfServer.cpp   | Error fetching summary.                                                                                                                                                                                                                                                     | src/pyblat/extc/bindings/binder/gfServer.cpp   |
| gfServer_1.cpp | This code is a C++ function that binds the functions pystatusServer , pygetFileList , and pyqueryServer from the gfServer.hpp header file to the cppbinding module in Python . It also declares the holder types                                                            | src/pyblat/extc/bindings/binder/gfServer_1.cpp |

</details>

<details closed><summary>Bindings</summary>

| File           | Summary                                                                                                                                                                                                                                                           | Module                                  |
| :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------- |
| dbg.h          | Error fetching summary.                                                                                                                                                                                                                                           | src/pyblat/extc/bindings/dbg.h          |
| faToTwoBit.cpp | This code is a C++ function that converts files in fasta format to 2 bit format . It checks for duplicate sequence names and can strip off version numbers . It also converts non ACGT characters to N.                                                           | src/pyblat/extc/bindings/faToTwoBit.cpp |
| faToTwoBit.hpp | This code provides a function , faToTwoBit , which converts DNA from fasta to 2bit format . It also provides a function , unknownToN , which replaces unknown characters with N. Both functions are part of the cppbinding namespace                              | src/pyblat/extc/bindings/faToTwoBit.hpp |
| gfClient.cpp   | This code is a C++ implementation of the gfClient program , which is a client for the genomic finding program that produces a .psl file . It includes functions for reading in memory files , building a gfClientOption object , and                              | src/pyblat/extc/bindings/gfClient.cpp   |
| gfClient.hpp   | This code defines the gfClientOption struct , which contains variables that can be overridden by command line , and the pygfClient and read_inmem_file functions . The gfClientOption struct contains variables such as hostName                                  | src/pyblat/extc/bindings/gfClient.hpp   |
| gfServer.cpp   | Prompt too long to generate summary.                                                                                                                                                                                                                              | src/pyblat/extc/bindings/gfServer.cpp   |
| gfServer.hpp   | This code provides functions for a genoFind server , which is used to search for sequences in a database . It includes functions for building an index , starting and stopping the server , querying the server , and logging usage statistics . It also includes | src/pyblat/extc/bindings/gfServer.hpp   |

</details>

<details closed><summary>Core</summary>

| File          | Summary                                                                                                                                                                                                                                                                                          | Module                                     |
| :------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------- |
| aliType.h     | This code defines various types of sequence alignment and stringency levels for a genoFind program . It includes enum types for gfType ( DNA , RNA , Protein , etc . ) and ffStringency ( Exact , CDNA , Tight ,                                                                                 | src/pyblat/extc/include/core/aliType.h     |
| axt.h         | This code contains routines to read and write alignments in the AXT format , which is a simple alignment format with four lines per alignment . It also contains code for simple DNA alignment scoring schemes . It is copyright 2002 Jim Kent , but license is                                  | src/pyblat/extc/include/core/axt.h         |
| bPlusTree.h   | This code implements a B+ Tree index file for disk - based storage . It provides functions to create a B+ Tree from a sorted list , lookup a value given a key , and traverse the tree . It also contains the layout of the file                                                                 | src/pyblat/extc/include/core/bPlusTree.h   |
| binRange.h    | This code provides functions to handle binning , which helps to restrict attention to parts of a database that contain information about a particular window on a chromosome . It includes functions to add and remove items from a binKeeper , find items in a bin                              | src/pyblat/extc/include/core/binRange.h    |
| bits.h        | This code provides functions to handle operations on arrays of bits , such as allocating , resizing , cloning , setting , clearing , and counting bits . It also provides functions to perform bitwise operations such as AND , OR , and XOR ,                                                   | src/pyblat/extc/include/core/bits.h        |
| chain.h       | This code provides functions for creating and manipulating chain objects , which are pairwise alignments that can include gaps in both sequences at once . It is suitable for cross species genomic comparisons , similar to psl . It includes functions for sorting , writing ,                 | src/pyblat/extc/include/core/chain.h       |
| common.h      | Prompt too long to generate summary.                                                                                                                                                                                                                                                             | src/pyblat/extc/include/core/common.h      |
| dlist.h       | This file contains headers for generic doubly - linked list routines . It provides functions to create , initialize , reset , and free doubly - linked lists , as well as functions to add and remove nodes from the list , sort the list , and                                                  | src/pyblat/extc/include/core/dlist.h       |
| dnaseq.h      | This code provides functions to manage DNA sequences , including creating , cloning , and freeing them , as well as translating them into proteins , and creating a hash of the sequences keyed by name . It also provides functions to determine if a sequence is DNA                           | src/pyblat/extc/include/core/dnaseq.h      |
| dnautil.h     | This code provides functions for working with DNA and amino acids , such as converting between upper and lower case , filtering out non - DNA characters , and calculating the reverse complement of DNA . It also includes functions for calculating the score of a DNA or amino                | src/pyblat/extc/include/core/dnautil.h     |
| dystring.h    | This code provides functions for creating and manipulating a dynamically resizing string , which can be used for formatted output . It includes functions for appending strings , characters , and variables , as well as for quoting strings , resizing strings , and freeing strings           | src/pyblat/extc/include/core/dystring.h    |
| errAbort.h    | ErrAbort.h is a library that provides an error handler and warning message printer stack . It allows users to customize the behavior of the error handler and warning message printer , and provides functions to abort , warn , and set handlers . It                                           | src/pyblat/extc/include/core/errAbort.h    |
| errCatch.h    | errCatch is a library that helps catch errors so that errAborts are not fatal and warns do not necessarily get printed immediately . It provides a way to catch errors and warnings , and then handle them accordingly . It also provides a way to                                               | src/pyblat/extc/include/core/errCatch.h    |
| fa.h          | This file contains routines for reading and writing fasta format sequence files . It includes functions for reading a single sequence , reading all sequences in a file , and writing a single sequence or all sequences in a list to a file . It also includes functions                        | src/pyblat/extc/include/core/fa.h          |
| fuzzyFind.h   | This file is a header file for the fuzzyFind DNA sequence aligner . It contains functions for finding and scoring alignments between a needle and haystack DNA sequence , as well as functions for manipulating and displaying the alignments . It also contains a                               | src/pyblat/extc/include/core/fuzzyFind.h   |
| genoFind.h    | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/include/core/genoFind.h    |
| gfClientLib.h | This code provides functions for genoFind clients to read and manipulate files in .2bit ,.nib , and .fa formats , as well as create a list of dnaSeqs and unmask them .                                                                                                                          | src/pyblat/extc/include/core/gfClientLib.h |
| gfInternal.h  | This code contains functions related to the gfRange struct , which is used to store information about a range of bases found by genoFind . The functions include gfRangeFree , gfRangeFreeList , gfRangeCmpTarget                                                                                | src/pyblat/extc/include/core/gfInternal.h  |
| hash.h        | This code provides functions to create and manipulate hash tables , which are data structures that provide name / value pairs . It includes functions to add elements to a hash , retrieve a named element , iterate through all elements in a hash , and free up                                | src/pyblat/extc/include/core/hash.h        |
| linefile.h    | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/include/core/linefile.h    |
| localmem.h    | LocalMem.h provides a set of routines for allocating and disposing of small to medium size pieces of memory . It includes functions for creating a local memory pool , allocating memory from the pool , adjusting memory size , cloning memory blocks ,                                         | src/pyblat/extc/include/core/localmem.h    |
| maf.h         | This code provides functions for reading , writing , and manipulating multiple alignment format ( MAF ) files . It includes functions for opening and closing MAF files , reading and writing MAF alignments , finding components of MAF alignments , and manipulating                           | src/pyblat/extc/include/core/maf.h         |
| memalloc.h    | This code provides functions to allow the user to control memory allocation and deallocation , as well as debug scrambled heaps . It includes functions to push and pop memory handlers , set the default memory handler , push a careful memory handler , check the                             | src/pyblat/extc/include/core/memalloc.h    |
| net.h         | This file provides functions for wrapping around network communications , such as connecting to a server , sending and receiving strings , and parsing URLs . It also provides functions for setting timeouts , catching broken pipes , and reading and writing data from / to a socket          | src/pyblat/extc/include/core/net.h         |
| netlib.h      | This file provides functions to wrap around network communications , such as connecting to a server , sending and receiving strings , and parsing URLs . It also provides functions to read and write data from a socket , and to set timeouts for read and write operations                     | src/pyblat/extc/include/core/netlib.h      |
| nib.h         | This file provides an interface to nucleotides stored 4 bits per base , allowing for room for N. It contains functions for opening and verifying a file , loading parts of a file , writing a file , and parsing a file name . It also                                                           | src/pyblat/extc/include/core/nib.h         |
| obscure.h     | This header file contains a collection of functions that are useful but not commonly used . It includes functions for incrementing a 32 - bit value on disk , counting the number of digits in a number , printing out a long number with commas , formatting                                    | src/pyblat/extc/include/core/obscure.h     |
| ooc.h         | This code provides functions to handle overused N - mers ( tiles ) in genome indexing schemes . It includes functions to set items of tileCounts to maxPat if they are in oocFile , and to mask out simple repeats in                                                                            | src/pyblat/extc/include/core/ooc.h         |
| options.h     | This code provides functions for processing command line options into a hash . It includes functions for validating options , returning values for different types , and checking if an option exists . It also includes functions for parsing options into a hash and freeing the hash .        | src/pyblat/extc/include/core/options.h     |
| patSpace.h    | PatSpace is a homology finding algorithm that occurs mostly in pattern space . It is used to find occurrences of DNA in a pattern space and is copyright 2000 Jim Kent . It is free to use for all purposes . It requires a sequence array ,                                                     | src/pyblat/extc/include/core/patSpace.h    |
| pipeline.h    | This code creates a process pipeline that can be used for reading or writing , avoiding many of the obscure problems associated with system ( ) and popen ( ) . It allows for the specification of a file at the other end of the pipeline , as well as the                                      | src/pyblat/extc/include/core/pipeline.h    |
| portable.h    | This header file provides wrappers around functions that vary from server to server and operating system to operating system . It includes functions for listing files in a directory , creating directories , making and renaming files , getting the current directory , getting the host name | src/pyblat/extc/include/core/portable.h    |
| psl.h         | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/include/core/psl.h         |
| rangeTree.h   | This module is a way of keeping track of non - overlapping ranges ( half - open intervals ) using a self - balancing rbTree code . It is useful in place of a bitmap when the total number of ranges is significantly                                                                            | src/pyblat/extc/include/core/rangeTree.h   |
| repMask.h     | This header file provides functions for loading , freeing , and outputting data from the Repeat Masker Out format , which is used to store information about repeat elements in a genome . It also provides a function for opening a Repeat Masker Out file .                                    | src/pyblat/extc/include/core/repMask.h     |
| sig.h         | This file contains signatures that start various binary files , such as binary alignment files , gene files , and index files . It is copyright 2000 Jim Kent , but license is granted for all use - public , private or commercial . It contains signatures for binary                          | src/pyblat/extc/include/core/sig.h         |
| sqlList.h     | This code provides functions for processing comma separated lists , such as converting them to arrays , converting arrays to strings , and parsing and printing enumerated and set column values . It is copyright 2002 Jim Kent , but license is granted for all use - public                   | src/pyblat/extc/include/core/sqlList.h     |
| sqlNum.h      | sqlNum.h is a file containing routines to convert from ascii to unsigned / integer values more quickly than atoi . It was developed for use with SQL databases , and is used by AutoSQL and other parsers in the source tree                                                                     | src/pyblat/extc/include/core/sqlNum.h      |
| supStitch.h   | SupStitch is a C library used to stitch together a bundle of ffAli alignments that share a common query and target sequence into larger alignments . It is commonly used when the query sequence was broken up into overlapping blocks in the initial alignment                                  | src/pyblat/extc/include/core/supStitch.h   |
| trans3.h      | This code defines a trans3 structure which contains a sequence and three translated reading frames . It also provides functions to create , free , and find trans3 structures in a t3Hash , as well as functions to calculate offsets and frames .                                               | src/pyblat/extc/include/core/trans3.h      |
| twoBit.h      | This code provides functions for reading and writing DNA sequences represented as two bits per pixel , along with associated list of regions containing N 's and masked regions . It includes functions for reading and writing .2bit files , reading parts of sequences , and converting        | src/pyblat/extc/include/core/twoBit.h      |
| udc.h         | UDC is a caching system that keeps blocks of data fetched from URLs in sparse local files for quick use the next time the data is needed . It simplifies caching by only allowing reads , not writes . The cache directory is constructed from the                                               | src/pyblat/extc/include/core/udc.h         |
| verbose.h     | This header file provides functions for writing out status messages to stderr according to the current verbosity level . It also provides functions for setting the verbosity level , setting the log file , and setting the verbosity level for a CGI .                                         | src/pyblat/extc/include/core/verbose.h     |
| aliType.c     | aliType.h provides definitions for the type of alignment , including functions to return a string representing the type and to return the type from a string .                                                                                                                                   | src/pyblat/extc/src/core/aliType.c         |
| bPlusTree.c   | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/bPlusTree.c       |
| bits.c        | This file contains functions to handle operations on arrays of bits , such as setting , clearing , and counting bits . It also includes functions to allocate , reallocate , and free memory for bit arrays . It is copyright 2002 Jim Kent , but license                                        | src/pyblat/extc/src/core/bits.c            |
| chain.c       | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/chain.c           |
| common.c      | Prompt too long to generate summary.                                                                                                                                                                                                                                                             | src/pyblat/extc/src/core/common.c          |
| dlist.c       | struct dlNode _ dlFindVal(struct dlList _ list , void \* val ,                                                                                                                                                                                                                                   | src/pyblat/extc/src/core/dlist.c           |
|               | int ( _ compare)(const void _ elem1 , const void \* elem2 ) )                                                                                                                                                                                                                                    |                                            |
|               | / \* Return node on list if any                                                                                                                                                                                                                                                                  |                                            |
| dnaseq.c      | This code provides functions to manage DNA sequences , including creating , cloning , freeing , and translating them . It also provides functions to determine if a sequence is lower case , DNA , or protein , and to create a mask from an upper case sequence .                               | src/pyblat/extc/src/core/dnaseq.c          |
| dnautil.c     | Prompt too long to generate summary.                                                                                                                                                                                                                                                             | src/pyblat/extc/src/core/dnautil.c         |
| dystring.c    | DyString : A library of functions for creating and manipulating dynamically resizing strings . It includes functions for creating a new dynamic string , freeing a dynamic string , appending characters and strings to the end of a dynamic string , expanding the buffer size                  | src/pyblat/extc/src/core/dystring.c        |
| errAbort.c    | Summary : errAbort.c is a file that provides an error handler for programs . It maintains two stacks - a warning message printer stack , and an " abort handler " stack . It provides functions for setting and reverting to old                                                                 | src/pyblat/extc/src/core/errAbort.c        |
| errCatch.c    | This code provides a structure for catching errors and warnings in a program , allowing them to be handled without causing the program to abort . It includes functions for creating and freeing the errCatch structure , pushing and popping handlers , and finishing up error catching         | src/pyblat/extc/src/core/errCatch.c        |
| fa.c          | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/fa.c              |
| ffAli.c       | This file contains utility functions for working with ffAlis , which are data structures used to represent alignments between two DNA sequences . The functions include ffFreeAli ( ) , which disposes of memory gotten from fuzzyFind ( ) , ffOneIntronOrient                                   | src/pyblat/extc/src/core/ffAli.c           |
| ffAliHelp.c   | ffAliHelp is a set of helper routines for producing ffAli type alignments . It includes functions for concatenating , sorting , merging , and expanding alignments , as well as functions for scoring and sliding introns .                                                                      | src/pyblat/extc/src/core/ffAliHelp.c       |
| ffScore.c     | ffScore is a C program that scores fuzzyFind ( ffAli ) alignments . It includes functions to calculate gap penalties , score matches , and score alignments based on the given stringency .                                                                                                      | src/pyblat/extc/src/core/ffScore.c         |
| fuzzyFind.c   | Prompt too long to generate summary.                                                                                                                                                                                                                                                             | src/pyblat/extc/src/core/fuzzyFind.c       |
| genoFind.c    | Prompt too long to generate summary.                                                                                                                                                                                                                                                             | src/pyblat/extc/src/core/genoFind.c        |
| gfBlatLib.c   | Prompt too long to generate summary.                                                                                                                                                                                                                                                             | src/pyblat/extc/src/core/gfBlatLib.c       |
| gfClientLib.c | This code provides functions for loading and masking DNA sequences from .2bit ,.nib ,.fa ,.Z ,.gz , and .bz2 files . It includes functions for reading a list of filenames , unm                                                                                                                 | src/pyblat/extc/src/core/gfClientLib.c     |
| gfInternal.c  | This code provides functions to expand a range and load a cached target sequence from a NIB or 2bit file . It also provides a function to extract the sequence name and optionally the file name from a given spec .                                                                             | src/pyblat/extc/src/core/gfInternal.c      |
| gfOut.c       | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/gfOut.c           |
| hash.c        | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/hash.c            |
| kxTok.c       | KxTok is a quick little tokenizer for stuff first loaded into memory . It was originally developed for the " Key eXpression " evaluator . It can tokenize strings , punctuation , and operators , and can also be                                                                                | src/pyblat/extc/src/core/kxTok.c           |
| linefile.c    | Prompt too long to generate summary.                                                                                                                                                                                                                                                             | src/pyblat/extc/src/core/linefile.c        |
| localmem.c    | LocalMem.c is a file containing routines for allocating and managing memory in a local memory pool . It includes functions for allocating memory , cloning strings and memory blocks , and adding references to a list . It also includes functions for calculating the                          | src/pyblat/extc/src/core/localmem.c        |
| memalloc.c    | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/memalloc.c        |
| nib.c         | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/nib.c             |
| obscure.c     | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/obscure.c         |
| options.c     | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/options.c         |
| osunix.c      | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/osunix.c          |
| pipeline.c    | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/pipeline.c        |
| psl.c         | Prompt too long to generate summary.                                                                                                                                                                                                                                                             | src/pyblat/extc/src/core/psl.c             |
| servcl.c      | This code creates a web server for command line execution , with functions for creating temporary files , returning the path for CGI executables , calculating speed , and returning the path for temporary files .                                                                              | src/pyblat/extc/src/core/servcl.c          |
| supStitch.c   | Error fetching summary.                                                                                                                                                                                                                                                                          | src/pyblat/extc/src/core/supStitch.c       |
| trans3.c      | Trans3 : trans3New ( ) is a function that creates a new set of translated sequences from a given DNA sequence . It includes functions to free the trans3 structure , find a trans3 in a hash , offset a peptide in the context                                                                   | src/pyblat/extc/src/core/trans3.c          |
| twoBit.c      | Prompt too long to generate summary.                                                                                                                                                                                                                                                             | src/pyblat/extc/src/core/twoBit.c          |
| udc.c         | Prompt too long to generate summary.                                                                                                                                                                                                                                                             | src/pyblat/extc/src/core/udc.c             |
| verbose.c     | This code provides functions for writing out status messages according to the current verbosity level . It includes functions for setting the verbosity level , setting the log file , and printing messages with a given verbosity level . It also includes functions for printing messages     | src/pyblat/extc/src/core/verbose.c         |

</details>

<details closed><summary>Extc</summary>

| File         | Summary                                                                                                                                                                                                                              | Module                       |
| :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------- |
| blat.c       | Error fetching summary.                                                                                                                                                                                                              | src/pyblat/extc/blat.c       |
| faToTwoBit.c | This code converts DNA from fasta to 2bit format . It takes in multiple fasta files and outputs a single 2bit file . It has options to ignore lower - case masking , strip off version numbers , and ignore duplicate sequences . It | src/pyblat/extc/faToTwoBit.c |
| gfClient.c   | gfClient is a client for the genomic finding program that produces a .psl file . It takes in a fasta format file and produces a .psl file with the output . It has various options to control the output format , query              | src/pyblat/extc/gfClient.c   |
| gfServer.c   | Prompt too long to generate summary.                                                                                                                                                                                                 | src/pyblat/extc/gfServer.c   |

</details>

<details closed><summary>Net</summary>

| File    | Summary                                                                                                                                                                                                                                  | Module                              |
| :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------- |
| gfNet.h | This code is a Python program that takes a list of numbers and prints out the sum of all the numbers in the list . It begins by initializing a variable to 0 , then iterates through the list of numbers , adding each number to         | src/pyblat/extc/include/net/gfNet.h |
| log.h   | This code provides logging functions for servers , allowing them to log to a file and/or syslog . It includes functions to open syslog and file logging , set the minimum priority to log , and log errors , warnings , info , and debug | src/pyblat/extc/include/net/log.h   |
| gfNet.c | This code provides functions for setting up a network connection to a BLAT / iPCR server , as well as functions for beginning and ending requests , and disconnecting from the server .                                                  | src/pyblat/extc/src/net/gfNet.c     |
| log.c   | Summary : log.c is a logging program for servers that can log to a file and/or syslog . It includes functions to open syslog and file logging , set the minimum priority to log , and log messages with different levels of priority     | src/pyblat/extc/src/net/log.c       |

</details>

<details closed><summary>Pyblat</summary>

| File      | Summary                                                                                                                                                                                                                          | Module               |
| :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------- |
| py.typed  | This code is a Python program that takes a list of numbers and prints out the sum of all the numbers in the list . It begins by initializing a variable to 0 , then iterates through the list of numbers , adding each number to | src/pyblat/py.typed  |
| server.py | This code creates a Server class that can be used to start , stop , and query a server . It also contains functions to convert a file to two bit , get the status of the server , and get a list of files .                      | src/pyblat/server.py |

</details>

<details closed><summary>Root</summary>

| File             | Summary                                                                                                                                                                                                                                 | Module           |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------- |
| .clang-format    | This code is a Cpp style configuration based on the Google style guide . It sets rules for Access Modifier Offset , Alignments , Brace Wrapping , Break Before Binary Operators , Column Limit , Indent Width , Insert Tra              | .clang-format    |
| all_includes.hpp | This code includes a variety of libraries for C++ programming , such as the < algorithm > , < chrono > , < cstring > , < ctime > , < faToTwoBit.hpp > , < gfClient.hpp > , <                                                            | all_includes.hpp |
| build.py         | This code is used to build a C++ extension for a Python package called pyblat . It checks the environment for a conda environment , removes environment variables , checks the htslib path , and gets the htslib library and include    | build.py         |
| tasks.py         | This code contains functions to start , stop , and query a server using the pyblat and extc libraries . It also contains functions to run commands using the invoke library , and to read and write data using the asyncio and simdjson | tasks.py         |

</details>
<hr />

## 🚀 Getting Started

### ✅ Prerequisites

Before you begin, ensure that you have the following prerequisites installed:

> `[📌  INSERT-PROJECT-PREREQUISITES]`

### 💻 Installation

1. Clone the pyblat repository:

```sh
git clone https://github.com/cauliyang/pyblat.git
```

2. Change to the project directory:

```sh
cd pyblat
```

3. Install the dependencies:

```sh
poetry install .
```

### 🤖 Using pyblat

```sh
./myapp
```

### 🧪 Running Tests

```sh
#run tests
```

<hr />

## 🛠 Future Development

- [x] [📌 COMPLETED-TASK]
- [ ] [📌 INSERT-TASK]
- [ ] [📌 INSERT-TASK]

---

## 🤝 Contributing

Contributions are always welcome! Please follow these steps:

1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).

```sh
git checkout -b new-feature-branch
```

4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.

```sh
git commit -m 'Implemented new feature.'
```

6. Push your changes to your forked repository on GitHub using the following command

```sh
git push origin new-feature-branch
```

7. Create a pull request to the original repository.
   Open a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.
   The project maintainers will review your changes and provide feedback or merge them into the main branch.

---

## 🪪 License

This project is licensed under the `[📌  INSERT-LICENSE-TYPE]` License. See the [LICENSE](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository) file for additional info.

---

## 🙏 Acknowledgments

[📌 INSERT-DESCRIPTION]

---
