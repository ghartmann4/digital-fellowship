
//This code takes input from the user for three pitch classes and one modulus 
// number, then calculates the set class of the pitch classes and whether
// there exist any other members of that set class parsimoniously related to 
// it in the given pitch-class universe (mod c)
#include <iostream>
#include <cstring>
using namespace std;

// define a function to crash to crash the program for bad input
int inputtest( string in_s ) // returns 1 if the input is bad
{ // inputtest
// end the program if there's bad input
if( (in_s == "") || (in_s == "crash") || (in_s == "no") || (in_s == "n") ) 
	{ // * 
	cout << "ENDING PROGRAM" << endl;
	return 1;
	} // *
return 0;
} // inputtest





string getmodulusnumber( void ) // have the user input the modulus number
{ // getmodulusnumber
string modulusnumber;
int trynumber = 0;
int error = 0;
cout << "enter a modulus number" << endl;
while (true) { // *
	trynumber++ ; 
	if (trynumber > 11) // program gives up
		{ // **
		cout << "ERROR: IMPROPER INPUT" << endl;
		return "crash"; // crashes program
		} // **
	error = 0 ;
	cin >> modulusnumber;
	if (modulusnumber == "0") // bad
		{ // ** 
		cout << "ERROR: MODULUS NUMBER CANNOT BE ZERO" << endl;
		error = 1;
		} // **
	if ( inputtest(modulusnumber) != 0 ) { break ;} // this case causes the program to crash
	if ( error == 0) { break ;} // this means the inputted modulusnumber is okay
	cout << "Enter another modulus number" << endl;
	} // * 
return modulusnumber;
} // getmodulusnumber



const unsigned int nmembers = 3; // number of members in a setclass

// this function sorts an array of integers, lists them from least to greatest
void sortlist( int list[], int length ) {
     int i = 1;
     while ( i < length ) {
           for ( int j = i; list[j - 1] > list[j]; j-- ) {
                int temp = list[j - 1];
                list[j - 1] = list[j];
                list[j] = temp;
              } 
              i++;
           }
}

// define a setclass as a c++ class      http://www.cplusplus.com/doc/tutorial/classes/
class setclass{
	int nlist[nmembers]; // an array of the for {n1,n2,n3}
	int nm; // the modulus number
	public:
	int getentry( int );
	int score( void );
	void print( void ); // couts the setclass -- displays it on the screen
	void print( string );
	setclass( int, int, int, int ); // constructor
	setclass(); // constructor
	setclass reduce( void ); 
	void sort( void );
	setclass reducechoose( void ); // reduces the setclass to prime form for all orders of the members
	setclass invert( void );
	void setentry( int, int );
	void increment( int );
	int pscore( void );
	setclass primeform( void );
	} ;
	
int setclass::score() { return nlist[0] + nlist[1] + nlist[2] ; }

int setclass::getentry( int in_n ) {
	if ( in_n==3 ) { return nm; }
	return nlist[in_n];
	}
	
// return the set with the lowest score or with the smallest left entries
setclass compare( setclass in_c1, setclass in_c2) {
	if ( in_c1.score() < in_c2.score() ) {return in_c1 ;}
	if ( in_c2.score() < in_c1.score() ) { return in_c2 ;}
// if the code makes it to this point, in_c1.score() = in_c2.score()
	if ( in_c1.getentry(0) < in_c2.getentry(0) ) { return in_c1; }
	if ( in_c2.getentry(0) < in_c1.getentry(0) ) { return in_c2; }
	if ( in_c1.getentry(1) < in_c2.getentry(1) ) { return in_c1; }
	if ( in_c2.getentry(1) < in_c1.getentry(1) ) { return in_c2; }
// if the code makes it this far, in_c1 and in_c2 have all the same entries; the function will just return one of them
	return in_c1;
	}

void setclass::print() { cout << "(" << nlist[0] << ", " << nlist[1] << ", " << nlist[2] << ") mod " << nm << endl; }

void setclass::print( string in_string ) {
	cout << in_string;
	cout << "(" << nlist[0] << ", " << nlist[1] << ", " << nlist[2] << ") mod " << nm << endl;
	}
	
setclass::setclass( int in_n1, int in_n2, int in_n3, int in_n4 ) {
	nlist[0] = in_n1;
	nlist[1] = in_n2;
	nlist[2] = in_n3;
	nm = in_n4;
	}
	
	
setclass::setclass() { }
	
void setclass::sort( void ) { sortlist( nlist, nmembers ) ; }
	



setclass setclass::reduce( void ) {
	int qlist[nmembers]; // these will be the partial quotients of nlist
	int mlist[nmembers]; 
	int m0;
	for (unsigned int i = 0; i < nmembers; i++) { qlist[i] = nlist[i] / nm; }
	for (unsigned int i = 0; i < nmembers; i++) { mlist[i] = nlist[i] - qlist[i] * nm; }
	m0 = mlist[0];
	for (unsigned int i = 0; i < nmembers; i++) { mlist[i] -= m0; }
	for (unsigned int i = 0; i < nmembers; i++) { if ( mlist[i] < 0 ) { mlist[i] += nm; } }
	setclass outclass(mlist[0],mlist[1],mlist[2],nm);
	outclass.sort();
	return outclass;
	}


