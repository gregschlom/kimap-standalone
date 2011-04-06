This is the minimal set of Boost include files required by KMime and KIMAP.
It contains <config>, <shared_ptr>, and <concept_check> headers from Boost 1.37

This set was generated with the bcp tool:
  cd [path to boost_1.37]
  bcp config shared_ptr concept_check [output path]
  
The bcp utility is a tool for extracting subsets of Boost:
http://www.boost.org/doc/libs/1_37_0/tools/bcp/bcp.html