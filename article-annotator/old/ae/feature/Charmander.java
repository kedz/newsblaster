package edu.columbia.cs.ae.feature;

public class Charmander {

	public static int[] computeCharFeatures (String text) {

		int len = text.length();

		int blackspaces = 0;	int alpha = 0;		int upper = 0;		int punct = 0;
		int whitespaces = 0;	int digit = 0;		int lower = 0;		int newline = 0;

		int backticks= 0;	// `	
		int brackets = 0;	// [		
		int crackets = 0;	// ]
		int percents = 0;	// %	24
		int slashes = 0;	// /
		int blashes = 0;	// \
		int exclams = 0;	// !	20
		int periods = 0;	// .
		int dollars = 0;	// $	23
		int carrots = 0;	// ^	25
		int quests = 0;		// ?
		int colons = 0;		// :
		int solons = 0;		// ;
		int parens = 0;		// (	28
		int qarens = 0;		// )	29
		int commas = 0;		// ,	
		int pounds = 0;		// #	22
		int ampers = 0;		// &	26
		int pluses = 0;		// +	33
		int dashes = 0;		// -	30
		int unders = 0;		// _	31
		int greats = 0;		// >
		int lesses = 0;		// <
		int equals = 0;		// =	32
		int curlys = 0;		// {
		int durlys = 0;		// }
		int tildas = 0;		// ~
		int quots = 0;		// '	42
		int duots = 0;		// "	43
		int stars = 0;		// *	27
		int bars = 0;		// |
		int car = 0;
		int tab = 0;
		int ats = 0;		// @	21
		int e = 0;			// e 	8
		int t = 0;			// t 	9
		int a = 0;			// a 	10
		int o = 0;			// o 	11
		int i = 0;			// i 	12
		int n = 0;			// n 	13
		int s = 0;			// s 	14
		int h = 0;			// h	15
		int r = 0;			// r 	16

		for (int j=0; j<len; j++) {
			char c = text.charAt(j);
			if (!Character.isWhitespace(c)) {
				// non-whitespace
				blackspaces++;
				if (Character.isLetterOrDigit(c)) {
					// alpha-numeric
					if (Character.isDigit(c)) { digit++; }
					else {
						// alpha
						alpha++;
						if (Character.isLowerCase(c)) { lower++; }
						if (Character.isUpperCase(c)) { upper++; }
						if (Character.toLowerCase(c)=='e') { e++; }
						else if (Character.toLowerCase(c)=='t') { t++; }
						else if (Character.toLowerCase(c)=='a') { a++; }
						else if (Character.toLowerCase(c)=='o') { o++; }
						else if (Character.toLowerCase(c)=='i') { i++; }
						else if (Character.toLowerCase(c)=='n') { n++; }
						else if (Character.toLowerCase(c)=='s') { s++; }
						else if (Character.toLowerCase(c)=='h') { h++; }
						else if (Character.toLowerCase(c)=='r') { r++; }
					}
				} // punctuation
				else if (c=='!') { punct++; exclams++; }
				else if (c=='@') { punct++; ats++; }
				else if (c=='#') { punct++; pounds++; }
				else if (c=='$') { punct++; dollars++; }
				else if (c=='%') { punct++; percents++; }
				else if (c=='^') { punct++; carrots++; }
				else if (c=='&') { punct++; ampers++; }
				else if (c=='*') { punct++; stars++; }
				else if (c=='(') { punct++; parens++; }
				else if (c==')') { punct++; qarens++; }
				else if (c=='-') { punct++; dashes++; }
				else if (c=='_') { punct++; unders++; }
				else if (c=='=') { punct++; equals++; }
				else if (c=='+') { punct++; pluses++; }
				else if (c=='{') { punct++; curlys++; }
				else if (c=='}') { punct++; durlys++; }
				else if (c=='[') { punct++; brackets++; }
				else if (c==']') { punct++; crackets++; }
				else if (c=='\\') { punct++; blashes++; }
				else if (c=='|') { punct++; bars++; }
				else if (c==':') { punct++; colons++; }
				else if (c==';') { punct++; solons++; }
				else if (c=='\'') { punct++; quots++; }
				else if (c=='"') { punct++; duots++; }
				else if (c==',') { punct++; commas++; }
				else if (c=='.') { punct++; periods++; }
				else if (c=='<') { punct++; lesses++; }
				else if (c=='>') { punct++; greats++; }
				else if (c=='/') { punct++; slashes++; }
				else if (c=='?') { punct++; quests++; }
			} else {
				whitespaces++;
				if (c=='\n') { newline++; }
				else if (c=='\r') { car++; }
				else if (c=='\t') { tab++; }
			}
		}

		int[] features = {	len, whitespaces, blackspaces, punct, digit, alpha, lower, upper, // 7
							e, t, a, o, i, n, s, h, r, newline, tab, car, // 19
							exclams, ats, pounds, dollars, percents, carrots, ampers, stars, parens, qarens, // 29
							dashes, unders, equals, pluses, curlys, durlys, brackets, crackets, blashes, bars, // 39
							colons, solons, quots, duots, commas, periods, lesses, greats, slashes, quests }; //49

		return features;
	}
}