setclass setclass::reducechoose( void ) {
	setclass classes[5];
	int min, minentrynumber;
	classes[0] = setclass(nlist[0],nlist[1],nlist[2],nm);
	classes[1] = setclass(nlist[1],nlist[0],nlist[2],nm);
	classes[2] = setclass(nlist[2],nlist[0],nlist[1],nm);
	classes[3] = setclass(nlist[1],nlist[2],nlist[0],nm);
	classes[4] = setclass(nlist[2],nlist[1],nlist[0],nm);
	for (unsigned int i = 0; i < 5; i++) { 
		classes[i] = classes[i].reduce();
		}
// find the most prime set
	setclass primeset = classes[0];
	for (unsigned int i = 1; i < 5; i++) {
		primeset = compare( primeset, classes[i] );
		}
	return primeset;
	}
	
	
setclass setclass::primeform( void ) {
	setclass c1(nlist[0],nlist[1],nlist[2],nm);
	setclass c1i = c1.invert(); 
	c1 = c1.reducechoose();
	c1i = c1i.reducechoose();
	return compare( c1, c1i );
	}

void setclass::setentry( int in_entrynumber, int in_value ) {
	if ( in_entrynumber == 3 ) { nm = in_value; }
	else { nlist[ in_entrynumber] = in_value; }
	}
	
	
setclass setclass::invert( void ) {
	setclass outclass( nm - nlist[0], nm - nlist[1], nm - nlist[2], nm );
	return outclass;
	}
	

// this returns true if all of the entries in the two set classes are the same
// does NOT determine if the two sets are from the same set class
bool testequality( setclass in_class1, setclass in_class2 ) {
	in_class1 = in_class1.reducechoose();
	in_class2 = in_class2.reducechoose();
	for (unsigned int i = 0; i < (nmembers + 1); i++ ) { 
		if ( in_class1.getentry(i) != in_class2.getentry(i) ) { return false; }
		}
// if the code makes it this far, the two sets must have all the same entries
	return true;
	}


// this function sees if the two sets are from the same set class
// reduces the sets to their prime from and then tests their equality
bool testequivalence( setclass in_c1, setclass in_c2 ) {
	in_c1 = in_c1.primeform();
	in_c2 = in_c2.primeform();
	return testequality( in_c1, in_c2 );
	}

	
void setclass::increment( int in_entrynumber ) {
	if (in_entrynumber == 3 ) { nm++ ;}
	else { nlist[in_entrynumber]++ ;}
	}
	


int setclass::pscore( void ) {
	int c_step = nm / 6;
	if (c_step == 0) { 
		cout << "NO PARSIMONIOUSLY RELATED SETS" << endl;
		return 0; 
		}
	int i_pscore = -3;
	setclass c1(nlist[0],nlist[1],nlist[2],nm);
	setclass c2(nlist[0]-c_step,nlist[1],nlist[2],nm);
	for (unsigned int i = 0; i < c_step * 2 + 1; i++) { 
		if ( testequivalence(c1,c2) ) { 
			i_pscore++ ;
			if (i != c_step) { c2.print() ;}
			} 
		c2.increment(0);
		}
	c2 = c1;
	c2.setentry( 1, nlist[1] - c_step );
	for (unsigned int i = 0; i < c_step * 2 + 1; i++) { 
		if ( testequivalence(c1,c2) ) { 
			i_pscore++ ;
			if (i != c_step) { c2.print() ;}
			} 
		c2.increment(1);
		}
	c2 = c1;
	c2.setentry( 2, nlist[2] - c_step );
	for (unsigned int i = 0; i < c_step * 2 + 1; i++) { 
		if ( testequivalence(c1,c2) ) { 
			i_pscore++ ;
			if (i != c_step) { c2.print() ;}
			} 
		c2.increment(2);
		}
	if (i_pscore == 0) { cout << "NO PARSIMONIOUSLY RELATED SETS" << endl; }
	return i_pscore;
	}
	


// ******************************** begin main function **********************************
int main() { // main
cout << endl;
cout << endl;
// **************************** get input from user **************************************
int inputs[4]; // locations 0-2 are the integers of the set class; location 3 is the modulus number
string st_inputs[4]; // these are the numbers inputted by the user 
int quotients[3]; // this will be the partial quotients of the members of the set class
cout << "enter the first number of the set class" << endl;
cin >> st_inputs[0];
if ( inputtest( st_inputs[0] ) != 0 ) { return 0 ;}
cout << "enter the second number of the set class" << endl;
cin >> st_inputs[1];
if ( inputtest( st_inputs[1] ) != 0 ) { return 0 ;}
cout << "enter the third number of the set class" << endl;
cin >> st_inputs[2];
if ( inputtest( st_inputs[2] ) != 0 ) { return 0 ;}
st_inputs[3] = getmodulusnumber();
if ( inputtest( st_inputs[3] ) != 0 ) { return 0 ;}
	
// ********************** convert inputted strings into ints *****************************
  std::string::size_type sz;   // alias of size_t
for (int entrynumber = 0; entrynumber < 4; entrynumber++) { inputs[entrynumber] = stoi (st_inputs[entrynumber] ,&sz) ; }
cout<< endl;
setclass userclass( inputs[0], inputs[1], inputs[2], inputs[3] );
userclass.print( "you have entered the class " );
setclass c1 = userclass.reducechoose(); // this is a placeholder setclass
c1 = userclass.invert();
setclass c2 = c1;
c1.print( "your class inverted is " );
c1 = c1.reducechoose();
userclass.primeform().print("your class in prime form is ");
int p, pi;
cout << endl;
cout << endl;
cout << "the following sets are parsimoniously related to your set:" << endl;
p = userclass.pscore();
cout << "your set has a pscore of " << p << endl;
cout << endl;
cout << endl;
cout << "the following sets are parsimoniously related to the inversion of your set:" << endl;
pi = c2.pscore();
cout << "the inversion of your set has a pscore of " << pi << endl;
cout << endl;
cout << endl;
return 0;
// ***************************** end of main *********************************************
} // main
