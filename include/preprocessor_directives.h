// usefull constants
#ifndef N_VERTICES
#define N_VERTICES 4
#endif

#ifndef N_COORDINATES
#define N_COORDINATES 2
#endif

#ifndef GIT_COMMIT 
#define GIT_COMMIT  "74dc7039"
#endif

// shortcuts for some instructions
#ifndef PRINT_DEBUG
#define PRINT_DEBUG(p,s,c) std::cout << "[" << GIT_COMMIT << "]"               \
                                     << "[" << __FILE__ << "]"                 \
                                     << "[" << __PRETTY_FUNCTION__ << "]"      \
                                     << "[" << __LINE__ << "]"                 \
                                     << "\tpixel " << p                        \
                                     << "\tsegment " << s                      \
                                     << ":\tif " << c << std::endl;
#endif 

#ifndef PRINT_VERTEX
#define PRINT_VERTEX(p1,p2) std::cout << "(" << p1[0] << ";" << p1[1] << ")"   \
                                      << " "                                   \
                                      << "(" << p2[0] << ";" << p2[1] << ")";
#endif 

#ifndef PRINT_COORDINATES
#define PRINT_COORDINATES(x,y) std::cout << "(" << x << ";" << y << ")" << " " \
                                         << std::endl;
#endif