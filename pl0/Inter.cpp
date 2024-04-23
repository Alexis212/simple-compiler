#include <iostream>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <string>
#include <stack>
#include <cmath>
#include <iomanip>
using namespace std;

struct iden {
  string nom;
  char cla;
  char tip;
  int di1;
  int di2;
  string apv[1000];
};
struct codigo {
   string mnemo;
   string dir1;
   string dir2;
};
codigo prgm[10000];
iden tabsim[10000];
int coni=0;
int conp=0;
const int ERR=-1;
bool flg=false;
stack<string> pila;
ostream& operator <<( ostream& sale, stack<string> s) {
    stack<string> paux;
    string sal="";
    while ( s.size()> 1 ) {
        sal = ", " + s.top() + sal;
        paux.push( s.top() );
        s.pop();
    }
    sal = "[" + s.top() + sal + "]";
    s.pop();
    while( !paux.empty() ) {
       s.push( paux.top() );
       paux.pop();
    }
    sale << sal;
    //sale << "";
    return sale;
}

void tokeniza(string lin) {
    if( lin == "@") flg = true;
    if( !flg ) {
        int idx=0, con=0;
        string cad="";
        char c;
        while( (c = lin[idx++]) != '#' ) {
            if( c != ',') cad += c;
            else {
               switch( con ) {
                 case 0: tabsim[coni].nom = cad; break;
                 case 1: tabsim[coni].cla = cad[0]; break;
                 case 2: tabsim[coni].tip = cad[0]; break;
                 case 3: tabsim[coni].di1 = atoi( cad.c_str() );
                         break;
                 case 4: tabsim[coni++].di2 = atoi( cad.c_str() );
                         break;
               }
               cad="";
               con++;
            }
        }
    }
    else {
        int idx=0, con=0;
        string cad="";
        char c;
        while( (c = lin[idx++]) != '\0' ) {
            if( c == ' ' && con == 0 ) {
                conp = atoi( cad.c_str() );
                con++;
                cad="";
            }
            else if( c == ' ' && con == 1) {
               prgm[conp].mnemo = cad;
               con++;
               cad="";
            } else if( c == ',' && con == 2) {
               prgm[conp].dir1 = cad;
               con++;
               cad="";
            }
            else if( c != 32 && con == 3) cad += c;
            else if( con != 3) cad += c;
        }
        prgm[conp].dir2=cad;
    }
}
void leeArch(string entrada) {
   ifstream fuente( entrada );
   string linea;
   if( fuente.is_open() ) {
      while( getline( fuente, linea) ) {
         tokeniza( linea );
      }
      fuente.close();
   }
}
int getIden( string id ) {
    for(int i=0; i < coni; i++)
        if(tabsim[i].nom == id ) return i;
    return ERR;
}
void exec() {
    int pc = getIden( "_P" );
    if( pc >= 0 ) pc = tabsim[pc].di1;
    while ( pc >= 0 && pc <= conp ) {
        /*cout << pc << " "
             << prgm[pc].mnemo << " "
             << prgm[pc].dir1 << ","
             << prgm[pc].dir2 << endl; */
        if( prgm[pc].mnemo == "OPR") {
            if( prgm[pc].dir1 == "0" &&
                prgm[pc].dir2 == "0") break;
            else if( prgm[pc].dir1 == "0" &&
                     prgm[pc].dir2 == "1") {
                pc = atoi( pila.top().c_str() ) - 1;
                pila.pop();
            }
            else if( prgm[pc].dir2 == "18") {
                system("cls");
            }
            else if( prgm[pc].dir2 == "19") {
                int idx = getIden( prgm[pc].dir1 );
                if( idx >= 0) {
                    string entrada;
                    getline(cin, entrada);
                    if( tabsim[idx].di1 == 0 &&
                        tabsim[idx].di2 == 0)
                            tabsim[idx].apv[0] = entrada;
                }
            }
            else if( prgm[pc].dir1 == "0" &&
                     prgm[pc].dir2 == "20") {
                if (pila.top() == "V") cout << "verdadero";
                else 
                   if (pila.top() == "F") cout << "falso";
                   else cout << pila.top();
                pila.pop();
            }
            else if( prgm[pc].dir1 == "0" &&
                     prgm[pc].dir2 == "21") {
                if (pila.top() == "V") cout << "verdadero" << endl;
                else if (pila.top() == "F") cout << "falso" << endl;
                else cout << pila.top() << endl;
                pila.pop();
            }
            else if( prgm[pc].dir1 == "0") {
                int op = atoi( prgm[pc].dir2.c_str());
                if( op > 1 && op < 8) {
                    double opd = strtod( pila.top().c_str(), 0 );
                    pila.pop();
                    double opi = strtod( pila.top().c_str(), 0 );
                    pila.pop();
                    double res;
                    ostringstream cnv;
                    switch( op ) {
                       case 2: res = opi + opd;
                               break;
                       case 3: res = opi - opd;
                               break;
                       case 4: res = opi * opd;
                               break;
                       case 5: res = opi / opd;
                               break;
                       case 6: res = (int) opi % (int) opd;
                               break;
                       case 7: res = pow(opi, opd);
                               break;
                    }
                    cnv << setprecision(500) << res;
                    pila.push( cnv.str() );
                    //cout << pila << endl;
                }
                else if( op > 8 && op < 15 ) {
                    double opd = strtod( pila.top().c_str(), 0 );
                    pila.pop();
                    double opi = strtod( pila.top().c_str(), 0 );
                    pila.pop();
                    bool res;
                    switch( op ) {
                       case  9: res = opi < opd;
                               break;
                       case 10: res = opi > opd;
                               break;
                       case 11: res = opi <= opd;
                               break;
                       case 12: res = opi >= opd;
                               break;
                       case 13: res = opi != opd;
                               break;
                       case 14: res = opi == opd;
                               break;
                    }
                    string rs;
                    if ( res ) rs = "V";
                    else rs = "F";
                    pila.push( rs );
                    //cout << pila << endl;
                }
            }
        }
        else if( prgm[pc].mnemo == "LIT" ) {
            string val = prgm[pc].dir1;
            if( val[0] == '"')
                pila.push( val.substr(1,val.size() - 2) );
            else pila.push( val );
            //cout << pila << endl;
        }
        else if( prgm[pc].mnemo == "JMP" ) {
            string dir2 = prgm[pc].dir2;
            int dir;
            if( dir2[0] == '_') {
                int idx = getIden( dir2 );
                if( idx >=0 ) dir = tabsim[idx].di1;
            }
            else {
                dir = atoi( dir2.c_str() );
            }
            pc = dir - 1;
        }
        else if( prgm[pc].mnemo == "JMC" ) {
            string val = pila.top(), cond = prgm[pc].dir1,
                   dir2 = prgm[pc].dir2;
            int dir;
            pila.pop();
            if( dir2[0] == '_') {
                int idx = getIden( dir2 );
                if( idx >=0 ) dir = tabsim[idx].di1;
            }
            else {
                dir = atoi( dir2.c_str() );
            }
            if( val == cond ) pc = dir - 1;
        }
        else if( prgm[pc].mnemo == "LOD" ) {
            int idx = getIden( prgm[pc].dir1 );
            if( idx >= 0 ) {
                if( tabsim[idx].di1 == 0 &&
                    tabsim[idx].di2 == 0 &&
                    tabsim[idx].nom[0] != '_') {
                    pila.push(tabsim[idx].apv[0]);
                    //cout << pila << endl;
                }
                else if( tabsim[idx].nom[0] == '_' ) {
                    ostringstream cnv;
                    cnv << tabsim[idx].di1;
                    pila.push( cnv.str() );
                    //cout << pila << endl;
                }
                else if( tabsim[idx].cla == 'F') {
                    pila.push(tabsim[idx].apv[0]);
                    //cout << pila << endl;
                }
                else if( tabsim[idx].cla == 'V' ||
                         tabsim[idx].cla == 'L' ||
                         tabsim[idx].cla == 'R' ) {
                    if( tabsim[idx].di1 > 0 && tabsim[idx].di2 > 0) {
                        int i, j, desp;
                        pila.pop();
                        j = atoi( pila.top().c_str());
                        pila.pop();
                        i = atoi( pila.top().c_str() );
                        pila.pop();
                        desp = i * tabsim[idx].di2 + 1;
                        pila.push( tabsim[idx].apv[j + desp] );
                        //cout << pila << endl;
                    }
                    else if( tabsim[idx].di1 > 0) {
                        int i = atoi( pila.top().c_str() ); pila.pop();
                        pila.push( tabsim[idx].apv[i + 1] );
                        //cout << pila << endl;
                    }
                }
            }
        }
        else if( prgm[pc].mnemo == "STO" ) {
            int idx = getIden( prgm[pc].dir2 );
            if( idx >= 0 ) {
                if( tabsim[idx].di1 == 0 &&
                    tabsim[idx].di2 == 0 ) {
                    tabsim[idx].apv[0] = pila.top();
                    pila.pop();
                    //cout << pila << endl;
                }
                else if( tabsim[idx].cla == 'F' ) {
                    tabsim[idx].apv[0] = pila.top();
                    pila.pop();
                    //cout << pila << endl;
                }
                else if( tabsim[idx].cla == 'V' ||
                         tabsim[idx].cla == 'L' ||
                         tabsim[idx].cla == 'R' ) {
                    if( tabsim[idx].di1 > 0 && tabsim[idx].di2 > 0) {
                        int i, j, desp;
                        string val = pila.top();
                        pila.pop();
                        j = atoi( pila.top().c_str() );
                        pila.pop();
                        i = atoi( pila.top().c_str() );
                        pila.pop();
                        desp = i * tabsim[idx].di2 + 1;
                        tabsim[idx].apv[j + desp] = val;
                    }
                    else if( tabsim[idx].di1 > 0) {
                        string val = pila.top();
                        pila.pop();
                        int i = atoi( pila.top().c_str()) ;
                        pila.pop();
                        tabsim[idx].apv[ i + 1 ] = val;
                    }
                }
            }
        }
        else if( prgm[pc].mnemo == "CAL" ) {
            int idx = getIden( prgm[pc].dir1 );
            if ( idx >= 0) {
               pc = tabsim[idx].di1 - 1;
            }
        }
        pc++;
    }
}
int main(int argc, char* argv[]) {
    if( argc > 1) {
       leeArch( string(argv[1]) + ".eje" );
       for(int i=0; i < coni; i++)
          cout << tabsim[i].nom << ","
               << tabsim[i].cla << ","
               << tabsim[i].tip << ","
               << tabsim[i].di1 << ","
               << tabsim[i].di2 << ",#," << endl;
       cout << "@" << endl;
       for(int i=1; i <= conp; i++)
          cout << i << " "
               << prgm[i].mnemo << " "
               << prgm[i].dir1 << ", "
               << prgm[i].dir2 << endl;
      cout << endl << endl
           << "[ Ejecutando " << argv[1] << ".eje" << " ]"
           << endl << endl;

       exec();
    }
}
